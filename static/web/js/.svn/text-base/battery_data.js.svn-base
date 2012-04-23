var chart;
var seriesData = [];

// create the chart when all data is loaded
function createChart() {
    Highcharts.setOptions({
	global: {
            useUTC: false
	}
    });
    
    chart = new Highcharts.StockChart({
        chart: {
            renderTo: 'container'
        },

        rangeSelector: {
            selected: 1
        },

        title: {
            text: 'Battery Life'
        },

        xAxis: {
            maxZoom: 7 * 24 * 3600000,
            plotBands: bands
        },
        yAxis: {
            title: {
                text: 'Battery Level in %'
            }
        },

        series: [{
            name: 'Battery Level',
            data: data
        }],

        tooltip: {
            formatter: function() {
                var s = '<b>'+ Highcharts.dateFormat('%a %b %e, %Y %H:%M', this.x) +'</b>';

                $.each(this.points, function(i, point) {
                    s += '<br/>Battery Level: '+ point.y.toFixed(2);
                });

                return s;
            }
        }
    });
}


$(document).ready(function() {
    if(data.length > 0) {
        createChart();
    }
});