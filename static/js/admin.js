var adminSocket = io(window.location.origin + '/admin');

function orderOnDelivery(e) {
    var data = {
        id: $(e.target).attr('data-key'),
        username: $(e.target).attr('data-user'),
        status: 'On Delivery'
    };

    orderChangeStatus(data).done(function(response) {
        if(response){
            $(`span.status-text[data-key="${data.id}"]`).html(data.status)
            adminSocket.emit('order status', data);
        }
    });
}

function orderVoid(e) {
    var data = {
        id: $(e.target).attr('data-key'),
        username: $(e.target).attr('data-user'),
        status: 'Void'
    };

    orderChangeStatus(data).done(function(response) {
        if(response){
            $(`span.status-text[data-key="${data.id}"]`).html(data.status)
            adminSocket.emit('order status', data);
        }
    });
}