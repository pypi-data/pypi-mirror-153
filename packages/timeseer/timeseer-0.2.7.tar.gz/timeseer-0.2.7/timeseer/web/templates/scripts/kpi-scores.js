(function () {
  var kpiScores = {{ kpi_scores|tojson }};
  var comparisonKpiScores = {{ comparison_kpi_scores|tojson }}
  var kpis = {{ kpis|sort(attribute='name')|map(attribute='name')|list|tojson }};

  var scores = kpis.map(function (kpi) {return kpiScores[kpi]||0;});
  var comparisonScores = kpis.map(function (kpi) {return comparisonKpiScores[kpi];});

  var data = [];
  {% if (compare_evaluation is defined and compare_evaluation is not none) or compare_to is not none %}
  if (Object.keys(comparisonKpiScores).length > 0) {
    data.push({
      type: 'scatterpolar',
      r: comparisonScores,
      theta: kpis,
      fill: 'toself',
      {% if compare_evaluation is defined and compare_evaluation is not none %}
      name: '{{ compare_evaluation.flow_evaluation.group.date|datetimeformat }}'
      {% else %}
      name: '{{ compare_to }}'
      {% endif %}
    });
  }
  {% endif %}
  data.push({
    type: 'scatterpolar',
    r: scores,
    theta: kpis,
    fill: 'toself',
    name: 'Current evaluation'
  });

  var layout = {
    polar: {
      radialaxis: {
        visible: true,
        range: [0, 100]
      }
    },
    showlegend: true,
    legend: {
      xanchor: 'right',
      x: 1.2,
      y: 1.2
    },
    margin: {
      t: 0,
      l: 15,
      r: 0,
      b: 30,
    }
  }

  Plotly.newPlot("timeseries_source_score", data, layout);
})();
