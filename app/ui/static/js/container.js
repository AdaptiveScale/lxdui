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
    newContainerForm:null,
    init: function(){
        console.log('Containers init');
        this.dataTable = $('#tableContainers').DataTable(this.tableSettings);
        $('#refreshContainers').on('click', $.proxy(this.refreshContainers, this));
        $('#buttonStart').on('click', $.proxy(this.startContainer, this));
        $('#buttonStop').on('click', $.proxy(this.stopContainer, this));
        $('#buttonRestart').on('click', $.proxy(this.restartContainer, this));
        $('#buttonDelete').on('click', $.proxy(this.deleteContainer, this));
        $('#buttonNewInstance').on('click', $.proxy(this.switchView, this, 'form'));
        $('#buttonBack').on('click', $.proxy(this.switchView, this, 'list'));
        App.setActiveLink('container');

        $('#buttonCloneContainer').on('click', $.proxy(this.cloneContainer, this));
        $('#buttonMoveContainer').on('click', $.proxy(this.moveContainer, this));
        $('#buttonExportContainer').on('click', $.proxy(this.exportContainer, this));
        $('#buttonSnapshotContainer').on('click', $.proxy(this.snapshotContainer, this));
        this.dataTable.on('select', $.proxy(this.onRowSelected, this));
        this.dataTable.on('deselect', $.proxy(this.onRowSelected, this));
        this.getData();
        this.newContainerForm = $('#newContainerForm');
        this.newContainerForm.on('submit', $.proxy(this.doCreateContainer, this));
        if(window.location.hash && window.location.hash=='#createContainer')
            this.switchView('form')
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
    getData: function(){
        this.setLoading(true);
        $.get(App.baseAPI+'container', $.proxy(this.getDataSuccess, this));
    },
    getDataSuccess: function(response){
        this.setLoading(false);
        this.data = response.data;
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
                        return '<a><i id="cloneContainer" onClick="$.proxy(App.containers.showCloneContainer('+field+'));" title="Clone Container" class="glyphicon glyphicon-duplicate btn btn-sm btn-default"></i></a>';
                    }
                },
            ]
        }));
    },
    onRowSelected: function(e, dt, type, indexes ){
        var state = this.dataTable.rows({selected:true}).count()>0?'visible':'hidden';
        $('#buttonStart').css('visibility',state);
        $('#buttonStop').css('visibility',state);
        $('#buttonRestart').css('visibility',state);
        $('#buttonDelete').css('visibility',state);
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
    onRestartSuccess: function(name){
        console.log('onRestartSuccess', name);
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
        $('#createContainerForm')[view=='form'?'show':'hide']();
        $('#containers')[view=='list'?'show':'hide']();
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
            },
            memory:{
                sizeInMB: Number(formData.memory.sizeInMB),
                hardLimitation: formData.memory['hardLimitation']?true:false
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
        this.getData();
    },
    onCreateFailed: function(response){
        console.log('createContainerFailed', response);
    },
    showCloneContainer: function(name) {
        $('#selectedClone').text('Clone Container: ' + name);
        this.selectedContainer = name;
        if ($('#cloneContainerForm').is(':visible')) {
            $('#cloneContainerForm').hide();
        }
        else {
            $('#cloneContainerForm').show();
        }
        $('#moveContainerForm').hide();
        $('#snapshotContainerForm').hide();
        $('#exportContainerForm').hide();
        $('#snapshotList').hide();
    },
    showMoveContainer: function(name) {
        $('#selectedMove').text('Move Container: ' + name);
        this.selectedContainer = name;
        $('#cloneContainerForm').hide();
        if ($('#moveContainerForm').is(':visible')) {
            $('#moveContainerForm').hide();
        }
        else {
            $('#moveContainerForm').show();
        }
        $('#snapshotContainerForm').hide();
        $('#exportContainerForm').hide();
        $('#snapshotList').hide();
    },
    showExportContainer: function(name) {
        $('#selectedExport').text('Export Image from Container: ' + name);
        this.selectedContainer = name;
        $('#cloneContainerForm').hide();
        $('#moveContainerForm').hide();
        $('#snapshotContainerForm').hide();
        if ($('#exportContainerForm').is(':visible')) {
            $('#exportContainerForm').hide();
        }
        else {
            $('#exportContainerForm').show();
        }
        $('#snapshotList').hide();
    },
    showSnapshotContainer: function(name) {
        $('#selectedSnapshot').text('Create Snapshot from Container: ' + name);
        this.selectedContainer = name;
        $('#cloneContainerForm').hide();
        $('#moveContainerForm').hide();
        if ($('#snapshotContainerForm').is(':visible')) {
            $('#snapshotContainerForm').hide();
        }
        else {
            $('#snapshotContainerForm').show();
        }
        $('#exportContainerForm').hide();
        $('#snapshotList').hide();
    },
    showSnapshotList: function(name) {
        $('#selectedSnapshotList').text('List of Snapshots for Container: ' + name);
        this.selectedContainer = name;
        if ($('#snapshotList').is(':visible')) {
            $('#snapshotList').hide();
        }
        else {
            $('#snapshotList').show();
        }
        $('#cloneContainerForm').hide();
        $('#moveContainerForm').hide();
        $('#snapshotContainerForm').hide();
        $('#exportContainerForm').hide();
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
    },
    snapshotContainer: function() {
        $.ajax({
            url:App.baseAPI+'snapshot/' + $('#snapshotName').val() + '/container/'+this.selectedContainer,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            success: $.proxy(this.onSnapshotSuccess, this)
        });
    },
    onSnapshotSuccess: function(response){
         console.log(response);
         console.log('Snapshot Success:', 'TODO - add alert and refresh local data');
    },
}