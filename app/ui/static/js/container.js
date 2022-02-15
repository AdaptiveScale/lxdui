App.containers = App.containers || {
    data:[],
    error:false,
    errorMessage:'',
    loading:false,
    selectedContainers: [],
    selectedContainer: null,
    dataTable:null,
    initiated:false,
    tableSettings: {
        rowId:'name',
        searching:true,
        responsive: false,
        select: true,
        dom: "<'tbl-header'<'row'<'col-sm-4 text-left'f><'col-sm-2 refresh-list-place'><'col-sm-6 json-place'>>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-4'i><'col-sm-2 text-right'l><'col-sm-6 text-right'p>>",
        "oLanguage": {
          "sLengthMenu": "List _MENU_ ",
        },
        buttons: [
            {
                text: 'JSON',
                action: function ( e, dt, node, config ) {
                    dt.button().add( 1, {
                        text: 'Button '+(counter++),
                        action: function () {
                            this.remove();
                        }
                    } );
                }
            }
        ],
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
        initComplete: function(settings, json) {
            var tempButtonJson = $('.rawJSONContainers').clone();
            var tempButtonRefresh = $('#refreshContainers').clone();
            tempButtonRefresh.removeClass('.refreshContainers');
            tempButtonJson.removeClass('rawJSONContainers');
            tempButtonJson.on('click', $.proxy(App.containers.showJSON, App.containers));
            tempButtonRefresh.on('click', $.proxy(App.containers.refreshContainers));
            $('.json-place').append(tempButtonJson);
            $('.refresh-list-place').append(tempButtonRefresh);
            tempButtonJson.show();
            tempButtonRefresh.show();
        },
    },
    newContainerForm:null,
    rawJson:null,
    init: function(){
        console.log('Containers init');
        this.dataTable = $('#tableContainers').DataTable(this.tableSettings);
        this.rawJson = ace.edit('rawJson');
        this.rawJson.session.setMode('ace/mode/json');
        this.rawJson.setOptions({readOnly: true});
        $('#refreshContainers').on('click', $.proxy(this.refreshContainers, this));
        $('#buttonStart').on('click', $.proxy(this.startContainer, this));
        $('#buttonStop').on('click', $.proxy(this.stopContainer, this));
        $('#buttonRestart').on('click', $.proxy(this.restartContainer, this));
        $('#buttonFreeze').on('click', $.proxy(this.freezeContainer, this));
        $('#buttonUnfreeze').on('click', $.proxy(this.unfreezeContainer, this));
        $('#buttonDelete').on('click', $.proxy(this.deleteContainer, this));
        $('#buttonNewInstance').on('click', $.proxy(this.switchView, this, 'form'));
        $('#buttonBack').on('click', $.proxy(this.switchView, this, 'list'));
        App.setActiveLink('container');

        $('#buttonCloneContainer').on('click', $.proxy(this.cloneContainer, this));
        $('#cloneForm').on('submit', $.proxy(this.cloneContainer, this));

        $('#buttonMoveContainer').on('click', $.proxy(this.moveContainer, this));
        $('#moveForm').on('submit', $.proxy(this.moveContainer, this));

        $('#buttonExportContainer').on('click', $.proxy(this.exportContainer, this));
        $('#exportForm').on('submit', $.proxy(this.exportContainer, this));

        $('#buttonSnapshotContainer').on('click', $.proxy(this.snapshotContainer, this));
        $('#snapshotForm').on('submit', $.proxy(this.snapshotContainer, this));

        this.dataTable.on('select', $.proxy(this.onRowSelected, this));
        this.dataTable.on('deselect', $.proxy(this.onRowSelected, this));
        //this.getData();
        this.newContainerForm = $('#newContainerForm');
        this.newContainerForm.on('submit', $.proxy(this.doCreateContainer, this));
        $('#selectAllContainers').on('change', $.proxy(this.toggleSelectAll, this));
        $('#cpu_percentage').on('change', $.proxy(this.updateValue, this, $('#containerCPUPercentage')));
        $('#containerCPUPercentage').on('change', $.proxy(this.updateValue, this, $('#cpu_percentage')));
        $('#memory_percentage').on('change', $.proxy(this.updateValue, this, $('#containerMemoryPercentage')));
        $('#containerMemoryPercentage').on('change', $.proxy(this.updateValue, this, $('#memory_percentage')));
        if(window.location.hash && window.location.hash=='#createContainer')
            this.switchView('form');

        this.initKeyValuePairs();
    },
    refreshContainers: function(e){
        console.log('refreshContainers');
        location.reload();
        //e.preventDefault();
        //this.getData();
    },
    setLoading: function(state){
        this.loading=true;
    },
    initKeyValuePairs: function() {
        for (key in App.properties.keyValues) {
            $('#advancedSettingsContainer').append('<div class="row">' +
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
    getData: function(){
        this.setLoading(true);
        $.get(App.baseAPI+'container', $.proxy(this.getDataSuccess2, this));
    },
    getDataSuccess2: function(response) {
        this.rawJson.setValue(JSON.stringify(response.data, null , '\t'));
    },
    getDataSuccess: function(response){
        this.setLoading(false);
        this.data = response.data;
        this.rawJson.setValue(JSON.stringify(response.data, null , '\t'));
        if(!this.initiated)
            return this.initiated = true;

        this.dataTable.clear();
        this.dataTable.destroy();
        this.dataTable=$('#tableContainers').DataTable(App.mergeProps(this.tableSettings, {
            data:this.data,
            columns : [
                { title:'#', data: null, defaultContent:''},
                { title:'Name', data : 'name'},
                { title:'Status', data : 'status' },
                { title:'IP Address', data : 'network',
                    render: function(field) {
                        if (!field || field['eth0']['addresses'].length === 0) return 'N/A';
                        return field['eth0']['addresses'][0]['address'];
                    }
                },
                { title:'OS Image', data : 'config',
                    render:function(field){
                        return field['image.distribution'] + ' ' + field['image.release'] + ' ' + field['image.architecture'];
                    }
                },
                { title:'Create at', data : 'created_at' },
                { title:'Actions', data : 'name',
                    render: function(field) {
                        return '<a><i id="cloneContainer" data-keyboard="true" onClick="$.proxy(App.containers.showCloneContainer('+field+'));" title="Clone Container" class="glyphicon glyphicon-duplicate btn btn-sm btn-default"></i></a>';
                    }
                },
            ]
        }));
    },
    showJSON: function(e) {
        this.rawJson.setValue('');
        $('.modal-title').text('');
        $('.modal-title').text('RAW JSON for Containers');
        $('.modal-title').append(' <span class="glyphicon glyphicon-refresh spinning loader">');
        $("#jsonModal").modal("show");

        this.getData();

    },
    onRowSelected: function(e, dt, type, indexes ){
        var state = this.dataTable.rows({selected:true}).count()>0;
        $('#selectAllContainers').prop('checked',state);
        var action = state?'removeAttr':'attr';
        $('#buttonStart')[action]('disabled', 'disabled');
        $('#buttonStop')[action]('disabled', 'disabled');
        $('#buttonRestart')[action]('disabled', 'disabled');
        $('#buttonDelete')[action]('disabled', 'disabled');
        $('#buttonFreeze')[action]('disabled', 'disabled');
        $('#buttonUnfreeze')[action]('disabled', 'disabled');
    },
    startContainer: function(){
        this.dataTable.rows( { selected: true } ).data().map(function(row){
            $.ajax({
                url: App.baseAPI+'container/start/' + row['name'],
                type: 'PUT',
                success: $.proxy(this.onStartSuccess, this, row['name'])
            });
        }.bind(this));
    },
    onStartSuccess: function(name){
        console.log('onStartSuccess', name);
        location.reload();
        //this.getData();
    },
    stopContainer: function() {
        this.dataTable.rows( { selected: true } ).data().map(function(row){
            $.ajax({
                url: App.baseAPI+'container/stop/' + row['name'],
                type: 'PUT',
                success: $.proxy(this.onStopSuccess, this, row['name'])
            });
        }.bind(this));
    },
    onStopSuccess: function(name){
        console.log('onStopSuccess', name);
        location.reload();
        //this.getData();
    },
    restartContainer: function() {
        this.dataTable.rows( { selected: true } ).data().map(function(row){
            $.ajax({
                url: App.baseAPI+'container/restart/' + row['name'],
                type: 'PUT',
                success: $.proxy(this.onRestartSuccess, this, row['name'])
            });
        }.bind(this));
    },
    freezeContainer: function() {
        this.dataTable.rows( { selected: true } ).data().map(function(row){
            $.ajax({
                url: App.baseAPI+'container/freeze/' + row['name'],
                type: 'PUT',
                success: $.proxy(this.onRestartSuccess, this, row['name'])
            });
        }.bind(this));
    },
    unfreezeContainer: function() {
        this.dataTable.rows( { selected: true } ).data().map(function(row){
            $.ajax({
                url: App.baseAPI+'container/unfreeze/' + row['name'],
                type: 'PUT',
                success: $.proxy(this.onRestartSuccess, this, row['name'])
            });
        }.bind(this));
    },
    onRestartSuccess: function(name){
        console.log('onRestartSuccess', name);
        location.reload();
        //this.getData();
    },
    deleteContainer: function() {
        this.dataTable.rows( { selected: true } ).data().map(function(row){
            $.ajax({
                url: App.baseAPI+'container/' + row['name'],
                type: 'DELETE',
                data:JSON.stringify({force:true}),
                success: $.proxy(this.onDeleteSuccess, this, row['name'])
            });
        }.bind(this));
    },
    onDeleteSuccess: function(name){
        this.dataTable.row("#"+name).remove().draw();
    },
    switchView: function(view){
        $('#cloneContainerForm').hide();
        $('#moveContainerForm').hide();
        $('#snapshotContainerForm').hide();
        $('#exportContainerForm').hide();
        $('#snapshotList').hide();

        $('#createContainerForm')[view=='form'?'show':'hide']();
        $('#containers')[view=='list'?'show':'hide']();
        $('#containerName').val(App.properties.left[Math.floor((Math.random() * 93) + 1)] + '-' + App.properties.right[Math.floor((Math.random() * 160) + 1)]);
    },
    generateRequest: function(formData){
        return {
            name: formData.name,
            image: formData.image,
            autostart: formData['autostart']?true:false,
            stateful: formData['stateful']?true:false,
            cpu:{
                percentage: Number(formData.cpu.percentage),
                hardLimitation: formData.cpu['hardLimitation']?true:false,
                cores: Number(formData.cpu.cores),
            },
            memory:{
                sizeInMB: Number(formData.memory.sizeInMB),
                hardLimitation: formData.memory['hardLimitation']?true:false
            },
            devices:{
                root:{
                    path: '/',
                    pool: formData.storagePool['name'],
                    size: formData.storagePool['size']+'GB',
                    type: 'disk',
                }
            },
            profiles:formData.profiles
        };
    },
    doCreateContainer: function(e){
        e.preventDefault();
        //Workaround for multiselect input
        var jsonForm = this.newContainerForm.serializeJSON();
        if($('#containerProfiles').val())
            jsonForm['profiles'] = $('#containerProfiles').val()

        var tempJSON = this.generateRequest(jsonForm);
        if (tempJSON['name'] == '') {
            tempJSON['name'] = App.properties.left[Math.floor((Math.random() * 93) + 1)] + '-' + App.properties.right[Math.floor((Math.random() * 160) + 1)];
        }
        tempJSON['config'] = this.readKeyValuePairs();
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
        this.switchView('list');
        this.newContainerForm.trigger('reset');
        this.refreshContainers();
    },
    onCreateFailed: function(response){
        console.log('createContainerFailed', response);
    },
    readKeyValuePairs: function() {
        keyValues = {}
        $('#advancedSettingsContainer').find('input:enabled').each(function() {
            keyValues[this.name] = this.value;
        })

        return keyValues;
    },
    showCloneContainer: function(name) {
        $('#cloneContainerModal .modal-title').text('');
        $('#newContainerClone').val('');
        $('#cloneContainerModal .modal-title').text('Clone Container: ' + name);
        $("#cloneContainerModal").modal("show");
        this.selectedContainer = name;
    },
    showMoveContainer: function(name) {
        $('#moveContainerModal .modal-title').text('');
        $('#moveContainerModal .modal-title').text('Move Container: ' + name);
        $('#newContainerMove').val('');
        $("#moveContainerModal").modal("show");
        this.selectedContainer = name;
    },
    showExportContainer: function(name) {
        $('#exportContainerModal .modal-title').text('');
        $('#exportContainerModal .modal-title').text('Export Image from Container: ' + name);
        $('#imageAlias').val('');
        $("#exportContainerModal").modal("show");
        this.selectedContainer = name;
    },
    showSnapshotContainer: function(name) {
        $('#snapshotContainerModal .modal-title').text('');
        $('#snapshotContainerModal .modal-title').text('Create Snapshot from Container: ' + name);
        $('#snapshotName').val('');
        $("#snapshotContainerModal").modal("show");
        this.selectedContainer = name;
    },
    showSnapshotList: function(name) {
        $('#selectedSnapshotList').text('List of Snapshots for Container: ' + name);
        if ($('#snapshotList').is(':visible') && this.selectedContainer === name) {
            $('#snapshotList').hide();
        }
        else {
            $('#snapshotList').show();
        }
        this.selectedContainer = name;
        this.getSnapshotList(name);
    },
    getSnapshotList: function(name){
        this.setLoading(true);
        $.get(App.baseAPI+'snapshot/container/'+name, $.proxy(this.getSnapshotSuccess, this));
    },
    getSnapshotSuccess: function (response){
        $('#snapshotList li').remove();
        $('#snapshotList br').remove();
        $.each(response.data, function(index, value) {
            $('#snapshotList').append('<li>'+value+'</li>');
        });
        $('#snapshotList').append('<br><br>');

    },
    cloneContainer: function() {
        $.ajax({
            url:App.baseAPI+'container/clone/'+this.selectedContainer,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                newContainer: $('#newContainerClone').val()
            }),
            success: $.proxy(this.onCloneSuccess, this)
        });
    },
    onCloneSuccess: function(response){
         console.log(response);
         console.log('clonedSuccess:', 'TODO - add alert and refresh local data');
         $("#cloneContainerModal").modal("hide");
         location.reload();
    },
    moveContainer: function() {
        $.ajax({
            url:App.baseAPI+'container/move/'+this.selectedContainer,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                newContainer: $('#newContainerMove').val()
            }),
            success: $.proxy(this.onMoveSuccess, this)
        });
    },
    onMoveSuccess: function(response){
         console.log(response);
         console.log('Moved Success:', 'TODO - add alert and refresh local data');
         $("#moveContainerModal").modal("hide");
         location.reload();
    },
    exportContainer: function() {
        $.ajax({
            url:App.baseAPI+'container/export/'+this.selectedContainer,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                imageAlias: $('#imageAlias').val(),
                force: true
            }),
            success: $.proxy(this.onExportSuccess, this)
        });
    },
    onExportSuccess: function(response){
         console.log(response);
         console.log('Export Success:', 'TODO - add alert and refresh local data');
         $("#exportContainerModal").modal("hide");
    },
    snapshotContainer: function() {
        $.ajax({
            url:App.baseAPI+'snapshot/' + $('#snapshotName').val() + '/container/'+this.selectedContainer,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                stateful: $('#snapshotStateful2').is(':checked'),
            }),
            success: $.proxy(this.onSnapshotSuccess, this)
        });
    },
    onSnapshotSuccess: function(response){
         console.log(response);
         console.log('Snapshot Success:', 'TODO - add alert and refresh local data');
         $("#snapshotContainerModal").modal("hide");
    },
    toggleSelectAll(event){
        if(event.target.checked){
            this.dataTable.rows().select();
        }else{
            this.dataTable.rows().deselect();
        }
    },
    updateValue:function(target, event){
        target.val(event.target.value);
    },
    showTerminalContainer: function(container) {
        window.open('/terminal/new/' + container + '/', '_blank');
    }
}
