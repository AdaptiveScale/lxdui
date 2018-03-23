App.network = App.network || {
    error: false,
    loading: false,
    data: [],
    tableSettings: {
        rowId:'name',
        searching:true,
        responsive: true,
        select: true,
        columnDefs: [
            {
                orderable: false,
                className: 'select-checkbox',
                targets:   0
            }
        ],
        select: {
            style:    'multi',
            selector: 'td:first-child'
        },
        order: [[ 1, 'asc' ]],
    },
    activeNetwork: {},
    init: function(opts){
        console.log('Network initialized')
        this.dataTable = $('#tableNetworks').DataTable(this.tableSettings);
        $('#buttonUpdateNetwork').on('click', $.proxy(this.updateNetwork, this));
        $('#buttonCreateNetwork').on('click', $.proxy(this.createNetwork, this));
        $('#buttonNewNetwork').on('click', $.proxy(this.showNewUpdateNetwork, this));
        $('#backNetwork').on('click', $.proxy(this.backToNetworks, this));

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
        this.getNetwork($(elem).attr('id'));
        $('#newUpdateNetwork').show();
        $('#networkList').hide();
        $('#buttonUpdateNetwork').show();
        $('#buttonCreateNetwork').hide();
    },
    showNewUpdateNetwork: function() {
        $('#newUpdateNetwork').show();
        $('#networkList').hide();
        $('#buttonUpdateNetwork').hide();
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
    }
}