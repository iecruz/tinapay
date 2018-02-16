function orderOnDelivery(e) {
    var data = {
        id: $(e.target).attr('data-key'),
        status: 'On Delivery'
    };

    orderChangeStatus(data).done(function(response) {
        if(response){
            $(`span.status-text[data-key="${data.id}"]`).html(data.status)
        }
    });
}

function orderVoid(e) {
    var data = {
        id: $(e.target).attr('data-key'),
        status: 'Void'
    };

    orderChangeStatus(data).done(function(response) {
        if(response){
            $(`span.status-text[data-key="${data.id}"]`).html(data.status)
        }
    });
}