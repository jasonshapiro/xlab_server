var mouseOverMarker;

var originalWayPoints = [];
var directionsWaypointArray = [];

//Trip data
var locationData, androidData, tripSummaryInfo, nextTripSummaryInfo,
    prevTripSummaryInfo, travelModes, hotspots, travelModeOverride;
var tripPathPoly, nextTripPathPoly, prevTripPathPoly, googleEncodedPathPoly;
var traces = [];
var tripPathArray = [];
var networkCircleMarkersArray = [];
var gpsCircleMarkersArray = [];
var simpleMarkersArray = [];
var infowindowArray = [];
var hotspotsArray = [];

var TRIP_DATA_PATH = '/slicer/trip/data/';
var SLICER_APPROVE_ENDPOINT = '/slicer/approve/';
var RED_DOT_PATH = '/static/web/images/debug/red_dot.png';
var YELLOW_MARKER_PATH = '/static/web/images/debug/yellow-marker.png';
var HOTSPOT_ICON_PATH = '/static/web/images/debug/fire-icon.png';
var MAX_POLYLINE_ACCURACY = 100;
var DRIVE_MODE = 1;

var showingNetworkCircleMarkers = true;
var showingGpsCircleMarkers = true;
var showingSimpleMarkers = false;
var showingCenterPolyline = false;
var showingPrevNextTrips = false;
var showingGoogleEncodedPolyline = true;
var showingHotspots = true;

function initialize(trip_id) {
    //Fetch the trip data
    var getParams = "st=" + st_window + "&et=" + et_window + "&acc=" + accuracy;
    $.get(TRIP_DATA_PATH + trip_id + '/?' + getParams, function(data) {
        locationData = data['traces'];
        if ("android_sm" in data) androidData = data['android_sm'];
        travelModes = data['travel_modes'];
        if ("hot_spots" in data) hotspots = data['hot_spots'];

        tripSummaryInfo = data['trip_summary'];

        if (tripSummaryInfo.velocity_profile != null &&
            tripSummaryInfo.velocity_profile != "") {
            var traceStrArray = tripSummaryInfo.velocity_profile.split("|");
            for (var i in traceStrArray) {
                var parts = traceStrArray[i].split(",");
                traces.push({'lat': parts[0], 'lon': parts[1],
                    'time': parts[2], 'v': parts[3]});
            }
        }

        if ("prev_trip_summary" in data &&
            data['prev_trip_summary'].travel_mode == DRIVE_MODE) {
            prevTripSummaryInfo = data['prev_trip_summary'];
        }
        if ("next_trip_summary" in data &&
            data['next_trip_summary'].travel_mode == DRIVE_MODE) {
            nextTripSummaryInfo = data['next_trip_summary'];
        }

        $('#loading').hide();

        mapInitialize();

        drawTrip();
        $("#trip_summary").html(getTripSummaryInfo());
        $("#delete_waypoints").html(getWayPointList());

        if(traces.length > 0) {
            renderVelocityData();
        } else {
            $("#velocity_vis").html("<span style=\"margin: 100px; font-weight: bold;\">Velocity profile is not available.</span>");
        }
    });
}

