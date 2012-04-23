var map, tripPathPoly, tripPathArray,
    marker, infowindow, eol;
var qvis;
var overlayMarkerArray = [];

var visHeight, visWidth, mapHeight,
    xAxisHeight = 20,
    visWidthPercentage = 0.7;

//Animation related
var step = 100; // metres
var tick = 100; // milliseconds
var animationInProgress = false;

//Trip data
var traces, tripSummaryInfo, travelModes, crime;

var showingOverlays = false;

var MIN_HIGH_ACCURACY_POINTS = 25;

var TRIP_DATA_PATH = '/traces/vis/data/';
var TRAVEL_MODE_ICONS_PATH = '/static/web/images/vis/modes/';
var TRIP_ORIGIN_ICON_PATH = '/static/web/images/vis/flag_green.png';
var TRIP_DEST_ICON_PATH = '/static/web/images/vis/checkered_flag.png';
var BLUE_DOT_PATH = '/static/web/images/vis/bluedot.PNG';
var RED_DOT_PATH = '/static/web/images/vis/red_dot.png';

function initialize(trip_id) {    
    //Fetch the trip data
    $.get(TRIP_DATA_PATH + trip_id + '/', function(data) {
        tripSummaryInfo = data['trip_summary'];
        crime = data['crime']
        travelModes = data['travel_modes'];
        traces = [];

        if (tripSummaryInfo.velocity_profile != null && tripSummaryInfo.velocity_profile != "") {
            var traceStrArray = tripSummaryInfo.velocity_profile.split("|");
            for (var i in traceStrArray) {
                var parts = traceStrArray[i].split(",");
                traces.push({'lat': parts[0], 'lon': parts[1],
                    'time': parts[2], 'v': parts[3]});
            }
        }

        $('#loading').hide();
        
        mapInitialize();
        processTraceData();

        if(tripSummaryInfo.encoded_path != null &&
            tripSummaryInfo.encoded_path != "") {
            drawTrip();
        }
        $("#trip_summary").html(getTripSummaryInfo());

         //Set the width and height of the "bottom" div
        visHeight = Math.floor($(window).height() - $('#header').height() * 2 - mapHeight);
        visWidth = Math.round($(window).width() * visWidthPercentage);

        //Protovis
        if(traces.length > 0) {
            renderVelocityData();
        } else {
            $("#velocity_vis").html("<span style=\"margin: 100px; font-weight: bold;\">Velocity profile is not available.</span>");
        }
    });
}

function mapInitialize() {
    mapHeight = Math.round( ($(window).height() - $("#header").height()) * 0.70);
    $('#map').css('height', mapHeight);
    
    var myOptions = {
        zoom: 15,
        center: new google.maps.LatLng(37.8716667, -122.2716667),
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControlOptions: { mapTypeIds: [] }
    };
    map = new google.maps.Map(document.getElementById("map"), myOptions);
}

function compareTime(a, b) {
    return a.time - b.time;
}

function processTraceData() {
    traces.sort(compareTime);
}

