App.containerDetails = App.containerDetails || {
    data:[],
    error:false,
    errorMessage:'',
    name: '',
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
        console.log(container);
        $.each(response.data, function(index, value) {
            $('#snapshotList').append('<h4>'+value+'</h4>');
            $('#snapshotList').append('<button class="btn btn-default" name="'+value.split('/').pop(-1)+'" id="restore-'+value.split('/').pop(-1)+'" onClick="$.proxy(App.containerDetails.restoreSnapshot());">Restore</button>');
            $('#snapshotList').append('<button class="btn btn-default" name="'+value.split('/').pop(-1)+'" id="create-'+value.split('/').pop(-1)+'" onClick="$.proxy(App.containerDetails.createContainerSnapshot());">New Container</button>');
            $('#snapshotList').append('<button class="btn btn-default" name="'+value.split('/').pop(-1)+'" id="delete-'+value.split('/').pop(-1)+'" onClick="$.proxy(App.containerDetails.deleteSnapshot());">Delete</button>')
            $('#snapshotList').append('<br>');
        });

    },
    showCloneContainer: function(name) {
        $('.modal-title').text('');
        $('#newContainerClone').val('');
        $('.modal-title').text('Clone Container: ' + name);
        $("#containerDetailModal").modal("show");

        $('#cloneContainerForm').show();
        $('#buttonCloneContainer').show();


        $('#buttonNewContainerSnapshot').hide();
        $('#moveContainerForm').hide();
        $('#snapshotContainerForm').hide();
        $('#exportContainerForm').hide();
        $('#buttonExportContainer').hide();
        $('#buttonSnapshotContainer').hide();
        $('#buttonMoveContainer').hide();
        $('#buttonCloneContainer').show();
    },
    showMoveContainer: function(name) {
        $('.modal-title').text('');
        $('.modal-title').text('Move Container: ' + name);
        $('#newContainerMove').val('');
        $("#containerDetailModal").modal("show");
        $('#cloneContainerForm').hide();

        $('#buttonExportContainer').hide();
        $('#buttonCloneContainer').hide();
        $('#buttonSnapshotContainer').hide();
        $('#buttonMoveContainer').show();
        $('#buttonNewContainerSnapshot').hide();

        $('#moveContainerForm').show();

        $('#snapshotContainerForm').hide();
        $('#exportContainerForm').hide();
    },
    showExportContainer: function(name) {
        $('.modal-title').text('');
        $('.modal-title').text('Export Image from Container: ' + name);
        $('#imageAlias').val('');
        $("#containerDetailModal").modal("show");

        $('#cloneContainerForm').hide();
        $('#moveContainerForm').hide();
        $('#snapshotContainerForm').hide();

        $('#buttonMoveContainer').hide();
        $('#buttonCloneContainer').hide();
        $('#buttonSnapshotContainer').hide();
        $('#buttonExportContainer').show();
        $('#buttonNewContainerSnapshot').hide();

        $('#exportContainerForm').show();

    },
    showSnapshotContainer: function(name) {
        $('.modal-title').text('');
        $('.modal-title').text('Create Snapshot from Container: ' + name);
        $('#snapshotName').val('');
        $("#containerDetailModal").modal("show");
//        $('#selectedSnapshot').text('Create Snapshot from Container: ' + name);
        $('#cloneContainerForm').hide();
        $('#buttonExportContainer').hide();
        $('#buttonCloneContainer').hide();
        $('#buttonMoveContainer').hide();
        $('#buttonSnapshotContainer').show();
        $('#moveContainerForm').hide();
        $('#buttonNewContainerSnapshot').hide();

        $('#snapshotContainerForm').show();
        $('#exportContainerForm').hide();
    },
    cloneContainer: function() {
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
         console.log(response);
         console.log('clonedSuccess:', 'TODO - add alert and refresh local data');
         location.reaload();
    },
    moveContainer: function() {
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
         console.log(response);
         console.log('Moved Success:', 'TODO - add alert and refresh local data');
         location.reaload();
    },
    exportContainer: function() {
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
         console.log(response);
         console.log('Export Success:', 'TODO - add alert and refresh local data');
         location.reload();
    },
    snapshotContainer: function() {
        $.ajax({
            url:App.baseAPI+'snapshot/' + $('#snapshotName').val() + '/container/'+this.name,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            success: $.proxy(this.onSnapshotSuccess, this)
        });
    },
    onSnapshotSuccess: function(response){
         console.log(response);
         console.log('Snapshot Success:', 'TODO - add alert and refresh local data');
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
        $('.modal-title').text('');
        $('.modal-title').text('Create Container from Snapshot: ' + snapshotName);
        $('#newContainerMove').val('');
        $("#containerDetailModal").modal("show");
        $('#cloneContainerForm').hide();

        $('#buttonExportContainer').hide();
        $('#buttonCloneContainer').hide();
        $('#buttonSnapshotContainer').hide();
        $('#buttonMoveContainer').hide();
        $('#buttonNewContainerSnapshot').show();

        if ($('#moveContainerForm').is(':visible') && this.selectedContainer === name) {
            $('#moveContainerForm').hide();
        }
        else {
            $('#createContainerSnapshotForm').show();
        }
        $('#snapshotContainerForm').hide();
        $('#exportContainerForm').hide();
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

}