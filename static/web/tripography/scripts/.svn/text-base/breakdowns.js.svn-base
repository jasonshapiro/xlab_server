// NOTE: The following is not really needed unless one wants custom colors...
var pieChartColors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

function create_pie_chart_data_table(raw_data, xlabel, ylabel) {
	var data = new google.visualization.DataTable();
	data.addColumn('string', xlabel)
	data.addColumn('number', ylabel)
	var temp = [] 
	for (var key in raw_data) {
		if (raw_data.hasOwnProperty(key)) {
			temp.push([key, Math.round(raw_data[key])])
		}
	}
	data.addRows(temp)
	return data
}



function plot_pie_chart(data, chart_div, options) {
	var chart = new google.visualization.PieChart(document.getElementById(chart_div));
	chart.draw(data, options);
}


function initialize_breakdowns() {

// create pie charts
$.ajax({
	url: "/tripography/api/statistics/",
	data: { user_id: user_id,
		types: 'breakdown_by_number,breakdown_by_time,breakdown_by_distance' },
		success: function (data) {

			// make some pie charts of mode breakdowns using Google Chart API
			data_breakdown_by_number = create_pie_chart_data_table(data.breakdown_by_number, 'Mode', 'Frequency')
			data_breakdown_by_time = create_pie_chart_data_table(data.breakdown_by_time, 'Mode', 'Time')
			data_breakdown_by_distance = create_pie_chart_data_table(data.breakdown_by_distance, 'Mode', 'Distance (mi)')
			var options = {
				'width': 300,
				'height': 260,
				'legend': 'none',
				'fontSize': 12,
				'colors': pieChartColors,
				'chartArea': {'width': 240, 'height': 240},
				'titleTextStyle': { 'textAlign': 'center' }
			}
			var opts1 = $.extend(true, {'title': 'Breakdown by Number of Trips'}, options)
			var opts2 = $.extend(true, {'title': 'Breakdown by Time (min)'}, options)
			var opts3 = $.extend(true, {'title': 'Breakdown by Distance (mi)'}, options)
			plot_pie_chart(data_breakdown_by_number, 'plot_breakdown_by_number', options)
			plot_pie_chart(data_breakdown_by_time, 'plot_breakdown_by_time', options)
			plot_pie_chart(data_breakdown_by_distance, 'plot_breakdown_by_distance', options)

			var legends = new google.visualization.PieChart(document.getElementById('colors-legend'));
			var options = {
					'width': 900,
					'height': 25,
					'chartArea': {'width': 900, 'height': 0},
					'legend': 'bottom',
					'fontSize': 12,
					'colors': pieChartColors
			}
			legends.draw(data_breakdown_by_number, options);
			tooltip_iframe = window.frames[document.getElementById('colors-legend').firstChild.name];
			tooltip_dom = tooltip_iframe.document.getElementById('chart').firstChild.nextSibling.nextSibling;
			tooltip_dom.style.display = 'none';
		}
})

}