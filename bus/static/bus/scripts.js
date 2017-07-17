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

//checks whether the form fields are empty and displays an error message if they are
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


//loads the stops into a dropdown
$(document).ready(function(){
    $.get("stops", function(data, status){
        var options = $('select[name="startStop"]')
        $.each(data, function() {
            options.append($("<option />").val(this.id).text(this.stop_id + "-" + this.name));
        });
    });
});

//loads the stops into a dropdown
$(document).ready(function(){
    $.get("stops", function(data, status){
        var options = $('select[name="endStop"]')
        $.each(data, function() {
            options.append($("<option />").val(this.id).text(this.stop_id + "-" + this.name));
        });
    });
});

//loads the route_ids into a dropdown
$(document).ready(function(){
    $.get("routes", function(data, status){
        var options = $('select[name="route"]')
        $.each(data, function() {
            options.append($("<option />").val(this.id).text(this.route_id));
        });
    });
});


//trying to use autocomplete:
//$(document).ready(function(){
//    $('#tags').autocomplete({
//        source: $.get("stops", function(data, status){
//                    return (data.stop_id);
//                });
//    });
//});