function actualiser() {
    //window.location.reload(true);
    alert("teste");

}

//document.getElementById("myFrame").addEventListener("load", timedRefresh(1000));

function timedRefresh(timeoutPeriod) {
	setTimeout("location.reload(true);",timeoutPeriod);
   
}
window.onload = timedRefresh(5000);
