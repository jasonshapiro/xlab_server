var map, bounds, tripPathPoly;
var tripPathArray = [];
var markersArray = [];
var visMarkersArray = [];
var androidSMArray = [];
var hotspotsArray = [];

var showingStateMachineData = true;
var showingVisData = false;
var showingRawData = true;
var showingHotspots = true;

var AJAX_CALL_PATH = '/traces/debug/';
var BLUE_DOT_PATH = '/static/web/images/debug/bluedot.PNG';
var BLUE_MARKER_PATH = '/static/web/images/debug/blue-marker.png';
var GREEN_MARKER_PATH = '/static/web/images/debug/green-marker.png';
var YELLOW_MARKER_PATH = '/static/web/images/debug/yellow-marker.png';
var PURPLE_MARKER_PATH = '/static/web/images/debug/purple-marker.png';
var RED_DOT_PATH = '/static/web/images/debug/red_dot.png';
var STANDING_MAN_PATH = '/static/web/images/debug/Man-icon.png';
var HOTSPOT_ICON_PATH = '/static/web/images/debug/fire-icon.png';

function mapInitialize() {
    var latlng = new google.maps.LatLng(37.8716667, -122.2716667); //Berkeley
    var myOptions = {
        zoom: 12,
        center: latlng,
        scaleControl: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"),
        myOptions);
}

function addMarker(marker) {
    markersArray.push(marker);
}

function addVisMarker(marker) {
    visMarkersArray.push(marker);
}

function addSMMarker(marker) {
    androidSMArray.push(marker);
}

//Clear all data in preparation for a new request
function clearData() {
    if (markersArray) {
        clearRawData();
        markersArray.length = 0;
    }

    if (visMarkersArray) {
        clearVisData();
        visMarkersArray.length = 0;
    }

    if (androidSMArray) {
        clearSMData();
        androidSMArray.length = 0;
    }

    if (hotspotsArray) {
        clearHotspotData();
        hotspotsArray.length = 0;
    }

    if(tripPathPoly != null) {
        tripPathPoly.setMap(null);
        tripPathArray.length = 0;
    }
}

function clearRawData() {
    for (var i in markersArray) {
        markersArray[i].marker.setMap(null);
    }
}

function clearVisData() {
    for (var i in visMarkersArray) {
        visMarkersArray[i].marker.setMap(null);
    }
}

function clearSMData() {
    for (var i in androidSMArray) {
        androidSMArray[i].marker.setMap(null);
    }
}

function clearHotspotData() {
    for (var i in hotspotsArray) {
        hotspotsArray[i].setMap(null);
    }
}

