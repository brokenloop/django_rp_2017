/**
 * Created by danieljordan on 11/07/2017.
 */
var map;
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

       getDirections(origin, destination);
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
        console.log(data);
    });

}