function drawTrip() {
    var cnt = 0;
    bounds = new google.maps.LatLngBounds();
    
    //Draw the location markers
    $.each(locationData, function(key, t) {
        var simpleMarker;
        var latlng = new google.maps.LatLng(t.lat, t.lon);

        //Don't show the points which are not part of the trip here....
        if(parseInt(t.hacc) < MAX_POLYLINE_ACCURACY) {
            tripPathArray.push(latlng);
        }

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

        var marker = new google.maps.Circle({
            map: map,
            center: latlng,
            radius: parseInt(t.hacc),
            clickable: true,
            strokeColor: strokeColor,
            strokeWeight: 1,
            fillOpacity: 0
        });

        if(t.service_provider != null &&
            (t.service_provider.toLowerCase() == "gps-passive" ||
                t.service_provider.toLowerCase() == "gps") ) {
            gpsCircleMarkersArray.push(marker);
        } else {
            networkCircleMarkersArray.push(marker);
        }
        if(t.time >= tripSummaryInfo.start_time && t.time <= tripSummaryInfo.end_time) {
            simpleMarker = new google.maps.Marker({
                position: latlng
            });
        } else {
            //Next and previous trips get a yellow marker
            simpleMarker = new google.maps.Marker({
                position: latlng,
                icon: YELLOW_MARKER_PATH
            });
        }
        simpleMarkersArray.push(simpleMarker);

        var contentString = '<table>' +
                                '<tr><td>ID</td><td>' + t.id + '</td></tr>' +
                                '<tr><td>Lat</td><td>' + t.lat + '</td></tr>' +
                                '<tr><td>Lon</td><td>' + t.lon + '</td></tr>' +
                                '<tr><td>Epoch Time</td><td>' + t.time + '</td></tr>' +
                                '<tr><td>Sample Time</td><td>' + dateFormat(new Date(t.time * 1000),
                                    "mmmm dS, h:MM TT") + '</td></tr>' +
                                '<tr><td>Service Provider</td><td>' + t.service_provider + '</td></tr>' +
                                '<tr><td>Velocity</td><td>' + (t.v / 0.44704).toFixed(2) + ' mph</td></tr>' +
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

    //Load Android state machine data if it is available
    if(androidData != null && androidData.length > 0) {
        $.each(androidData, function(key, sm) {
            var smLatlng = new google.maps.LatLng(sm.lat, sm.lon);
            var smMarker = new google.maps.Marker({
                position: smLatlng,
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

            simpleMarkersArray.push(smMarker);

            bounds.extend(smLatlng);
            map.fitBounds(bounds);
        });
    }

    //Create the hotspots array
    if (hotspots != null) {
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
        });
    }

    //Draw the Google directions
    if(tripSummaryInfo.direction_waypoints == null ||
        tripSummaryInfo.direction_waypoints == "") {
        alert("Direction waypoints are missing!");
    }
    var waypointStrArray = tripSummaryInfo.direction_waypoints.split("|");
    for (var i in waypointStrArray) {
        var latLngArray = waypointStrArray[i].split(",");
        originalWayPoints.push(new google.maps.LatLng(latLngArray[0], latLngArray[1]));
    }

    originLatLng = originalWayPoints[0];
    destLatLng = originalWayPoints[ originalWayPoints.length - 1 ];
    
    for (var j in originalWayPoints) {
        if(j == 0 || j == (originalWayPoints.length - 1) ) {
            continue;
        }
        var latlng = originalWayPoints[j];

        directionsWaypointArray.push({'location':latlng, 'stopover': false});
    }

    googleDirectionsRenderer = new google.maps.DirectionsRenderer({
        'map': map,
        'draggable': true
    });

    google.maps.event.addListener(googleDirectionsRenderer, 'directions_changed', function() {
        currentDirections = googleDirectionsRenderer.getDirections();
        updatedRoute = currentDirections.routes[0];
    });

    calcRoute();
    polylines();
}

function polylines() {
    //Prepare the polyline joining the center of every location marker
    //Draw the polyline
    tripPathPoly = new google.maps.Polyline({
        path: tripPathArray,
        strokeColor: "red",
        strokeOpacity: 0.9,
        strokeWeight: 3
    });

    if(tripSummaryInfo.google_encoded_path != null) {
        googleEncodedPathPoly = new google.maps.Polyline({
            path: google.maps.geometry.encoding.decodePath(
                tripSummaryInfo.google_encoded_path),
            strokeColor: "greenyellow",
            strokeOpacity: 0.9,
            strokeWeight: 3
        });
        googleEncodedPathPoly.setMap(map);
    }

    //Draw the prev and next trips
    if(prevTripSummaryInfo != null) {
        //Sanity check
        if(prevTripSummaryInfo.google_encoded_path == null) {
            alert("Google encoded path for trip " +
                prevTripSummaryInfo.id + " is null!");
        }
        
        prevTripPathPoly = new google.maps.Polyline({
            path: google.maps.geometry.encoding.decodePath(
                    prevTripSummaryInfo.google_encoded_path),
            strokeColor: "#FF6600",
            strokeOpacity: 0.9,
            strokeWeight: 3
        });
        //prevTripPathPoly.setMap(map);

        var prevString = '<table>' +
                                '<tr><td>Type</td><td>Previous</td></tr>' +
                                '<tr><td>Start time</td><td>' + dateFormat(
                                    new Date(prevTripSummaryInfo.start_time * 1000),
                                    "mmmm dS, h:MM TT") + '</td></tr>' +
                                '<tr><td>End time</td><td>' + dateFormat(
                                    new Date(prevTripSummaryInfo.end_time * 1000),
                                    "mmmm dS, h:MM TT") + '</td></tr>' +
                            '</table>';

        var prevInfowindow = new google.maps.InfoWindow({
            content: prevString
        });

        google.maps.event.addListener(prevTripPathPoly, 'click', function() {
            prevInfowindow.open(map, prevTripPathPoly);
        });
    }

    if (nextTripSummaryInfo != null) {
        //Sanity check
        if(nextTripSummaryInfo.google_encoded_path == null) {
            alert("Google encoded path for trip " +
                nextTripSummaryInfo.id + " is null!");
        }
        
        nextTripPathPoly = new google.maps.Polyline({
            path: google.maps.geometry.encoding.decodePath(
                    nextTripSummaryInfo.google_encoded_path),
            strokeColor: "#660000",
            strokeOpacity: 0.9,
            strokeWeight: 3
        });
        //nextTripPathPoly.setMap(map);

        var nextString = '<table>' +
                                '<tr><td>Type</td><td>Next</td></tr>' +
                                '<tr><td>Start time</td><td>' + dateFormat(
                                    new Date(nextTripSummaryInfo.start_time * 1000),
                                    "mmmm dS, h:MM TT") + '</td></tr>' +
                                '<tr><td>End time</td><td>' + dateFormat(
                                    new Date(nextTripSummaryInfo.end_time * 1000),
                                    "mmmm dS, h:MM TT") + '</td></tr>' +
                            '</table>';

        var nextInfowindow = new google.maps.InfoWindow({
            content: nextString
        });

        google.maps.event.addListener(nextTripPathPoly, 'click', function() {
            nextInfowindow.open(map, nextTripPathPoly);
        });
    }

    if(prevTripSummaryInfo == null && nextTripSummaryInfo == null) {
        $('#show_adjacent_trips').text("Next / prev trips not available");
    }    
}

function getWayPointList() {
    var wayPointListStr = "";
    for (var i in directionsWaypointArray) {
        var dw = directionsWaypointArray[i];

        wayPointListStr += '<li><a href="#" class="waypoint">' + dw.location.lat() + "," +
            dw.location.lng() + '</a></li>';
    }

    return wayPointListStr;
}

function getTravelMode() {
    if(travelModeOverride != null) {
        return travelModeOverride;
    }
    
    var mode = google.maps.DirectionsTravelMode.DRIVING;
    if (tripSummaryInfo == null || travelModes == null) {
        return mode;
    }

    if(travelModes[tripSummaryInfo.travel_mode] == "Walk") {
        mode = google.maps.DirectionsTravelMode.WALKING;
        $("input[name='google_travel_mode'][value='walk']").prop('checked', true);
    }
    else if(travelModes[tripSummaryInfo.travel_mode] == "Drive") {
        $("input[name='google_travel_mode'][value='drive']").prop('checked', true);
    }
    /*
    else if(travelModes[tripSummaryInfo.travel_mode] == "Bike") {
        mode = google.maps.DirectionsTravelMode.BICYCLING;
    }
    */
   
    return mode;
}

function calcRoute() {

    var request = {
        origin: originLatLng,
        destination: destLatLng,
        travelMode: getTravelMode(),
        optimizeWaypoints: false,
        waypoints: directionsWaypointArray
    };

    googleDirectionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            googleDirectionsRenderer.setDirections(response);
        }
    });
}

