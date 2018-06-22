$(function() {
    if (!("Notification" in window)) {
        console.log("This browser does not support desktop notification");
    }
    
    else if (Notification.permission !== "denied") {
        Notification.requestPermission();
    }
});

var username = $('body').attr('data-user');
var notifCount = 0;
if (username) {
    var socket = io(window.location.origin + '/' + username);
    
    socket.on('order notification', function(data) {
        ++notifCount;
        $('title').html(`${notifCount > 0 ? '(' + notifCount + ') ' : ''}Tinapay`)
        new Audio(window.location.origin + '/static/audio/notif.mp3').play();
        var notifConfig = {
            icon: window.location.origin + '/static/image/bread.png',
            body: 'Your order is ' + data['status'].toLowerCase()
        };
        new Notification('Tinapay', notifConfig);

        $('.notif-alert').prepend(`
            <div class="alert alert-light text-black border border-dark rounded-0" onclick="closeNotif(event)" style="overflow: auto;">
                <a class="float-right rounded-0"><i class="fa fa-arrow-right"></i></a>
                <p class="font-weight-bold mb-0">Order Status</p>
                <small>Your order for today is ${data['status'].toLowerCase()}.</small>
            </div>
        `);
    });
}

function closeNotif(e) {
    $(e.target).closest('.alert').fadeOut();
    --notifCount;
    $('title').html(`${notifCount > 0 ? '(' + notifCount + ') ' : ''}Tinapay`);
}