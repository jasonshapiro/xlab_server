
function convert_to_kgs_per_day(stat) { 

	// stat is in tonnes CO2 per year -> convert to kgs/day
	return Math.round(stat*1000/days_in_year)
}



function convert_to_cost_per_day(stat) {
	// stat is in cost per year
	return Math.round(stat/days_in_year*100)/100
}

function iter_to(start,end,intervals) {
	var curr = start;
	var result = [curr]
	if ((end > start && intervals > 0) || (start > end && intervals < 0 )) {
		while (curr < end) {
			curr = curr + intervals
			result.push(curr)
		}
		return result;
	} else {
		return [start, end];
	}
}

function plot_quarter_radar_blank(options_user, chart_div) {

	var options_default = {
			'numAxes': 10,
			'height': 400,
			'width': 400,
			'padding': 25,
			'radius': 0, // calculated below
			'polar_percents': [20, 40, 60, 80, 100]
	}
	options_default.radius = Math.min(options_default.height, options_default.width) - options_default.padding*2;
	options = $.extend({}, options_default, options_user);

	var h = options.height;
	var w = options.width;
	var padding = options.padding;
	var r = options.radius;
	var polar_percents = options.polar_percents
	var polar_axes_angles = iter_to(0,90,(90)/(options.numAxes-1))

	options.polar_percents = polar_percents
	options.polar_axes_angles = polar_axes_angles
	options.origin = {'x': padding, 'y': h-padding}

	var chart = d3.select(chart_div)
	.append('svg:svg')
	.attr('width', w)
	.attr('height', h)
	.append('svg:g')
	.attr('height', h)
	.attr('width', w)
	.attr('class', 'chart-area')

	var bg = chart.append('svg:g')
	.attr('class','bg')
	.attr('height', h)
	.attr('width', w)
	.attr('x', 0)
	.attr('y', 0)

	var temp_gradient_colors = ['#CFCFC3',	'#D1D1C5',	'#D3D3C8',	'#D5D5CA',	'#D7D7CD',	'#D9D9CF',	'#DBDBD2',	'#DDDDD4',	'#DFDFD7',	'#E1E1D9',	'#E3E3DC',	'#E5E5DE',	'#E7E7E1',	'#E9E9E3',	'#EBEBE6',	'#EDEDE8',	'#EFEFEB',	'#F1F1ED',	'#F3F3F0',	'#F5F5F2',	'#F7F7F5',	'#F9F9F7',	'#FBFBFA',	'#FDFDFC',	'#FFFFFF']
	var temp_gradient_colors = ['#0A9ECF','#14A2D1','#1EA6D3','#28AAD5','#33AED7','#3DB2D9','#47B6DB','#51BADD','#5BBEDF','#66C2E1','#70C6E3','#7ACAE5','#84CEE7','#8ED2E9','#99D6EB','#A3DAED','#ADDEEF','#B7E2F1','#C1E6F3','#CCEAF5','#D6EEF7','#E0F2F9','#EAF6FB','#F4FAFD','#FFFFFF']
	temp_gradient_colors.reverse()


	// circle in the background (TODO: ADD GRADIENT)
//	bg.append('svg:circle') // big background circle
//	.attr('cy', h - padding)
//	.attr('cx', padding)
//	.attr('r', r)
//	.attr('fill', '#ddd')

	for (var j = 0; j < temp_gradient_colors.length; j++) {
		bg.append('svg:circle')
		.attr('cy', h - padding)
		.attr('cx', padding)
		.attr('r',r*(1-j/temp_gradient_colors.length) )
		.attr('fill', temp_gradient_colors[j])
	}

	bg.selectAll('.polarRing').data(polar_percents).enter() // polar grid
	.append('svg:circle')
	.attr('cx', padding)
	.attr('cy', h - padding)
	.attr('stroke', 'white')
	.attr('fill-opacity', 0)
	.attr('r', d3.scale.linear().domain([0, d3.max(polar_percents)]).range([padding, r]) )
	bg.append('svg:rect') // cut off left
	.attr('x', 0)
	.attr('y', 0)
	.attr('width', padding)
	.attr('height', h)
	.attr('fill', 'white')
	bg.append('svg:rect') // cut off right
	.attr('x', 0)
	.attr('y', h - padding)
	.attr('width', w)
	.attr('height', padding)
	.attr('fill', 'white')
	bg.selectAll('.spoke').data(polar_axes_angles).enter()
	.append('svg:line') // spokes
	.attr('class','spoke')
	.attr('x1', padding)
	.attr('y1', h - padding)
	.attr('x2', function (d, i) { return padding + r*Math.cos(d*Math.PI/180) })
	.attr('y2', function (d, i) { return h - padding - r*Math.sin(d*Math.PI/180) })
	.attr('stroke', 'black')



	return [chart, options];
}

