
FormAutocomplete = function (params) {
    var url = params.url,
        $container = params.$container,
        $form = $container.find('[data-role=form]'),
        $input = $container.find('[data-role=autocomplete-input]'),
        $appendTo = $container.find('[data-role=autocomplete-container]');

    console.log($input);

    $input.autocomplete({
        serviceUrl: function () {
            return url + '?' + $form.serialize()
        },
        width: 'flex',
        appendTo: $appendTo,
        minChars: 2,
        maxHeight: 700,
        formatResult: function (suggestion, currentValue) {
            return suggestion.html;
        },
        onSelect: function (suggestion) {
            window.location = suggestion.data;
        }
    });
};
