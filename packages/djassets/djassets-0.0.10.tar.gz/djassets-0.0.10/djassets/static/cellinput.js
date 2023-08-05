
CellInput = function (params) {

    var $container = params.$container,
        selector = params.selector,
        onSuccess = params.onSuccess;

    function handleInputChange() {
        var $input = $(this),
            data = {};

        data[$input.attr('name')] = $input.val();

        $input.blur();

        $.post($input.data('url'), data)
            .done(handleSaveSuccess)
            .error(handleSaveError);
    }

    function handleSaveSuccess(response) {
        onSuccess(response);
        $.notify({message: response.message}, {type: 'success'});
    }

    function handleSaveError(response) {
        $.notify({message: response.responseText}, {type: 'danger'});
    }

    function handleInputFocus() {
        $(this).select();
    }

    $container.on('change', selector, handleInputChange);
    $container.on('focus', selector, handleInputFocus);

};
