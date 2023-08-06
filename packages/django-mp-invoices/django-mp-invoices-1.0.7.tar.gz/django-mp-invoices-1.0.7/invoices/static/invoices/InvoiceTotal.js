
InvoiceTotal = function ($container, target) {

    function handleTotalUpdated (event, total) {
        $.each(total, function (key, value) {

            if (key === 'discount_percentage') {
                $container.find('[data-role=discount-input]').val(value);
                return;
            }

            $container.find('[data-role=' + key + ']').text(value);

        });
    }

    $(window).on(target + '-total-updated', handleTotalUpdated);

};