function getTripSummaryInfo() {
    //Format start time
    var start_time = dateFormat(new Date(tripSummaryInfo.start_time * 1000), "mmmm dS, h:MM TT");
    var end_time = dateFormat(new Date(tripSummaryInfo.end_time * 1000), "mmmm dS, h:MM TT");
    var dist_traveled = (tripSummaryInfo.distance_traveled / 1609.344);

    var gpsCircleMarkerStr = showingGpsCircleMarkers ? "Hide GPS bubbles" : "Show GPS bubbles";
    var networkCircleMarkerStr = showingNetworkCircleMarkers ? "Hide Network bubbles" : "Show Network bubbles";
    var centerpolylineStr = showingCenterPolyline ? "Hide polyline" : "Show polyline";

    var contentString = '<table>' +
                            '<tr><th>User</th><td>' + tripSummaryInfo.username + '</td></tr>' +
                            '<tr><th>Start time</th><td>' + start_time + '</td></tr>' +
                            '<tr><th>End time</th><td>' + end_time + '</td></tr>' +
                            '<tr><th>Travel mode</th><td>' + travelModes[tripSummaryInfo.travel_mode] + '</td></tr>' +
                            '<tr><th>Dist. traveled</th><td>' + dist_traveled.toFixed(2) + ' miles</td></tr>' +
                            '<tr><th>Score</th><td>' + tripSummaryInfo.score + '</td></tr>' +
                            '<tr>' +
                                '<td><a id="gps_circle_markers" href="#">' + 
                                    gpsCircleMarkerStr + '</a> / <a id="network_circle_markers" href="#">' +
                                    networkCircleMarkerStr + '</a>' +
                                '</td>' +
                                '<td>' +
                                    '<a id="center_polyline" href="#">' +
                                    centerpolylineStr + '</a>' +
                                '</td>' +
                             '</tr>' +
                        '</table>';

    //Populate the trip summary info in the submission form
    $("#approve_trip_form input[name='start_time']").val(
        dateFormat(new Date(tripSummaryInfo.start_time * 1000), "mm/dd/yyyy HH:MM"));
    $("#approve_trip_form input[name='end_time']").val(
        dateFormat(new Date(tripSummaryInfo.end_time * 1000), "mm/dd/yyyy HH:MM"));

    return contentString;
}

