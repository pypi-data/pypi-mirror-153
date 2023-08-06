
InvoiceList = function (params) {

    var $container = params.$container,
        addItemUrl = params.addItemUrl,
        target = params.target;

    function handleListItemSelected(event, itemId, params) {

        var data = {};

        data[target] = itemId;

        $.ajax({
            url: addItemUrl,
            method: 'POST',
            data: data,
            success: function (response) {
                handleAddItemSuccess(response, params || {});
            },
            error: handleAddItemError
        });
    }

    function handleAddItemSuccess(response, params) {
        var $items = getItemsContainer(),
            $item = getItemContainer(response.item_id);

        if ($item.length) {
            $item.replaceWith(response.html);
        } else {
            $items.prepend(response.html);
        }

        if (params.focus) {
            getItemContainer(response.item_id)
                .find('[data-role=qty-input]')
                .focus();
        }

        $(window).trigger(target + '-updated', response[target]);
        $(window).trigger(target + '-total-updated', response.total);
    }

    function handleAddItemError(response) {
        $.notify({message: response.responseText}, {type: 'danger'});
    }

    function getItemsContainer() {
        return $container.find('[data-role=list-items]');
    }

    function getItemContainer(itemId) {
        return getItemsContainer().find(
            '[data-role=list-item][data-item-id=' + itemId + ']');
    }

    function handleSaveItemSuccess(response) {
        $(window).trigger(target + '-updated', response[target]);
        $(window).trigger(target + '-total-updated', response.total);
    }

    new CellInput({
        $container: $container,
        selector: '[data-role=discount-input]',
        onSuccess: function (response) {
            $(window).trigger(target + '-total-updated', response.total);
        }
    });

    new CellInput({
        $container: $container,
        selector: '[data-role=qty-input]',
        onSuccess: handleSaveItemSuccess
    });

    new CellInput({
        $container: $container,
        selector: '[data-role=price-input]',
        onSuccess: handleSaveItemSuccess
    });

    new DeleteAction({
        $container: $container,
        selector: '[data-role=delete-action]',
        method: 'DELETE',
        onDelete: function (itemId, response) {
            getItemContainer(itemId).remove();
            $(window).trigger(target + '-updated', response[target]);
            $(window).trigger(target + '-total-updated', response.total);
        }
    });

    new InvoiceTotal($container, target);

    $(window).on(target + '-selected', handleListItemSelected);

};
