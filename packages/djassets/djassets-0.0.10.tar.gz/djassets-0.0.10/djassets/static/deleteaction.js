
DeleteAction = function (params) {

    var $container = params.$container,
        selector = params.selector,
        onDelete = params.onDelete,
        method = params.method || 'POST';

    function handleDeleteClick() {
        var $btn = $(this);

        $btn.prop('disabled', true);

        $.ajax({
            method: method,
            url: $btn.data('url'),
            success: function (response) {
                onDelete($btn.data('item-id'), response);

                $.notify({
                    message: response.message
                }, {
                    type: 'success'
                });
            },
            error: function (response) {
                $.notify({
                    message: response.responseText
                }, {
                    type: 'danger'
                });
            }
        });
    }

    $container.on('click', selector, handleDeleteClick);

};
