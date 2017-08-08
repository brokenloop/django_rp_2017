/**
 * Created by danieljordan on 11/07/2017.
 */

function populate_hour(selector, low, high) {
    for (var i = low; i <= high; i++) {
        if (i == new Date().getHours()) {
            $(selector).append('<option value=' + i +' selected>' + i + ':00</option>');
        } else {
            $(selector).append('<option value=' + i +'>' + i + ':00</option>');
        }
    }
}

function populate_day(selector, low, high) {
    var weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    for (var i = low; i <= high; i++) {
        if (i == new Date().getDay()) {
           $(selector).append('<option value=' + i +' selected>' + weekdays[i] + '</option>');
        } else {
            $(selector).append('<option value=' + i +'>' + weekdays[i] + '</option>');
        }
    }
}

// populate hour and day selects
$(document).ready(function() {
    populate_hour('#hour', 5, 23);
    populate_day('#day', 0, 6);
});


function getTime(params) {
   $.get("time", params, function(data, status){
       // alert("Data: " + data.Name + "\nStatus: " + status);
       $('#timePrediction').text(data.time)
      console.log(data);
   })
       .fail(function() {
           alert("Invalid input! Please change the input parameters.");
       });
}

// Submitting the form and returning time prediction
$(document).ready(function(){
   $("#submitBtn").click(function(){
       // params = $("form").serialize();
       var startStop= $('#startStop').val().split(" ")[0];
       var endStop=$('#endStop').val().split(" ")[0];
       // var route_pattern = $('#routeList').val();
       var route = $('#routeList').val();
       var pattern = $('#direction').val();
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


//INPUT ROUTES:

//loads routes and displays them using autocomplete
$(document).ready(function(){
    var route_list = [];
    $.get("routes", function(data, status){
        $.each(data, function() {
            route_list.push(this.route_id);
        });
    });
    $('#routeList').autocomplete({
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


//INPUT DIRECTION:

// listener for route input
$(document).ready(function(){
    $('#routeList').change(function() {
        var value1=$.trim($('#routeList').val());
        //checks if input fields are filled
        if (value1.length>0){
            var routeChosen = value1;

            //gets the route and populates dropdown "Direction" with journeyPatterns
            $.get("routes" + "/" + routeChosen, function(data){
                var options = $('#direction')
                options.empty()
                $.each(data, function() {
                    options.append($("<option></option>").text(this));
                });
            });

        }
    });
});


//INPUT ORIGIN:

$(document).ready(function(){
    $('#direction').change(function() {
        var value1 = $.trim($('#routeList').val());
        var value2 = $.trim($('#direction').val());
        //checks if input fields are filled
        if ((value1.length>0) && (value2.length>0)){
            var routeChosen = value1;
            var directionChosen = value2;

            //gets the route and populates dropdown "Direction" with journeyPatterns
            $.get("routes" + "/" + "stops" + "/" + routeChosen + "/" + directionChosen, function(data){
                var options = $('#startStop')
                options.empty()
                options.append($("<option></option>").text("Origin"))
                $.each(data, function(index, stops) {
                    options.append($("<option></option>").text(this.stop_id + " - " + this.name));
                });
            });
        }
    });
});


//INPUT DESTINATION:

$(document).ready(function(){
    $('#startStop').change(function() {
        var value1 = $.trim($('#routeList').val());
        var value2 = $.trim($('#direction').val());
        var value3 = $.trim($('#startStop').val().split(" - ")[0]);
        //checks if input fields are filled
        if ((value1.length>0) && (value2.length>0) && (value3.length>0)){
            var routeChosen = value1;
            var directionChosen = value2;
            var originChosen = value3;

            //gets the route, journeyPattern and origin stop and populates dropdown "Destination" with stops
            $.get("routes" + "/" + "stops" + "/" + routeChosen + "/" + directionChosen + "/" + originChosen, function(data){
                var options = $('#endStop')
                options.empty()
                options.append($("<option></option>").text("Destination"))
                $.each(data, function(index, stops) {
                    options.append($("<option></option>").text(this.stop_id + " - " + this.name));
                });
            });
        }
    });
});


//GOOGLE MAPS FUNCTIONS:

//Takes form inputs and creates markers based on the origin/destination and the stops inbetween
$(document).ready(function(){
    $('#submitBtn').on('click', function() {
        var origin= $('#startStop').val().split(" - ")[0];
        var destination=$('#endStop').val().split(" - ")[0];
        var line = $('#routeList').val();
        var journeyPattern = $('#direction').val();

        $.get("routes/stops/" + line + "/" + journeyPattern + "/" + origin + "/" + destination, function(data){
            deleteMarkers();
            $.each(data, function(index, stop) {
                createMarker(stop.lat, stop.lon);
                setMapOnAll(map);
            });
            var bounds = new google.maps.LatLngBounds();
            for (var i = 0; i < markerArray.length; i++) {
                bounds.extend(markerArray[i].getPosition());
            }
            map.fitBounds(bounds);
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

function createPolyLine(coords) {
    busPath = new google.maps.Polyline({
        path: coords,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2,
    });
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