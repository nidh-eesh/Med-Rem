
//Medicine Search Styling
$(document).ready(function () {
    $('select').selectize({
        sortField: 'text'
    });
});
//

//Appointment Date Validation
var today = new Date();
var dd = today.getDate();
var mm = today.getMonth() + 1;
var yyyy = today.getFullYear();
var hh = today.getHours();
var m = today.getMinutes();
    
if (dd < 10) {
    dd = '0' + dd;
}
    
if (mm < 10) {
    mm = '0' + mm;
}
        
today = yyyy + "-" + mm + "-" + dd + "T" + hh + ":" + m;
console.log(today)
document.getElementById("datefield").setAttribute("min", today);
//


//Checkbox Validation
function handleData()
{
    var form_data = new FormData(document.querySelector("form"));
    
    if(!form_data.has("timeofday[]"))
    {
        document.getElementById("chk_option_error").style.visibility = "visible";
      return false;
    }
    else
    {
        document.getElementById("chk_option_error").style.visibility = "hidden";
      return true;
    }
    
}