function refreshOrder() {
    $(".order-input").val(0);
    $("#widgets > .col").each(function (index) {
        const order = (index + 1) * 10;
        let pk = $(this).attr("data-pk");
        let sel = $("#order-form input[value=" + pk + "].pk-input").next();
        sel.val(order);
    })
}

$(document).ready(function () {
    $('#not-used-widgets').sortable({
        group: 'widgets',
        animation: 150,
        onEnd: refreshOrder
    });
    $('#widgets').sortable({
        group: 'widgets',
        animation: 150,
        onEnd: refreshOrder
    });
});
