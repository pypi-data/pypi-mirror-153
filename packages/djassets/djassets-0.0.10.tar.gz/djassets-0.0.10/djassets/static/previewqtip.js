
PreviewQTip = function (params) {

    var $target = params.$target,
        classes = params.classes;

    $target.qtip({
        position: {
            target: 'mouse',
            adjust: {x: 20, y: -10}
        },
        content: {
            text: '<img src="' + $target.data('url') + '" />'
        },
        style: {
            def: false,
            classes: classes
        }
    });

};
