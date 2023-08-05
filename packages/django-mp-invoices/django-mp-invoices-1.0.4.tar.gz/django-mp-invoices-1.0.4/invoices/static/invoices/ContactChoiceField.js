
ContactSelect = function (params) {

    var $field = params.$field,
        url = params.url;

    function handleFieldChange() {
        var data = {};

        data[$field.attr('name')] = $field.val();

        $field.prop('disabled', true);

        $.post(url, data, handleUpdate);
    }

    function handleUpdate(response) {
        $field.prop('disabled', false);
        if (response.message) {
            $.notify({message: response.message}, {type: 'success'});
        }
        $(window).trigger('product-total-updated', response.total);
    }

    function handleOptionCreated(event, obj) {
        var $option = $('<option />');

        $option.text(obj.name);
        $option.prop('value', obj.id);

        $field.append($option);
        $field.val(obj.id);

        handleFieldChange();
    }

    $field.on('change', handleFieldChange);
    $(window).on($field.attr('name') + '-created', handleOptionCreated);

};
