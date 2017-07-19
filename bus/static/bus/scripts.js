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

// $( ":submit" ).submit(function( event ) {
//   alert( "Handler for .submit() called." );
//   // event.preventDefault();
// });

// $( "form" ).on( "submit", function( event ) {
//   event.preventDefault();
//   console.log( $( this ).serialize() );
// });

// Submitting the form and returning time prediction
$(document).ready(function(){
    $("#submitBtn").click(function(){
        params = $("form").serialize();
        getTime(params);
    });
});

////checks whether the form fields are empty and displays an error message if they are
//$(document).ready(function(){
//    $("#submitBtn").click(function(){
//        var isValid = true;
//        $(".form-control").each(function() {
//            if ( $(this).val() === '' )
//                isValid = false;
//        });
//        if (!isValid)
//            alert("One or more input fields have been left empty. Please make sure to fill all of them :)");
//        return isValid;
//    });
// });

// $(document).ready(function(){
//     $("button").click(function(){
//         alert("Click!");
//     });
// });

////loads the stops into a dropdown
//$(document).ready(function(){
//    $.get("stops", function(data, status){
//        var options = $('select[name="startStop"]')
//        $.each(data, function() {
//            options.append($("<option />").val(this.id).text(this.stop_id + "-" + this.name));
//        });
//    });
//});

////loads the stops into a dropdown
//$(document).ready(function(){
//    $.get("stops", function(data, status){
//        var options = $('select[name="endStop"]')
//        $.each(data, function() {
//            options.append($("<option />").val(this.id).text(this.stop_id + "-" + this.name));
//        });
//    });
//});

////loads the route_ids into a dropdown
//$(document).ready(function(){
//    $.get("routes", function(data, status){
//        var options = $('select[name="route"]')
//        $.each(data, function() {
//            options.append($("<option />").val(this.id).text(this.route_id));
//        });
//    });
//});


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

$(document).ready(function(){
    function updateFunction(){

    }
});