"""Timeseer Client allows querying of data and metadata."""

import json
import time

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Union

from kukur import Metadata, SeriesSelector
from kukur.client import Client as KukurClient

import pyarrow as pa
import pyarrow.flight as fl


class Client(KukurClient):
    """Client connects to Timeseer using Arrow Flight."""

    def upload_data(
        self,
        metadata_or_data: Union[Metadata, list[tuple[Metadata, pa.Table]]],
        table: Optional[pa.Table] = None,
        *,
        analyze=True,
        block=True
    ):
        """Upload time series data to Timeseer.

        This requires a configured 'flight-upload' source in Timeseer.

        There are two ways to call this method.

        One requires two arguments:
            metadata: any known metadata about the time series. This will be merged with the metadata
                already known by Timeseer depending on the source configuration. The source of the series should match
                the source name of a 'flight-upload' source.
            table: a pyarrow.Table of two columns.
                The first column with name 'ts' contains Arrow timestamps.
                The second column with name 'value' contains the values as a number or string.

        The second accepts a list of tuples of the same arguments. This allows uploading multiple time series at the
        same time.

        When `analyze` is `True`, start a flow evaluation.
        When `block` is `True`, block execution until the flow evaluation is done.
        """
        if table is not None:
            assert isinstance(metadata_or_data, Metadata)
            self._upload_data_single(metadata_or_data, table, analyze, block)
        else:
            assert not isinstance(metadata_or_data, Metadata)
            self._upload_data_multiple(metadata_or_data, analyze, block)

    def _upload_data_single(
        self, metadata: Metadata, table: pa.Table, analyze: bool, block: bool
    ):
        self._upload_data_multiple([(metadata, table)], analyze, block)

    def _upload_data_multiple(
        self, many_series: list[tuple[Metadata, pa.Table]], analyze: bool, block: bool
    ):
        client = self._get_client()
        selectors = []
        for metadata, table in many_series:
            metadata_json = metadata.to_data()
            selector = SeriesSelector.from_tags(
                metadata.series.source, metadata.series.tags, metadata.series.field
            )
            selectors.append(selector)
            descriptor = fl.FlightDescriptor.for_command(
                json.dumps(
                    dict(
                        metadata=metadata_json,
                    )
                )
            )
            writer, reader = client.do_put(descriptor, table.schema)
            writer.write_table(table)
            writer.done_writing()
            buf: pa.Buffer = reader.read()
            response: dict = json.loads(buf.to_pybytes())
            writer.close()

        if "flowName" in response:
            if analyze:
                _analyze_flow(
                    client, response["flowName"], limitations=selectors, block=block
                )
        elif block:
            _wait_for_flow_evaluation(client, response)

    def evaluate_flow(self, flow_name: str, *, block=True):
        """Evaluate a flow.

        Args:
            flow_name: the name of the flow to evaluate
            block: block until the evaluation completes (keyword-only, default True)
        """
        client = self._get_client()
        _analyze_flow(client, flow_name, block=block)

    def get_event_frames(
        self,
        selector: SeriesSelector,
        start_date: datetime = None,
        end_date: datetime = None,
        frame_type: Union[str, list[str]] = None,
    ) -> pa.Table:
        """Get all event frames matching the given criteria.

        Args:
            selector: the time series source, exposed flow or time series to which the event frames are linked.
            start_date: the start date of the range to find overlapping event frames in. Defaults to one year ago.
            end_date: the end date of the range to find overlapping event frames in. Defaults to now.
            frame_type: the type or types of event frames to search for. Finds all types when empty.

        Returns::
            A pyarrow Table with 4 columns.
            The first column ('start_date') contains the start date.
            The second column ('end_date') contains the end date.
            The third column ('type') contains the type of the returned event frame as a string.
            Columns 4 contains possible multiple references for the event frame.
        """
        if start_date is None or end_date is None:
            now = datetime.utcnow().replace(tzinfo=timezone(timedelta(0)))
            if start_date is None:
                start_date = now.replace(year=now.year - 1)
            if end_date is None:
                end_date = now

        query: Dict[str, Any] = {
            "query": "get_event_frames",
            "selector": selector.to_data(),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }

        if frame_type is not None:
            query["type"] = frame_type

        ticket = fl.Ticket(json.dumps(query))
        return self._get_client().do_get(ticket).read_all()

    def get_data_quality_score_data_sources(
        self, source_names: List[str]
    ) -> dict[str, int]:
        """Get the data quality score of a data source or exposed flow.

        Args:
            source_names: A list of time series sources or Flight Expose blocks

        Returns::
            A data quality score of every given source as a percentage.
        """
        body = {
            "source_names": source_names,
        }
        results = list(
            self._get_client().do_action(
                ("get_data_quality_score_data_sources", json.dumps(body).encode())
            )
        )
        return json.loads(results[0].body.to_pybytes())

    def get_kpi_scores(
        self,
        source_name: str,
    ) -> dict[str, dict[str, int]]:
        """Get the kpi scores of a data source or exposed flow.

        Args:
            source_name: The time series source or the name of the Flight Expose block.

        Returns::
            The score per KPI as a percentage, keyed by the source_name provided.
        """
        body = {
            "source_name": source_name,
        }

        results = list(
            self._get_client().do_action(("get_kpi_scores", json.dumps(body).encode()))
        )
        return json.loads(results[0].body.to_pybytes())

    def get_series_results(
        self, selector: SeriesSelector
    ) -> list[dict[str, Union[str, float]]]:
        """Return the univariate check results for the given series.

        Args:
            selector: The time series to return results for.

        Returns::
            A list of check results, where each check result is a dictionary with 'name' and 'result'.
            The result is returned as a floating point number between 0.0 (bad) and 1.0 (good)."""
        body = {
            "selector": selector.to_data(),
        }
        results = list(
            self._get_client().do_action(
                ("get_series_results", json.dumps(body).encode())
            )
        )
        return json.loads(results[0].body.to_pybytes())

    def get_series_statistics(self, selector: SeriesSelector) -> list[dict[str, Any]]:
        """Return the univariate statistics for the given series.

        Args:
            selector: The time series to return statistics for.

        Returns::
            A list of statistics. Each statistic is a dict with three fields:
              - name (str)
              - dataType (str) - one of 'float', 'pct', 'datetime', 'hidden', 'table'
              - result (exact type depending on the dataType)"""
        body = {"selector": selector.to_data()}
        results = list(
            self._get_client().do_action(
                ("get_series_statistics", json.dumps(body).encode())
            )
        )
        return json.loads(results[0].body.to_pybytes())

    def remove_data(self, selector: SeriesSelector):
        """Removes the series indicated by the SeriesSelector and related files.
           The source in the selector should match the source name of a
           'flight-upload' source.

        Args:
            selector: The time series to be removed. If selector contains no series
            name then all the series on the given source are removed.
        """
        body = {"selector": selector.to_data()}

        self._get_client().do_action(("remove_series", json.dumps(body).encode()))


def _analyze_flow(
    client: fl.FlightClient,
    flow_name: str,
    *,
    limitations: Optional[list[SeriesSelector]] = None,
    block=True
):
    flow: dict = dict(flowName=flow_name)
    if limitations is not None:
        flow["limitations"] = [selector.to_data() for selector in limitations]
    results = list(client.do_action(("evaluate_flow", json.dumps(flow).encode())))
    response = json.loads(results[0].body.to_pybytes())

    if block:
        _wait_for_flow_evaluation(client, response)


def _wait_for_flow_evaluation(client: fl.FlightClient, response: dict):
    while True:
        results = list(
            client.do_action(
                ("get_flow_evaluation_state", json.dumps(response).encode())
            )
        )
        state = json.loads(results[0].body.to_pybytes())
        if (
            state["completed"] == state["total"]
            and state["blockCompleted"] == state["blockTotal"]
        ):
            break
        time.sleep(1)
