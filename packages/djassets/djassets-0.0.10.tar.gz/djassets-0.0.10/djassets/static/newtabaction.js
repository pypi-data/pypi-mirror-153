
NewTabAction = function ($target, onResponse) {

    function handleTargetClick() {

        var url = $target.data('url');

        $target.prop('disabled', true);

        $.post(url, {}, function (response) {
            var win = window.open(response, '_blank');
            win.focus();
            if (onResponse) {
                onResponse($target, response);
            }
        }).fail(function (response) {
            $.notify({message: response.responseText}, {type: 'danger'});
        });
    }

    $target.click(handleTargetClick);
};
