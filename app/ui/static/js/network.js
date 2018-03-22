App.network = App.network || {
    error: false,
    loading: false,
    data: [],

    tableSettings: {
        searching:true,
        responsive: {
            details: false
        },
        select: true,
        autoWidth: true,
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
        order: [[ 1, 'asc' ]]
    },
    init: function(opts){
        console.log('Network initialized')
        $('#buttonUpdateNetwork').on('click', $.proxy(this.updateNetwork, this));
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
    updateNetwork: function(){
        $.ajax({
            url:App.baseAPI+'network/lxdbr0',
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
    }
}