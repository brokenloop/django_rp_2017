/**
 * Created by danieljordan on 11/07/2017.
 */
var map;
var directionsDisplay;
var directionsService;
var busPath;
var markerArray = [];
var markerCluster;
var mapKey = "AIzaSyB3um4WUb5l36zZyCnovdVFE6OEBfgf3wQ";
var roadKey = "AIzaSyAUX0EvazigXFp19OEGF-I5XsUQQuqkrAY";
var directionsKey = "AIzaSyApzdf0AVWA3e8TgSBmTFIOoEivYSn3_Os";
var routeList;
var stopData = {};
var stopList = [];
// var markerList = []

loadStopData();

function loadStopData() {
    $.get("stops", function(data, status){
        $.each(data, function(index, value) {
            stopData[value.stop_id] = {lat: value.lat, lon: value.lon, name: value.name};
            stopList.push(value.stop_id.toString() + " " + value.name)
            // markerList.push({lat: value.lat, lng: value.lng});
        });
        fillStops(stopData);
        createMarkerArray();
    });
}

// populate hour and day selects
$(document).ready(function() {
    populate_day('#day', 0, 6);
});


//INPUT ROUTES:

//loads routes and displays them using autocomplete - called asyncly from loadStopData()
function fillStops(data) {
    $(document).ready(function(){
        $('#startStop, #endStop').autocomplete({
            minLength: 1,
            source: function (request, response) {
            var results = $.ui.autocomplete.filter(stopList, request.term);
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


// Submitting and returning directions
$(document).ready(function(){
   $("#submitBtn").click(function(){
       // params = $("form").serialize();
       var startStopId= $('#startStop').val().split(" ")[0];
       var endStopID=$('#endStop').val().split(" ")[0];
       var origin = stopData[startStopId];
       var destination = stopData[endStopID];

       var time = $('#timepicker').val();
       var timeparts = time.split(":");
       var hour = timeparts[0];
       var day = $('#day').val();
       var weather = $('#weather').val();

       clearMarkers();
       getDirections(origin, destination, hour, day, weather);
       calculateAndDisplayRoute(origin, destination);
       // createBusLeg(12, 12, 12, 12);
   });
});


function getDirections(origin, destination, hour, day, weather) {
    var params =  {
        origin: origin.lat.toString() + "," + origin.lon.toString(),
        destination: destination.lat.toString() + "," + destination.lon.toString(),
        mode: 'transit',
        transit_mode: 'bus',
        key: directionsKey,
        hour: hour,
        day: day,
        weather: weather,
    };


    var url = "https://maps.googleapis.com/maps/api/directions/json";
    // https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=YOUR_API_KEY

    $.get("directions", params, function(data) {
        clearResults("#journeyInfo");
        populateJourneyResults(data);
        scrollTo(".journey-detail");
    });

}


// code adapted from https://developers.google.com/maps/documentation/javascript/examples/directions-travel-modes
function calculateAndDisplayRoute(startStop, endStop) {
    directionsService.route({
      origin: {lat: startStop.lat, lng: startStop.lon},
      destination: {lat: endStop.lat, lng: endStop.lon},
      travelMode: "TRANSIT",
      transitOptions: {
          // routingPreference: "LESS_WALKING",
          modes: ["BUS"],
      }
    }, function(response, status) {
      if (status == 'OK') {
        directionsDisplay.setDirections(response);
        directionsDisplay.setMap(map);
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    });
}


function populateJourneyResults(data) {
    var legs = data.routes[0].legs[0].steps;
    $.each(legs, function(index, value) {
        if (value.travel_mode === "TRANSIT") {
            var line = value.transit_details.line.short_name;
            var duration = value.duration.text;
            var origin = value.transit_details.departure_stop.name;
            var destination = value.transit_details.arrival_stop.name;
            var num_stops = value.transit_details.num_stops;
            createBusLeg(line, duration, num_stops, origin, destination);
        } else if (value.travel_mode === "WALKING") {
            var duration = value.duration.text;
            var distance_text = value.distance.text;
            var distance_value = value.distance.value;
            var instruction = value.html_instructions;
            createWalkLeg(duration, distance_text, distance_value, instruction);
        }
    });
}

function createBusLeg(line, duration, num_stops, origin, destination) {

    var button = '<p><button class="btn btn-info col-xs-12 text-left" type="button" data-toggle="collapse" style="text-align:left;"' +
                            'data-target="#' + line +'div" aria-expanded="false" aria-controls="collapseExample">' +
                        '<div class="pull-left">Line ' + line + '</div><div class="pull-right">' + duration + '</div>'
                      '</button>' +
                    '</p>'

    var info = '<div class="collapse" id="' + line +'div">' +
                        '<div class="panel panel-default">' +
                            '<div class="panel-body">' +
                                // '<br>' +
                                '<p><b>Get on at:</b> ' + origin + '</p>' +
                                '<p><b>Ride for: </b>' + num_stops + ' stops</p>' +
                                '<p><b>Get off at:</b> ' + destination + '</p>' +
                            '</div>' +
                        '</div>' +
                    '</div>'

    $("#journeyInfo").append(button);
    $("#journeyInfo").append(info);
}

function createWalkLeg(duration, distance_text, distance_value, instruction) {
    var button = '<p><button class="btn btn-success col-xs-12 text-left" type="button" data-toggle="collapse" style="text-align:left;"' +
                            'data-target="#' + distance_value +'div" aria-expanded="false" aria-controls="collapseExample">' +
                        '<div class="pull-left">Walk' + '</div><div class="pull-right">' + duration + '</div>' +
                      '</button>' +
                    '</p>'


    var info = '<div class="collapse top-buffer" id="' + distance_value +'div">' +
                        '<div class="panel panel-default">' +
                            '<div class="panel-body">' +
                                // '<br>' +
                                '<p><b>Details:</b> ' + instruction +
                                '<p><b>Distance:</b> ' + distance_text +

                            '</div>' +
                        '</div>' +
                    '</div>'

    $("#journeyInfo").append(button);
    $("#journeyInfo").append(info);
}

function clearResults(divID) {
    $(divID).empty();
}

// gets timepicker ready
$(document).ready(function() {
    var options = { twentyFour: true, timeSeparator: ':' };
    $('.timepicker').wickedpicker(options);
});


function createMarkerArray() {
    $.each(stopData, function(index, value) {
        var marker = new google.maps.Marker({
          position: {lat: value.lat, lng: value.lon},
          // map: map,
          stopID: index,
        });

        marker.addListener('click', function() {
            fillStopInputs(marker.stopID);
        });
        markerArray.push(marker);
    });
    markerCluster = new MarkerClusterer(map, markerArray,
            {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
}

function setMapOnAll(map) {
    for (var i = 0; i < markerArray.length; i++) {
        markerArray[i].setMap(map);
    }
}

function clearMarkers() {
    markerCluster.clearMarkers();
}

function fillStopInputs(stopID) {
    var stop = stopData[stopID];
    var origin = $.trim($('#startStop').val());
    if (origin.length > 0) {
        $('#endStop').val(stopID.toString() + " " + stop.name);
    } else {
        $('#startStop').val(stopID.toString() + " " + stop.name);
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


function scrollTo(element) {
    $('html, body').animate({
        scrollTop: $(element).offset().top
    }, 500);
    return false;
}