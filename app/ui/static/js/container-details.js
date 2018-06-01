App.containerDetails = App.containerDetails || {
    data:[],
    updates:{
        image:''
    },
    error:false,
    errorMessage:'',
    name: '',
    activeSnapshot: '',
    selectedSnapshots: [],
    selectedSnapshot: null,
    dataTable:null,
    initiated:false,
    tableSettings: {
        rowId:'name',
        searching:false,
        responsive: false,
        bLengthChange: false,
        bInfo: false,
        bPaginate: false,
        order: [[ 1, 'asc' ]],
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
    },
    loading:false,
    rawJson:null,
    init: function(){
        console.log('Container Details init');
        this.dataTable = $('#tableSnapshots').DataTable(this.tableSettings);
        this.rawJson = ace.edit('rawJson');
        this.rawJson.session.setMode('ace/mode/json');
        this.rawJson.setOptions({readOnly: true});
        $('#refreshContainers').on('click', $.proxy(this.refreshContainers, this));
        $('#rawJSONContainerDetails').on('click', $.proxy(this.showJSON, this));
        $('#buttonStartDetail').on('click', $.proxy(this.startContainer, this));
        $('#buttonStopDetail').on('click', $.proxy(this.stopContainer, this));
        $('#buttonRestartDetail').on('click', $.proxy(this.restartContainer, this));
        $('#buttonFreezeDetail').on('click', $.proxy(this.freezeContainer, this));
        $('#buttonUnfreezeDetail').on('click', $.proxy(this.unfreezeContainer, this));
        $('#buttonDeleteDetail').on('click', $.proxy(this.deleteContainerDetail, this));
        $('#buttonBackDetail').on('click', $.proxy(this.switchView, this, 'list'));
        this.dataTable.on('select', $.proxy(this.onRowSelected, this));
        this.dataTable.on('deselect', $.proxy(this.onRowSelected, this));
        App.setActiveLink('');

        $('#buttonCloneContainerDetail').on('click', $.proxy(this.showCloneContainer, this));
        $('#buttonMoveContainerDetail').on('click', $.proxy(this.showMoveContainer, this));
        $('#buttonExportContainerDetail').on('click', $.proxy(this.showExportContainer, this));
        $('#buttonSnapshotContainerDetail').on('click', $.proxy(this.showSnapshotContainer, this));

        $('#buttonCloneContainer2').on('click', $.proxy(this.cloneContainerDetail, this));
        $('#buttonMoveContainer2').on('click', $.proxy(this.moveContainerDetail, this));
        $('#buttonExportContainer2').on('click', $.proxy(this.exportContainerDetail, this));
        $('#buttonSnapshotContainer2').on('click', $.proxy(this.snapshotContainerDetail, this));
        $('#buttonNewContainerSnapshot2').on('click', $.proxy(this.newContainerFromSnapshotDetail, this));
        $('.profileTag').on('click', $.proxy(this.deleteProfile, this));
        $('#buttonAdd').on('click', $.proxy(this.onAddProfileClick, this));
        $('.formModifier').on('click', $.proxy(this.formChanged, this));
        $('#buttonSave').on('click', $.proxy(this.saveChanges, this));
        $('#containerProfiles').on('change', $.proxy(this.addProfile, this));
        $('#editNameButton').on('click', $.proxy(this.focusOnName, this));
        $('#containerNameInput').on('blur', $.proxy(this.onNameChange, this));
        $('#buttonAutostartActive').on('click', $.proxy(this.onAutoStartToggle, this, true));
        $('#buttonAutostartInactive').on('click', $.proxy(this.onAutoStartToggle, this, false));
        $('[data-toggle="popover"]').popover();
        $('#buttonDeleteSnapshot').on('click', $.proxy(this.deleteSnapshots, this));
        $('#buttonRestoreSnapshot').on('click', $.proxy(this.restoreSnapshots, this));

        this.initKeyValuePairs();
    },
    initContainerDetails: function(name) {
        this.name = name;
        this.getSnapshotList();
    },
    initKeyValuePairs: function() {
        for (key in App.properties.keyValues) {
            $('#advancedSettings').append('<div class="row">' +
                    '<div class="col-lg-5">'+
                        '<div class="form-group row">' +
                            '<input type="text" class="form-control" placeholder="' + key + '"  disabled />' +
                            '<a href="#" class="hover-info" onmouseover="$.proxy(App.containerDetails.showPopover(this));" title="Information" data-toggle="popover" data-trigger="hover" data-content="'+ App.properties.keyValues[key].description + '" data-original-title="Information">' +
                                 '<span class="glyphicon glyphicon-info-sign"></span>' +
                             '</a>' +
                        '</div>' +
                    '</div>'+
                    '<div class="col-lg-5">' +
                        '<div class="form-group row">' +
                            '<input type="text" name="'+ key +'" id="' + key + '" class="form-control" placeholder="" value="" disabled />' +
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
    enableInput: function(e) {
        $('#buttonSave').show();
        $(e).parent().parent().parent().find('input').eq(1).removeAttr('disabled', '');
        $(e).removeClass('btn-default');
        $(e).addClass('btn-success');

        $(e).siblings().removeClass('btn-danger');
        $(e).siblings().addClass('btn-default');
    },
    disableInput: function(e) {
        $('#buttonSave').show();
        $(e).parent().parent().parent().find('input').eq(1).attr('disabled', 'disabled');
        $(e).removeClass('btn-default');
        $(e).addClass('btn-danger');

        $(e).siblings().removeClass('btn-success');
        $(e).siblings().addClass('btn-default');
    },
    showPopover: function(e) {
        $(e).popover('show');
    },
    refreshContainers: function(e){
        console.log('refreshContainers');
        location.reload();
    },
    setLoading: function(state){
        this.loading=true;
    },
    getData: function(){
        this.setLoading(true);
        $.get(App.baseAPI+'container/'+this.name, $.proxy(this.getDataSuccess, this));
    },
    getDataSuccess: function(response) {
        this.rawJson.setValue(JSON.stringify(response.data, null , '\t'));
    },
    showJSON: function(e) {
        this.rawJson.setValue('');
        $('.modal-title').text('');
        $('.modal-title').text('RAW JSON for Container ' + this.name);
        $('.modal-title').append(' <span class="glyphicon glyphicon-refresh spinning loader">');
        $("#jsonModal").modal("show");

        this.getData();

    },
    startContainer: function(){
        $.ajax({
            url: App.baseAPI+'container/start/' + this.name,
            type: 'PUT',
            success: $.proxy(this.onStartSuccess, this, this.name)
        });
    },
    onStartSuccess: function(name){
        console.log('onStartSuccess', name);
        location.reload();
    },
    stopContainer: function() {
        $.ajax({
            url: App.baseAPI+'container/stop/' + this.name,
            type: 'PUT',
            success: $.proxy(this.onStartSuccess, this, this.name)
        });
    },
    onStopSuccess: function(name){
        console.log('onStopSuccess', name);
        location.reload();
    },
    restartContainer: function() {
        $.ajax({
            url: App.baseAPI+'container/restart/' + this.name,
            type: 'PUT',
            success: $.proxy(this.onStartSuccess, this, this.name)
        });
    },
    freezeContainer: function() {
         $.ajax({
            url: App.baseAPI+'container/freeze/' + this.name,
            type: 'PUT',
            success: $.proxy(this.onStartSuccess, this, this.name)
        });
    },
    unfreezeContainer: function() {
         $.ajax({
            url: App.baseAPI+'container/unfreeze/' + this.name,
            type: 'PUT',
            success: $.proxy(this.onStartSuccess, this, this.name)
        });
    },
    onRestartSuccess: function(name){
        location.reaload();
    },
    deleteContainerDetail: function() {
        $.ajax({
            url: App.baseAPI+'container/' + this.name,
            type: 'DELETE',
            data:JSON.stringify({force:true}),
            success: $.proxy(this.onDeleteSuccess, this, this.name)
        });
    },
    onDeleteSuccess: function(name){
        console.log('onDelete', name);
        window.location = '/ui/containers';
    },
    getSnapshotList: function(){
        this.setLoading(true);
        $.get(App.baseAPI+'snapshot/container/'+this.name, $.proxy(this.getSnapshotSuccess, this));
    },
    getSnapshotSuccess: function (response){
        var container = this.name;
        $.each(response.data, function(index, value) {
            var tempPlaceholder = $('<div class="col-sm-6"></div>');
            var inputPlaceholder = $('div');
            inputPlaceholder.append('<td></td>');
            tempPlaceholder.append('<button class="btn btn-default pull-right" name="'+value.name+'" id="delete-'+value.name+'" onClick="$.proxy(App.containerDetails.deleteSnapshot());"><span class="glyphicon glyphicon-remove-sign"></span> Delete</button>');
            tempPlaceholder.append('<button class="btn btn-default pull-right" name="'+value.name+'" id="restore-'+value.name+'" onClick="$.proxy(App.containerDetails.restoreSnapshot());"> <span class="glyphicon glyphicon-repeat"></span> Restore</button>');
            tempPlaceholder.append('<button class="btn btn-default pull-right" name="'+value.name+'" id="create-'+value.name+'" onClick="$.proxy(App.containerDetails.createContainerSnapshot());"><span class="glyphicon glyphicon-plus-sign"></span> New Container</button>');
            this.dataTable = $('#tableSnapshots').DataTable(this.tableSettings);
            this.dataTable.row.add([
                null,
                value.name,
                value.createdAt,
                value.stateful ? 'Yes' : 'No',
                tempPlaceholder.html(),
            ]).draw();
        });

    },
     onRowSelected: function(e, dt, type, indexes ){
        var state = this.dataTable.rows({selected:true}).count()>0;
        $('#selectAllSnapshots').prop('checked',state);
        var action = state?'removeAttr':'attr';
        $('#buttonNewContainerSnapshot')[action]('disabled', 'disabled');
        $('#buttonRestoreSnapshot')[action]('disabled', 'disabled');
        $('#buttonDeleteSnapshot')[action]('disabled', 'disabled');
    },

    showCloneContainer: function(name) {
        $('.modal-title').text('');
        $('#newContainerClone').val('');
        $('.modal-title').text('Clone Container: ' + this.name);
        $("#containerDetailModal").modal("show");

        $('#cloneContainerForm').show();
        $('#buttonCloneContainer2').show();


        $('#buttonNewContainerSnapshot2').hide();
        $('#createContainerSnapshotForm').hide();
        $('#moveContainerForm').hide();
        $('#snapshotContainerForm').hide();
        $('#exportContainerForm').hide();
        $('#buttonExportContainer2').hide();
        $('#buttonSnapshotContainer2').hide();
        $('#buttonMoveContainer2').hide();
        $('#buttonCloneContainer2').show();
    },
    showMoveContainer: function(name) {
        $('.modal-title').text('');
        $('.modal-title').text('Move Container: ' + this.name);
        $('#newContainerMove').val('');
        $("#containerDetailModal").modal("show");
        $('#cloneContainerForm').hide();

        $('#buttonExportContainer2').hide();
        $('#buttonCloneContainer2').hide();
        $('#buttonSnapshotContainer2').hide();
        $('#buttonMoveContainer2').show();
        $('#buttonNewContainerSnapshot2').hide();
        $('#createContainerSnapshotForm').hide();

        $('#moveContainerForm').show();

        $('#snapshotContainerForm').hide();
        $('#exportContainerForm').hide();
    },
    showExportContainer: function(name) {
        $('.modal-title').text('');
        $('.modal-title').text('Export Image from Container: ' + this.name);
        $('#imageAlias').val('');
        $("#containerDetailModal").modal("show");

        $('#cloneContainerForm').hide();
        $('#moveContainerForm').hide();
        $('#snapshotContainerForm').hide();

        $('#buttonMoveContainer2').hide();
        $('#buttonCloneContainer2').hide();
        $('#buttonSnapshotContainer2').hide();
        $('#buttonExportContainer2').show();
        $('#buttonNewContainerSnapshot2').hide();
        $('#createContainerSnapshotForm').hide();

        $('#exportContainerForm').show();

    },
    showSnapshotContainer: function(name) {
        $('.modal-title').text('');
        $('.modal-title').text('Create Snapshot from Container: ' + this.name);
        $('#snapshotName').val('');
        $("#containerDetailModal").modal("show");
        $('#cloneContainerForm').hide();
        $('#buttonExportContainer2').hide();
        $('#buttonCloneContainer2').hide();
        $('#buttonMoveContainer2').hide();
        $('#buttonSnapshotContainer2').show();
        $('#moveContainerForm').hide();
        $('#buttonNewContainerSnapshot2').hide();
        $('#createContainerSnapshotForm').hide();

        $('#snapshotContainerForm').show();
        $('#exportContainerForm').hide();
    },
    cloneContainerDetail: function() {
        var container = this.name;
        $.ajax({
            url:App.baseAPI+'container/clone/'+container,
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
         window.location = '/ui/containers';
    },
    moveContainerDetail: function() {
        $.ajax({
            url:App.baseAPI+'container/move/'+this.name,
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
         window.location = '/ui/containers';
    },
    exportContainerDetail: function() {
        $.ajax({
            url:App.baseAPI+'container/export/'+this.name,
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
         location.reload();
    },
    snapshotContainerDetail: function() {
        $.ajax({
            url:App.baseAPI+'snapshot/' + $('#snapshotName').val() + '/container/'+this.name,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                stateful: $('#snapshotStateful').is(':checked'),
            }),
            success: $.proxy(this.onSnapshotSuccess, this)
        });
    },
    onSnapshotSuccess: function(response){
         location.reload();
    },
    restoreSnapshots: function() {
      this.dataTable.rows( { selected: true } ).data().map(function(row){
        console.log('row', row);
        var name = this.name;
        $.ajax({
//              url:App.baseAPI+'snapshot/'+snapshotName+'/container/'+container,
            url:App.baseAPI+'snapshot/'+row[1]+'/container/'+name,
            type: 'DELETE',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                imageAlias: $('#imageAlias').val(),
                force: true
            }),
            success: $.proxy(this.onSnapshotDeleteSuccess, this)
        });
        }.bind(this));
    },

    restoreSnapshot: function() {
        console.log("Restore");
        var snapshotName = $(event.target).prop('name');
        var container = this.name;
        $.ajax({
            url:App.baseAPI+'snapshot/'+snapshotName+'/container/'+container,
            type: 'PUT',
            dataType: 'json',
            contentType: 'application/json',
            success: $.proxy(this.onRestoreSuccess, this)
        });
    },
    onRestoreSuccess: function(response) {
        setTimeout(function() {
            location.reload();
        }, 3000)
    },
    createContainerSnapshot: function() {
        console.log("Create Container");
        var snapshotName = $(event.target).prop('name');
        var container = this.name;
        this.activeSnapshot = snapshotName;
        $('.modal-title').text('');
        $('.modal-title').text('Create Container from Snapshot: ' + snapshotName);
        $('#newContainerMove').val('');
        $("#containerDetailModal").modal("show");
        $('#cloneContainerForm').hide();

        $('#buttonExportContainer2').hide();
        $('#buttonCloneContainer2').hide();
        $('#buttonSnapshotContainer2').hide();
        $('#buttonMoveContainer2').hide();
        $('#buttonNewContainerSnapshot2').show();

        $('#createContainerSnapshotForm').show();

        $('#snapshotContainerForm').hide();
        $('#exportContainerForm').hide();
    },
    newContainerFromSnapshotDetail: function() {
         var container = this.name;
         $.ajax({
            url:App.baseAPI+'snapshot/'+ this.activeSnapshot +'/container/'+this.name+'/create',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                newContainer: $('#newContainerSnapshot').val(),
                force: true
            }),
            success: $.proxy(this.onCreateFromSnapshotSuccess, this)
        });
    },
    onCreateFromSnapshotSuccess: function() {
        location.reload();
    },
    deleteSnapshot: function() {
        console.log("Delete Snapshot");
        var snapshotName = $(event.target).prop('name');
        var container = this.name;
        $.ajax({
            url:App.baseAPI+'snapshot/'+snapshotName+'/container/'+container,
            type: 'DELETE',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                imageAlias: $('#imageAlias').val(),
                force: true
            }),
            success: $.proxy(this.onSnapshotDeleteSuccess, this)
        });
    },
    deleteSnapshots: function() {
        this.dataTable.rows( { selected: true } ).data().map(function(row){
        console.log('row', row);
        var name = this.name;
        $.ajax({
                url:App.baseAPI+'snapshot/'+row[1]+'/container/'+name,
                 type: 'DELETE',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                imageAlias: $('#imageAlias').val(),
                force: true
            }),
            success: $.proxy(this.onSnapshotDeleteSuccess, this)
        });
        }.bind(this));
    },
    onSnapshotDeleteSuccess: function(response) {
        location.reload();
    },
    deleteProfile: function(event){
        this.data.profiles.splice(this.data.profiles.indexOf($(event.target).data('id')),1);
        this.updates['profiles'] = this.data.profiles;
        this.updateProfiles();
    },
    onDeleteProfileSuccess:function(response){
        window.location.reload();
    },
    updateProfiles: function(){
        $('#profileList').empty();
        for(var i=0,profile;profile=this.updates.profiles[i];i++){
            var tempProfile = '<span class="label label-default no-right-padding mg-right">'+profile;
            tempProfile += '<a id="button_'+profile+'" class="btn tag-button glyphicon glyphicon-remove profileTag" data-id="'+profile+'" data-container="'+this.data.name+'"></a></span>';
            $('#profileList').append(tempProfile);
        }
        $('.profileTag').on('click', $.proxy(this.deleteProfile, this));
    },
    onAddProfileClick: function(){
        $('#containerProfiles').show();
        $('#buttonAdd').hide();
    },
    addProfile: function(event){
        var tempSelected = $('#containerProfiles').find(':selected').text();
        if(this.data.profiles.indexOf(tempSelected)!==-1){
            return;
        }
        this.data.profiles.push(tempSelected);
        this.updates['profiles'] = this.data.profiles;
        this.updateProfiles();
        $('#containerProfiles').hide();
        $('#buttonAdd').show();
    },
    saveChanges:function(){

        this.updates['config'] = this.readKeyValuePairs();
        console.log(this.updates);
        $.ajax({
            url: App.baseAPI+'container/',
            type:'PUT',
            dataType:'json',
            contentType:'application/json',
            data: JSON.stringify(this.updates),
            success:$.proxy(this.onSaveChangesSuccess, this)
        });
    },
    readKeyValuePairs: function() {
        keyValues = {}
        $('#advancedSettings').find('input:enabled').each(function() {
            keyValues[this.name] = this.value;
        })

        return keyValues;
    },
    onSaveChangesSuccess:function(response){
        if(this.updates['newName']){
            return window.location.pathname = '/ui/containers/'+this.updates['newName'];
        }
        return window.location.reload();
    },
    setInitialData: function(){
        this.updates['image'] = this.data.config['volatile.base_image'];
        this.updates['name'] = this.data.name;
    },
    formChanged: function(){
        console.log('enableSave');
        $('#buttonSave').show();
        $('.formChanged').unbind('click');
    },
    focusOnName: function(){
        $('#containerNameInput').focus();
    },
    onNameChange: function(event){
        this.updates['newName'] = event.target.textContent;
    },
    onAutoStartToggle:function(state){
    console.log('newState', state);
        this.updates['autostart']=state;
        if(state){
             $('#buttonAutostartActive').removeClass('btn-default');
             $('#buttonAutostartActive').addClass('btn-success');
             $('#buttonAutostartInactive').removeClass('btn-success');
             $('#buttonAutostartInactive').addClass('btn-default');
        }else{
             $('#buttonAutostartActive').removeClass('btn-success');
             $('#buttonAutostartActive').addClass('btn-default');
             $('#buttonAutostartInactive').removeClass('btn-default');
             $('#buttonAutostartInactive').addClass('btn-success');
        }
    }
}