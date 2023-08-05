SelectChainedBox = function (params) {

    var $select = params.$select,
        $target = params.$target,
        value = String(params.value);

    function isVisible() {
        var currentValue = $select.val();

        if ($select.prop('multiple')) {
            return currentValue && $.inArray(value, currentValue) !== -1;
        }
        return currentValue == value;
    }

    function refresh() {
        if (isVisible()) {
            $target.show();
        } else {
            $target.hide();
        }
    }

    $select.on('change', refresh);

    refresh();
};