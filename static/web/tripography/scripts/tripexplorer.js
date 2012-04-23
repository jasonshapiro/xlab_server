var map;
var trip_list = new Array();
var filters = {};
var TRAVEL_MODES = new Array('Unknown', 'Drive', 'Walk', 'Bike', 'Bus',
		'Train','Running','Stand','Light Rail','Not Driving','Not Standing' ,'Motorbike');
//'Train','Running','Stand','Light Rail','Not Driving','Not Standing', 'Motorized Bicycle');

var PATH_COLORS = [
                   '#ff6666','#ffcc00','#ccff00','#33ff00','#00cc66',
                   '#33ccff', '#3366ff','#cc66ff', '#ff66ff','#993333',
                   '#996600','#66cc00','#006666', '#336699','#996699'
                   ]

var zCounter = 1

function strip_tags(input) {
	return input.replace(/(<([^>]+)>)/ig,"")
}


function initialize_filters() {
	
	$('.filter-date').datepicker({
		maxDate: "-1D",
		onSelect: function (dateText) { 
			filters.start_date = dateText;
			load_trips();
			}
	});
	
	filters.start_date = $.datepicker.formatDate('m/d/yy', $('.filter-date').datepicker('getDate'));
	filters.user_id = user_id;
	
	$('.filter-form').change( function () { load_trips(); return false; });
};

