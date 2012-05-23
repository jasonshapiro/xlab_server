/**
 * @author Jason Shapiro
 */

//// AJAX

function capitaliseFirstLetter(string)
	{
	    return string.charAt(0).toUpperCase() + string.slice(1);
	}
	

/// if this round is chose, you will get a ___ with a 50% chance and ___ with a 50% chance.
function budgetGenerator (data1) {
//var data1 = {"budget_line_info": {"prob_x": 0.5, "y_max": 200.0, "y_units": "dollars", "lines_per_session": 50, "x_label": "", "y_label": "", "title": "Cash Money", "currency": "$", "number_sessions": 1, "x_units": "dollars", "x_max": 200.0, "x_min": 100.0, "probabilistic": true, "id": 13, "y_min": 100.0}};
var data1 = {"budget_line_info": {"prob_x": 0.5, "y_max": 20.0, "y_units": "pounds", "lines_per_session": 50, "x_label": "apples", "y_label": "oranges", "title": "Apples or Oranges", "currency": "-", "number_sessions": 1, "x_units": "pounds", "x_max": 30.0, "x_min": 10.0, "probabilistic": false, "id": 4, "y_min": 10.0}};

//function budgetGenerator(data1) {
		
	var xdata = (data1.budget_line_info.x_max - data1.budget_line_info.x_min) * Math.random() + data1.budget_line_info.x_min
	var ydata = (data1.budget_line_info.y_max - data1.budget_line_info.y_min) * Math.random() + data1.budget_line_info.y_min
	
	/// Display Formatting Functions
	
	
	
	/// Data Formatting for Different Types (requires currency to be '-' for non-monetary values)
	
	if (data1.budget_line_info.currency != '-') {
		var xmax = ymax = Math.max(data1.budget_line_info.x_max, data1.budget_line_info.y_max);
		var xlabel = ylabel = '';
		var curlabel = data1.budget_line_info.currency;
		var unitdecimal = 2;
	}
	else {
		var xmax = data1.budget_line_info.x_max;
		var ymax = data1.budget_line_info.y_max;
		var xlabel = capitaliseFirstLetter(data1.budget_line_info.x_units) + " of " + capitaliseFirstLetter(data1.budget_line_info.x_label);
		var ylabel = capitaliseFirstLetter(data1.budget_line_info.y_units) + " of " + capitaliseFirstLetter(data1.budget_line_info.y_label);
		var curlabel = '';
		var unitdecimal = 1;
	};
	
	// Plot Intialization
	
	
	var placeholder = $('#placeholder');
	
	var data = [{ 
				data: [[xdata,0], [0, ydata]],
				lines: { show: true, fill: true }
			},
			{	
				data: [[0, ydata]],
				points: {
						show: true,
						radius: 5}
			}];
	
	var options = {
		colors: [ "#f6931f", "#000000"],
		xaxis: {
			min: 0,
			max: xmax,
			ticks: 5,
				},
		yaxis: {
			min: 0,
			max: ymax,
			ticks: 5,
				}
		};
	
	
	var plot = $.plot(placeholder, data, options);
	
	
	// Slider Initialization
	
	$("#sliderd").slider({ 
		min: 0,
		max: xdata.toFixed(unitdecimal),
		step: Math.pow(.1,unitdecimal),
		slide: function( event, ui ) {
				$( "#displayx" ).val( curlabel + ui.value + " " + xlabel );
				$( "#displayy" ).val( curlabel + (ydata - (ydata/xdata)*ui.value).toFixed(unitdecimal) + " " + ylabel );
								
				var dataSet = [{ 
				data: [[xdata,0], [0, ydata]],
				lines: { show: true, fill: true }
			},
			{	
				data: [[ ui.value, (ydata - (ydata/xdata)*ui.value).toFixed(unitdecimal) ]],
				points: {
						show: true,
						radius: 5
						}
			}];
				plot.setData(dataSet);
				plot.draw();
				
			} 
			});
	$( "#displayx" ).val( curlabel + $( "#sliderd" ).slider( "value" ) + " " + xlabel );
	$( "#displayy" ).val( curlabel + ydata.toFixed(unitdecimal) + " " + ylabel );

//////// TODO: Automatically Focus Slider For keyboard movement	$( "sliderd" ).slider().focus()

///	$( "#submit" ).click(function() {
		
//	})

/// TODO: parameter for post be client.desktop


};



var url = "http://127.0.0.1/experiments/budget/?format=json";

console.log(url)


$.ajax(url, {
	dataType: "json",
	crossDomain: true,
	success: function(data) {
		console.log(data);
		budgetGenerator(data);
	},
	error: function(XMLHttpRequest, textStatus, errorThrown) {
		alert('Failure: ' + XMLHttpRequest + "\n TextStatus: " + textStatus + "\n Error Thrown: " + errorThrown )
	}
});



