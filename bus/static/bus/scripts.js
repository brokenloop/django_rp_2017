/**
 * Created by danieljordan on 11/07/2017.
 */

function getStops() {
    $.get("stops", function(data, status){
        alert("Data: " + data + "\nStatus: " + status);
    });
}

