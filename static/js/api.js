function orderChangeStatus(data) {
    return $.ajax({
        type: 'POST',
        url: '/api/order/change_status',
        data: data,
        dataType: 'JSON'
    })
}