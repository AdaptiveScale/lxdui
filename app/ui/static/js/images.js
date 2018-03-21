App.images = App.images || {
    error: false,
    loading: false,
    data: [],
    remoteData: [],
    activeTab:'local',

    tableLocal: null,
    tableRemote: null,
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
        console.log('Images initialized')
        $('#btnLocalImages').on('click', $.proxy(this.onSwitchToggle, this, 'local'));
        $('#btnRemoteImages').on('click', $.proxy(this.onSwitchToggle, this, 'remote'));
        $('#buttonUpdate').on('click', $.proxy(this.getData, this));
        $('#buttonDelete').on('click', $.proxy(this.doDeleteLocalImages, this));
        $('#buttonDownload').on('click', $.proxy(this.doDownload, this));
        this.initLocalTable();
        this.initRemoteTable();
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
    initLocalTable: function(){
        this.tableLocal =$('#tableImagesLocal').DataTable(App.mergeProps(this.tableSettings, {rowId: 'fingerprint'}));
        this.setLocalTableEvents();
    },
    setLocalTableEvents: function(){
        this.tableLocal.on('select', $.proxy(this.onItemSelectChange, this));
        this.tableLocal.on('deselect', $.proxy(this.onItemSelectChange, this));
    },
    initRemoteTable: function(){
        this.tableRemote =$('#tableImagesRemote').DataTable(App.mergeProps(this.tableSettings, {rowId: 'image'}));
        this.setRemoteTableEvents();
    },
    setRemoteTableEvents: function(){
        this.tableRemote.on('select', $.proxy(this.onItemSelectChange, this));
        this.tableRemote.on('deselect', $.proxy(this.onItemSelectChange, this));
    },
    onItemSelectChange : function(e, dt, type, indexes ){
        if(this.activeTab=='local'){
            var state = this.tableLocal.rows({selected:true}).count()>0?'visible':'hidden';
            $('#buttonLaunch').css('visibility',state);
            $('#buttonDelete').css('visibility',state);
            return;
        }
        if(this.activeTab=='remote'){
            var state = this.tableRemote.rows({selected:true}).count()>0?'visible':'hidden';
            $('#buttonDownload').css('visibility',state);
            return;
        }
    },
    doDeleteLocalImages: function(){
        this.tableLocal.rows( { selected: true } ).data().map(function(row){
            $.ajax({
                url: App.baseAPI+'image/' + row['fingerprint'],
                type: 'DELETE',
                success: $.proxy(this.onDeleteSuccess, this, row['fingerprint'])
            });
        }.bind(this));
    },
    onDeleteSuccess: function(fingerprint){
        this.tableLocal.row("#"+fingerprint).remove().draw();
    },
    doDownload: function(){
        this.tableRemote.rows({selected: true}).data().map(function(row){
            $.ajax({
                url:App.baseAPI+'image/remote',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    image:row['image']
                }),
                success: $.proxy(this.onDownloadSuccess, this, row['image'])
            });
            this.tableRemote.row('#'+row['image']).remove().draw(false);
        }.bind(this));
    },
    onDownloadSuccess: function(imageName, response){
         console.log('downloadSuccess:', 'TODO - add alert and refresh local data');
    },
    getData: function(){
        this.setLoading(true);
        if(this.activeTab=='local')
            return $.get(App.baseAPI+'image', $.proxy(this.getDataSuccess, this));
        if(this.activeTab=='remote')
            return $.get(App.baseAPI+'image/remote', $.proxy(this.getDataSuccess, this));
    },
    onSwitchToggle: function(screen){
        if(screen==='local'){
            $('#tableImagesLocalWrapper').show();
            $('#tableImagesRemoteWrapper').hide();
            $('#buttonDownload').css('visibility','hidden');
            this.activeTab = 'local';
            return;
        }
        if(screen==='remote'){
            $('#tableImagesLocalWrapper').hide();
            $('#tableImagesRemoteWrapper').show();
            $('#buttonDelete').css('visibility','hidden');
            this.activeTab = 'remote';
            return;
        }
    },
    updateLocalTable: function(jsonData){
        this.data = jsonData;
        this.tableLocal.clear();
        this.tableLocal.destroy();
        this.tableLocal = $('#tableImagesLocal').DataTable(App.mergeProps(this.tableSettings, {
            rowId:'fingerprint',
            data : this.data,
            columns : [
                { title:'Select', data: null, defaultContent:''},
                { title:'OS', data : 'properties.os'},
                { title:'Description', data : 'properties.description' },
                { title:'Aliases', data : 'aliases'},
                { title:'Release', data : 'properties.release' },
                { title:'Architecture', data : 'properties.architecture' },
                { title:'Size', data : 'size' }
            ]
        }));
    },
    updateRemoteTable: function(jsonData){
        this.remoteData = jsonData;
        this.tableRemote.clear();
        this.tableRemote.destroy();
        this.tableRemote=$('#tableImagesRemote').DataTable(App.mergeProps(this.tableSettings, {
            rowId:'image',
            data : this.remoteData,
            columns : [
                { title:'Select', data: null, defaultContent:''},
                { title: 'Distribution', data : 'distribution' },
                { title: 'Architecture', data : 'architecture' },
                { title: 'Image', data : 'image' },
                { title: 'Name', data : 'name' }
            ]
        }));
    },
    getDataSuccess: function(response){
        this.setLoading(false);
        if(this.activeTab=='local'){
            this.updateLocalTable(response.data);
        }
        if(this.activeTab == 'remote'){
            this.updateRemoteTable(response.data);
        }
    },
    getRemoteData: function(){
        $.get(App.baseAPI+'image/remote', $.proxy(this.getDataSuccess, this));
    }
}