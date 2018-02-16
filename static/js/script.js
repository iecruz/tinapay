$(function() {
    if (!("Notification" in window)) {
        console.log("This browser does not support desktop notification");
    }
    
    else if (Notification.permission !== "denied") {
        Notification.requestPermission();
    }
});

var username = $('body').attr('data-user');

if (username) {
    var socket = io(window.location.origin + '/' + username);
    
    socket.on('order notification', function(data) {
        new Audio(window.location.origin + '/static/audio/notif.mp3').play();
        new Notification('Delivery Status: ' + data['status']);
    });
}