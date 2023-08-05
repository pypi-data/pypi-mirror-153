
List = function (params) {

    var $container = params.$container,
        url = params.url,
        nextPageUrl = url,
        xhr = null;

    function reload() {
        nextPageUrl = url;
        clearItems();
        loadMore();
    }

    function loadMore() {
        abortRequest();
        togglePreloader(true);
        toggleLoadMore(false);

        xhr = $.ajax({
            url: getLoadUrl(),
            method: 'GET',
            success: function(response) {
                getItemsContainer().append(response.items);
                nextPageUrl = response['next_page_url'];

                togglePreloader(false);
                toggleLoadMore(response['has_next']);
                toggleNoItems(isEmpty());
            }
        });
    }

    function getLoadUrl() {
        var url = new URL(window.location.origin + nextPageUrl),
            form = getForm();

        if (!form) {
            return url.href;
        }

        $.each(form.serializeArray(), function () {
            url.searchParams.set(this.name, this.value);
        });

        return url.href;
    }

    function getForm() {
        return $container.find('[data-role=form]');
    }

    function togglePreloader(isVisible) {
        var action = isVisible ? 'show' : 'hide';
        $container.find('[data-role=preloader]')[action]();
    }

    function toggleLoadMore(isVisible) {
        var action = isVisible ? 'show' : 'hide';
        $container.find('[data-role=load-more]')[action]();
    }

    function toggleNoItems(isVisible) {
        var action = isVisible ? 'show' : 'hide';
        $container.find('[data-role=no-items]')[action]();
    }

    function getItemsContainer() {
        return $container.find('[data-role=list-items]');
    }

    function isEmpty() {
        return !getItemsContainer().find('tr').length;
    }

    function clearItems() {
        getItemsContainer().empty();
    }

    function abortRequest() {
        if (xhr) {
            xhr.abort();
            xhr = null;
        }
    }

    $container.on('click', '[data-role=load-more-btn]', loadMore);
    $container.on('change', '[data-role=form] input', reload);

    loadMore();

};
