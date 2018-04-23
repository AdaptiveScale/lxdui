App.containerDetails = App.containerDetails || {
    data:[],
    updates:{
        image:''
    },
    error:false,
    errorMessage:'',
    name: '',
    activeSnapshot: '',
    loading:false,
    init: function(){
        console.log('Container Details init');
        $('#refreshContainers').on('click', $.proxy(this.refreshContainers, this));
        $('#buttonStartDetail').on('click', $.proxy(this.startContainer, this));
        $('#buttonStopDetail').on('click', $.proxy(this.stopContainer, this));
        $('#buttonRestartDetail').on('click', $.proxy(this.restartContainer, this));
        $('#buttonDeleteDetail').on('click', $.proxy(this.deleteContainerDetail, this));
        $('#buttonBackDetail').on('click', $.proxy(this.switchView, this, 'list'));
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
    },
    initContainerDetails: function(name) {
        this.name = name;
        this.getSnapshotList();
    },
    refreshContainers: function(e){
        console.log('refreshContainers');
        location.reload();
    },
    setLoading: function(state){
        this.loading=true;
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
    onRestartSuccess: function(name){
        console.log('onRestartSuccess', name);
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
        //location.reload()
        window.location = '/ui/containers';
        //window.location.href = '/ui/containers';
    },
    getSnapshotList: function(){
        this.setLoading(true);
        $.get(App.baseAPI+'snapshot/container/'+this.name, $.proxy(this.getSnapshotSuccess, this));
    },
    getSnapshotSuccess: function (response){
        var container = this.name;
        $.each(response.data, function(index, value) {
            var row = $('<div class="row"></div>');
            row.append('<h5 class="col-sm-6 ">'+value+'</h5>');
            var tempPlaceholder = $('<div class="col-sm-6"></div>');
            tempPlaceholder.append('<button class="btn btn-default pull-right" name="'+value.split('/').pop(-1)+'" id="restore-'+value.split('/').pop(-1)+'" onClick="$.proxy(App.containerDetails.restoreSnapshot());"> <span class="glyphicon glyphicon-repeat"></span> Restore</button>');
            tempPlaceholder.append('<button class="btn btn-default pull-right" name="'+value.split('/').pop(-1)+'" id="create-'+value.split('/').pop(-1)+'" onClick="$.proxy(App.containerDetails.createContainerSnapshot());"><span class="glyphicon glyphicon-plus-sign"></span> New Container</button>');
            tempPlaceholder.append('<button class="btn btn-default pull-right" name="'+value.split('/').pop(-1)+'" id="delete-'+value.split('/').pop(-1)+'" onClick="$.proxy(App.containerDetails.deleteSnapshot());"><span class="glyphicon glyphicon-remove-sign"></span> Delete</button>');
            row.append(tempPlaceholder);
            $('#snapshotList').append(row);
        });

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
         //location.reload();
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
         //location.reload();
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
            success: $.proxy(this.onSnapshotSuccess, this)
        });
    },
    onSnapshotSuccess: function(response){
         location.reload();
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
        location.reload();
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
        $.ajax({
            url: App.baseAPI+'container/',
            type:'PUT',
            dataType:'json',
            contentType:'application/json',
            data: JSON.stringify(this.updates),
            success:$.proxy(this.onSaveChangesSuccess, this)
        });
    },
    onSaveChangesSuccess:function(response){
        window.location.reload();
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
    }
}