function plot_radar(data, chart_div) {

	var h = 400;
	var w = 400;
	var padding = 25;
	var r = Math.min(h, w) - padding*2

	var chart = d3.select(chart_div)
	.append('svg:svg')
	.attr('width', h)
	.attr('height', w)
	.append('svg:g')
	.attr('height', h)
	.attr('width', w)

	var bg = chart.append('svg:g')
	.attr('class','bg')
	.attr('height', h)
	.attr('width', w)
	.attr('x', 0)
	.attr('y', 0)

	var polar_percents = [25, 50, 75, 100];

	// circle in the background (TODO: ADD GRADIENT)
	bg.append('svg:circle') // big background circle
	.attr('cy', h - padding)
	.attr('cx', padding)
	.attr('r', r)
	.attr('fill', '#ddd')
	bg.selectAll('.polarRing').data(polar_percents).enter() // polar grid
	.append('svg:circle')
	.attr('cx', padding)
	.attr('cy', h - padding)
	.attr('stroke', 'gray')
	.attr('fill-opacity', 0)
	.attr('r', d3.scale.linear().domain([0, d3.max(polar_percents)]).range([padding, r]) )
	.attr('')
	bg.append('svg:rect') // cut off left
	.attr('x', 0)
	.attr('y', 0)
	.attr('width', padding)
	.attr('height', h)
	.attr('fill', 'white')
	bg.append('svg:rect') // cut off right
	.attr('x', 0)
	.attr('y', h - padding)
	.attr('width', w)
	.attr('height', padding)
	.attr('fill', 'white')
	bg.selectAll('.spoke').data([0, 30, 60, 90]).enter()
	.append('svg:line') // spokes
	.attr('class','spoke')
	.attr('x1', padding)
	.attr('y1', h - padding)
	.attr('x2', function (d, i) { return padding + r*Math.cos(d*Math.PI/180) })
	.attr('y2', function (d, i) { return h - padding - r*Math.sin(d*Math.PI/180) })
	.attr('stroke', 'black')

	var data_points_group = chart.append('svg:g') // group for all the data points
	.attr('class', 'pg')
	.attr('height', h)
	.attr('width', w)
	.attr('x', 0)
	.attr('y', 0)

	// plot emissions
	curDataSet = data.emissions
	curData = []
	for (var i = 0; i < curDataSet.length; i++) {
		curData.push(curDataSet[i][0])
	}
	curAngle = 0
	curX = d3.scale.linear().domain([0, d3.max(curData)]).range([0, r])
	for (var i = 0; i < curData.length; i++ ) {
		data_points_group.selectAll('.emissions-point-group')
		.data(curData).enter().append('svg:g')
		.attr('x', function (d, i) { return padding + curX(d)*Math.cos(curAngle*Math.PI/180 ) })
		.attr('y', function (d, i) { return h - padding - curX(d)*Math.sin(curAngle*Math.PI/180 )})
		.append('svg:circle')
		.attr('cx', function (d, i) { return padding + curX(d)*Math.cos(curAngle*Math.PI/180 ) })
		.attr('cy', function (d, i) { return h - padding - curX(d)*Math.sin(curAngle*Math.PI/180 )})
		.attr('r', 10)
		.attr('stroke', 'darkgray')
		.attr('fill', 'white')
	}

	// plot calories
	curDataSet = data.calories
	curData = []
	for (var i = 0; i < curDataSet.length; i++) {
		curData.push(curDataSet[i][0])
	}
	curAngle = 30
	curX = d3.scale.linear().domain([0, d3.max(curData)]).range([0, r])
	for (var i = 0; i < curData.length; i++ ) {
		data_points_group.selectAll('.calories-point-group')
		.data(curData).enter().append('svg:g')
		.attr('x', function (d, i) { return padding + curX(d)*Math.cos(curAngle*Math.PI/180 ) })
		.attr('y', function (d, i) { return h - padding - curX(d)*Math.sin(curAngle*Math.PI/180 )})
		.append('svg:circle')
		.attr('cx', function (d, i) { return padding + curX(d)*Math.cos(curAngle*Math.PI/180 ) })
		.attr('cy', function (d, i) { return h - padding - curX(d)*Math.sin(curAngle*Math.PI/180 )})
		.attr('r', 10)
		.attr('stroke', 'darkgray')
		.attr('fill', 'white')
	}

	// plot cost
	curDataSet = data.calories
	curData = []
	for (var i = 0; i < curDataSet.length; i++) {
		curData.push(curDataSet[i][0])
	}
	curAngle = 60
	curX = d3.scale.linear().domain([0, d3.max(curData)]).range([0, r])
	for (var i = 0; i < curData.length; i++ ) {
		data_points_group.selectAll('.cost-point-group')
		.data(curData).enter().append('svg:g')
		.attr('x', function (d, i) { return padding + curX(d)*Math.cos(curAngle*Math.PI/180 ) })
		.attr('y', function (d, i) { return h - padding - curX(d)*Math.sin(curAngle*Math.PI/180 )})
		.append('svg:circle')
		.attr('cx', function (d, i) { return padding + curX(d)*Math.cos(curAngle*Math.PI/180 ) })
		.attr('cy', function (d, i) { return h - padding - curX(d)*Math.sin(curAngle*Math.PI/180 )})
		.attr('r', 10)
		.attr('stroke', 'darkgray')
		.attr('fill', 'white')
	}

	// plot time
	curDataSet = data.time
	curData = []
	for (var i = 0; i < curDataSet.length; i++) {
		curData.push(curDataSet[i][0])
	}
	curAngle = 90
	curX = d3.scale.linear().domain([0, d3.max(curData)]).range([0, r])
	for (var i = 0; i < curData.length; i++ ) {
		data_points_group.selectAll('.time-point-group')
		.data(curData).enter().append('svg:g')
		.attr('x', function (d, i) { return padding + curX(d)*Math.cos(curAngle*Math.PI/180 ) })
		.attr('y', function (d, i) { return h - padding - curX(d)*Math.sin(curAngle*Math.PI/180 )})
		.append('svg:circle')
		.attr('cx', function (d, i) { return padding + curX(d)*Math.cos(curAngle*Math.PI/180 ) })
		.attr('cy', function (d, i) { return h - padding - curX(d)*Math.sin(curAngle*Math.PI/180 )})
		.attr('r', 10)
		.attr('stroke', 'darkgray')
		.attr('fill', 'white')
	}



	// create the axes (lines and arcs, numbers, labels)

	// apply user info

}

