MonoSubmitForm = function (params) {
    var $form = params.$form,
        btnText = params.btnText;

    $form.on('submit', function () {
        $form.find('[type=submit]').prop('disabled', true).text(btnText);
    });
};
