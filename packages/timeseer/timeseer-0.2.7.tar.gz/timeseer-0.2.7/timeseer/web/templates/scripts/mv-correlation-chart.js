$('.correlation').each(function (index, element) {
    var series = $(element).find('.correlation-header').map(function () {
        return $(this).attr('data-series');
    }).get();
    var labels = $(element).find('.correlation-header').map(function () {
        return $(this).text();
    }).get();
    var values = $(element).find('.correlation-value').map(function () {
        return parseFloat($(this).text());
    }).get();
    var correlations = [];
    for (var i=0; i<values.length; i+=series.length) {
        correlations.push(values.slice(i, i + series.length));
    }

    var data = [
        {
          x: series,
          y: series,
          z: correlations,
          type: 'heatmap',
          zmin: -1,
          zmax: 1
        },
    ];

    layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        xaxis: {
            type: 'category',
            tickangle: -45,
            automargin: true,
            tickmode: 'array',
            tickvals: series,
            ticktext: labels,
        },
        yaxis: {
            type: 'category',
            automargin: true,
            tickmode: 'array',
            tickvals: series,
            ticktext: labels,
        },
        margin: {
            r: 0,
            t: 0,
        },
        height: 700,
    };
    config = {
        displayModeBar: false,
        responsive: true,
    };

    Plotly.newPlot(element, data, layout, config);
});
