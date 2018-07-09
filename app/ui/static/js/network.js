App.network = App.network || {
    error: false,
    loading: false,
    data: [],
    tableSettings: {
        rowId:'name',
        searching:true,
        responsive: false,
        select: true,
        columnDefs: [
            {
                orderable: false,
                className: 'select-checkbox',
                targets:   0
            }
        ],
        dom: "<'tbl-header'<'row'<'col-sm-4 text-left'f><'col-sm-2 refresh-list-place'><'col-sm-6 json-place'>>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-4'i><'col-sm-2 text-right'l><'col-sm-6 text-right'p>>",
        "oLanguage": {
          "sLengthMenu": "List _MENU_ ",
        },
        select: {
            style:    'multi',
            selector: 'td:first-child'
        },
        order: [[ 1, 'asc' ]],
        initComplete: function(settings, json) {
            var tempButton = $('.rawJSONNetworks').clone();
            tempButton.removeClass('rawJSONNetworks');
            tempButton.on('click', $.proxy(App.network.showJSON, App.network));
//            $('#'+$(this).closest('table').attr('id')+'_filter').prepend(tempButton);
            $('.json-place').append(tempButton);
            tempButton.show();
        },
    },
    activeNetwork: {},
    rawJson: null,
    init: function(opts){
        console.log('Network initialized')
        this.dataTable = $('#tableNetworks').DataTable(this.tableSettings);
        this.rawJson = ace.edit('rawJson');
        this.rawJson.session.setMode('ace/mode/json');
        this.rawJson.setOptions({readOnly: true});
        $('#buttonUpdateNetwork').on('click', $.proxy(this.updateNetwork, this));
        $('#buttonCreateNetwork').on('click', $.proxy(this.createNetwork, this));
        $('#buttonNewNetwork').on('click', $.proxy(this.showNewUpdateNetwork, this));
        $('#backNetwork').on('click', $.proxy(this.backToNetworks, this));
        App.setActiveLink('network');
        $('#buttonDeleteNetwork').on('click', $.proxy(this.deleteNetwork, this));
        $('#selectAllNetworks').on('change', $.proxy(this.toggleSelectAll, this, 'Remote'));
        this.dataTable.on('select', $.proxy(this.onItemSelectChange, this));
        this.dataTable.on('deselect', $.proxy(this.onItemSelectChange, this));

    },
    setLoading: function(state){
        var tempLoaderState = state?'show':'hide';
        var tempTableState = state?'hide':'show';
        $('#loader')[tempLoaderState]();
        if(this.activeTab == 'local')
            return $('#tableImagesLocalWrapper')[tempTableState]();
        else
            return $('#tableImagesRemoteWrapper')[tempTableState]();
    },
    getData: function(){
        this.setLoading(true);
        $.get(App.baseAPI+'network', $.proxy(this.getDataSuccess2, this));
    },
    getDataSuccess2: function(response){
        this.setLoading(false);
        this.rawJson.setValue(JSON.stringify(response.data, null , '\t'));
        //this.updateLocalTable(response.data);
    },
    showJSON: function(e) {
        this.rawJson.setValue('');
        $('.modal-title').text('');
        $('.modal-title').text('RAW JSON for Networks');
        $('.modal-title').append(' <span class="glyphicon glyphicon-refresh spinning loader">');
        $("#jsonModal").modal("show");

        this.getData();

    },
    getNetwork: function(name){
        $('#name').val(name);
        $('#name').prop('readonly', true);
        return $.get(App.baseAPI+'network/'+name, $.proxy(this.getDataSuccess, this));
    },
    getDataSuccess: function(response) {
        this.activeNetwork = response.data;
        $('#IPv4_ADDR').val(this.activeNetwork.IPv4_ADDR);
        $('#IPv4_NETMASK').val(this.activeNetwork.IPv4_NETMASK);
        $('#IPv4_DHCP_START').val(this.activeNetwork.IPv4_DHCP_START);
        $('#IPv4_DHCP_END').val(this.activeNetwork.IPv4_DHCP_END);
    },
    showUpdateNetwork: function(elem) {
        this.getNetwork(elem);

        $('#newUpdateNetwork').show();
        $('#networkList').hide();
        $('#buttonUpdateNetwork').show();
        $('.updateWarningText').show();
        $('#buttonCreateNetwork').hide();
    },
    showNewUpdateNetwork: function() {
        $('#newUpdateNetwork').show();
        $('#networkList').hide();
        $('#buttonUpdateNetwork').hide();
        $('.updateWarningText').hide();
        $('#buttonCreateNetwork').show();
    },
    backToNetworks: function() {
        $('#entire_form').trigger('reset');
        $('#name').prop('readonly', false);
        $('#newUpdateNetwork').hide();
        $('#networkList').show();
    },
    updateNetwork: function(){
        $.ajax({
            url:App.baseAPI+'network/' + $('#name').val(),
            type: 'PUT',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                IPv4_ENABLED: true,
                IPv4_AUTO: false,
                IPv4_ADDR: $('#IPv4_ADDR').val(),
                IPv4_NETMASK: $('#IPv4_NETMASK').val(),
                IPv4_DHCP_START: $('#IPv4_DHCP_START').val(),
                IPv4_DHCP_END: $('#IPv4_DHCP_END').val()
            }),
            success: $.proxy(this.onNetworkUpdateSuccess, this)
        });
    },
    onNetworkUpdateSuccess: function(response){
         console.log(response);
         console.log('updateSuccess:', 'TODO - add alert and refresh local data');
    },
    createNetwork: function(){
        $.ajax({
            url:App.baseAPI+'network/'+$('#name').val(),
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                IPv4_ENABLED: true,
                IPv4_AUTO: false,
                IPv4_ADDR: $('#IPv4_ADDR').val(),
                IPv4_NETMASK: $('#IPv4_NETMASK').val(),
                IPv4_DHCP_START: $('#IPv4_DHCP_START').val(),
                IPv4_DHCP_END: $('#IPv4_DHCP_END').val()
            }),
            success: $.proxy(this.onNetworkCreateSuccess, this)
        });
    },
    onNetworkCreateSuccess: function(response){
         console.log(response);
         console.log('createdSuccess:', 'TODO - add alert and refresh local data');
    },
    deleteNetwork: function() {
        this.dataTable.rows( { selected: true } ).data().map(function(row){
            $.ajax({
                url: App.baseAPI+'network/' + row['name'],
                type: 'DELETE',
                success: $.proxy(this.onDeleteSuccess, this, row['name'])
            });
        }.bind(this));
    },
    onDeleteSuccess: function(name){
        this.dataTable.row("#"+name).remove().draw();
        $('.success-msg').text('Network ' + name + ' has been removed');
        var parent = $('.success-msg').parent().toggleClass('hidden');

        setTimeout(function(){
          parent.toggleClass('hidden');
        }, 10000);

    },
    toggleSelectAll:function(name, event){
        if(event.target.checked){
            this.dataTable.rows().select();
        }else{
            this.dataTable.rows().deselect();
        }
    },
    onItemSelectChange : function(e, dt, type, indexes ){
        var state = this.dataTable.rows({selected:true}).count()>0;
        $('#selectAllNetworks').prop('checked', state);
    }
}