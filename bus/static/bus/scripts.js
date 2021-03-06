/**
 * Created by danieljordan on 11/07/2017.
 */
var map;
var busPath;
var markerArray = [];
var roadKey = "AIzaSyAUX0EvazigXFp19OEGF-I5XsUQQuqkrAY";
var numStops;
var routeData;

loadRouteData();

function loadRouteData() {
    $.get("routes", function(data, status){
        routeData = {};
        $.each(data, function(index, value) {
            if (routeData[value.route_id]) {
                // if entry exists, add new value to the array
                routeData[value.route_id].push({headsign: value.headsign, pattern: value.journey_pattern});
            } else {
                //otherwise, create new entry
                routeData[value.route_id] = [{headsign: value.headsign, pattern: value.journey_pattern}];
            }
        });
        fillRoute(routeData)
    });
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
    populate_day('#day', 0, 6);
});


function getClockTime(params) {
   $.get("clocktime", params, function(data, status){
       $('#originPrediction').text(data.clocktime[0]);
       $('#destinationPrediction').text(data.clocktime[1]);
       $('#journeyTime').text(data.travel_time);
       $('#numStops').text(numStops);
      scrollTo(".bus-time");

   })
       .fail(function() {
           alert("Invalid input! Please change the input parameters.");
       });
}

// Submitting the form and returning time prediction
$(document).ready(function(){
   $("#submitBtn").click(function(){
       var startStop= $('#startStop').val().split(" ")[0];
       var endStop=$('#endStop').val().split(" ")[0];
       var route = $('#route').val();
       var pattern = $('#direction').val();
       var time = $('#timepicker').val();
       var timeparts = time.split(":");
       var hour = timeparts[0];
       var minutes = timeparts[1];
       var day = $('#day').val();
       var weather = $('#weather').val();

       params = {
           'startStop': startStop,
           'endStop': endStop,
           'route': route,
           'pattern': pattern,
           'hour': hour,
           'minutes': minutes,
           'day': day,
           'weather': weather,
       }
       getClockTime(params);
   });
});


// Clears inputs - specify inputs to be cleared in the following form: {inputId: Label}
function clearInputs(inputs) {
    $.each(inputs, function(id, label) {
       var option = $('#' + id);
       option.empty();
       option.append($("<option></option>").text(label));
    });
}


//INPUT ROUTES:

