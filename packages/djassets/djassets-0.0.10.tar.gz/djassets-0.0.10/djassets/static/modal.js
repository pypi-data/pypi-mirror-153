
Modal = function (params) {

    var $target = params.$target,
        selector = params.selector,
        onSuccess = params.onSuccess,
        onFormRender = params.onFormRender,
        onModalRender = params.onModalRender,
        onCancel = params.onCancel,
        contentGetter = params.contentGetter,
        focusOn = params.focusOn,
        traditional = params.traditional || false,
        url = params.url || $target.data('url');

    if (!contentGetter) {
        contentGetter = function (response) {
            return response;
        }
    }

    function showModal() {
        $.get(url, function (response) {

            var $modal = $(contentGetter(response)).modal(),
                isCanceled = true;

            function toggleSubmitBtn(isActive) {
                $modal.find('[data-role=submit-btn]').prop('disabled', !isActive);
            }

            function handleFormSubmit(event) {

                event.preventDefault();

                toggleSubmitBtn(false);

                $(this).ajaxSubmit({
                    method: 'POST',
                    url: url,
                    success: handleFormSubmitSuccess,
                    error: handleFormSubmitError,
                    traditional: traditional,
                    complete: function () {
                        toggleSubmitBtn(true);
                    }
                });

            }

            function handleSubmitBtnClick() {
                $modal.find('form').submit();
            }

            function removeModal() {
                $modal.remove();
                if (isCanceled && onCancel) {
                    onCancel();
                }
            }

            function handleFormSubmitSuccess(response) {

                isCanceled = false;
                $modal.modal('hide');

                if ($.notify && response.message) {
                    $.notify({message: response.message}, {type: 'success'});
                }

                if (response.url) {
                    window.location = response.url
                }

                if (onSuccess) {
                    onSuccess(response);
                }
            }

            function handleFormSubmitError(response) {
                $modal.find('form').replaceWith(response.responseText);

                if (onFormRender) {
                    onFormRender($modal, response);
                }
            }

            if (focusOn) {
                $modal.find(focusOn).focus();
            }

            if (onModalRender) {
                onModalRender($modal, response);
            }

            if (onFormRender) {
                onFormRender($modal, response);
            }

            $modal.on('submit', 'form', handleFormSubmit);

            $modal.on('click', '[data-role=submit-btn]', handleSubmitBtnClick);

            $modal.on('hidden.bs.modal', removeModal);

        });
    }

    if ($target) {
        $target.click(showModal);
    }

    if (selector) {
        $('document').on('click', selector, showModal);
    }

    this.show = showModal;

};
