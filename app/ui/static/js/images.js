App.images = App.images || {
    error: false,
    loading: false,
    data: [],
    remoteData: [],
    activeTab:'local',
    tableLocal: null,
    tableRemote: null,
    tableNightly: null,
    tableHub: null,
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
            var tempButton = $('.rawJSONImages').clone();
            tempButton.removeClass('rawJSONImages');
            tempButton.on('click', $.proxy(App.images.showJSON, App.images));
            $('#'+$(this).closest('table').attr('id')+'_wrapper .json-place').prepend(tempButton);
            tempButton.show();
        }
    },
    containerTemplate:null,
    newContainerForm:null,
    publishImageForm: null,
    itemTemplate:null,
    rawJson:null,
    simplemde:null,
    publishPage:0,
    publishFormValid:false,
    init: function(opts){
        this.data = constLocalImages || [];
        this.remoteData = constRemoteImages || [];
        this.containerTemplate = $('.multiContainerTemplate');
        this.rawJson = ace.edit('rawJson');
        this.rawJson.session.setMode('ace/mode/json');
        this.rawJson.setOptions({readOnly: true});
        $('#btnLocalImages').on('click', $.proxy(this.switchView, this, 'localList'));
        $('#btnRemoteImages').on('click', $.proxy(this.switchView, this, 'remoteList'));
        $('#btnNightlyImages').on('click', $.proxy(this.switchView, this, 'nightlyList'));
        $('#btnHubImages').on('click', $.proxy(this.switchView, this, 'hubList'));

        $('#buttonUpdate').on('click', $.proxy(this.getData, this));
        $('#buttonDelete').on('click', $.proxy(this.doDeleteLocalImages, this));
        $('#buttonDownload').on('click', $.proxy(this.doDownload, this));
        $('#buttonDownloadNightly').on('click', $.proxy(this.doDownload, this));
        $('#buttonDownloadHub').on('click', $.proxy(this.doDownload, this));
        $('#buttonLaunchContainers').on('click', $.proxy(this.launchContainers, this));
        $('#buttonBack').on('click', $.proxy(this.switchView, this, 'localList'));
        $('.image').on('click', $.proxy(this.setActive, this));
        $('#buttonPublish').on('click', $.proxy(this.publishImage, this));
        App.setActiveLink('image');
        this.newContainerForm = $('#newContainerForm');
        this.newContainerForm.on('submit', $.proxy(this.doCreateContainer, this));
        $('.imageSize').each(this.convertImageSize);
        this.initLocalTable();
        this.initRemoteTable();
        this.initNightlyTable();
        this.initHubTable();

        this.tableLocal.on('select', $.proxy(this.onRowSelected, this));
        this.tableLocal.on('deselect', $.proxy(this.onRowSelected, this));

        $('#selectAllLocal').on('change', $.proxy(this.toggleSelectAll, this, 'Local'));
        $('#selectAllRemote').on('change', $.proxy(this.toggleSelectAll, this, 'Remote'));
        this.itemTemplate = $('.itemTemplate').clone();
        $('#modalDownloadButton').on('click', $.proxy(this.doDownload, this));
        $('#exTab2 > ul > li:nth-child(1)').addClass('active');// set first tab as active
        $('#exTab > ul > li:nth-child(1)').addClass('active');// set first tab as active
        $('#architectureRemote').on('change', $.proxy(this.filterRemoteTable, this));
        $('#architectureNightly').on('change', $.proxy(this.filterNightlyTable, this));

        this.publishImageForm = $('#publishImageToHubForm');
        this.publishImageForm.on('submit', $.proxy(this.doPublishImage, this));
        $('#publishToHub').on('click', $.proxy(this.doPublishImage, this));

        this.simplemde = new SimpleMDE({
            element: document.getElementById("documentation"),
            spellChecker: false,
            hideIcons: ["side-by-side", "fullscreen"],
        });
        this.initKeyValuePairs();

        if (architecture == 'x86_64') {
            architecture = 'amd64';
        }
        this.tableRemote.search(architecture).draw();
        this.tableNightly.search(architecture).draw();

        $('#architectureNightly').val(architecture);
        $('#architectureRemote').val(architecture);

        if (localImagesLength == 0){
            this.switchView('nightlyList');
            $('.nav-tabs li:eq(1) a').tab('show');
        }
        $('#buttonPublishNext').on('click', $.proxy(this.onPublishNext, this));
        $('#buttonPublishBack').on('click', $.proxy(this.onPublishBack, this));

        $('#btnImageDetails').on('click', $.proxy(this.onPublishSwitchToPage, this, 0));
        $('#btnReadme').on('click', $.proxy(this.onPublishSwitchToPage, this, 1));
        $('#btnAuthorization').on('click', $.proxy(this.onPublishSwitchToPage, this, 2));
        $('#publishImageToHubForm').parsley().on('form:validate', $.proxy(this.onPublishFormValidation, this));
        $('#imageTags').tagit({
            fieldName:'imageTags'
        });
    },
    convertImageSize:function(index, item){
        $(item).text(App.formatBytes($(item).text()));
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
    initKeyValuePairs: function() {
        for (key in App.properties.keyValues) {
            $('#advancedSettingsMultipleContainer').append('<div class="row">' +
                    '<div class="col-lg-1"></div>'+
                    '<div class="col-lg-4">'+
                        '<div class="form-group row">' +
                            '<input type="text" class="form-control" placeholder="' + key + '"  disabled />' +
                            '<a href="#" class="hover-info" onmouseover="$.proxy(App.containerDetails.showPopover(this));" title="Information" data-toggle="popover" data-trigger="hover" data-content="'+ App.properties.keyValues[key].description + '" data-original-title="Information">' +
                                 '<span class="glyphicon glyphicon-info-sign"></span>' +
                             '</a>' +
                        '</div>' +
                    '</div>'+
                    '<div class="col-lg-1"></div>'+
                    '<div class="col-lg-4">' +
                        '<div class="form-group row">' +
                            '<input type="text" name="'+ key +'" id="' + key + '" class="form-control" placeholder="" value="" disabled />' +
                            '<a href="#" class="hover-info" onmouseover="$.proxy(App.containerDetails.showPopover(this));" title="Information" data-toggle="popover" data-trigger="hover" data-content="'+ _.get(App,'properties.keyValues["'+key+'"].valueDescription', 'No content available') + '" data-original-title="Information">' +
                                 '<span class="glyphicon glyphicon-info-sign"></span>' +
                             '</a>' +
                        '</div>' +
                    '</div>' +
                     '<div class="col-lg-2">' +
                         '<div class="btn-group" role="group">' +
                            '<button type="button" id="" class="formModifier btn btn-sm btn-default" onClick="$.proxy(App.containerDetails.enableInput(this));">On</button>' +
                            '<button type="button" id="" class="formModifier btn btn-sm btn-danger" onClick="$.proxy(App.containerDetails.disableInput(this));">Off</button>' +
                        '</div>' +
                     '</div>' +
                '</div>');
        }
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
    initNightlyTable: function(){
        this.tableNightly =$('#tableImagesNightly').DataTable(App.mergeProps(this.tableSettings, {rowId: 'fingerprint'}));
        this.setNightlyTableEvents();
    },
    setNightlyTableEvents: function(){
        this.tableNightly.on('select', $.proxy(this.onItemSelectChange, this));
        this.tableNightly.on('deselect', $.proxy(this.onItemSelectChange, this));
    },
    initHubTable: function() {
        this.tableHub =$('#tableImagesHub').DataTable(App.mergeProps(this.tableSettings, {rowId: 'fingerprint'}));
        this.setHubTableEvents();
    },
    setHubTableEvents: function() {
        this.tableHub.on('select', $.proxy(this.onItemSelectChange, this));
        this.tableHub.on('deselect', $.proxy(this.onItemSelectChange, this));
    },
    filterRemoteTable: function(e) {
        this.tableRemote.search(e.target.value).draw();
    },
    filterNightlyTable: function(e) {
        this.tableNightly.search(e.target.value).draw();
    },
    onRowSelected: function(e, dt, type, indexes ){
         if(this.tableLocal.rows({selected:true}).count() == 1){
            $('#buttonPublish').removeAttr('disabled', 'disabled');
          }
          else {
             $('#buttonPublish').attr('disabled', 'disabled');
          }
    },
    onItemSelectChange : function(e, dt, type, indexes ){
        if(this.activeTab=='local'){
            var state = this.tableLocal.rows({selected:true}).count()>0;
            var visibility= !state?'attr':'removeAttr';
            $('#buttonLaunchContainers')[visibility]('disabled', 'disabled');
            $('#buttonDelete')[visibility]('disabled', 'disabled');
            $('#selectAllLocal').prop('checked',this.tableLocal.rows({selected:true}).count()==this.tableLocal.rows().count());
            return;
        }
        if(this.activeTab=='remote'){
            var state = this.tableRemote.rows({selected:true}).count()>0
            var visibility= !state?'attr':'removeAttr';
            $('#buttonDownload')[visibility]('disabled', 'disabled');
            $('#selectAllRemote').prop('checked',this.tableRemote.rows({selected:true}).count()==this.tableRemote.rows().count());
            return;
        }
        if(this.activeTab=='nightly'){
            var state = this.tableNightly.rows({selected:true}).count()>0
            var visibility= !state?'attr':'removeAttr';
            $('#buttonDownloadNightly')[visibility]('disabled', 'disabled');
            $('#selectAllNightly').prop('checked',this.tableNightly.rows({selected:true}).count()==this.tableNightly.rows().count());
            return;
        }
        if(this.activeTab=='hub'){
            var state = this.tableHub.rows({selected:true}).count()>0
            var visibility= !state?'attr':'removeAttr';
            $('#buttonDownloadHub')[visibility]('disabled', 'disabled');
            $('#selectAllHub').prop('checked',this.tableHub.rows({selected:true}).count()==this.tableHub.rows().count());
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
         $('#buttonLaunchContainers').hide();
         $('#buttonDelete').hide();
         var counter = parseInt($('#btnLocalImages > span').text());
         $('#btnLocalImages > span').text(counter-1);
    },
    doDownload: function(){
        activeTab = this.activeTab;
        $('#modalDownloadButton').hide();
        toastr.success('Image is being downloaded','Downloading');
        $('.imageDownloadLoader').show();
        if(activeTab=='nightly') {
            this.tableNightly.rows({selected: true}).data().map(function(row){
                $.ajax({
                    url:App.baseAPI+'image/remote',
                    type: 'POST',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        image:row['fingerprint']
                    }),
                    success: $.proxy(this.onDownloadSuccess, this, row['image'])
                });
                this.tableRemote.row('#'+row['image']).remove().draw(false);
            }.bind(this));
        } else if(activeTab=='remote') {
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
        } else if(activeTab=='hub') {
            this.tableHub.rows({selected: true}).data().map(function(row){
                $.ajax({
                    url:App.baseAPI+'image/hub',
                    type: 'POST',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        image:row['fingerprint']
                    }),
                    success: $.proxy(this.onDownloadSuccess, this, row['fingerprint'])
                });
                //this.tableHub.row('#'+row['image']).remove().draw(false);
            }.bind(this));
        }
    },
    onDownloadSuccess: function(imageName, response){
         location.reload();
    },
    getData: function(){
        //this.setLoading(true);
        if(this.activeTab=='local')
            location.reload();
            //return $.get(App.baseAPI+'image', $.proxy(this.getDataSuccess, this));
        if(this.activeTab=='remote')
            return $.get(App.baseAPI+'image/remote', $.proxy(this.getDataSuccess, this));

        if(this.activeTab=='nightly')
            return $.get(App.baseAPI+'image/remote/nightly/list', $.proxy(this.getDataSuccess, this));
    },
    getDataJSON: function(){
        //this.setLoading(true);
        if(this.activeTab=='local')
            return $.get(App.baseAPI+'image', $.proxy(this.getDataSuccess, this));
        if(this.activeTab=='remote')
            return $.get(App.baseAPI+'image/remote', $.proxy(this.getDataSuccess, this));
       if(this.activeTab=='nightly')
            return $.get(App.baseAPI+'image/remote/nightly/list', $.proxy(this.getDataSuccess, this));
       if(this.activeTab=='hub')
            return $.get(App.baseAPI+'image/remote/hub/list', $.proxy(this.getDataSuccess, this));
    },
    activateScreen: function(screen){
        this.tableLocal.rows({selected:true}).deselect();
        this.tableRemote.rows({selected:true}).deselect();
        this.tableNightly.rows({selected:true}).deselect();
        this.tableHub.rows({selected:true}).deselect();
        $('.mg-bottom15').show();
        if(screen==='local'){
            $('#tableImagesLocalWrapper').show();
            $('#tableImagesRemoteWrapper').hide();
            $('#buttonDelete').show();
            $('#buttonLaunchContainers').show();
            $('.local-tab-action-buttons').show();
            $('#buttonJSONRaw').show();
            $('#buttonDownload').hide();
            this.activeTab = 'local';
            return;
        }
        if(screen==='remote'){
            $('#tableImagesLocalWrapper').hide();
            $('#tableImagesRemoteWrapper').show();
            $('#buttonLaunchContainers').hide();
            $('#buttonJSONRaw').hide();
            $('#buttonDownload').show();
            $('#buttonDelete').hide();
            this.activeTab = 'remote';
            this.getData();
            return;
        }
        if(screen==='nightly') {
            this.activeTab = 'nightly';
            this.getData();
            return;
        }
        if(screen==='hub') {
            this.activeTab = 'hub';
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
                { title:'Size', data : 'size',
                    render:function(field){
                        return App.formatBytes(field);
                    }
                }
            ]
        }));
    },
    updateRemoteTable: function(jsonData){
        $('#remoteLength').text(jsonData.length);
        this.remoteData = jsonData;
        this.tableRemote.clear();
        this.tableRemote.destroy();
        this.tableRemote=$('#tableImagesRemote').DataTable(App.mergeProps(this.tableSettings, {
            rowId:'image',
            data : this.remoteData,
            columns : [
                { title:'Select', data: null, defaultContent:''},
                { title: 'OS', data : 'image', render(field, type, full, meta) {
                    return '<a class="pointer"'+
                            'onClick="App.images.showRemoteDetails(\''+field+'\');"'+
                            'data-keyboard="true">'+full.name+'</a>'
                }},
                { title: 'Description', data: null, render(field, type, full, meta) {
                    return '<td>'+full.name+' '+full.distribution+' ' + full.architecture +
                           '</td>'
                }},
                { title: 'Alias', data : 'image' },
                { title: 'Ver', data : 'distribution' },
                { title: 'Arch', data : 'architecture' }
            ]
        }));
        this.tableRemote.search(architecture).draw();
    },
    updateNightlyTable: function(jsonData){
        $('#nightlyLength').text(jsonData.length);
        this.nightlyData = jsonData;
        this.tableNightly.clear();
        this.tableNightly.destroy();
        this.tableNightly=$('#tableImagesNightly').DataTable(App.mergeProps(this.tableSettings, {
            rowId:'fingerprint',
            data : this.nightlyData,
            columns : [
                { title:'Select', data: null, defaultContent:''},
                { title: 'OS', data : null, render(field, type, full, meta) {
                    if(full.metadata.properties['description'] === undefined) {
                        return '<a class="pointer"'+
                            'onClick="App.images.showRemoteDetails(\''+full.metadata.image+'\');"'+
                            'data-keyboard="true">'+full.metadata.name+'</a>'
                    }
                    else {
                        return '<a class="pointer"'+
                               'onClick="App.images.showNightlyDetails(\''+full.metadata.properties['os']+'/'+full.metadata.properties['release']+'/'+full.metadata.properties['architecture']+'\', \''+full.metadata.fingerprint+'\');">'+full.metadata.properties['os']+'</a>';
                    }

                }},
                { title: 'Description', data: null, render(field, type, full, meta) {
                    if(full.metadata.properties['description'] === undefined) {
                        return full.metadata.aliases[0].description;
                    }
                    else {
                        return full.metadata.properties.description;
                    }
                }},
                { title: 'Alias', data : null, render(field, type, full, meta) {
                    if(full.metadata.properties['description'] === undefined) {
                        return full.metadata.aliases[0]['description'];
                    }
                    else {
                        var aliases = '';
                        for (i=0; i<full.metadata.aliases.length; i++) {
                            aliases+= '<li>'+full.metadata.aliases[i]['name']+'</li>'
                        }

                        return aliases;
                    }
                } },
                { title: 'Ver', data : null, render(field, type, full, meta) {
                    return full.metadata.properties['release'];
                } },
                { title: 'Arch', data : null, render(field, type, full, meta) {
                    return full.metadata.properties['architecture'];
                } },
                { title: 'Size', data: null, render(field, type, full, meta) {
                    return '<span class="imageSize">'+full.metadata.size+'</span>';
                }}
            ]
        }));
        this.tableNightly.search(architecture).draw();
        $('#tableImagesNightly .imageSize').each(this.convertImageSize);
    },
    getDataSuccess: function(response){
        this.setLoading(false);
        this.rawJson.setValue(JSON.stringify(response.data, null , '\t'));
//        if(this.activeTab=='local'){
//            this.updateLocalTable(response.data);
//        }
        if(this.activeTab == 'remote'){
            this.updateRemoteTable(response.data);
        }
        if (this.activeTab == 'nightly') {
            this.updateNightlyTable(response.data);
        }
    },
    showJSON: function(e) {
        this.rawJson.setValue('');
        $('.modal-title').text('');
        $('.modal-title').text('RAW JSON for Images');
        $('.modal-title').append(' <span class="glyphicon glyphicon-refresh spinning loader">');
        $("#jsonModal").modal("show");

        this.getDataJSON();

    },
    getRemoteData: function(){
        $.get(App.baseAPI+'image/remote', $.proxy(this.getDataSuccess, this));
    },
    generateContainerFormSection: function(image, pos){
        var tempSection = this.containerTemplate.clone();
        tempSection.prop('id',image.fingerprint);
        tempSection.find('input[name="name"]').prop('name', 'containers['+pos+'][name]');
        //Handle exported containers
        if (image.properties.os !== undefined)
            tempSection.find('input[name="containers['+pos+'][name]"]').val(App.properties.left[Math.floor((Math.random() * 93) + 1)] + '-' + App.properties.right[Math.floor((Math.random() * 160) + 1)] + '-');
        else
            tempSection.find('input[name="containers['+pos+'][name]"]').val(App.properties.left[Math.floor((Math.random() * 93) + 1)] + '-' + App.properties.right[Math.floor((Math.random() * 160) + 1)] + '-');

        tempSection.find('input[name="image"]').prop('name', 'containers['+pos+'][image]');
        tempSection.find('input[name="containers['+pos+'][image]"]').val(image.fingerprint);

        tempSection.find('input[name="count"]').prop('name', 'containers['+pos+'][count]');
        tempSection.find('input[name="containers['+pos+'][count]"]').on('change', $.proxy(this.onCountChange, this, $(tempSection.find('.nodeCount'))));

        tempSection.find('input[name="cpu[percentage]"]').prop('name', 'containers['+pos+'][cpu[percentage]]');
        tempSection.find('#cpu_percentage').prop('id', 'cpu_percentage_'+pos);
        tempSection.find('#cpu_percentage_'+pos).on('change',$.proxy(this.updateFieldValue, this,tempSection.find('input[name="containers['+pos+'][cpu[percentage]]"]')));
        tempSection.find('input[name="containers['+pos+'][cpu[percentage]]"]').on('change',$.proxy(this.updateFieldValue, this,tempSection.find('#cpu_percentage_'+pos)));

        tempSection.find('input[name="cpu[hardLimitation]"]').prop('name', 'containers['+pos+'][cpu[hardLimitation]]');

        tempSection.find('input[name="memory[sizeInMB]"]').prop('name', 'containers['+pos+'][memory[sizeInMB]]');
        tempSection.find('#memory_percentage').prop('id', 'memory_percentage_'+pos);
        tempSection.find('#memory_percentage_'+pos).on('change',$.proxy(this.updateFieldValue, this,tempSection.find('input[name="containers['+pos+'][memory[sizeInMB]]"]')));
        tempSection.find('input[name="containers['+pos+'][memory[sizeInMB]]"]').on('change',$.proxy(this.updateFieldValue, this,tempSection.find('#memory_percentage_'+pos)));
        tempSection.find('input[name="memory[hardLimitation]"]').prop('name', 'containers['+pos+'][memory[hardLimitation]]');

        tempSection.find('input[name="autostart"]').prop('name', 'containers['+pos+'][autostart]');
        tempSection.find('input[name="stateful"]').prop('name', 'containers['+pos+'][stateful]');

        tempSection.find('select[name="profiles"]').prop('name', 'containers['+pos+'][profiles]');
        tempSection.find('select[name="containers['+pos+'][profiles]"]').addClass('selectpicker');
        tempSection.find('select[name="containers['+pos+'][profiles]"]').prop('id', image.fingerprint+'_profiles');

        tempSection.find('.imageName').text(image.properties.description);

        tempSection.find('#accordion').prop('id', 'accordion_'+pos);
        tempSection.find('#accordion_link').prop('id', 'accordion_link_'+pos);
        tempSection.find('#accordion_link_'+pos).prop('data-parent', '#accordion_'+pos);
        tempSection.find('#accordion_link_'+pos).prop('href', '#collapse_'+pos);

        tempSection.find('#advancedSettingsMultipleContainer').prop('id', 'advancedSettingsMultipleContainer_'+image.fingerprint);

        tempSection.find('#collapse').prop('id', 'collapse_'+pos);

        tempSection.show();
        return tempSection;
    },
    onCountChange: function(countNode, event){
        $(countNode).text($(event.target).val() +' Nodes');
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
        //initialize profile pickers
        $('.selectpicker').selectpicker();
        this.switchView('form');
        $('.image-tabs').addClass('hidden');
    },
    switchView: function(view){
        $('#createMultipleContainersForm')[view=='form'?'show':'hide']();
        $('#tableImagesLocalWrapper')[view=='localList'?'show':'hide']();
        $('#tableImagesRemoteWrapper')[view=='remoteList'?'show':'hide']();
        if(view!=='form'){
            $('.image-tabs').removeClass('hidden');
            $('#multiContainerSection').empty();
        }else{
            $('.mg-bottom15').hide();
        }
        if(view=='remoteList'){
            return this.activateScreen('remote');
        }
        if(view=='localList'){
            return this.activateScreen('local');
        }
        if(view=='nightlyList'){
            return this.activateScreen('nightly');
        }
        if (view=='hubList') {
            return this.activateScreen('hub');
        }
        $('#buttonLaunchContainers').hide();
        $('#buttonDelete').hide();
        $('#rawJSONImages').hide();
        $('.local-tab-action-buttons').hide();

        $('#containerNameImages').val(App.properties.left[Math.floor((Math.random() * 93) + 1)] + '-' + App.properties.right[Math.floor((Math.random() * 160) + 1)] + '-');
    },
    generateContainer: function(name, formData){
        return {
            ...formData,
            name:name
        }
    },
    generateImageContainers: function(formData){
        var imageContainers = [];
        var tempData = this.cleanupFormData($.extend({}, true,formData));
        for(var i=0;i<=Number(formData.count)-1;i++){
            if (tempData.name == '') {
                imageContainers.push(this.generateContainer(App.properties.left[Math.floor((Math.random() * 93) + 1)] + '-' + App.properties.right[Math.floor((Math.random() * 160) + 1)], tempData));
            }
            else {
                imageContainers.push(this.generateContainer(tempData.name+(i+1),tempData));
            }
        }
        return imageContainers;
    },
    cleanupFormData(specs){
        delete specs['count'];
        specs['cpu']['percentage']=Number(specs['cpu']['percentage']);
        specs['cpu']['hardLimitation']=Boolean(specs['cpu']['hardLimitation']) || false;
        specs['memory']['sizeInMB']=Number(specs['memory']['sizeInMB']);
        specs['memory']['hardLimitation']=Boolean(specs['memory']['hardLimitation']) || false;
        specs['stateful']=Boolean(specs['stateful']);
        specs['autostart']=Boolean(specs['autostart']);
        if($('#'+specs.image+'_profiles').val()){
            specs['profiles'] = $('#'+specs.image+'_profiles').val();
        }

        specs['config'] = this.readKeyValuePairs('#advancedSettingsMultipleContainer_'+specs.image);
        return specs;
    },
    generateRequest: function(inputJSON){
        var tempRequest = [];
        var containerArray = $.map(inputJSON.containers, function(val, ind){ return [val]; });
        for(var i=containerArray.length-1, container; container=containerArray[i];i--){
            var tempData = this.generateImageContainers(container);
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
    },
    readKeyValuePairs: function(selector) {
        keyValues = {}
        $(selector).find('input:enabled').each(function() {
            keyValues[this.name] = this.value;
        })

        return keyValues;
    },
    launchContainer:function(fingerprint){
        this.tableLocal.row('#'+fingerprint).select();
        this.launchContainers();
    },
    toggleSelectAll:function(name, event){
        if(event.target.checked){
            this['table'+name].rows().select();
        }else{
            this['table'+name].rows().deselect();
        }
    },
    updateFieldValue: function(target, event){
        target.val(event.target.value);
    },
    showRemoteDetails: function(image){
        this.tableRemote.rows().deselect();
        this.tableRemote.rows('#'+image).select();
        $.get(App.baseAPI+'image/remote/details?alias='+image, $.proxy(this.onGetRemoteDetailsSuccess, this));
    },
    showNightlyDetails: function(image, fingerprint) {
        this.tableNightly.rows().deselect();
        this.tableNightly.rows('#'+fingerprint).select();
        $.get(App.baseAPI+'image/remote/details?alias='+image, $.proxy(this.onGetRemoteDetailsSuccess, this));
    },
    onGetRemoteDetailsSuccess: function(response){
        this.generateModalDetails(response);
    },
    generateItem:function(key, value){
        return '<div class="form-group"><label class="control-label col-sm-3">'+key+'</label><p class="col-sm-9" title="'+value+'">'+value+'</p></div>';
    },
    generateModalDetails: function(response) {
      var tempData = response.data;
      var modalBody = $('#modalBody');
      modalBody.empty();

      $('.imageName').text(tempData.properties.name);
      // Architecture
      modalBody.append(this.generateItem('Os', tempData.properties.os));
      modalBody.append(this.generateItem('Distribution', tempData.properties.distribution));
      modalBody.append(this.generateItem('Release', tempData.properties.release));
      modalBody.append(this.generateItem('Architecture', (tempData.architecture + '(' + tempData.properties.architecture + ')')));
      modalBody.append(this.generateItem('Size', App.formatBytes(tempData.size)));

      modalBody.append('<div class="form-group col-lg-12"><hr style="border:1px solid lightgrey;"/></div>');

      modalBody.append(this.generateItem('Fingerprint', tempData.fingerprint));
      modalBody.append(this.generateItem('Filename', tempData.filename));
      modalBody.append(this.generateItem('Created at', tempData.created_at));
      modalBody.append(this.generateItem('Uploaded at', tempData.uploaded_at));
      modalBody.append(this.generateItem('Expires at', tempData.expires_at));
      modalBody.append(this.generateItem('Aliases', tempData.properties.build));
      modalBody.append(this.generateItem('Build', tempData.properties.build));
      modalBody.append(this.generateItem('Description', tempData.properties.description));
      modalBody.append(this.generateItem('Build', tempData.properties.build));
      modalBody.append(this.generateItem('Serial', tempData.properties.serial));
      modalBody.append(this.generateItem('Public', tempData.public));

      modalBody.append('<div class="form-group col-lg-12"><hr style="border:1px solid lightgrey;"/></div>');
      modalBody.append('<div class="form-group"><a data-toggle="collapse" class="collapse-acc" data-parent="#aliases" href="#aliasesList">Aliases</a></div>');
      modalBody.append('<div id="aliasesList" class="form-group panel-collapse collapse"></div>');

      var aliasesList = $('#aliasesList');
      tempData.aliases.forEach(function(alias, index){
           aliasesList.append('<div id="aliases" class="form-group"><b>Alias '+(index+1)+'</b></div>')
           aliasesList.append(this.generateItem('Description',alias.description));
           aliasesList.append(this.generateItem('Name',alias.name));
           aliasesList.append(this.generateItem('Target',alias.target));
      }.bind(this));
      modalBody.append(aliasesList);
      $('#myModal').modal().show();

    },
    publishImage: function(e) {
        $("#publishImageModal").modal("show");
        var image = this.getImageByFingerPrint(this.data, this.tableLocal.rows({selected:true}).data()[0]['fingerprint']);

        $('#lxcVersion').text(App.lxdVersion);
        $('#fingerprint').text(image.fingerprint);
        $('#source').text('NA');
        $('#size').text(App.formatBytes(image.size));
        $('#architecture').text(image.architecture);
        $('#os').text(image.properties['os']);
        $('#release').text(image.properties['release']);
        this.publishPage=0;
        this.updatePublishButtons();
    },
    doPublishImage: function(e){
        e.preventDefault();
        if(!$("#publishImageToHubForm").parsley().validate()){
//        if(!this.publishFormValid){
            return false;
        }
        var image = this.getImageByFingerPrint(this.data, this.tableLocal.rows({selected:true}).data()[0]['fingerprint']);

        var logoImg = $('input[name="logo"]').get(0).files[0];

        var tempJSON = this.publishImageForm.serializeJSON();

        var formData = new FormData();
        formData.append('logo', logoImg);

        tempJSON['fingerprint'] = image.fingerprint;
        tempJSON['documentation'] = this.simplemde.value();

        formData.append('input', JSON.stringify(tempJSON));

        console.log('formData', formData);

        $.ajax({
            url: App.baseAPI +'image/hub/publish',
            type:'POST',
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            data: formData,
            success: $.proxy(this.onPublishSuccess, this),
            error: $.proxy(this.onPublishFailed, this)
        });
    },
    onPublishSuccess: function(response){
//        location.reload();
    },
    onPublishFailed: function(response) {
        console.log('failed');
    },
    updatePublishButtons: function(){
        $('.tabImageDetails, .tabImageReadme, .tabImageAuthorization').removeClass('active');
        switch(this.publishPage){
            case 0:
                $('#buttonPublishCancel').show();
                $('#buttonPublishNext').show();
                $('#buttonPublishBack').hide();
                $('#buttonPublishToHUB').hide();
                $('.tabImageDetails').addClass('active');
                $('#5').show();
                $('#6, #7').hide();
                return;
            case 1:
                $('#buttonPublishCancel').hide();
                $('#buttonPublishToHUB').hide();
                $('#buttonPublishBack').show();
                $('#buttonPublishNext').show();
                $('.tabImageReadme').addClass('active');
                $('#6').show();
                $('#5, #7').hide();
                return;
            case 2:
                $('#buttonPublishCancel').hide();
                $('#buttonPublishNext').hide();
                $('#buttonPublishBack').show();
                $('#buttonPublishToHUB').show();
                $('.tabImageAuthorization').addClass('active');
                $('#7').show();
                $('#6, #5').hide();
                return;
        }
    },
    onPublishBack: function(){
        this.publishPage--;
        this.updatePublishButtons();
    },
    onPublishNext: function(){
        console.log('here');
        this.publishPage++;
        this.updatePublishButtons();
    },
    onPublishSwitchToPage:function(pageNumber){
        this.publishPage=pageNumber;
        this.updatePublishButtons();
    },
    onPublishFormValidation: function(formInstance){
        if(!formInstance.isValid({group: 'block1'})){
            formInstance.valiidationResult = false;
            return this.onPublishSwitchToPage(0);
        }
        if(!formInstance.isValid({group: 'block2'})){
            formInstance.valiidationResult = false;
            return this.onPublishSwitchToPage(1);
        }
        if(!formInstance.isValid({group: 'block3'})){
            formInstance.valiidationResult = false;
            return this.onPublishSwitchToPage(2);
        }
    }
}