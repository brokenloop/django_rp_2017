/**
 * Created by danieljordan on 11/07/2017.
 */

function getStops() {
    $.get("stops", function(data, status){
        console.log(data);
    });
}


function getTime(params) {
    $.get("time", params, function(data, status){
        // alert("Data: " + data.Name + "\nStatus: " + status);
        console.log(data);
    });
}

function getRoutes() {
    $.get("routes", function(data) {
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


// $(document).ready(function(){
//     $("button").click(function(){
//         alert("Click!");
//     });
// });