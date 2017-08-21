/**
 * Created by danieljordan on 11/07/2017.
 */
var map;
var directionsDisplay;
var directionsService;
var busPath;
var markerArray = [];
var mapKey = "AIzaSyB3um4WUb5l36zZyCnovdVFE6OEBfgf3wQ";
var roadKey = "AIzaSyAUX0EvazigXFp19OEGF-I5XsUQQuqkrAY";
var directionsKey = "AIzaSyApzdf0AVWA3e8TgSBmTFIOoEivYSn3_Os";
var routeList;
var stopData = {};
var stopList = [];

loadStopData();

function loadStopData() {
    $.get("stops", function(data, status){
        $.each(data, function(index, value) {
            stopData[value.stop_id] = {lat: value.lat, lon: value.lon, name: value.name};
            stopList.push(value.stop_id.toString() + " " + value.name)
        });
        fillStops(stopData);
        // console.log(stopList);
    });
}


//INPUT ROUTES:

//loads routes and displays them using autocomplete - called asyncly from loadStopData()
function fillStops(data) {
    $(document).ready(function(){

        // reset inputs
        // clearInputs({direction: 'Direction', startStop: 'Origin', endStop: 'Destination'});

        // get list of routes
        // var stop_list = [];
        //  $.each(data, function(index, value) {
        //         stop_list.push(value);
        //      console.log(value);
        //     });
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

       // console.log(origin);

       getDirections(origin, destination);
       calculateAndDisplayRoute(origin, destination);
       // createBusLeg(12, 12, 12, 12);
   });
});


function getDirections(origin, destination) {
    var params =  {
        origin: origin.lat.toString() + "," + origin.lon.toString(),
        destination: destination.lat.toString() + "," + destination.lon.toString(),
        mode: 'transit',
        transit_mode: 'bus',
        key: directionsKey,
    };


    // console.log(params);
    var url = "https://maps.googleapis.com/maps/api/directions/json";
    // https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=YOUR_API_KEY

    $.get("directions", params, function(data) {
        // console.log(data);
        populateJourneyResults(data);
    });

}


// code adapted from https://developers.google.com/maps/documentation/javascript/examples/directions-travel-modes
function calculateAndDisplayRoute(startStop, endStop) {
    // console.log(startStop);

    // console.log(typeof startStop.lat);
    // var selectedMode = document.getElementById('mode').value;
    directionsService.route({
      origin: {lat: startStop.lat, lng: startStop.lon},
      destination: {lat: endStop.lat, lng: endStop.lon},
      travelMode: "TRANSIT",
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
    // console.log(legs);
    $.each(legs, function(index, value) {
        if (value.travel_mode === "TRANSIT") {
            var line = value.transit_details.line.short_name;
            var duration = value.duration.text;
            var origin = "origin";
            var destination = "destination";
            console.log(duration);
            createBusLeg(line, duration, origin, destination);
        }
    });
}

function createBusLeg(line, duration, origin, destination) {

    var button = '<div class="col-xs-12">' +
                    '<button type="button" class="btn btn-info col-xs-12" data-toggle="collapse" data-target="#' + line +'div"> ' +
                        'Line: ' + line + ' - ' + duration +
                     '</button>' +
                  '</div>'

    // var div = '<div class="panel panel-default"><div class="panel-body>A Basic Panel</div></div>';
    var div = '<p>Hello</p>';

    // var div = '<div id="' + line +'div" class="collapse">  '
    //             + '<p>Origin: ' + origin + '<br>'
    //             + 'Destination: ' + destination + '</p>' +
    //           '</div>'
    // var leg = '<button type="button" class="btn btn-info" data-toggle="collapse" data-target="#demo">Simple collapsible</button>'
    $("#journeyInfo").append(button);
    $("#journeyInfo").append(div);
}

function createWalkLeg(duration, instruction) {

}