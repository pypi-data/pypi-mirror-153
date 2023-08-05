
TaskProgress = function ($target) {

    var url = $target.data('url'),
        interval;

    interval = setInterval(function () {
        $.get(url, function (response) {
            $target.text(response.text);
            $target.width(response.percent + '%');
            $target.prop('aria-valuenow', response.percent);

            if (response.percent == 100) {
                clearInterval(interval);
            }
        });
    }, 2500);

};
