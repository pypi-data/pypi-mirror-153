$('.histogram').each(function (index, histogram) {
    var readFloat =  function () {
        return parseFloat($(this).text());
    };
    var binTexts = $(histogram).find('.histogram-bin-text').map(function () {
        return $(this).text();
    }).get();
    var binStarts = $(histogram).find('.histogram-bin-start').map(readFloat).get();
    var binEnds = $(histogram).find('.histogram-bin-end').map(readFloat).get();
    var values = $(histogram).find('.histogram-value').map(function () {
        return parseInt($(this).text(), 10);
    }).get();
    var extraLines = $(histogram).find('.histogram-line').map(readFloat).get();

    let data = [{
        type: 'bar',
        x: binStarts.map(function (start, i) {
            return start + (binEnds[i] - start) / 2;
        }),
        y: values,
        fill: 'toself',
        marker: {
            color: '#bee5eb',
        },
    }];
    let layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        margin: {
            r: 0,
            t: 0,
            pad: 4,
        },
        xaxis: {
            title: $(histogram).find('.histogram-bin-label').text(),
            tickangle: -45,
            automargin: true,
            range: [binStarts[0], binEnds[binEnds.length-1]],
            tickmode: 'array',
            tickvals: data[0].x,
            ticktext: binTexts,
        },
        yaxis: {
            automargin: true,
            title: $(histogram).find('.histogram-value-label').text(),
        },
        showlegend: false,
        bargap: 0.15,
    };
    let config = {
        displayModeBar: false,
        responsive: true,
    };

    layout.shapes = extraLines.map(function (xValue) {
        return {
            type: 'line',
            yref: 'paper',
            x0: xValue,
            y0: 0,
            x1: xValue,
            y1: 1,
            line:{
                color: 'rgb(192, 3, 3)',
                width: 2,
                dash:'dot',
            },
        }
    });

    if (histogram.getAttribute('data-height')) {
        layout.height = histogram.getAttribute('data-height');
    }

    if (histogram.getAttribute('data-score-coloring')) {
        data[0].marker.color = binStarts.map(function (score) {
            var color = 'rgba(250,105,106,1)';
            if (score >= 80) {
                color = 'rgba(100,191,124,1)';
            } else if (score >= 70) {
                color = 'rgba(254,235,130,1)';
            } else if (score >= 60) {
                color = 'rgba(251,170,121,1)';
            }
            return color;
        });
    }

    Plotly.newPlot(histogram, data, layout, config);
});
