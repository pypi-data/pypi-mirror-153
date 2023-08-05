
Clipboard = function ($container, onSuccess) {

    var $target = $container.find('[data-role=copy-to-clipboard]');

    function handleTargetClick() {

        var $target = $(this),
            $input = $('<textarea />'),
            input = $input[0];

        $input.val($target.data('value'));
        $input.css('z-index', '-1');
        $input.insertAfter($target);

        input.select();
        input.setSelectionRange(0, 99999);

        document.execCommand("copy");

        $input.remove();

        $.notify({
            message: $target.data('message')
        }, {
            type: 'success'
        });

        if (onSuccess) {
            onSuccess($container);
        }

    }

    $target.click(handleTargetClick);
};