function plot_comparisons_radar(raw_data, colors, chart_div) {


	var axesLabels = ['Cost',
	                  'Calories',
	                  'Emissions',
	                  'Time']

	// order some data to match the order of the axes labels (for iteration)
	var user_data = []
	user_data[0] = raw_data.cost
	user_data[1] = raw_data.calories
	user_data[2] = raw_data.emissions
	user_data[3] = raw_data.time
	var range_data = []
	range_data[0] = [0, comparisons_max.cost]
	range_data[1] = [0, comparisons_max.calories]
	range_data[2] = [0, comparisons_max.emissions]
	range_data[3] = [0, comparisons_max.time]
	var temp_axes_labels = ['Travel costs', 'Calories burned traveling', 'Travel emissions', 'Time spent traveling']
	var temp_axes_units = ['dollars/day', 'per day', 'kg CO2/day', 'minutes/day']

	// color ranges generated with: http://www.herethere.net/~samson/php/color_gradient/?cbegin=%23EE7AE9&cend=%238B4789&steps=5
	var temp_color_ranges = colors;


	var chart_options = {
			'numAxes': axesLabels.length,
			'height': 430,
			'width': 550,
			'radius': 350
	}

	var chart_out = plot_quarter_radar_blank(chart_options, chart_div);
	var chart = d3.select(chart_div).select('.chart-area')     // handle to the chart area
	var options = chart_out[1]                                 // full chart options
	var origin = options.origin

	// label the axes names
	var axesLabelsGroups = chart.append('svg:g')
	.attr('class','axis-label-groups')
	.attr('width', options.width)
	.attr('height', options.height)
	.attr('x',0)
	.attr('y',0)
	var axesLabelsGroup = axesLabelsGroups.selectAll('.axis-label-group').data(axesLabels).enter()
	.append('svg:g')
	.attr('width', options.width)
	.attr('height', options.height)
	.attr('class','axis-label-group')
	.attr('x',0)
	.attr('y',0)
	axesLabelsGroup.append('svg:text')
	.attr('text-anchor', 'start')
	.attr('x', options.padding)
	.attr('y', options.height - options.padding)
	.attr('transform', function(d,i) {
		var curAngle = options.polar_axes_angles[i]
		var trX = 1.05*options.radius*Math.cos(curAngle*Math.PI/180)
		var trY = -1.05*options.radius*Math.sin(curAngle*Math.PI/180)
		return 'translate('+ trX +','+ trY +')'
	})
	.text(String)


	for (var j = 0; j < options.polar_axes_angles.length; j++) {

		var curAngle = options.polar_axes_angles[j]
		var curMaxData = range_data[j][1]
		var curUserData = user_data[j]

		var x = d3.scale.linear()
		.domain([0, curMaxData])
		.range([0, options.radius]);

		(function (curUserData,j){

			// plot data
			var curPoints = chart.selectAll('.ptg-' + j).data(curUserData).enter().append('svg:circle')
			.attr('cx', function(d,i) { return origin.x + Math.cos(curAngle*Math.PI/180)*(x(curUserData[i][0])) })
			.attr('cy', function(d,i) { return origin.y - Math.sin(curAngle*Math.PI/180)*(x(curUserData[i][0])) })
			.attr('r', 7)
			.attr('class', 'ptg-' + j)
			.attr('fill', function (d, i) { return temp_color_ranges[i] })

			.on('mouseover', function (d,i) {
				var o = d3.select(this)
				o.attr('fill', 'lightgray');
				// point hover tip text
				var temp_the_text = temp_axes_labels[j] + ': ' + curUserData[i][1] + ' - ' + Math.round(curUserData[i][0]*100)/100 + ' ' + temp_axes_units[j]
				document.getElementById('profile-radar-chart-tip').innerHTML = temp_the_text

			})
			.on('mouseout', function (d,i) {
				var o = d3.select(this)
				.attr('fill', function (d, k) { return temp_color_ranges[i] })
			})

		})(curUserData,j);

//		// label the axes grids
//		var gridText  = chart.selectAll('.gridtext-' + j).data(curGridData).enter().append('svg:text')
//		.attr('x', function (d,i) { return origin.x + Math.cos(curAngle*Math.PI/180)*(x(curGridData[i])) } )
//		.attr('y', function (d,i) { return origin.y - Math.sin(curAngle*Math.PI/180)*(x(curGridData[i])) } )
//		.attr('text-anchor', 'middle')
//		.text(String)

	}


}


