function plot_occurrence(eventFrameOccurrences) {
    var max = function (a, b) {
        return Math.max(a, b);
    };
    var element = function (index) {
        return function (arr) {
            return arr[index];
        };
    };
    var scale = function (values, max) {
        return values.map(function (value) {
            if (value === 0) {
                return 0;
            }
            if (value === 1 || max === 1) {
                return Math.max(50 * value / max, 5);
            }
            return Math.max(50 * value / max, 5);
        });
    };

    var maxCount = Object.values(eventFrameOccurrences).map(function (elements) {
        return elements.map(element(1)).reduce(max, 0);
    }).reduce(max, 0);

    if (maxCount === 0) {
        return;
    }

    var data = Object.keys(eventFrameOccurrences).sort().map(function (kpi) {
        var intervals = eventFrameOccurrences[kpi].map(element(0));
        var counts = eventFrameOccurrences[kpi].map(element(1));
        var title = kpi.charAt(0).toUpperCase() + kpi.slice(1);
        var trace = {
            name: title,
            x: intervals,
            y: Array(intervals.length).fill(title),
            text: counts,
            hoverinfo: 'text',
            mode: 'markers',
            marker: {
                color: 'rgba(250,105,106,1)',
                size: scale(counts, maxCount),
            },
        };

        var customData = eventFrameOccurrences[kpi].map(element(2));
        if (customData.length > 0 && customData[0]) {
            trace.customdata = customData;
        }

        return trace;
    }).reverse();

    var layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        hovermode: 'closest',
        showlegend: false,
        yaxis: {
            automargin: true,
        },
        xaxis: {
            type: 'category',
            tickangle: -45,
            automargin: true,
        },
        margin: {
            r: 0,
            t: 0,
        }
    };

    Plotly.newPlot('occurrence-chart', data, layout, {displayModeBar: false, responsive: true});
    document.getElementById('occurrence-chart').on('plotly_click', function(data) {
        if (data.points.length > 0 && data.points[0].customdata) {
            window.location.assign(data.points[0].customdata);
        }
    })

};
