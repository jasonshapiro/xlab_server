/**
 * @author Jason Shapiro
 */


function capitaliseFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
};
	
	
function dialogGenerator(data1) {
	$("#content").prepend('<div class="dialog">','</div>')
	for (x in data1.objects) {
		$("#dialog").append('<submit id="objectno' + x.id + '" value="' + x.info.title + '">')
	}
};


/// if this round is chose, you will get a ___ with a 50% chance and ___ with a 50% chance.

function budgetGenerator(data1, objectno, responseno) {
	
	$(".dialog").remove()
	$("#loading").show().fadeOut(1000);

	var objectno = (typeof objectno !== 'undefined') ? objectno : 0;
	var responseno = (typeof responseno !== 'undefined') ? responseno : 1;
				
	var xdata = (data1.objects[objectno].info.x_max - data1.objects[objectno].info.x_min) * Math.random() + data1.objects[objectno].info.x_min
	var ydata = (data1.objects[objectno].info.y_max - data1.objects[objectno].info.y_min) * Math.random() + data1.objects[objectno].info.y_min
	
	/// Display Formatting Functions
	
	
	
	/// Data Formatting for Different Types (requires currency to be '-' for non-monetary values)
	
	if (data1.objects[objectno].info.currency != '-') {
		var xmax = ymax = Math.max(data1.objects[objectno].info.x_max, data1.objects[objectno].info.y_max);
		var xlabel = ylabel = '';
		var curlabel = data1.objects[objectno].info.currency;
		var unitdecimal = 2;
	}
	else {
		var xmax = data1.objects[objectno].info.x_max;
		var ymax = data1.objects[objectno].info.y_max;
		var xlabel = capitaliseFirstLetter(data1.objects[objectno].info.x_units) + " of " + capitaliseFirstLetter(data1.objects[objectno].info.x_label);
		var ylabel = capitaliseFirstLetter(data1.objects[objectno].info.y_units) + " of " + capitaliseFirstLetter(data1.objects[objectno].info.y_label);
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
	;
	
	window.setTimeout(function() {
		$("#wrapper").animate({opacity: 1}, 1000)
		}, 1000);
	
	
	// Slider Initialization
	
	$("#sliderd").slider({ 
		min: 0,
		max: xdata.toFixed(unitdecimal),
		step: Math.pow(.1,unitdecimal),
		slide: function( event, ui ) {
				
				// Aesthetic Hack: y value displaying as -0.0
				
				var yval = (ydata - (ydata/xdata)*ui.value).toFixed(unitdecimal);
					
				$( "#displayx" ).val( curlabel + ui.value + " " + xlabel );
				if (yval <= 0) {
					$( "#displayy" ).val( curlabel + 0 + " " + ylabel );	
				}
				else {
					$( "#displayy" ).val( curlabel + yval + " " + ylabel );	
				};
		
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

}; // end budgetGenerator

// Beginning of Script 

var objectnum;
var responsenum;
var globaldata;

$(document).ready(function() {

	$("#wrapper").css("opacity",".01");
	
	var url = "http://127.0.0.1/api/v1/budget_line/?format=json";
	
	$.ajax(url, {
		dataType: "json",
		crossDomain: true,
		success: function(data) {
			console.log(data);
			globaldata = data;
			$("#loading").hide();
			
			if (data.objects.length == 0 || data.objects === "undefined") {
				// Display Message about no experiments
			}
			else {
				
			}
			
			
			
			
			
			
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			alert('Failure: ' + XMLHttpRequest + "\n TextStatus: " + textStatus + "\n Error Thrown: " + errorThrown )
		}
	});

});
