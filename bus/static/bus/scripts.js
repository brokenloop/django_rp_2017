/**
 * Created by danieljordan on 11/07/2017.
 */

function getTime(params) {
    $.get("time", params, function(data, status){
        // alert("Data: " + data.Name + "\nStatus: " + status);
        console.log(data);
    });
}

// Submitting the form and returning time prediction
$(document).ready(function(){
    $("#submitBtn").click(function(){
        params = $("form").serialize();
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


//loads routes and displays them using autocomplete
$(document).ready(function(){
    var route_list = [];
    $.get("routes", function(data, status){
        $.each(data, function() {
            route_list.push(this.route_id);
        });
    });
    $('input[name="route"]').autocomplete({
        minLength: 1,
        source: function (request, response) {
            var results = $.ui.autocomplete.filter(route_list, request.term);
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


// listener for origin and destination inputs, checks if they're empty and does something if both aren't
$(document).ready(function(){
    $('#startStop, #endStop').change(function() {
        var value1=$.trim($('#startStop').val());
        var value2=$.trim($('#endStop').val());

        if ((value1.length > 0) && (value2.length > 0)){
            var origin = 2041;
            var destination = 4568;
            getRoutes(origin, destination);
        }

    });
});


function getRoutes(origin, destination) {
    $.get("stops/common/" + origin + "/" + destination, function(data){
        console.log(data);
    });
}


$(document).ready(function(){
    $('#testBtn').on('click', function() {
        // var marker = new google.maps.Marker({
        //    position: {
        //               lat: 53.340937,
        //               lng: -6.2626352
        //           },
        //    setMap: map
        //       });
        // alert("Fuck");
        var marker = new google.maps.Marker({
            position: {
                  lat: 53.340937,
                  lng: -6.2626352
              },
            title:"Hello World!"
        });

        // To add the marker to the map, call setMap();
        marker.setMap(map);

    });
});


// returns all stops accessible by another stop
$(document).ready(function(){
    $('#testBtn').on('click', function() {
        $.get('stops/accessible/', {stop_id: '495'}, function(data) {
            console.log(data);
        });
    });
});



