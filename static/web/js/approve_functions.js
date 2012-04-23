var map, bounds;
var currentDirections = null;
var googleDirectionsService = new google.maps.DirectionsService();
var googleDirectionsRenderer, originLatLng, destLatLng, updatedRoute;

var STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID',
    'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO',
    'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',
    'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'];

function mapInitialize() {
    mapHeight = Math.round( ($(window).height() - $("#header").height()) * 0.65);
    $('#map').css('height', mapHeight);

    var myOptions = {
        zoom: 15,
        center: new google.maps.LatLng(37.8716667, -122.2716667),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map"), myOptions);
}

function isStateHighway(instruction) {
    for (var i in STATES) {
        var state = STATES[i];

        var statePos = instruction.toLowerCase().lastIndexOf(state.toLowerCase() + "-");
        var forwardSlashPos = instruction.toLowerCase().lastIndexOf("/");

        if (statePos != -1 && statePos < forwardSlashPos) {
            return true;
        }
    }

    return false;
}

function isLeftTurn(instruction) {
    //Surely there's a better way to do this
    var startsWith = instruction.toLowerCase().indexOf("turn ");
    var containsTurn = instruction.toLowerCase().indexOf(" turn ");
    var containsTurns = instruction.toLowerCase().indexOf(" turns ");
    var containsLeft = instruction.toLowerCase().indexOf(" left ");

    if ( (startsWith != -1 || containsTurn != -1 || containsTurns != -1) &&
        containsLeft != -1) {

        return true;
    } else {
        return false;
    }
}

function approveTrip(userId, updated_route, cDirections, submitUrl, tripId) {
    var travelMode = $("#approve_trip_form select option:selected").val();
    var startTime = jQuery.trim($("#approve_trip_form input[name='start_time']").val());
    var endTime = jQuery.trim($("#approve_trip_form input[name='end_time']").val());
    var visAvailable = $('#disable_vis').is(':checked') ? 0 : 1;

    if (updated_route == null) {
        alert("Google Directions Result object is null!");
    } else {
        var totalDistance = 0;
        var highwayDistance = 0;
        var leftTurns = 0;
        var plainTextDirections = [];
        var encodedPath = google.maps.geometry.encoding.encodePath(updated_route.overview_path);

        var waypointArray = [];
        var tempWaypointArray = [];
        for (var cnt = 0; cnt < updated_route.overview_path.length; cnt++) {
            var latLng = updated_route.overview_path[cnt];
            var latLngStr = latLng.lat().toFixed(6) + "," + latLng.lng().toFixed(6);
            tempWaypointArray.push(latLngStr);
        }

        //If there are greater than 10 waypoints, down sample to 10 or 11 points
        //The logic is as follows:
        //  - pick the first and last points
        //  - pick evenly spaced points in the rest of them
        var wpSampleSize = parseInt(tempWaypointArray.length / 10);
        if(wpSampleSize > 0) {
            //If there are between 10 and 20 points, we'd rather have fewer points
            if(wpSampleSize == 1) {
                wpSampleSize = 2;
            }
            
            var start = 1;
            var end = tempWaypointArray.length - 2;
            
            waypointArray.push(tempWaypointArray[0]);

            for (var wpIndex = 0; wpIndex < tempWaypointArray.length; wpIndex++) {
                if(wpIndex > start && wpIndex <= end) {

                    if(wpIndex % wpSampleSize == 0) {
                        waypointArray.push(tempWaypointArray[wpIndex]);
                    }
                }
            }

            waypointArray.push(tempWaypointArray[tempWaypointArray.length - 1]);
        } else {
            waypointArray = tempWaypointArray;
        }

        var legCount = 0;
        for(var i in cDirections.routes[0].legs) {
            legCount++;
            var leg = cDirections.routes[0].legs[i];

            if (1 == legCount) {
                var originLat = leg.start_location.lat();
                var originLon = leg.start_location.lng();
                var originAddress = leg.start_address;
            }
            var destLat = leg.end_location.lat();
            var destLon = leg.end_location.lng();
            var destAddress = leg.end_address;

            var steps = leg.steps;

            for (var j in steps) {
                var step = steps[j];
                var cleanInstruction = step.instructions.replace(/<.*?>/g, '');

                plainTextDirections.push(cleanInstruction);
                totalDistance += step.distance.value;

                if (cleanInstruction.toLowerCase().indexOf(" i-") != -1 ||
                    cleanInstruction.toLowerCase().indexOf(" us-") != -1 ||
                    isStateHighway(cleanInstruction)) {

                    highwayDistance += step.distance.value;
                }

                if (isLeftTurn(cleanInstruction)) {
                    leftTurns += 1;
                }
            }
        }

        //Upload the details to the server
        var submit = {user_id: userId,
                        origin_lat: originLat, origin_lon: originLon, origin_address: originAddress,
                        dest_lat: destLat, dest_lon: destLon, dest_address: destAddress,
                        distance_traveled: totalDistance, highway_distance: highwayDistance,
                        left_turns: leftTurns, plain_text_directions: plainTextDirections.join("\n"),
                        travel_mode: travelMode, encoded_path: encodedPath, start_time: startTime,
                        end_time: endTime, vis_available: visAvailable, waypoints: waypointArray.join("|")
                     };

        $.post(submitUrl, submit, function(data) {
            if (data == "1") {
                window.close();
                //Change the backgorund color on non standing trip
                if (window.opener && ! window.opener.closed && tripId != null) {
                    var rowId = "row" + tripId;
                    var tr = window.opener.document.getElementById(rowId);
                    tr.style.backgroundColor = "greenyellow";
                }
            } else {
                alert("An error occurred - " + data);
            }
        });
    }
}