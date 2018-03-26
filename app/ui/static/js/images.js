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
    containerTemplate:null,
    newContainerForm:null,
    init: function(opts){
        console.log('Images initialized');
        this.data = constLocalImages || [];
        this.remoteData = constRemoteImages || [];
        this.containerTemplate = $('.multiContainerTemplate');
        $('#btnLocalImages').on('click', $.proxy(this.onSwitchToggle, this, 'local'));
        $('#btnRemoteImages').on('click', $.proxy(this.onSwitchToggle, this, 'remote'));
        $('#buttonUpdate').on('click', $.proxy(this.getData, this));
        $('#buttonDelete').on('click', $.proxy(this.doDeleteLocalImages, this));
        $('#buttonDownload').on('click', $.proxy(this.doDownload, this));
        $('#buttonLaunchContainers').on('click', $.proxy(this.launchContainers, this));
        $('#buttonBack').on('click', $.proxy(this.switchView, this, 'localList'));
        this.newContainerForm = $('#newContainerForm');
        this.newContainerForm.on('submit', $.proxy(this.doCreateContainer, this));
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
            $('#buttonLaunchContainers').css('visibility',state);
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
         $('#buttonLaunchContainers').css('visibility','hidden');
         $('#buttonDelete').css('visibility','hidden');
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
    },
    generateContainerFormSection: function(image, pos){
        var tempSection = this.containerTemplate.clone();
        tempSection.prop('id',image.fingerprint);
        tempSection.find('input[name="name"]').prop('name', 'image['+pos+'][name]');
        tempSection.find('input[name="image['+pos+'][name]"]').val(image.properties.os.toLowerCase()+'-');

        tempSection.find('input[name="image"]').prop('name', 'image['+pos+'][image]');
        tempSection.find('input[name="image['+pos+'][image]"]').val(image.fingerprint);

        tempSection.find('input[name="count"]').prop('name', 'image['+pos+'][count]');
        tempSection.find('input[name="image['+pos+'][count]"]').on('change', $.proxy(this.onCountChange, this, tempSection.find('.nodeCount')));


        tempSection.find('.imageName').text(image.properties.description);
        tempSection.show();
        return tempSection;
    },
    onCountChange: function(countNode, event){
        $(countNode).text($(event.target).val() +' Node(s)');
    },
    getImageByFingerPrint: function(tempList, fingerprint){
        return tempList.filter(function(image){
            return image.fingerprint === fingerprint;
        })[0];
    },
    launchContainers: function(){
        var count = 0;
        this.tableLocal.rows({selected: true}).data().map(function(row){
            var tempForm = this.generateContainerFormSection(
                this.getImageByFingerPrint(this.data, row['fingerprint'])
            , count);
            $('#multiContainerSection').append(tempForm);
            count+=1;
        }.bind(this));
        this.switchView('form');
    },
    switchView: function(view){
        $('#createMultipleContainersForm')[view=='form'?'show':'hide']();
        $('#tableImagesLocalWrapper')[view=='localList'?'show':'hide']();
        $('#tableImagesRemoteWrapper')[view=='remoteList'?'show':'hide']();
        if(view!=='form'){
            $('#multiContainerSection').empty();
        }
    },
    generateContainer: function(name, image, specs){
        return {
            name:name,
            image:image.image,
            ...specs
        }
    },
    generateImageContainers: function(jsonImage, specs){
        var imageContainers = [];
        for(var i=0;i<=Number(jsonImage.count)-1;i++){
            imageContainers.push(this.generateContainer(jsonImage.name+(i+1), jsonImage, specs));
        }
        return imageContainers;
    },
    cleanupFormData(specs){
        delete specs['image'];
        specs['cpu']['percentage']=Number(specs['cpu']['percentage']);
        specs['cpu']['hardLimitation']=Boolean(specs['cpu']['hardLimitation']) || false;
        specs['memory']['sizeInMB']=Number(specs['memory']['sizeInMB']);
        specs['memory']['hardLimitation']=Boolean(specs['memory']['hardLimitation']) || false;
        specs['stateful']=Boolean(specs['stateful']) || true;
        specs['autostart']=Boolean(specs['autostart']) || true;
        return specs;
    },
    generateRequest: function(inputJSON){
        var tempRequest = [];
        var tempSpecs = this.cleanupFormData($.extend({}, true, inputJSON));
        for(item in inputJSON.image){
            var tempData = this.generateImageContainers(inputJSON.image[item], tempSpecs);
            tempRequest=tempRequest.concat(tempData);
        }
        return tempRequest;
    },
    doCreateContainer: function(e){
        e.preventDefault();
        var tempForm = $.extend({}, true,this.newContainerForm.serializeJSON());
        var tempJSON = this.generateRequest(tempForm);
        $.ajax({
            url: App.baseAPI +'container/',
            type:'POST',
            dataType:'json',
            contentType: 'application/json',
            data: JSON.stringify(tempJSON),
            success: $.proxy(this.onCreateSuccess, this),
            error: $.proxy(this.onCreateFailed, this)
        });
    },
    onCreateSuccess: function(response){
        this.switchView('localList');
        window.location = App.baseWEB +'containers';
    }
}