
CategoryTree = function (params) {

    var data = params.data,
        $container = params.$container,
        $list = $container.find('[data-role=categories]'),
        $filter = $container.find('[data-role=category-filter]'),
        $input = $container.find('[data-role=category-input]');

    function handleFilterKeyup() {
        var val = $(this).val();

        if (!val) {
            $list.treeview('clearSearch');
            return;
        }

        $list.treeview('search', [val, {
            ignoreCase: true,
            exactMatch: false,
            revealResults: true
        }]);
    }

    function handleSearchComplete() {
        var tree = $list.treeview(true);

        $.each(tree.getEnabled(), function () {
            var $li = $list.find('[data-nodeid=' + this.nodeId + ']');
            $li[this.searchResult ? 'show' : 'hide']();
        })
    }

    function handleSearchCleared() {
        $list.find('li').show();
    }

    function handleNodeSelected(event, node) {
        $input.val(node.id).trigger('change');
    }

    function handleNodeUnselected(event, node) {
        $input.val('').trigger('change');
    }

    $list.treeview({
        data: data,
        nodeIcon: 'fa fa-folder',
        highlightSearchResults: false,
        onSearchComplete: handleSearchComplete,
        onSearchCleared: handleSearchCleared,
        onNodeSelected: handleNodeSelected,
        onNodeUnselected: handleNodeUnselected
    });

    $filter.on('keyup', handleFilterKeyup);

};
