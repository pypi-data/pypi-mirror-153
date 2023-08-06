

function displayChart() {
    const ws = new WebSocket('ws://localhost:8000/ws');
    const chartOptions = {
        width: 1500,
        height: 1000,
        timeScale: {
            timeVisible: true,
            secondsVisible: true,
        },
        layout: { textColor: 'black', background: { type: 'solid', color: 'white' } }
    };
    const chart = LightweightCharts.createChart(document.getElementById('chart_container'), chartOptions);
    const lineSeries = chart.addLineSeries({ color: '#2962FF' });
    //chart.timeScale().fitContent();
    ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        lineSeries.update(data);
    };
};