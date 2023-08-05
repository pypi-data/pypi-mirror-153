
ConfirmPopup = function (params) {
    var $target = params.$target,
        url = params.url,
        yes = params.yes || 'Confirm',
        no = params.no || 'Cancel',
        title = params.title || '';

    function handleTargetClick() {

        var $container = $('<div />').text(title);

        function confirm() {
            var dialog = $container.dialog('instance'),
                $buttons = dialog.uiButtonSet.find('button'),
                instanceId = dialog.opener.data('instance-id'),
                wrapper = dialog.opener.data('wrapper'),
                data = {pk: instanceId};

            $buttons.prop('disabled', true);

            $.post(url, data, function (response) {
                closePopup();
                $(wrapper).remove();
                $.notify({message: response.message}, {type: 'success'});
            });
        }

        function closePopup() {
            $container.dialog('destroy');
        }

        $container.dialog({
            modal: true,
            buttons : [
                {
                    text: yes,
                    click: confirm
                },
                {
                    text: no,
                    click: closePopup
                }
            ]
        });
    }

    $target.click(handleTargetClick);
};
