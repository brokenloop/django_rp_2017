/**
 * Created by danieljordan on 11/07/2017.
 */

function populate_hour(selector, low, high) {
    for (var i = low; i <= high; i++) {
        $(selector).append('<option value=' + i +'>' + i + ':00</option>')
    }
}

function populate_day(selector, low, high) {
    var weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    for (var i = low; i <= high; i++) {
        $(selector).append('<option value=' + i +'>' + weekdays[i] + '</option>')
    }
}

// populate hour and day selects
$(document).ready(function() {
    populate_hour('#hour', 5, 23);
    populate_day('#day', 0, 6)
});

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
                console.log(data);
                var options = $('select[name="route"]')
                $.each(data, function() {
                    options.append($("<option></option>").text(this));
                });
            });

        }

    });
});


$(document).ready(function(){
    $('#testBtn').on('click', function() {

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
