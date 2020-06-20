if (window.location.href.indexOf('#') > 0) {
    document.getElementById('start').style.display = 'none'
}

function slideSplash() {
    $("#start").slideUp("slow");
}

$(document).ready(function(){
    $("#start").click(function(){
        $("#start").slideUp("slow");
    });
});