function plot_1d_line(raw_data, chart_div) {
	// chart_div : selector for the container div that will hold the chart
	// max : the maximum value for the chart
	// raw_data : array in [ [1.2, 'Label 1'], [2.3, 'Label 2'], ...] form

	data = []
	labels = []
	for (var i in raw_data) {
		data.push(raw_data[i][0]) // extract numbers from dictionary
		labels.push(raw_data[i][1]) // extract labels from dictionary
	}

	var h = 120
	var w = 800
	var rpadding = 80
	var lpadding = rpadding

	var x = d3.scale.linear()
	.domain([0, d3.max(data)])
	.range([lpadding, w-rpadding])


	var chart = d3.select(chart_div)
	.append('svg:svg')
	.attr('width', w)
	.attr('height', h)
	.append('svg:g')
	.attr('class', 'chart-area')
	.attr('transform', 'translate(0,80)')

	chart.append('svg:line')
	.attr('y1', 5)
	.attr('y2', 5)
	.attr('x1', lpadding)
	.attr('x2', w-rpadding)
	.attr('stroke', '#000')

	chart.selectAll('line.tick')
	.data(x.ticks(30))
	.enter().append('svg:line')
	.attr('class', 'tick')
	.attr('x1', x)
	.attr('x2', x)
	.attr('y1', 0)
	.attr('y2', 10)
	.attr('stroke', '#666')

	var points = chart.selectAll('g.point')
	.data(data).enter()
	.append('svg:g')
	.attr('class', 'point')
	.attr('x', x)
	.attr('y', 7)
	.on('mouseover', function (d,i) {
		var pg = d3.select(this)
		pg.select('.point-circle-you')
		.attr('stroke','#00BFFF')
		.attr('fill', 'white')
		.attr('r', 20)
		pg.select('.point-circle')
		.attr('stroke','#FFB90F')
		.attr('fill', 'white')
		.attr('r', 20)
		pg.append('svg:text')
		.attr('text-anchor','middle')
		.attr('fill', 'black')
		.attr('x', pg.attr('x'))
		.attr('y', pg.attr('y'))
		.attr('dy',5)
		.style('pointer-events', 'none')
		.attr('class', 'temp')
		.text(Math.round(d*10)/10)
	})
	.on('mouseout', function (d,i) {
		var pg = d3.select(this)
		pg.select('.point-circle-you')
		.attr('fill','#1874CD')
		.attr('stroke', 'white')
		.attr('r', 7)
		pg.select('.point-circle')
		.attr('fill','#FF8C00')
		.attr('stroke', 'white')
		.attr('r', 7)
		pg.select('.temp').remove()
	})

	points.append('svg:circle')
	.attr('cx', x)
	.attr('cy', 5)
	.attr('r', 7)
	//.attr('class','point-circle')
	.attr('class', function (d,i) {return i == data.length-1 ? 'point-circle-you' : 'point-circle'} )
	.attr('stroke', 'white')
	.attr('stroke-width', 2)
	.attr('fill', function (d, i) { return i == data.length-1 ? '#1874CD' : '#FF8C00' })

	points.append('svg:text')
	.text( function(d,i) { return labels[i]})
	.attr('text-anchor', 'left')
	.attr('letter-spacing', 1.5)
	.attr('font-family', 'Sans-Serif')
	.attr('font-size', '3em')
	.attr('font-weight', 'normal')
	.attr('transform', function (d,i) {
		return 'translate(' + (d/d3.max(data)*(w-rpadding-lpadding) + lpadding) + ',-5),rotate(-45)'
	})


	//.attr('transform', 'rotate(-45)')
	//.attr('x', x)

}

