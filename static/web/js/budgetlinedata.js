/**
 * @author Jason Shapiro
 */


function capitaliseFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
};

function dialogGenerator(data1) {
	$( "#content" ).prepend('<div class="dialog" style="display:block; margin: 0px auto">','</div>');
	$( ".dialog" ).prepend('<h1> You Have Multiple Experiments: </h1>','<p> Please Select the One You Wish to Take Below </p>');
	
	for (var i =0; i < data1.objects.length; i++) {
			$( ".dialog" ).append('<input type="submit" id="objectno' + i + '" value="' + data1.objects[i].info.title + '" style="margin: 10px" onClick="budgetGenerator(globaldata, ' + i + ',interceptglo)">');
	}
};


/// if this round is chose, you will get a ___ with a 50% chance and ___ with a 50% chance.

function budgetGenerator(data1, objectno, interceptno) {
	
	$(".dialog").remove()
	$("#loading").show().fadeOut(500);

	var objectno = (typeof objectno !== 'undefined') ? objectno : 0;
	objectglo = objectno;

// Not Robust - Add error catching for edge cases
	
	if (data1.objects[objectno].intercepts == null || typeof data1.objects[objectno].intercepts[interceptglo] === 'undefined') {
		$( "#wrapper" ).hide();
		$( "#content" ).prepend('<h1> The Experiment is Complete </h1>', '<p> Click <a href="http://xmobile.berkeley.edu/"> here </a> to return to the homepage. </p>')
	}
	else {
					
		var xdata = Number(data1.objects[objectno].intercepts[interceptno].x_intercept);
		var ydata = Number(data1.objects[objectno].intercepts[interceptno].y_intercept);
		
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
	
		
		window.setTimeout(function() {
			$("#wrapper").animate({opacity: 1}, 500)
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
						$( "#displayy" ).val( curlabel + 0.00 + " " + ylabel );	
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
					
				} ,
			value: 0
			});
		$( "#displayx" ).val( curlabel + $( "#sliderd" ).slider( "value" ) + " " + xlabel );
		$( "#displayy" ).val( curlabel + ydata.toFixed(unitdecimal) + " " + ylabel );
	
		$( "#senddata" ).click(function() {
			$( "#senddata" ).unbind();
			var url = 'http://xmobile.berkeley.edu/api/v1/budget_line_input/' + globaldata.objects[objectglo].intercepts[interceptglo].response_id + '/';
			$("#wrapper").animate({opacity: .01}, 300);
			
			window.setTimeout(function() {
				
				$( "#loading" ).fadeIn(300);
				$.ajax(url, {
					data: '{"progress": ' + Math.round(100 * $( "#sliderd").slider( "value" ) / globaldata.objects[objectglo].intercepts[interceptglo].x_intercept) + '}',
					type: 'PUT',
					contentType: "application/json",
					success: function() {
						interceptglo++;
						budgetGenerator(globaldata, objectglo, interceptglo);
					},
					error: function() {
						alert('Error: Contact an adminstrator and tell them that Jason screwed up.') // TODO: FIX COPY
					}
				})
			
			}, 300);			
				
		});
	
	};
	
	
	
//////// TODO: Automatically Focus Slider For keyboard movement	$( "sliderd" ).slider().focus()

}; // end budgetGenerator

// Beginning of Script 


var globaldata;
var objectglo;
var interceptglo = 0;

$(document).ready(function() {

	$("#wrapper").css("opacity",".01");
	
	var url = "http://xmobile.berkeley.edu/api/v1/budget_line/?format=json";
	
	$.ajax(url, {
		dataType: "json",
		crossDomain: true,
		success: function(data) {
			globaldata = data;
			$("#loading").hide();
			
			if (data.objects.length == 0 || data.objects === "undefined") {
				alert('You have no experiments. Please contact an administrator.');				
			}
			else if (data.objects.length == 1) {
				budgetGenerator(data)
			}
			else {
				dialogGenerator(data)
			}
			
			
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			alert('Failure: ' + XMLHttpRequest + "\n TextStatus: " + textStatus + "\n Error Thrown: " + errorThrown )
		}
	});

});