function loadData(userId, timestamp, tripLength, maxAccuracy) {
    $("#load_traces_form span").text("Loading traces...").show();
    
    //Clear the existing markers
    clearData();

    var submit = {type: 'fetch', user_id: userId, timestamp: timestamp,
                        trip_length: tripLength, max_accuracy: maxAccuracy};

    $.post(AJAX_CALL_PATH, submit, function(data) {
        //console.debug(data);
        var cnt = 0;
        bounds = new google.maps.LatLngBounds();

        var location = data['location'];
        var android_sm = data['android_sm'];
        var hotspots = data['hot_spots'];

        $.each(location, function(key, t) {
            var latlng = new google.maps.LatLng(t.lat, t.lon);
            tripPathArray.push(latlng);

            //Display normal markers
            var marker = new google.maps.Marker({
                position: latlng,
                map: map,
                title: t.id + ", " + t.lat + ", " + t.lon + ", " +
                        t.sample_time + ", " + t.travel_mode + ", " + t.velocity
            });

            if( $("#load_traces_form input[name='highlight_accuracy']").is(':checked') ) {
                var color;
                if(t.course == 1) color = YELLOW_MARKER_PATH;
                else if(t.course == 10) color = GREEN_MARKER_PATH;
                else if(t.course == 100) color = BLUE_MARKER_PATH;
                else if(t.course == 1000) color = PURPLE_MARKER_PATH;
                marker.setIcon(color);
            }

            var contentString = '<table>' +
                                    '<tr><td>ID</td><td>' + t.id + '</td></tr>' +
                                    '<tr><td>Lat</td><td>' + t.lat + '</td></tr>' +
                                    '<tr><td>Lon</td><td>' + t.lon + '</td></tr>' +
                                    '<tr><td>Epoch Time</td><td>' + t.sample_time_epoch + '</td></tr>' +
                                    '<tr><td>Sample Time</td><td>' + t.sample_time + '</td></tr>' +
                                    '<tr><td>Service Provider</td><td>' + t.service_provider + '</td></tr>' +
                                    '<tr><td>Velocity</td><td>' + t.velocity + '</td></tr>' +
                                    '<tr><td>Altitude</td><td>' + t.altitude + '</td></tr>' +
                                    '<tr><td>Fix accuracy</td><td>' + t.accuracy + ' m</td></tr>' +
                                    '<tr><td>Accuracy used</td><td>' + t.course + '</td></tr>' +
                                '</table>';
            var infowindow = new google.maps.InfoWindow({
                content: contentString
            });

            google.maps.event.addListener(marker, 'click', function() {
                infowindow.open(map,marker);
            });

            addMarker({
                id: t.id,
                marker: marker
            });

            //Display circles
            var strokeColor = "red";
            if(t.service_provider != null) {

                if(t.service_provider.toLowerCase() == "wifi_yes" ||
                    t.service_provider.toLowerCase() == "network" ||
                    t.service_provider.toLowerCase() == "net") {
                    strokeColor = "green";
                } else if(t.service_provider.toLowerCase() == "network-passive") {
                    strokeColor = "blue";
                } else if(t.service_provider.toLowerCase() == "gps-passive") {
                    strokeColor = "#FF6600"; //Orange
                } else if(t.service_provider.toLowerCase() == "gsm" ||
                    t.service_provider.toLowerCase() == "cdma") {
                    strokeColor = "yellow";
                }
            }

            var visMarker = new google.maps.Circle({
                center: latlng,
                radius: parseInt(t.accuracy),
                clickable: true,
                fillColor: "red",
                fillOpacity: 0,
                strokeColor: strokeColor,
                strokeWeight: 1
            });

            addVisMarker({
                id: t.id,
                marker: visMarker
            });

            bounds.extend(latlng);
            map.fitBounds(bounds);
            cnt++;
        });

        //Prepare the polyline
        tripPathPoly = new google.maps.Polyline({
            path: tripPathArray,
            strokeColor: "#3939fc",
            strokeOpacity: 0.6,
            strokeWeight: 3
        });

        if(cnt > 0) {
            $("#load_traces_form span").text("Loaded " + cnt + " traces").show();
            $("#raw_data").text("Hide raw data").show();
            $("#vis_data").text("Show vis data").show();
        } else {
            $("#load_traces_form span").text("No traces were found.").show();
        }

        //Load Android state machine data if it is available
        if(android_sm != null && android_sm.length > 0) {
            cnt = 0;
            $.each(android_sm, function(key, sm) {
                var smLatlng = new google.maps.LatLng(sm.lat, sm.lon);
                var smMarker = new google.maps.Marker({
                    position: smLatlng,
                    map: map,
                    icon: RED_DOT_PATH
                });

                var smContentString = '<table>' +
                                        '<tr><td>Lat</td><td>' + sm.lat + '</td></tr>' +
                                        '<tr><td>Lon</td><td>' + sm.lon + '</td></tr>' +
                                        '<tr><td>Sample Time</td><td>' + sm.sample_time + '</td></tr>' +
                                        '<tr><td>SM Data</td><td>' + sm.data + '</td></tr>' +
                                    '</table>';
                var smInfowindow = new google.maps.InfoWindow({
                    content: smContentString
                });

                google.maps.event.addListener(smMarker, 'click', function() {
                    smInfowindow.open(map, smMarker);
                });

                addSMMarker({
                    id: sm.id,
                    marker: smMarker
                });

                cnt++;
            });

            if(cnt > 0) {
                $("#sm_data").text("Hide state machine data").show();
            }
        }

        //Show hot spots if they are available
        if(hotspots != null && hotspots.length > 0) {
            cnt = 0;
            $.each(hotspots, function(key, hs) {
                var hLatlng = new google.maps.LatLng(hs.lat, hs.lon);
                var hotspotMarker = new google.maps.Marker({
                    position: hLatlng,
                    icon: HOTSPOT_ICON_PATH
                });

                var hsContentString = '<table>' +
                                        '<tr><td>Lat</td><td>' + hs.lat + '</td></tr>' +
                                        '<tr><td>Lon</td><td>' + hs.lon + '</td></tr>' +
                                        '<tr><td>Description</td><td>' + hs.desc + '</td></tr>' +
                                    '</table>';
                var hsInfowindow = new google.maps.InfoWindow({
                    content: hsContentString
                });

                google.maps.event.addListener(hotspotMarker, 'click', function() {
                    hsInfowindow.open(map, hotspotMarker);
                });

                hotspotMarker.setMap(map);
                hotspotsArray.push(hotspotMarker);

                cnt++;
            });

            if(cnt > 0) {
                $("#hotspot_data").text("Hide hot spots").show();
            }
        }
    });
}

