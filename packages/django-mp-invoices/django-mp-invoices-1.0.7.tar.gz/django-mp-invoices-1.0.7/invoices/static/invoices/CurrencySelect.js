
CurrencySelect = function (params) {

    var $container = params.$container,
        url = params.url;

    function handleSelectChange() {
        $.post(
            url,
            {currency: $(this).val()}
        ).done(function (response) {
            $.notify({message: response.message}, {type: 'success'});
        }).error(function (response) {
            $.notify({message: response.responseText}, {type: 'danger'});
        });
    }

    $container.on('change', handleSelectChange);

};
