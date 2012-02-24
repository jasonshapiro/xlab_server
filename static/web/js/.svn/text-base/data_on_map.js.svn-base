var map;
var markersArray = [];
var clickListener;

var clickCount = 0;
var rectangle, bounds;
var southWestMarker, southWestLatLng, northEastLatLng;

var AJAX_CALL_PATH = '/traces/dataonmap/';

function mapInitialize() {
    var latlng = new google.maps.LatLng(37.8716667, -122.2716667); //Berkeley
    var myOptions = {
        zoom: 12,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"),
        myOptions);
}

function addMarker(marker) {
    markersArray.push(marker);
}

function clearMarkers() {
    if (markersArray) {
        for (i in markersArray) {
            markersArray[i].marker.setMap(null);
        }
        markersArray.length = 0;
    }

    rectangle.setMap(null);
}

function drawRectangle(event) {
    clickCount++;

    if(clickCount == 1) {
        southWestLatLng = new google.maps.LatLng(event.latLng.lat(),
            event.latLng.lng());
        southWestMarker = new google.maps.Marker({
            position: southWestLatLng,
            map: map
        });
    } else if(clickCount == 2) {
        northEastLatLng = new google.maps.LatLng(event.latLng.lat(),
            event.latLng.lng());

        rectangle = new google.maps.Rectangle();
        bounds = new google.maps.LatLngBounds(southWestLatLng, northEastLatLng);
        var rectOptions = {
            strokeColor: "#FF0000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#FF0000",
            fillOpacity: 0.1,
            map: map,
            bounds: bounds
        };
        rectangle.setOptions(rectOptions);

        google.maps.event.removeListener(clickListener);
        southWestMarker.setMap(null);
        $('#load_data').removeAttr('disabled');
        clickCount = 0;
    }

}

$(document).ready(function() {
    $("#data_on_map span").hide();

    //Show the map
    mapInitialize();

    //Load data
    $("#load_data").click( function() {
        var dataType = $("#load_data_form select[name='data_type'] option:selected").val();

        var submit = {type: dataType,
                        sw_lat: rectangle.getBounds().getSouthWest().lat(),
                        sw_lon: rectangle.getBounds().getSouthWest().lng(),
                        ne_lat: rectangle.getBounds().getNorthEast().lat(),
                        ne_lon: rectangle.getBounds().getNorthEast().lng()
                     };

        $.post(AJAX_CALL_PATH, submit, function(data) {
            var cnt = 0;
            
            $.each(data, function(key, t) {
                var latlng = new google.maps.LatLng(t.lat, t.lon);
                var marker = new google.maps.Marker({
                    position: latlng,
                    map: map,
                    title: t.lat + ", " + t.lon + ", " + t.details
                });

                addMarker({
                    id: t.id,
                    marker: marker
                });

                map.fitBounds(bounds);
                cnt++;
            });

            if(cnt > 0) {
                $("#data_on_map span").text("Loaded " + cnt + " data points").show();
            } else {
                $("#data_on_map span").text("No data.").show();
            }

        });

        return false;
    });

    //Enable selection of a rectangle on the map
    $("#select_rectangle").click( function() {
        $('#select_rectangle').attr('disabled', 'disabled');
        $('#clear_selection').removeAttr('disabled');
        
        clickListener = google.maps.event.addListener(map, 'click', drawRectangle);
    });

    //Clear selected region on the map
    $("#clear_selection").click( function() {
        clearMarkers();
        
        $('#clear_selection').attr('disabled', 'disabled');
        $('#load_data').attr('disabled', 'disabled');
        $('#select_rectangle').removeAttr('disabled');
    });

});


