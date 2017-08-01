/**
 * Created by danieljordan on 11/07/2017.
 */

function populate(selector, low, high) {
    for (i = low; i <= high; i++) {
        $(selector).append('<option value=i>i</option>')
    }
}

// populate hour and day selects
// $(document).ready(function() {
//
// });

function getTime(params) {
    $.get("time", params, function(data, status){
        // alert("Data: " + data.Name + "\nStatus: " + status);
       console.log(data);
    });
}

// Submitting the form and returning time prediction
$(document).ready(function(){
    $("#testBtn").click(function(){
        // params = $("form").serialize();
        var startStop=$.trim($('#startStop').val().substring(0,4));
        var endStop=$.trim($('#endStop').val().substring(0,4));
        var route_pattern = $('#route').val().split(" ");
        var route = route_pattern[0];
        var pattern = route_pattern[1];
        var hour = $('#hour').val();
        var day = $('#day').val();
        var weather = $('#weather').val();

        params = {
            'startStop': startStop,
            'endStop': endStop,
            'route': route,
            'pattern': pattern,
            'hour': hour,
            'day': day,
            'weather': weather,
        }
        console.log(params);

        getTime(params);
    });
});


//loads stops and displays them using autocomplete
$(document).ready(function(){
    var start_stop = [];
    $.get("stops", function(data, status){
        $.each(data, function() {
            start_stop.push(this.stop_id +"-"+ this.name);
        });
    });
    $('input[name="startStop"]').autocomplete({
        minLength: 1,
        source: function (request, response) {
        var results = $.ui.autocomplete.filter(start_stop, request.term);
        if (results.length == 0) {
                results.push ({
                    id: 0,
                    label: "No match found",
                });
            }
        response(results.slice(0, 20));
        }
    });
});

//loads stops and displays them using autocomplete
$(document).ready(function(){
    var end_stop = [];
    $.get("stops", function(data, status){
        $.each(data, function() {
            end_stop.push(this.stop_id+"-"+this.name);
        });
    });
    $('input[name="endStop"]').autocomplete({
        minLength: 1,
        source: function (request, response) {
        var results = $.ui.autocomplete.filter(end_stop, request.term);
        if (results.length == 0) {
                results.push ({
                    id: 0,
                    label: "No match found",
                });
            }
        response(results.slice(0, 20));
        }
    });
});

// listener for origin and destination inputs
$(document).ready(function(){
    $('#startStop, #endStop').change(function() {
        var value1=$.trim($('#startStop').val().substring(0,4));
        var value2=$.trim($('#endStop').val().substring(0,4));
        //checks if input fields are filled
        if ((value1.length>0) && (value2.length>0)){
            var origin = value1;
            var destination = value2;

            //gets routes that connect the stops and displays them in the route dropdown
            $.get("stops/common/" + origin + "/" + destination, function(data){
                var options = $('select[name="route"]')
                options.empty()
                $.each(data, function() {
                    options.append($("<option></option>").text(this));
                });
            });

        }
    });
});


//Takes form inputs and creates markers based on the origin/destination and the stops inbetween
$(document).ready(function(){
    $('#testBtn').on('click', function() {
        var origin = $.trim($('#startStop').val().substring(0,4));
        var destination = $.trim($('#endStop').val().substring(0,4));
        var route_pattern = $('#route').val().split(" ");
        var line = route_pattern[0];
        var journeyPattern = route_pattern[1];

        $.get("routes/stops/" + line + "/" + journeyPattern + "/" + origin + "/" + destination, function(data){
            deleteMarkers();
            $.each(data, function(index, stop) {

                createMarker(stop.lat, stop.lon);

                setMapOnAll(map);

            });
        });
    });
});

//Creates a new marker
function createMarker(lat, lon){
    var marker = new google.maps.Marker({
        position: {
              'lat': lat,
              'lng': lon,
          },
        title:"Station Marker",
        map: map
    });
    markerArray.push(marker);
}

function setMapOnAll(map) {
    for (var i = 0; i < markerArray.length; i++) {
        markerArray[i].setMap(map);
    }
}

function clearMarkers() {
    setMapOnAll(null);
}

function deleteMarkers() {
    clearMarkers();
    markerArray = [];
}