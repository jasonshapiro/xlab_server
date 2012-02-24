/*
 * 
 *  Trends:
 *  	* refactor such that json object are jqplot-compatible datapoints
 *  	* ability to go previous/next
 *  		* need:
 *  			first score date
 *  			last score date
 *  			number of scores to retrieve
 * 
 * 
 */

var VIEWS = ['day', 'week', 'weeks4', 'all']
var VIEWS_RANGE = {
		'day': 7*24*60*60*1000, // 7 days 
		'week': 8*7*24*60*60*1000, // 8 weeks
		'weeks4': 4*4*7*24*60*60*1000, // 2 4 weeks
		'all': 9999*365.25*24*60*60*1000 // 9999 years
		}
//view: 0: daily | 1: weekly | 2: every 4 weeks | 3: all

var user
var trends_plot
var trends_plot_data
var trends_view = VIEWS[0]
var trends_data_bounds
var trends_data_economics_money
var trends_data_economics_time
var trends_data_emissions
var trends_data_calories
var trends_min_date // Date object
var trends_max_date // Date object

var trends_plot_options = {}
trends_plot_options.series_visible = [true, true, true, true]
trends_plot_options.options = {
	    axes: {
	    	xaxis: {
	    		renderer: $.jqplot.DateAxisRenderer,
	    		tickOptions: {
	    			mark: 'outside',
	    			formatString: '%b %d'
	    			},
    			tickInterval: '1 day'
	    		},
    		yaxis: {
    			label: 'Score',
    			min: 0,
    			max: 10,
    			labelRenderer: $.jqplot.CanvasAxisLabelRenderer
    			}
    		},
    	highlighter: {
    		show: true,
    		showLabel: true,
    		tooltipAxes: 'xy',
    		formatString: '%s - %s'
    	}    	
	}

function initialize_trends() {
	register_trends_view_buttons()
	register_lines_view_buttons()
	load_trends_data_bounds()
	$('.trends .day-view').trigger('click')
}

function refresh_trends() {
	setup_trends_scroller()
	get_trends_data(trends_view, trends_min_date.getTime()/1000, trends_max_date.getTime()/1000)
	plot_trends_data()
}


function register_trends_view_buttons() {
	function r() {
		refresh_trends()
		$('.trends .view .button').removeClass('active')
	}
	
	$('.trends .day-view').click( function() { trends_view=VIEWS[0]; r() ; $(this).addClass('active') })
	$('.trends .week-view').click( function() { trends_view=VIEWS[1]; r() ; $(this).addClass('active') })
	$('.trends .weeks4-view').click( function() { trends_view=VIEWS[2]; r() ; $(this).addClass('active') })
	// $('.trends .year-view').click( function() { trends_view=VIEWS[3]; r() ; $(this).addClass('active') })
}

function unregister_trends_view_buttons() {
	$('.trends .day-view').unbind()
	$('.trends .week-view').unbind()
	$('.trends .weeks4-view').unbind()
	// $('.trends .year-view').unbind()
}

function register_lines_view_buttons() {
	// Perhaps useful to let the user turn on/off lines
	
	function r(series) {
		trends_plot_options.series_visible[series] = !trends_plot_options.series_visible[series]
		plot_trends_data()
	}
	
	$('.trends .lines .economics_money').click( function() { $(this).toggleClass('disabled'); r(0) } )
	$('.trends .lines .economics_time').click( function() { $(this).toggleClass('disabled'); r(1) } )
	$('.trends .lines .emissions').click( function() { $(this).toggleClass('disabled'); r(2) } )
	$('.trends .lines .calories').click( function() { $(this).toggleClass('disabled'); r(3) } )
	
}


function load_trends_data_bounds(user_input) {
	user = typeof(user_input) != 'undefined' ? user_input : user
	$.ajax('/tripography/statistics/get_stats_bounds/',{
		type: 'GET',
		async: false,
		data: {user: user},
	    success: function (data) {
	    	trends_data_bounds = data
	    }
	})
}

