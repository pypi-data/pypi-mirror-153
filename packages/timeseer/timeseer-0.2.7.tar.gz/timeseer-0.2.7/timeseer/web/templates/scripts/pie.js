$('.score-pie').each(function (index, pie) {
    var labels = $(pie).find('.pie-label').map(function () {
        return $(this).text();
    }).get();
    var values = $(pie).find('.pie-value').map(function () {
        return parseInt($(this).text(), 10);
    }).get();

    var data = [{
        type: 'pie',
        values: values,
        labels: labels,
        hoverinfo: 'percent+value',
        marker: {
            colors: ['rgba(250,105,106,1)', 'rgba(100,191,124,1)'],
        },
    }];
    var layout = {
        showlegend: false,
        margin: {
            r: 0,
            t: 0,
            b: 0,
            pad: 4,
        },
    };
    var config = {
        displayModeBar: false,
        responsive: true,
    };

    if (pie.getAttribute('data-height')) {
        layout.height = pie.getAttribute('data-height');
    }

    Plotly.newPlot(pie, data, layout, config);
});
