var simpleMarkersArray = [];
var infowindowArray = [];

var showingSimpleMarkers = true;

var SLICER_ADD_ENDPOINT = '/slicer/add/';
var HOTSPOT_ICON_PATH = '/static/web/images/debug/fire-icon.png';

function initialize() {
    mapInitialize();
    if(locationData.length > 0) {drawTrip();}
}

function drawTrip() {
    var cnt = 0;
    bounds = new google.maps.LatLngBounds();
    
    //Draw the location markers
    $.each(locationData, function(key, t) {
        var latlng = new google.maps.LatLng(t.lat, t.lon);        
        var simpleMarker = new google.maps.Marker({
            position: latlng,
            map: map
        });
        simpleMarkersArray.push(simpleMarker);

        var contentString = '<table>' +
                                '<tr><td>Lat</td><td>' + t.lat + '</td></tr>' +
                                '<tr><td>Lon</td><td>' + t.lon + '</td></tr>' +
                                '<tr><td>Epoch Time</td><td>' + t.time + '</td></tr>' +
                                '<tr><td>Sample Time</td><td>' + dateFormat(new Date(t.time * 1000),
                                    "mmmm dS, h:MM TT") + '</td></tr>' +
                                '<tr><td>Service Provider</td><td>' + t.service_provider + '</td></tr>' +
                                '<tr><td>Velocity</td><td>' + t.v + '</td></tr>' +
                                '<tr><td>Fix accuracy</td><td>' + t.hacc + ' m</td></tr>' +
                            '</table>';
        var infowindow = new google.maps.InfoWindow({
            content: contentString
        });
        infowindowArray.push(infowindow);

        google.maps.event.addListener(simpleMarker, 'click', function() {
            for(var i in infowindowArray) {
                infowindowArray[i].close();
            }
            infowindow.open(map,simpleMarker);
        });

        bounds.extend(latlng);
        map.fitBounds(bounds);
        cnt++;
    });

    //Add hot spots if they are available
    if (hotspots != null && hotspots.length > 0) {
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
        });
    }

    //Draw the Google Directions path
    var random1 = 0;
    var random2 = 0;
    if(locationData.length < 2) {
        alert("Insufficient location data points!");
    } else if (locationData.length == 2) {
        random1 = 0;
        random2 = 1;
    } else {
        var limit = locationData.length + 1;
        random1 = Math.floor(Math.random() * limit);
        while(random1 == random2) {
            random2 = Math.floor(Math.random() * limit);
        }
    }
    originLatLng = new google.maps.LatLng(locationData[random1].lat,
        locationData[random1].lon);
    destLatLng = new google.maps.LatLng(locationData[random2].lat,
        locationData[random2].lon);

    googleDirectionsRenderer = new google.maps.DirectionsRenderer({
        'map': map,
        'draggable': true
    });

    google.maps.event.addListener(googleDirectionsRenderer, 'directions_changed', function() {
        currentDirections = googleDirectionsRenderer.getDirections();
        updatedRoute = currentDirections.routes[0];
    });

    //Populate the trip summary info in the submission form
    $("#approve_trip_form input[name='start_time']").val(
        dateFormat(new Date(startTime * 1000), "mm/dd/yyyy HH:MM"));
    $("#approve_trip_form input[name='end_time']").val(
        dateFormat(new Date(endTime * 1000), "mm/dd/yyyy HH:MM"));

    calcRoute();
}

function calcRoute() {

    var request = {
        origin: originLatLng,
        destination: destLatLng,
        travelMode: google.maps.DirectionsTravelMode.DRIVING
    };

    googleDirectionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            googleDirectionsRenderer.setDirections(response);
        }
    });
}

$(document).ready(function() {
    $('#loading').hide();
    initialize();

    $('#approve_trip_form').submit( function() {
        var startTime = jQuery.trim($("#approve_trip_form input[name='start_time']").val());
        var endTime = jQuery.trim($("#approve_trip_form input[name='end_time']").val());

        //Start and end times are mandatory
        if (startTime == "" || endTime == "") {
            alert("Start and end times are mandatory!");
        } else {
        approveTrip(userId, updatedRoute, currentDirections,
            SLICER_ADD_ENDPOINT + "/?standing_trip=" + 
                getQueryVariable("standing_trip"), null);
        }
        return false;
    });


    $('#raw_trip_data').live("click", function() {
        if(showingSimpleMarkers) {
            for (var i in simpleMarkersArray) {
                simpleMarkersArray[i].setMap(null);
            }
            showingSimpleMarkers = false;
            $('#raw_trip_data').text("Show raw traces");
        } else if (simpleMarkersArray != null) {
            for (var j in simpleMarkersArray) {
                simpleMarkersArray[j].setMap(map);
            }
            showingSimpleMarkers = true;
            $('#raw_trip_data').text("Hide raw traces");
        } else {
            alert("Raw trace data not available!");
        }

        return false;
    });

});