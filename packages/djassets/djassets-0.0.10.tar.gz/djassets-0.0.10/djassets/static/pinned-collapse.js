
PinnedCollapse = function (params) {

    var $container = params.$container,
        cookieName = $container.data('role') + '-state';

    function saveState(isCollapsed) {
        $.cookie(cookieName, isCollapsed, {path: '/'});
    }

    $container.on('shown.bs.collapse', function () {
        saveState(false);
    });

    $container.on('hidden.bs.collapse', function () {
        saveState(true);
    });

    if ($.cookie(cookieName) !== 'true') {
        $container.collapse('show');
    }

};
