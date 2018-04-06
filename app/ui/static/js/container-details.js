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

        $('#buttonCloneContainerDetail').on('click', $.proxy(this.cloneContainer, this));
        $('#buttonMoveContainerDetail').on('click', $.proxy(this.moveContainer, this));
        $('#buttonExportContainerDetail').on('click', $.proxy(this.exportContainer, this));
        $('#buttonSnapshotContainerDetail').on('click', $.proxy(this.snapshotContainer, this));

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
        $.each(response.data, function(index, value) {
            $('#snapshotList').append('<li>'+value+'</li>');
        });

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