$(document).ready(function() {
    $("#load_traces_form span").hide();
    $("#raw_data").hide();
    $("#vis_data").hide();
    $("#sm_data").hide();

    //Show the map
    mapInitialize();

    //Check if this request has GET params and handle accordingly
    var userId = getQueryVariable("user_id");
    var timestamp = getQueryVariable("timestamp");
    var tripLength = getQueryVariable("trip_length");
    var maxAccuracy = getQueryVariable("max_accuracy");
    var standLat = getQueryVariable("stand_lat");
    var standLon = getQueryVariable("stand_lon");

    if(userId != null && timestamp != null && tripLength != null &&
        maxAccuracy != null) {

        $("#load_traces_form select[name='user_id']").val(userId);
        $("#load_traces_form input[name='timestamp']").val(decodeURIComponent(timestamp));
        $("#load_traces_form input[name='trip_length']").val(tripLength);
        $("#load_traces_form input[name='max_accuracy']").val(maxAccuracy);

        loadData(userId, decodeURIComponent(timestamp), tripLength, maxAccuracy);
    }

    //Show the standing marker if available
    if(standLat != null && standLon != null) {
        var standLatlng = new google.maps.LatLng(standLat, standLon);
        var standMarker = new google.maps.Marker({
            position: standLatlng,
            map: map,
            icon: STANDING_MAN_PATH
        });
    }

    //Load traces
    $("#load_traces").submit( function() {        
        var userId = $("#load_traces_form select[name='user_id'] option:selected").val();
	if(userId == null) { userId = jQuery.trim($("#load_traces_form input[name='user_id']").val()); }
        var timestamp = jQuery.trim($("#load_traces_form input[name='timestamp']").val());
        var tripLength = jQuery.trim($("#load_traces_form input[name='trip_length']").val());
        var maxAccuracy = jQuery.trim($("#load_traces_form input[name='max_accuracy']").val());
        
        loadData(userId, decodeURIComponent(timestamp), tripLength, maxAccuracy);
        
        return false;
    });

    $('#raw_data').live("click", function() {
        if(showingRawData) {
            clearRawData();
            showingRawData = false;
            $('#raw_data').text("Show raw data");
        } else if (markersArray.length != 0) {
            for (var i in markersArray) {
                markersArray[i].marker.setMap(map);
            }
            showingRawData = true;
            $('#raw_data').text("Hide raw data");
        } else {
            alert("Raw data not available!");
        }

        return false;
    });

    $('#vis_data').live("click", function() {
        if(showingVisData) {
            clearVisData();
            tripPathPoly.setMap(null);
            showingVisData = false;
            $('#vis_data').text("Show vis data");
        } else if (visMarkersArray.length != 0) {
            for (var i in visMarkersArray) {
                visMarkersArray[i].marker.setMap(map);
            }
            tripPathPoly.setMap(map);
            showingVisData = true;
            $('#vis_data').text("Hide vis data");
        } else {
            alert("Vis data not available!");
        }

        return false;
    });

    $('#sm_data').live("click", function() {
        if(showingStateMachineData) {
            clearSMData();
            showingStateMachineData = false;
            $('#sm_data').text("Show state machine data");
        } else if (androidSMArray.length != 0) {
            for (var i in androidSMArray) {
                androidSMArray[i].marker.setMap(map);
            }
            showingStateMachineData = true;
            $('#sm_data').text("Hide state machine data");
        } else {
            alert("State machine data not available!");
        }

        return false;
    });

    $('#hotspot_data').live("click", function() {
        if(showingHotspots) {
            clearHotspotData();
            showingHotspots = false;
            $('#hotspot_data').text("Show hot spots");
        } else if (hotspotsArray.length != 0) {
            for (var i in hotspotsArray) {
                hotspotsArray[i].setMap(map);
            }
            showingHotspots = true;
            $('#hotspot_data').text("Hide hot spots");
        } else {
            alert("Hot spots not available!");
        }

        return false;
    });

    //Download labeled data for the selected user and time period
    $('#download_data_form').submit(function() {
        //We fetch the selected user and time period details from the "Load Traces" form
        var userId = $("#load_traces_form select option:selected").val();
	if(userId == null) { userId = jQuery.trim($("#load_traces_form input[name='user_id']").val()); }

        var timestamp = jQuery.trim($("#load_traces_form input[name='timestamp']").val());
        var tripLength = jQuery.trim($("#load_traces_form input[name='trip_length']").val());

        var params = {
          'type': 'download',
          'user_id': userId,
          'timestamp': timestamp,
          'trip_length': tripLength
        };

        $.each(params, function(name, value){
            $('<input />').attr('type', 'hidden')
                .attr('name', name)
                .attr('value', value)
                .appendTo('#download_data_form');
        });

        return true;
    });
});


