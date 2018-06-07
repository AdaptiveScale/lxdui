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
        dom: "<'tbl-header'<'row'<'col-sm-4 text-left'f><'col-sm-2 refresh-list-place'><'col-sm-6 json-place'>>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-4'i><'col-sm-5 text-right'l><'col-sm-3 text-right'p>>",
        "oLanguage": {
          "sLengthMenu": "List _MENU_ ",
        },
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
        $('#buttonNewContainerSnapshot').on('click', $.proxy(this.createContainerSnapshot, this));
        $('#exTab3 > ul > li:nth-child(1)').addClass('active');

        this.initKeyValuePairs();
    },
    initContainerDetails: function(name) {
        this.name = name;
        this.getSnapshotList();
    },
    initKeyValuePairs: function() {
        for (key in App.properties.keyValues) {
            $('#advancedSettings').append('<div class="row">' +
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
        window.location = '/ui/containers';
    },
    getSnapshotList: function(){
        this.setLoading(true);
        $.get(App.baseAPI+'snapshot/container/'+this.name, $.proxy(this.getSnapshotSuccess, this));
    },
    getSnapshotSuccess: function (response){
        var container = this.name;
        this.dataTable.rows().remove().draw();
        $.each(response.data, function(index, value) {
            var tempPlaceholder = $('<div class="col-sm-6"></div>');
            var inputPlaceholder = $('div');
            inputPlaceholder.append('<td></td>');
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
            if(this.dataTable.rows({selected:true}).count() > 0) {
             if(this.dataTable.rows({selected:true}).count() == 1){
                $('#buttonDeleteSnapshot').removeAttr('disabled', 'disabled');
                $('#buttonRestoreSnapshot').removeAttr('disabled', 'disabled');
                $('#buttonNewContainerSnapshot').removeAttr('disabled', 'disabled');
              }
              else {
                 $('#buttonRestoreSnapshot').attr('disabled', 'disabled');
                $('#buttonNewContainerSnapshot').attr('disabled', 'disabled');
                $('#buttonDeleteSnapshot').removeAttr('disabled', 'disabled');
                }
            }
            else {
                $('#buttonRestoreSnapshot').attr('disabled', 'disabled');
                $('#buttonNewContainerSnapshot').attr('disabled', 'disabled');
                $('#buttonDeleteSnapshot').attr('disabled', 'disabled');
            }

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
    showCloneContainerfromSnapshot: function(name) {
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
         setTimeout(function() {
            App.containerDetails.getSnapshotList();
            $("#containerDetailModal").modal("hide");
        }, 1000);
    },
    restoreSnapshots: function() {
      this.dataTable.rows( { selected: true } ).data().map(function(row){
        var name = this.name;
        $.ajax({
            url:App.baseAPI+'snapshot/'+row[1]+'/container/'+name,
            type: 'PUT',
            dataType: 'json',
            contentType: 'application/json',
            success: $.proxy(this.onRestoreSuccess, this)
        });
        }.bind(this));
    },

    restoreSnapshot: function() {
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
         this.dataTable.rows( { selected: true } ).data().map(function(row){
            var name = this.name;
            var container = this.name;
             $.ajax({
                url:App.baseAPI+'snapshot/'+ row[1] +'/container/'+this.name+'/create',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    newContainer: $('#newContainerSnapshot').val(),
                    force: true
                }),
                success: $.proxy(this.onCreateFromSnapshotSuccess, this)
            });
         }.bind(this));
    },
    onCreateFromSnapshotSuccess: function() {
        $("#containerDetailModal").modal("hide");
    },
    deleteSnapshot: function() {
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
        setTimeout(function() {
            App.containerDetails.getSnapshotList();
        }, 1000);
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