function initialize_map() {

	//set up the google map
	var latlng = new google.maps.LatLng(37.8717, -122.2718);
	var myOptions = {
	  zoom: 11,
	  center: latlng,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	map = new google.maps.Map(document.getElementById("map_canvas"),myOptions);
	
	// add a method to get bounds of a polyline
	google.maps.Polyline.prototype.getBounds = function () {
		var bounds = new google.maps.LatLngBounds();
		this.getPath().forEach(function(e) {
			bounds.extend(e);
		});
		return bounds;
	};
	
};

function getKeys(obj) {
	var keys = [];
	for (var key in obj) {
		keys.push(key);
	}
	return keys;
};

function get_type(thing){
    if(thing===null)return "[object Null]"; // special case
    return Object.prototype.toString.call(thing);
}

function process_get_trips(data) {

	for (var i = 0; i < data.length; i++ ) {
		var trip_info = data[i].fields;
		var decoded_path_latlngs = google.maps.geometry.encoding.decodePath(trip_info.encoded_path);
		var polyOptions = {
				  // TODO: Should eventually make a set of polyline colors
				  strokeColor: PATH_COLORS[i],
			      strokeOpacity: 1.0,
			      strokeWeight: 5,
			      path: decoded_path_latlngs,
			      zIndex: zCounter
				};
		zCounter++
		trip_info.color = PATH_COLORS[i];
		trip_info.decoded_path_latlngs = decoded_path_latlngs;
		trip_info.path = new google.maps.Polyline(polyOptions);
		trip_list.push(trip_info);
	}
	
	update_tripsummary_table();
	update_loaded_trips_info();
	plot_loaded_trips();
	register_tripsummary_table_controls();

}

function update_tripsummary_table() {
	
	var display_fields = new Array('origin_address','dest_address','travel_mode', 'calories');
	//console.log(foo = trip_list);
	
	var HTMLString;
	var TRString = '';
	for (var i in trip_list ) {
		trip = trip_list[i]
		//console.log(getKeys(trip));
		
		// travel mode select dropdown menu
		var tmString = '<select class="travel_mode_edit">';
		
		// if there is a user correction, display the user's correction 
		if (parseInt(trip.corrected_travel_mode) != 0) {
			trip.travel_mode = trip.corrected_travel_mode
		}
		
		for (var j in TRAVEL_MODES) {
			if (trip.travel_mode == j) {
				tmString += '<option value="' + j + '" selected="selected">' + TRAVEL_MODES[j] + '</option>';
			} else {
				tmString += '<option value="' + j + '">' + TRAVEL_MODES[j] + '</option>';
			}
		}
		tmString += '</select>';
		
		var start_time = new Date(trip.start_time*1000)
		var duration = Math.round((trip.end_time - trip.start_time)/60.0)
		
		// var notes = trip.notes == null ? "" : trip.notes
		// var notesStr = '<textarea class="notes-edit">' + notes + '</textarea>'
		
		var TDString = '' +
			'<td class="trip_color"><span style="background: ' + trip.color + ';"> </span></td>' +
			'<td class="origin_address">' + trip.origin_address + '</td>' +
			'<td class="dest_address">' + trip.dest_address + '</td>' +
			'<td class="travel_mode">' + tmString + '</td>' +
			'<td class="start_time">' + start_time.format('hh:mm a') + '</td>' +
			'<td class="duration">' + duration + '</td>' +
			'<td class="distance">' + Math.round(trip.distance_traveled/1609.344*10)/10 + '</td>' +
			// '<td class="notes">' + notesStr + '</td>' +
			'<td class="expand hidden"><a class="expand-link"><span></span></td>' +
			'<td class="edit hidden"><a class="edit-link"><span class="hidden">Edit<span></a></td>' +
			'<td class="save hidden"><a class="save-link"><span class="hidden">Save<span></a></td>';
		TRString += '<tr class="data">' + TDString + '</tr>';
		
		var TDString2 = '' +
			'<td colspan="8">' +
				'<div class="data2-content hidden">' + 
					'here is some more stuff!' + 
				'</div>' +
			'</td>';
		
		TRString += '<tr class="data2 hidden">' + TDString2 + '</tr>';
	};
	
	HTMLString = '' + 
		'<table class="tripsummary-table">' + 
			'<thead>' + 
				'<td class="trip_color"></td>' +
				'<td class="origin_address">Origin Address</td>' +
				'<td class="dest_address">Destination Address</td>' +
				'<td class="travel_mode">Mode</td>' +
				'<td class="start_time">Start Time</td>' +
				'<td class="duration">Duration (min)</td>' +
				'<td class="distance">Miles</td>' +
				// '<td class="notes">Notes</td>' +
				'<td class="expand hidden"></td>' +
				'<td class="edit hidden">Edit</td>' +
				'<td class="save hidden">Save</td>' +
			'</thead>' + 
			'<tbody>' + TRString + '</tbody>' +  
		'</table>';
	
	$('#trip-explorer-trips-list').html( HTMLString );
	//console.log(HTMLString);
}

function update_loaded_trips_info() {
	
	var t = $.datepicker.formatDate('MM d, yy', $('.filter-date').datepicker('getDate'));
	var HTMLString;
	if (trip_list.length > 0) {
		var tripform = trip_list.length > 1 ? 'trips' : 'trip';
		HTMLString = trip_list.length + ' ' + tripform + ' recorded for ' + t + '.'
	} else {
		HTMLString = 'No trips recorded for ' + t;
	}
	
	HTMLString = '<p>' + HTMLString + '</p>';
	$('.loaded-trips-info').html( HTMLString );
	
}

function clear_paths() {
	for (var i in trip_list) {
		trip_list[i].path.setMap(null);
	}
}

function plot_loaded_trips() {
	
	if (trip_list.length > 0) {
		var latlngbounds = new google.maps.LatLngBounds();
		for (var i in trip_list) {
			var latlngs = trip_list[i].decoded_path_latlngs;
			for (var j in latlngs) { latlngbounds.extend(latlngs[i]) } // for zooming to fit loaded trips
			plot_path(trip_list[i].path);
		}
		map.fitBounds(latlngbounds);
	}
}

function plot_path(path) {
	path.setMap(map);
}


function get_trip_paths(tripsummary_table) {
	paths = new Array();
	var encoded_paths_td = $(tripsummary_table).find('.data').each( function(i, trip_data) {
		var tripid = parseInt($(trip_data).find('.id').text());
		var encoded_path = $(trip_data).find('.encoded_path').text();
		var path_coords = google.maps.geometry.encoding.decodePath(encoded_path);
		
		var path = new google.maps.Polyline(polyOptions);
		paths[i] = {
			tripid: tripid,
			path: path
		};
		
	});
};

function register_tripsummary_table_controls() {
	
	$('.tripsummary-table').find('.data').each( function (i, row) {
		
		
		// mode editing
		$(row).find('.travel_mode_edit').toggleEdit(
				{
					onpreview: function(event, ui) {
						var modeSelected = ui.element[0].value;
						var trip_start_time = trip_list[i].start_time;
						$.ajax('/tripography/trip_explorer/edit_trip/',
								{
									data: { 
										travel_mode: modeSelected,
										start_time: trip_start_time,
										trip_owner: user_id
									},
									type: 'GET',
									success: function(data) {
										//console.log(data)
										// pass; blurring dropdown menu automatically saves
									} 
								});
					}
				}
			);
		

		
		// notes editing
		/*
		$(row).find('.notes-edit').toggleEdit(
				{
					onpreview: function(event, ui) {
						//ui.element[0].value = strip_tags(ui.element[0].value)
						$(row).find('.notes-edit.toggleEdit').val(strip_tags(ui.element[0].value))
						var new_notes = ui.element[0].value;
						var trip_start_time = trip_list[i].start_time;
						$.ajax('/tripography/trip_explorer/edit_trip/',
								{
									data: {
										notes: new_notes,
										start_time: trip_start_time
									},
									type: 'POST',
									success: function(data) { 
										// do nothing
									} 
								});
					}
				}
			);
		*/
		
		/*
		$(row).find('.expand-link').click( function() { $(row).next().slideToggle().find('.data2-content').slideToggle()  } )
		*/
		
		// edit/save links
		/*
		$(row).find('.edit-link').click( function() { set_edit_link(this, row) });
		
		$(row).hover( function() {
			trip_list[i].path.setOptions({zIndex: zCounter})
			zCounter++
		})
		*/
		
		// zoom and center on clicked trip
		$(row).click( function() {
			map.fitBounds(trip_list[i].path.getBounds()) // center on path
			trip_list[i].path.setOptions({zIndex: zCounter})
			zCounter++
			// bring the polyline to the front
		})
	})
}

function unregister_tripsummary_table_controls() {
	$('.edit-link, .save-link, .expand-link').unbind();
	
	$('.tripsummary-table').find('.data').each( function (i, row) {
		
		$(row).find('.travel_mode_edit').hide().toggleEdit('destroy');
	})
}

function set_edit_link(h, r) {
	//console.log('You clicked edit!');
	$(h).unbind();
	$(r).find('td.edit').addClass('hidden');
	$(r).find('td.save').removeClass('hidden').find('.save-link').click( function() { set_save_link(h, r) })
};


function set_save_link(h, r) {
	//console.log('You saved it!');
	$(h).unbind();
	$(r).find('td.save').addClass('hidden');
	$(r).find('td.edit').removeClass('hidden').find('.edit-link').click( function() { set_edit_link(h, r) })

};


function load_trips() {
	clear_paths();
	unregister_tripsummary_table_controls();
	
	trip_list = new Array();
	$.ajax( {
		type: 'GET',
		data: filters,
		url: '/tripography/trip_explorer/get_trips/',
		success: function(data) {
			
			console.log(filters)
			process_get_trips(data);
		}
	});
};