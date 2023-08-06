function plotBadActors(badActors) {
    var series = [];
    var labels = [];
    var scores = [];
    var urls = []
    for (var i=0; i<badActors.length; i++){
        series.push(badActors[i].selector.name)
        scores.push(badActors[i].tiles.map(tile => {
            if (tile.state == "bug") {
                return (tile.score + 1) / 2
            } else if(tile.state == "no data") {
                return tile.score + 1
            } else {
                return (tile.score) / 2
            }

        }))
        urls.push(badActors[i].tiles.map(tile => tile.url))
        if (i == 0) {
            labels = badActors[i].tiles.map(tile => tile.startDate)
        }

    }

    var colorscaleValue = [
        [0, '#009D89'],
        [0.09, '#FDDB7F'],
        [0.5, '#FCB800'],
        [0.5, '#FF80A8'],
        [0.95, '#FF0153'],
        [1.0, '#C2C4C6'],
    ];

    var data = [
        {
            x: labels,
            y: series,
            z: scores,
            type: 'heatmap',
            customdata: urls,
            colorscale: colorscaleValue,
            showscale: false,
            zmin: 0,
            zmax: 1,
            hoverinfo: "x+y",
            xgap: 1,
            ygap: 1,
        }
    ];
    var layout = {
        xaxis: {
            type: 'category',
            tickangle: -45,
            automargin: true,
            tickmode: 'auto',
            nticks: 24,
            fixedrange: true,
        },
        yaxis: {
            type: 'category',
            automargin: true,
            tickmode: 'array',
            fixedrange: true,
        },
        margin: {
            r: 20,
            t: 20,
        },
        height: 700,
    };
    var config = {
        displayModeBar: false,
        responsive: true,
    };

    Plotly.newPlot('bad-actor-visualization', data, layout, config);
    document.getElementById('bad-actor-visualization').on('plotly_click', function (data) {
        if (data.points.length > 0 && data.points[0].customdata) {
            window.location.href = data.points[0].customdata;
        }
    });
}
