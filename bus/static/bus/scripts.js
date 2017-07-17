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

// $(document).ready(function(){
//     $("button").click(function(){
//         alert("Click!");
//     });
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
$(document).ready(function(){
    var test = [];
     $.get("stops", function(data, status){
                    $.each(data, function() {
//                        console.log(this.name);
//                        return data.name
                          test.push(this.name);
                    });
                })
    $('input[name="tags"]').autocomplete({
        minLength: 2,
        source: function (request, response) {
            var results = $.ui.autocomplete.filter(test, request.term);

            response(results.slice(0, 20));
        }
    });
});