function drawTrip() {

    if(tripSummaryInfo.encoded_path != null &&
        tripSummaryInfo.encoded_path != "") {
        
        tripPathPoly = new google.maps.Polyline({
            path: google.maps.geometry.encoding.decodePath(
                tripSummaryInfo.encoded_path),
            strokeColor: "#FF0000",
            strokeOpacity: 0.6,
            strokeWeight: 3
        });
    }
    
    var bounds = new google.maps.LatLngBounds();
    var tempPathArray = tripPathPoly.getPath();

    for (var i = 0; i < tempPathArray.length; i++) {
        bounds.extend( tempPathArray.getAt(i) );
    }

    tripPathPoly.setMap(map);
    map.fitBounds(bounds);

    tripPathArray = tripPathPoly.getPath();

    //Create a marker for later use
    marker = new google.maps.Marker({
        position: tripPathArray.getAt(0),
        map: map
    });

    if(tripSummaryInfo.travel_mode <= 5) {
        marker.setIcon(TRAVEL_MODE_ICONS_PATH +
            tripSummaryInfo.travel_mode + '.png');
    }

    //Add markers for the trip origin and destination
    if(showFlags > 0 ) {
        startMarker = new google.maps.Marker({
            position: new google.maps.LatLng(tripSummaryInfo.origin_lat,
                tripSummaryInfo.origin_lon),
            map: map,
            icon: TRIP_ORIGIN_ICON_PATH
        });

        endMarker = new google.maps.Marker({
            position: new google.maps.LatLng(tripSummaryInfo.dest_lat,
                ripSummaryInfo.dest_lon),
            map: map,
            icon: TRIP_DEST_ICON_PATH
        });
    }

    //Display accident and crime data if they are available
    if(tripSummaryInfo.accidents != null &&
        tripSummaryInfo.accidents != "") {

        var latLonArray = tripSummaryInfo.accidents.split("|");
        for (var j in latLonArray) {
            var latLonPair = latLonArray[j].split(",");

            var latlng = new google.maps.LatLng(latLonPair[0], latLonPair[1]);
            var aMarker = new google.maps.Marker({
                position: latlng,
                icon: RED_DOT_PATH
            });
            overlayMarkerArray.push(aMarker);
        }
    }

    for (var k in crime) {
        var c = crime[k];

        var cLatlng = new google.maps.LatLng(c.lat, c.lon);
        var cMarker = new google.maps.Marker({
            position: cLatlng,
            title: c.desc,
            icon: BLUE_DOT_PATH
        });
        overlayMarkerArray.push(cMarker);
    }
}

function getTripSummaryInfo() {
    //Format start time
    var start_time = dateFormat(new Date(tripSummaryInfo.start_time * 1000), "mmmm dS, h:MM TT");
    var end_time = dateFormat(new Date(tripSummaryInfo.end_time * 1000), "mmmm dS, h:MM TT");
    var dist_traveled = (tripSummaryInfo.distance_traveled / 1609.344);

    var overlayDisplayStr;
    if(overlayMarkerArray.length > 0) {
        overlayDisplayStr = showingOverlays ? "Hide" : "Show";
    } else {
        overlayDisplayStr = "Not available";
    }
    
    var contentString = '<table>' +
                            '<tr><th>User</th><td>' + tripSummaryInfo.username + '</td></tr>' +
                            '<tr><th>Start time</th><td>' + start_time + '</td></tr>' +
                            '<tr><th>End time</th><td>' + end_time + '</td></tr>' +
                            '<tr><th>Travel mode</th><td>' + travelModes[tripSummaryInfo.travel_mode] + '</td></tr>' +
                            '<tr><th>Dist. traveled</th><td>' + dist_traveled.toFixed(2) + ' miles</td></tr>' +
                            '<tr><th>Overlays</th><td><a id="overlay_display" href="#">' +
                                overlayDisplayStr + '</a></td></tr>' +
                        '</table>' +
                        '<button id="play_trip" type="button">Play</button>';

    return contentString;
}

function startAnimation() {
    if (animationInProgress == false) {
        eol = tripPathPoly.Distance();
        animationInProgress = true;
        animate(0);
    }
}

function animate(d) {
    if (d>eol) {
      //map.panTo(endLocation.latlng);
      //marker.setPosition(endLocation.latlng);
      animationInProgress = false;
      return;
    }
    var p = tripPathPoly.GetPointAtDistance(d);
    //map.panTo(p);
    marker.setPosition(p);
    timerHandle = setTimeout("animate("+(d+step)+")", tick);
}

/**
 * Use a binary search to get the position to which the marker should be moved.
 */
function moveMarker(time) {
    var high = traces.length - 1;
    var low = 0;
    var mid = 0;
    var latlng;

    while (low <= high) {
        mid = parseInt((low + high) / 2)
        var val = traces[mid];

        if (low == mid || high == mid) {
            latlng = new google.maps.LatLng(val.lat, val.lon);
            marker.setPosition( latlng );
            break;
        }

        if (val.time > time) {
            high = mid - 1;
        } else if (val.time < time) {
            low = mid + 1;
        } else {
            latlng = new google.maps.LatLng(val.lat, val.lon);
            marker.setPosition( latlng );
            break;
        }
    }
}