//loads routes and displays them using autocomplete - called asyncly from loadRouteData()
function fillRoute(data) {
    $(document).ready(function(){

        // reset inputs
        clearInputs({direction: 'Direction', startStop: 'Origin', endStop: 'Destination'});

        // get list of routes
        var route_list = [];
         $.each(data, function(index, value) {
                route_list.push(index);
            });
        $('#route').autocomplete({
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

}


//INPUT DIRECTION:

// listener for route input
$(document).ready(function(){
    $('#route').change(function() {
        var routeVar=$.trim($('#route').val());
        //checks if input fields are filled
        if (routeVar.length>0){
            var options = $('#direction')

            // clear inputs
            clearInputs({direction: 'Direction', startStop: 'Origin', endStop: 'Destination'});

            $.each(routeData[routeVar], function(key, value) {
                options.append($("<option value=" + value.pattern + "></option>").text("Towards: " + value.headsign));
            });
        }
    });
});


//INPUT ORIGIN:

//Listener for direction input
$(document).ready(function(){
    $('#direction').change(function() {
        var routeVar = $.trim($('#route').val());
        var directionVar = $.trim($('#direction').val());
        //checks if input fields are filled
        if ((routeVar.length>0) && (directionVar.length>0)){

            // clear inputs
            clearInputs({startStop: 'Origin', endStop: 'Destination'});

            //gets the route and populates dropdown "Direction" with journeyPatterns
            $.get("routes" + "/" + "stops" + "/" + routeVar + "/" + directionVar, function(data){
                var optionsOrigin = $('#startStop');
                $.each(data, function(index, stop) {
                    optionsOrigin.append($("<option></option>").text(stop.stop_id + " - " + stop.name));
                });
            });
        }
    });
});


//INPUT DESTINATION:

//Listener for origin stop
$(document).ready(function(){
    $('#startStop').change(function() {
        var routeChosen = $.trim($('#route').val());
        var directionChosen = $.trim($('#direction').val());
        var originChosen = $.trim($('#startStop').val().split(" - ")[0]);
        //checks if input fields are filled
        if ((routeChosen.length>0) && (directionChosen.length>0) && (originChosen.length>0)){
            //gets the route, journeyPattern and origin stop and populates dropdown "Destination" with stops
            $.get("routes" + "/" + "stops" + "/" + routeChosen + "/" + directionChosen + "/" + originChosen, function(data){
                clearInputs({endStop: 'Destination'});
                var optionsDestination = $('#endStop');
                $.each(data, function(index, stop) {
                    optionsDestination.append($("<option></option>").text(stop.stop_id + " - " + stop.name));
                });
            });
        }
    });
});


//GOOGLE MAPS FUNCTIONS:

//Takes form inputs and creates markers based on the origin/destination and the stops in between
$(document).ready(function(){
    $('#submitBtn').on('click', function() {
        var origin= $('#startStop').val().split(" - ")[0];
        var destination=$('#endStop').val().split(" - ")[0];
        var line = $('#route').val();
        var journeyPattern = $('#direction').val();

        $.get("routes/stops/" + line + "/" + journeyPattern + "/" + origin + "/" + destination, function(data){
            deleteMarkers();
            removeLine();
            var stopCoords = [];
            var stopCount = 0;
            var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
            var labelIndex = 0;
            numStops = data.length;
            $.each(data, function(index, stop) {
                var icon;
                if (stopCount == 0) {
                    label = labels[labelIndex++ % labels.length];
                    var contentString = '<div id="content">' + '<p id="stopHeader">' + stop.stop_id + " - " + stop.name + '</p>' + '</div>';
                    createMarker(stop.lat, stop.lon, contentString, label);
                } else if (stopCount == numStops - 1) {
                    label = labels[labelIndex++ % labels.length];
                    var contentString = '<div id="content">' + '<p id="stopHeader">' + stop.stop_id + " - " + stop.name + '</p>' + '</div>';
                    createMarker(stop.lat, stop.lon, contentString, label);
                }
                stopCount++;
                stopCoords.push({lat: stop.lat, lng: stop.lon});
            });
            setMapOnAll(map);
            getSnappedCoords(stopCoords);
            var bounds = new google.maps.LatLngBounds();
            for (var i = 0; i < markerArray.length; i++) {
                bounds.extend(markerArray[i].getPosition());
            }
            map.fitBounds(bounds);
        });
    });
});


//Creates a new marker
function createMarker(lat, lon, contentString, label){
    var marker = new google.maps.Marker({
        position: {
              'lat': lat,
              'lng': lon,
          },
        title:"Station Marker",
        label: label,
        map: map,
    });
    markerArray.push(marker);

    var infoWindow = new google.maps.InfoWindow({
        content: contentString
    });
    marker.addListener('click', function(){
        infoWindow.open(map, marker);
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


function createPolyLine(coords) {
    busPath = new google.maps.Polyline({
        path: coords,
        strokeColor: '#42d1ff',
        strokeOpacity: 1.0,
        strokeWeight: 2,
    });
}


function drawLine() {
    busPath.setMap(map);
}


function removeLine() {
    if (busPath) {
        busPath.setMap(null);
    }
}

function getSnappedCoords(coords) {
    path = [];
    $.each(coords, function(index, value) {
        path.push(value.lat.toString() + "," + value.lng.toString());
    });
    path = path.join("|");
    $.get('https://roads.googleapis.com/v1/snapToRoads', {
        interpolate: true,
        key: roadKey,
        path: path
      }, function(data) {
        coords = transformCoords(data);
        createPolyLine(coords);
        drawLine();
      });
}

function transformCoords(data) {
    data = data.snappedPoints;
    var coords = [];
    $.each(data, function(index, value) {
        coords.push({
            lat: value.location.latitude,
            lng: value.location.longitude
        });
    });
    return coords;
}


function scrollTo(element) {
    $('html, body').animate({
        scrollTop: $(element).offset().top
    }, 500);
    return false;
}

$(document).ready(function() {
    var options = { twentyFour: true, timeSeparator: ':' };
    $('.timepicker').wickedpicker(options);
});