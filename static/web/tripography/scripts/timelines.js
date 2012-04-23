function plot_vs_time (dates, raw_data, line_titles, suffix, chart_div) {

	var data = new google.visualization.DataTable();
	data.addColumn('date', 'Date');
	data.addColumn('number', '');

	var dataRows = []
	for (var i = 0; i < dates.length; i++ ) {
		var currentRow = []
		var currentDateEpoch = dates[i]
		var currentDate = new Date(currentDateEpoch*1000)
		currentRow.push(currentDate)
		currentRow.push(raw_data.current_day[i])
		dataRows.push(currentRow)
	}
	data.addRows(dataRows)

	var chart = new google.visualization.AnnotatedTimeLine(document.getElementById(chart_div));
	var options = {
			'allValuesSuffix' : ' ' + suffix
	}

	chart.draw(data, options);
}

function initialize_timeline_page() {
	
	
	
	$.ajax({
		url: "/tripography/api/statistics/",
		data: { user_id: user_id,
			types: 'vs_time2' },
			success: function (raw_data) {
				user_data = raw_data
				
				$('#data-view li:first').trigger('click')

			}
	})	
}

