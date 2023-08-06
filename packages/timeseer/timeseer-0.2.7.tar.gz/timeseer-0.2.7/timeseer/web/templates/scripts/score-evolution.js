$('.report-evolution').each(function () {
    let dates = $(this).find('.report-date').map(function () {
        return this.getAttribute('data-date');
    }).get();
    let scores = $(this).find('.report-score').map(function () {
        return parseFloat($(this).text());
    }).get();
    let urls = $(this).find('tr[data-report-url]').map(function () {
        return this.getAttribute('data-report-url');
    }).get();
    let formattedDates = $(this).find('.report-date').map(function () {
        return $(this).text();
    }).get();

    let trace = {
        x: dates,
        y: scores,
        hoverinfo: 'text',
        hovertext: scores.map(function (score, i) {return formattedDates[i] + ': ' + score + '%'}),
        customdata: urls,
        type: 'scatter',
        line: {
            color: 'blue',
            shape: 'hv',
        },
    };

    let layout = {
        margin: {
            r: 0,
            t: 0,
            pad: 4,
        },
        yaxis: {
            title: 'Score',
        },
        showlegend: false,
    };

    let config = {
        displayModeBar: false,
        responsive: true,
    };

    Plotly.newPlot(this, [trace], layout, config);
    this.on('plotly_click', function (data) {
        if (data.points.length > 0 && data.points[0].customdata) {
            window.open(data.points[0].customdata, '_blank');
        }
    });
});
