if (window.location.href.indexOf('#') > 0) {
    document.getElementById('start').style.display = 'none'
}

$(document).ready(function(){
    $("#start-button").click(function(){
        $("#start").slideUp("slow");
    });
});