$(document).ready(function() {
    $('#loading').hide();
    initialize(trip_id);

    //Toggle the travel mode sent to Google
    $("input[name='google_travel_mode']").change(function() {
        if ($("input[name='google_travel_mode']:checked").val() == 'drive') {
            travelModeOverride = google.maps.DirectionsTravelMode.DRIVING;
        }
        else{
            travelModeOverride = google.maps.DirectionsTravelMode.WALKING;
        }

        //Recalculate the route with the new mode
        calcRoute();
    });

    $('#approve_trip_form').submit( function() {
        approveTrip(tripSummaryInfo.user_id, updatedRoute, currentDirections,
            SLICER_APPROVE_ENDPOINT + tripSummaryInfo.ts_id + "/",
            tripSummaryInfo.ts_id);

        return false;
    });

    $('#approve_original_trip').click( function() {
        var submit = {use_original: 1}
        
        var submitUrl = SLICER_APPROVE_ENDPOINT + tripSummaryInfo.id + "/";
        $.post(submitUrl, submit, function(data) {
            if (data == "1") {
                window.close();
                //Change the backgorund color on non standing trip
                if (window.opener && ! window.opener.closed &&
                        tripSummaryInfo.id != null) {
                    var rowId = "row" + tripSummaryInfo.id;
                    var tr = window.opener.document.getElementById(rowId);
                    tr.style.backgroundColor = "greenyellow";
                }
            } else {
                alert("An error occurred - " + data);
            }
        });
    });
    
    $(".waypoint").live( {
        click: function() {
            var latLonArray = $(this).text().split(",");

            //Create the new way point list
            var tempWaypointArray = [];
            for (var i in directionsWaypointArray) {
                var dw = directionsWaypointArray[i];

                //Use all the waypoints except the one selected
                if (dw.location.lat() != latLonArray[0] ||
                    dw.location.lng() != latLonArray[1]) {
                    tempWaypointArray.push(dw);
                }
            }
            directionsWaypointArray.length = 0;
            directionsWaypointArray = tempWaypointArray;

            //Refresh the directions
            calcRoute();
            $("#delete_waypoints").html(getWayPointList());
            if (mouseOverMarker != null) {
                mouseOverMarker.setMap(null);
            }
        },
        mouseover: function() {
            var latLonArray = $(this).text().split(",");
            var latLon = new google.maps.LatLng(latLonArray[0], latLonArray[1]);
            mouseOverMarker = new google.maps.Marker({
                position: latLon,
                map: map
            });
        },
        mouseout: function() {
            if (mouseOverMarker != null) {
                    mouseOverMarker.setMap(null);
            }
        }
    });

    $('#gps_circle_markers').live("click", function() {
        if(showingGpsCircleMarkers) {
            for (var i in gpsCircleMarkersArray) {
                gpsCircleMarkersArray[i].setMap(null);
            }
            showingGpsCircleMarkers = false;
            $('#gps_circle_markers').text("Show GPS bubbles");
        } else if (gpsCircleMarkersArray != null) {
            for (var j in gpsCircleMarkersArray) {
                gpsCircleMarkersArray[j].setMap(map);
            }
            showingGpsCircleMarkers = true;
            $('#gps_circle_markers').text("Hide GPS bubbles");
        } else {
            alert("GPS traces not available!");
        }

        return false;
    });

    $('#network_circle_markers').live("click", function() {
        if(showingNetworkCircleMarkers) {
            for (var i in networkCircleMarkersArray) {
                networkCircleMarkersArray[i].setMap(null);
            }
            showingNetworkCircleMarkers = false;
            $('#network_circle_markers').text("Show Network bubbles");
        } else if (networkCircleMarkersArray != null) {
            for (var j in networkCircleMarkersArray) {
                networkCircleMarkersArray[j].setMap(map);
            }
            showingNetworkCircleMarkers = true;
            $('#network_circle_markers').text("Hide Network bubbles");
        } else {
            alert("Network traces not available!");
        }

        return false;
    });

    $('#center_polyline').live("click", function() {
        if(showingCenterPolyline) {
            tripPathPoly.setMap(null);
            showingCenterPolyline = false;
            $('#center_polyline').text("Show polyline");
        } else if (tripPathPoly != null) {
            tripPathPoly.setMap(map);
            showingCenterPolyline = true;
            $('#center_polyline').text("Hide polyline");
        } else {
            alert("Polyline not available!");
        }

        return false;
    });

    $('#show_adjacent_trips').live("click", function() {
        if(showingPrevNextTrips) {
            if(nextTripPathPoly != null) nextTripPathPoly.setMap(null);
            if(prevTripPathPoly != null) prevTripPathPoly.setMap(null);
            showingPrevNextTrips = false;
            $('#show_adjacent_trips').text("Show next / prev trips");
        } else if (nextTripPathPoly != null || prevTripPathPoly != null) {
            if(nextTripPathPoly != null) nextTripPathPoly.setMap(map);
            if(prevTripPathPoly != null) prevTripPathPoly.setMap(map);
            showingPrevNextTrips = true;
            $('#show_adjacent_trips').text("Hide next / prev trips");
        } else {
            alert("Next / prev trips not available!");
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

    $('#show_google_encoded').live("click", function() {
        if(showingGoogleEncodedPolyline) {
            googleEncodedPathPoly.setMap(null);
            showingGoogleEncodedPolyline = false;
            $('#show_google_encoded').text("Show Google encoded path");
        } else if (googleEncodedPathPoly != null) {
            googleEncodedPathPoly.setMap(map);
            showingGoogleEncodedPolyline = true;
            $('#show_google_encoded').text("Hide Google encoded path");
        } else {
            alert("Google encoded path not available!");
        }

        return false;
    });

    $('#show_hotspots').live("click", function() {
        if(showingHotspots) {
            for (var i in hotspotsArray) {
                hotspotsArray[i].setMap(null);
            }
            showingHotspots = false;
            $('#show_hotspots').text("Show hotspots");
        } else if (hotspotsArray.length != 0) {
            for (var i in hotspotsArray) {
                hotspotsArray[i].setMap(map);
            }
            showingHotspots = true;
            $('#show_hotspots').text("Hide hotspots");
        } else {
            alert("Hotpsots not available!");
        }

        return false;
    });
});