function setup_trends_scroller(user_input) {
	user = typeof(user_input) != 'undefined' ? user_input : user
	
	var pre_bounds = eval('trends_data_bounds.' + trends_view)
	var bounds = {min: new Date(pre_bounds.min*1000), max: new Date(pre_bounds.max*1000)}
	var defaultValues = {min: new Date(pre_bounds.max*1000 - VIEWS_RANGE[trends_view]), max: new Date(pre_bounds.max*1000)}
	
	trends_min_date = defaultValues.min
	trends_max_date = defaultValues.max

	$('#trends_scroller').unbind().replaceWith('<div id="trends_scroller" class="dateSlider"></div>')
	
	$('#trends_scroller').dateRangeSlider({
		  defaultValues: defaultValues,
		  bounds: bounds,
		  wheelMode: null,
		  wheelSpeed: 8,
		  arrows: true,
		  valueLabels: "show",
		  formatter: function(value){
		    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
		    var day = value.getDate();
		    return "" + months[value.getMonth()] + " " + (day < 10 ? "0" + day : day ) + ", " + value.getFullYear()
		  },
		  durationIn: 0,
		  durationOut: 400,
		  delayOut: 200
		})
		.bind('valuesChanged', function(event,ui) { 
			trends_min_date = new Date(ui.values.min)
			trends_min_date.setHours(0,0,0,0)
			trends_max_date = new Date(ui.values.max)
			trends_max_date.setHours(0,0,0,0)
			get_trends_data(trends_view, trends_min_date.getTime()/1000, trends_max_date.getTime()/1000)
			plot_trends_data()
		})
	
}

function convert_epoch_to_datetime_string(time) {
	var myDate = new Date(time*1000)
	return myDate.format('yyyy-MM-dd h:mma')
}

function get_trends_data(interval, start_range, end_range, user_input) {
	
	// default arguments
	//interval = typeof(interval) != 'undefined' ? interval : 'day'
	user = typeof(user_input) != 'undefined' ? user_input : user
	//start_range = typeof(start_range) != 'undefined' ? start_range : 'first'
	//end_range = typeof(end_range) != 'undefined' ? end_range : 'last'
	
	$.ajax({
		url: "api/statistics/",
		data: {
			user_id: user_id,
			types: 'vs_time2'
			},
	    success: function (data) {
	    	
	    	console.log('whutup')
	    	console.log(data)
	    	
	    	// plot the data....
	    	$('#vstime .economics_money.icon.button').trigger('click')
	    	
	    	trends_data_economics_money = []
	    	trends_data_economics_time = []
	    	trends_data_emissions = []
	    	trends_data_calories = []
	    	for (var i = 0; i < data.length; i++) {
	    		var dt = convert_epoch_to_datetime_string(data[i].fields.score_start_time)
	    		trends_data_economics_money.push([dt, parseFloat(data[i].fields.economics_money)])
	    		trends_data_economics_time.push([dt,parseFloat(data[i].fields.economics_time)])
	    		trends_data_emissions.push([dt,parseFloat(data[i].fields.emissions)])
	    		trends_data_calories.push([dt,parseFloat(data[i].fields.calories)])
	    		

	    	}
	    	
    		plot_data =  [
    		              trends_data_economics_money,
    		              trends_data_economics_time,
    		              trends_data_emissions,
    		              trends_data_calories]
	    }
	})
}

function plot_trends_data() {
	
	$('#trends_canvas').empty();
	
	//console.log(plot_data)
	
	if (plot_data[0].length < 1) {
		
		$('#trends_canvas').html('<span class="nodata">No data available for plotting for selected view.</span>');
		$('#trends_scroller').slideUp()
		
	} else {
		
		var options = trends_plot_options.options
		options.axes.xaxis.min = trends_min_date.toString()
		options.axes.xaxis.max = trends_max_date.toString()
		
		
		trends_plot = $.jqplot('trends_canvas', plot_data, options);
		
		trends_plot.series[0].show = trends_plot_options.series_visible[0]
		trends_plot.series[1].show = trends_plot_options.series_visible[1]
		trends_plot.series[2].show = trends_plot_options.series_visible[2]
		trends_plot.series[3].show = trends_plot_options.series_visible[3]
		
		trends_plot.redraw()
	
	}
	
}

