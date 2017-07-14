/**
 * Created by danieljordan on 11/07/2017.
 */

function getStops(params) {
    $.get("stops", params, function(data, status){
        console.log(data);
    });
}

function getTime(params) {
    $.get("time", params, function(data, status){
        // alert("Data: " + data.Name + "\nStatus: " + status);
        console.log(data);
    });
}

// $( ":submit" ).submit(function( event ) {
//   alert( "Handler for .submit() called." );
//   // event.preventDefault();
// });

// $( "form" ).on( "submit", function( event ) {
//   event.preventDefault();
//   console.log( $( this ).serialize() );
// });

$(document).ready(function(){
    $("#submitBtn").click(function(){
        params = $("form").serialize();
        getTime(params);
    });
});