function items_at(arrayOfArrays, anIndex) {
	// arrayOfArrays : an array of arrays
	// anIndex : the index of the items to retrieve in an array of arrayOfArrays
	var result = []
	for (var i = 0; i < arrayOfArrays.length; i++) {
		result.push(arrayOfArrays[i][anIndex])
	}
	return result
}


function initialize() {
	// create radar chart of overall comparisons

	$.ajax({
		url: "/tripography/api/statistics/",
		type: 'GET',
		data: { user_id: user_id,
			types: 'comparisons_all_latest' } ,
			success: function (data) {
				//console.log(this.data)
			}
	})
	
	
	$.ajax({
		url: "/tripography/api/statistics/", 
		data: { user_id: user_id,
			types: 'comparisons_all_latest' } ,
			success: function (data) {

				var comparisons_temp = $.extend(true, {}, comparisons_ini)
				/*
				console.log('comp temp test')
				console.log(comparisons_temp)

				var temp = data.comparisons_all_latest
				console.log('temp test')
				console.log(data)*/
				var temp = data.comparisons_all_latest

				comparisons_temp.emissions.push([temp.emissions, 'You'])
				comparisons_temp.calories.push([parseInt(temp.calories), 'You'])
				comparisons_temp.cost.push([temp.cost, 'You'])
				comparisons_temp.time.push([parseFloat(temp.time), 'You'])

				//   var radar_colors = [ // first column: bay area, second national, third study, etc...
//				['#32985F','#36A567','#3AB26F','#3EBF77','#43CD80'], // green
//				['#5AA7E7','#5196D0','#4885B9','#3F74A2','#36648B'], // blue
//				['#DA6FD5','#C665C2','#B25BAF','#9E519C','#8B4789'], // purple
//				['#FF4500','#E73E00','#D03800','#B93100','#A22B00'], // red
//				]

				var radar_colors = [ 
				                    '#32985F', // green
				                    '#DA6FD5', // purple
				                    '#FF4500', // red
				                    ]

				var colorLabels = ['SF Bay Area',
				                   'US National',
				                   'You']

				// make some 1D line graphs of user comparisons (all time) using D3
				plot_comparisons_radar(comparisons_temp, radar_colors, '#profile-radar-chart')

				// create legend
				var htmlStr = '<table>'

					htmlStr += '<tr><td colspan="2"><span class="radar-legend-title">Average Travel Statistics</span></td> </tr>'
						htmlStr += '<tr>' + 
						'<td><span class="radar-color-box" style="background: ' + radar_colors[radar_colors.length - 1] +'; "></span></td>' +	
						'<td><span class="radar-legend-text">'+colorLabels[radar_colors.length - 1]+'</span></td>' + 

						'</tr>'

						for (var i = 0; i < radar_colors.length - 1; i++) {
							htmlStr += '<tr>' + 
							'<td><span class="radar-color-box" style="background: ' + radar_colors[i] +'; "></span></td>' +	
							'<td><span class="radar-legend-text">'+colorLabels[i]+'</span></td>' + 

							'</tr>'
						}
				htmlStr += '</table>' + '<p>More statistics (such as those for other cities and for the study group) will be added as the study progresses.</p>'
				$('#comparisons-legend').html(htmlStr)
			}
	})



	// load some statistics about the user
	$.ajax({
		url: "/tripography/api/statistics/",
		data: { user_id: user_id,
			types: 'user_stats' },
			success: function (data) {
				//console.log('stats data')
				//console.log(data)
				$('.total-trips-logged').html(parseInt(data.user_stats.total_trips))
				$('.total-miles-logged').html(parseInt(data.user_stats.total_miles))
				$('.total-time-logged').html(parseInt(data.user_stats.total_time) + " minutes")
			}
	})


	// create a timeline for the user's stats
	/* 
	 * Old, custom style.
	 * Rather hideous.
	 * 
	 */
	/*
	$.ajax({
		url: "api/statistics/",
		data: { user_id: user_id,
			types: 'vs_time' },
			success: function (data) {
				plot_vs_time(data.vs_time.date, data.vs_time.cost, comparisons_ini.cost, '#vstime_cost')
				plot_vs_time(data.vs_time.date, data.vs_time.time, comparisons_ini.time, '#vstime_time')
				plot_vs_time(data.vs_time.date, data.vs_time.calories, comparisons_ini.calories, '#vstime_calories')
				plot_vs_time(data.vs_time.date, data.vs_time.emissions, comparisons_ini.emissions, '#vstime_emissions')
			}
	})
	 */

//	$.ajax({
//	url: "api/statistics/",
//	data: { user_id: user_id,
//	types: 'vs_time' },
//	success: function (data) {
//	plot_vs_time(data.vs_time.date, data.vs_time.cost, comparisons_ini.cost, '#vstime_cost')
//	plot_vs_time(data.vs_time.date, data.vs_time.time, comparisons_ini.time, '#vstime_time')
//	plot_vs_time(data.vs_time.date, data.vs_time.calories, comparisons_ini.calories, '#vstime_calories')
//	plot_vs_time(data.vs_time.date, data.vs_time.emissions, comparisons_ini.emissions, '#vstime_emissions')
//	}
//	})




}