/*=====================================================*/
/*=====================================================*/
/*=====================================================*/

comparisons = {}
comparisons.data = {}
comparisons.plots = {}

comparisons.data.emissions = [
                              [8.8, 0, 'Bay Area'],
			                  [8.1, 0, 'National Average'],
			                  [1, 0, 'Recommended']
			                 ]

comparisons.data.calories = [
			                  [156, 0, 'Recommended']
			                 ]

comparisons.data.economics_money = [
                              [6750, 0, 'Bay Area'],
			                  [4500, 0, 'National Average'],
			                  [3750, 0, 'Recommended']
			                 ]

comparisons.data.economics_time = [
                                    [76, 0, 'Bay Area'],
      			                    [85, 0, 'National Average']
      			                 ]


function initialize_comparisons() {

	function r(d, p) {
		// convert d to float and round to p digits
		return Math.round(parseFloat(d)*(10^p))/(10^p)
	}
	
	$.ajax( '/tripography/statistics/get_comparisons/', {
		type: 'GET',
		async: false,
		data: {user: user},
		success: function(data, status, jqXHR) {
//			console.log('Comparisons data:')
//			console.log(data)
//			console.log(status)
//			console.log(jqXHR)
			
			comparisons.data.emissions.unshift([ r(data.emissions, 1), 0,'You'])
			comparisons.data.calories.unshift([ r(data.calories, 1), 0,'You'])
			comparisons.data.economics_money.unshift([ r(data.economics_money, 1), 0,'You'])
			comparisons.data.economics_time.unshift([ r(data.economics_time, 1), 0,'You'])
			
//			console.log('Emissions / Calories / Economics Money / Economics Time')
//			console.log(comparisons.data)
//			console.log(r(data.emissions, 1))
//			console.log(r(data.calories, 1))
//			console.log(r(data.economics_money, 1))
//			console.log(r(data.economics_time, 1))
		}
	})
	
	plot_comparisons()
} 

function plot_comparisons() {
	
	comparisons.plots.economics_money = plot_comparisons_data('comparisons_plot_economics_money', comparisons.data.economics_money)
	comparisons.plots.economics_time = plot_comparisons_data('comparisons_plot_economics_time', comparisons.data.economics_time)
	comparisons.plots.emissions = plot_comparisons_data('comparisons_plot_emissions', comparisons.data.emissions)
	comparisons.plots.calories = plot_comparisons_data('comparisons_plot_calories', comparisons.data.calories)
}

function plot_comparisons_data(canvas_id, data) {
	
	function get_bounds(data) {
		var min = 999999
		var max = -999999
		for (var i = 0; i < data.length; i++) {
			var x = data[i][0]
			min = x < min ? x : min;
			max = x > max ? x : max;
		}
		var padding = (max-min)/4.0;
		return {min: min-padding, max: max+padding}
	}
	
	var bounds = get_bounds(data)
	
	var options  = { 
		seriesDefaults: {
		      showMarker : true,
		      showLine: false,
		      color: '#339933',
		      pointLabels: { show: true, location: 's' }
		    },
	    series: [
	             { markerOptions: {color: '#ff9900'} },
	             { markerOptions: {color: '#339933'} }
	             ],
	    axes: {
	    	xaxis: {
	    		min: bounds.min >= 0 ? bounds.min : 0,
	    		max: bounds.max
	    	},
	    	yaxis: {
	    		min: -1,
	    		max: 0.5,
	    		showTicks: false
	    	}
	    }, 
	    grid: {
	    	drawBorder: false,
	    	drawGridlines: true,
	    	shadow: false,
	    	background: '#ccffcc'
	    },
    	highlighter: {
			show: true,
			showLabel: true,
			tooltipAxes: 'x',
			formatString: '%.1f',
			tooltipLocation: 'n'
    	}
    	
	}
	
	var you = data.shift()
	
	
	return $.jqplot(canvas_id, [data, [you]], options)
}