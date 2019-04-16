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
    treeSource: [],
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
        "<'row'<'col-sm-4'i><'col-sm-2 text-right'l><'col-sm-6 text-right'p>>",
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
    activeNode: null,
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

        $('#cloneContainerSubmit').on('submit', $.proxy(this.cloneContainerDetail, this));
        $('#moveContainerSubmit').on('submit', $.proxy(this.moveContainerDetail, this));
        $('#exportContainerSubmit').on('submit', $.proxy(this.exportContainerDetail, this));
        $('#snapshotContainerSubmit').on('submit', $.proxy(this.snapshotContainerDetail, this));
        $('#containerFromSnapshotForm').on('submit', $.proxy(this.newContainerFromSnapshotDetail, this));

         $('#cloneContainerSubmit').on('click', $.proxy(this.cloneContainerDetail, this));
        $('#moveContainerSubmit').on('click', $.proxy(this.moveContainerDetail, this));
        $('#exportContainerSubmit').on('click', $.proxy(this.exportContainerDetail, this));
        $('#snapshotContainerSubmit').on('click', $.proxy(this.snapshotContainerDetail, this));
        $('#containerFromSnapshotForm').on('click', $.proxy(this.newContainerFromSnapshotDetail, this));

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

        $('#file-btn-home').on('click', $.proxy(this.home, this));
        $('#file-btn-new').on('click', $.proxy(this.createNewFile, this));
        $('#file-btn-edit').on('click', $.proxy(this.viewSelectedFile, this, true));
        $('#file-btn-view').on('click', $.proxy(this.viewSelectedFile, this, false));
        $('#file-btn-upload').on('click', $.proxy(this.uploadFile, this));
        $('#file-btn-delete').on('click', $.proxy(this.deleteFile, this));
        $('#uploadFileSubmit').on('click', $.proxy(this.uploadFile2, this));
        $('#deleteFileSubmit').on('click', $.proxy(this.deleteFile2, this));
        $('#newFileSubmit').on('click', $.proxy(this.newFile, this));
        $('#editFileSubmit').on('click', $.proxy(this.editFile, this));
        $('#file-btn-download').on('click', $.proxy(this.downloadFile, this));


        $('#exTab3 > ul > li:nth-child(1)').addClass('active');

        this.initKeyValuePairs();
        this.extractIPs();
        this.extractPorts();
        $('#addProxyForm').on('submit', $.proxy(this.addProxy, this));
        $('#addProxy').on('click', $.proxy(this.addProxy, this));
        $('.showAddProxyDialog').on('click', $.proxy(this.showAddProxy, this));
        $('.showAddNetworkInterfaceDialog').on('click', $.proxy(this.showAddNetworkInterface, this));
        $('#addNetworkInterfaceForm').on('submit', $.proxy(this.addNetworkInterface, this));
        $('#addNetwork').on('click', $.proxy(this.addNetworkInterface, this))
    },
    extractPorts: function(){
        $('.portToExtract').each((key,val)=> $(val).text(App.helpers.extractPort($(val).text())));
    },
    extractIPs: function() {
        $('.ipToExtract').each((key,val)=> $(val).text(App.helpers.extractIP($(val).text())));
    },
    downloadURI: function(uri, name) {
        var link = document.createElement("a");
        link.download = name;
        link.href = uri;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        delete link;
    },
    downloadFile: function() {
        this.activeNode = $("#tree").fancytree('getActiveNode');
        var activeNode = this.activeNode;
        if (!activeNode.folder)
            this.downloadURI(App.baseAPI+'file/download/container/' + this.name + '?path=' + activeNode.getKeyPath())
    },
    home: function() {
        $("#tree").fancytree('getTree').visit(function(node) {
            if (node.getKeyPath() == '/home') {
                node.setExpanded(true);
            }
            else {
                node.setExpanded(false);
            }
        });
    },
    editFile: function() {
        var activeNode = this.activeNode;
        $.ajax({
            url: App.baseAPI+'file/edit/container/' + this.name,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                'path': activeNode.getKeyPath(),
                'file': $('#editText').val()
            }),
            success: $.proxy(this.onEditFileSuccess, this)
        });
    },
    onEditFileSuccess: function() {
        $("#editFileModal").modal("hide");
        this.listDirectory('/');
    },
    newFile: function() {
        $.ajax({
            url: App.baseAPI+'file/new/container/' + this.name,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                'path': $("#fileName").val(),
                'file': $('#fileContent').val()
            }),
            success: $.proxy(this.onNewFileSuccess, this)
        });
    },
    onNewFileSuccess: function() {
        $("#newFileManagerModal").modal("hide");
        this.listDirectory('/');
    },
    deleteFile2: function() {
        var node = this.activeNode;
        $.ajax({
            url: App.baseAPI+'file/container/' + this.name,
            type: 'DELETE',
            contentType: 'application/json',
            data: JSON.stringify({
                'path': node.getKeyPath(),
            }),
            success: $.proxy(this.onFileDeletedSuccess, this)
        });
    },
    onFileDeletedSuccess: function() {
        $("#deleteFileModal").modal("hide");
        this.listDirectory('/');
    },
    uploadFile2: function() {
        var tempData = new FormData();
        tempData.append('path', $('#pathName').val());
        tempData.append('file', $('#uploadFile')[0].files[0]);
        $.ajax({
            url: App.baseAPI+'file/container/' + this.name,
            type: 'POST',
            contentType: false,
            processData: false,
            data: tempData,
            success: $.proxy(this.onFileUploadSuccess, this)
        });
    },
    onFileUploadSuccess: function() {
        this.listDirectory('/');
        $('#uploadFileModal').modal("hide");
        $('#uploadFile').val(''); //clear file selection value
    },
    viewSelectedFile: function(edit) {
        var node = $("#tree").fancytree('getActiveNode');
        if (node) {
            if (!node.folder) {
                this.readFileContent(node.getKeyPath(), edit);
            }
        }

    },
    readFileContent: function(path, edit) {
        $.ajax({
            url: App.baseAPI+'file/content/container/' + this.name + '?path='+path,
            type: 'GET',
            success: $.proxy(this.onFileContentSuccess, this, path, edit)
        });
    },
    onFileContentSuccess: function(path, edit, response) {
        this.viewFile(response.data, path, edit);
    },
    listDirectory: function(path) {
        return $.ajax({
            url: App.baseAPI+'file/list/container/' + this.name + '?path='+path,
            type: 'GET',
            success: $.proxy(this.onFileListSuccess, this)
        });
    },
    onFileListSuccess: function(response) {
        this.treeSource = response;
        var name = this.name;
        $("#tree").fancytree({
           source: this.treeSource,
           lazyLoad: function(event, data) {
                var node = data.node;
                data.result = {
                    url: App.baseAPI+'file/list/container/' + name + '?path='+node.getKeyPath(),
                    data: {mode: 'children', parent: node.key},
                    cache: false,
                }
           },
           dblclick: function(event, data) {
               var node = data.node;
               if (!node.folder) {
                    $.proxy(App.containerDetails.readFileContent(node.getKeyPath()));
               }
           },
           activate: function(event, data){
               $("#status").text("Activate: " + data.node);
               if(data.node.folder){
                $('#pathName').val(data.node.getKeyPath()+'/');
                $('#path').val(data.node.getKeyPath() + '/');
                $('#file-btn-download,#file-btn-view,#file-btn-edit').attr("disabled", "disabled");
               }
               else {
                $('#file-btn-download,#file-btn-view,#file-btn-edit').removeAttr("disabled");
               }
           }
       });
    },
    initContainerDetails: function(name) {
        this.name = name;
        this.getSnapshotList();
        this.listDirectory('/');
    },
    updateTreeSource: function(data) {
        this.listDirectory(data.node.title);
    },
    initKeyValuePairs: function() {
        $('#advancedSettings .manuallyAdded').remove()
        for (key in App.properties.keyValues) {
            $('#advancedSettings').append('<div class="row manuallyAdded">' +
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
                            '<input type="text" name="'+ key +'" id="' + key + '" class="form-control" placeholder="" value="'+((this.data.config)?this.data.config[key] || '':'')+'" '+((this.data.config && this.data.config[key])?'':'disabled')+' />' +
                            '<a href="#" class="hover-info" onmouseover="$.proxy(App.containerDetails.showPopover(this));" title="Information" data-toggle="popover" data-trigger="hover" data-content="'+ _.get(App,'properties.keyValues["'+key+'"].valueDescription', 'No content available') + '" data-original-title="Information">' +
                                 '<span class="glyphicon glyphicon-info-sign"></span>' +
                             '</a>' +
                        '</div>' +
                    '</div>' +
                     '<div class="col-lg-2">' +
                         '<div class="btn-group" role="group">' +
                            '<button type="button" id="" class="formModifier btn btn-sm btn-'+((this.data.config && this.data.config[key])?'success':'default')+'" onClick="$.proxy(App.containerDetails.enableInput(this));">On</button>' +
                            '<button type="button" id="" class="formModifier btn btn-sm btn-'+((this.data.config && this.data.config[key])?'default':'danger')+'" onClick="$.proxy(App.containerDetails.disableInput(this));">Off</button>' +
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
        $('#cloneContainerModal .modal-title').text('');
        $('#newContainerClone').val('');
        $('#cloneContainerModal .modal-title').text('Clone Container: ' + this.name);
        $("#cloneContainerModal").modal("show");
    },
    showMoveContainer: function(name) {
        $('#moveContainerModal .modal-title').text('');
        $('#moveContainerModal .modal-title').text('Move Container: ' + this.name);
        $('#newContainerMove').val('');
        $("#moveContainerModal").modal("show");
    },
    showExportContainer: function(name) {
        $('#exportContainerModal .modal-title').text('');
        $('#exportContainerModal .modal-title').text('Export Image from Container: ' + this.name);
        $('#imageAlias').val('');
        $("#exportContainerModal").modal("show");
    },
    showSnapshotContainer: function(name) {
        $('#snapshotContainerModal .modal-title').text('');
        $('#snapshotContainerModal .modal-title').text('Create Snapshot from Container: ' + this.name);
        $('#snapshotName').val('');
        $("#snapshotContainerModal").modal("show");
    },
    cloneContainerDetail: function(e) {
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
            $("#snapshotContainerModal").modal("hide");
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
        $('#containerFromSnapshotModal .modal-title').text('');
        $('#containerFromSnapshotModal .modal-title').text('Create Container from Snapshot: ' + snapshotName);
        $('#newContainerMove').val('');
        $("#containerFromSnapshotModal").modal("show");
//        $('#cloneContainerForm').hide();
    },
    createNewFile: function() {
        $('#newFileManagerModal .modal-title').text('');
        $('#newFileManagerModal .modal-title').text('New File');
        $("#newFileManagerModal").modal("show");
    },
    editSelectedFile: function(text, path) {
        $('#editFileModal .modal-title').text(path);
        $('#editText').text(text);
        $("#editFileModal").modal("show");
    },
    deleteFile: function() {
        var node = $("#tree").fancytree('getActiveNode');
        if (node) {
            $('#deleteFileModal .modal-title').text('');
            $('#deleteFileModal .modal-body').text('Delete file '+node.getKeyPath());
            $("#deleteFileModal").modal("show");
            this.activeNode = node;
        }


    },
    viewFile: function(text, path, edit) {
        this.activeNode = $("#tree").fancytree('getActiveNode');
        if (edit) {
            this.editSelectedFile(text, path);
        }
        else {
            $('#viewFileModal .modal-title').text(path);
            $('#viewText').text(text);
            $("#viewFileModal").modal("show");
        }
    },
    uploadFile: function() {
        $('#uploadFolderLocation').text($('#pathName').val());
        $("#uploadFileModal").modal("show");
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
    },
    removeProxy: function(name){
        $.ajax({
            url:App.baseAPI+'container/proxy/'+this.data.name+'/remove/'+name,
            type:'DELETE',
            dataType:'json',
            contentType:'application/json',
            success:$.proxy(this.removeProxySuccess, this)
        });
    },
    removeProxySuccess: function(){
        return window.location.reload();
    },
    showAddProxy: function(){
        $('#addProxyModal').modal('show');
        $('#container').val(_.get(this, 'data.network.eth0.addresses[0].address', '0.0.0.0'));
    },
    addProxy: function(e){
        var isValid = $('#addProxyForm')[0].checkValidity();
        if(e){
           e.preventDefault();
        }
        if(!isValid){
            return false;
        }
        var input = $('#addProxyForm').serializeJSON();
        $.ajax({
            url:App.baseAPI+'container/proxy/'+this.data.name+'/add/'+input.name,
            type:'POST',
            dataType:'json',
            data:JSON.stringify({
                listen:input.protocol+':'+input.host+':'+input.hostPort,
                connect:input.protocol +':'+input.container+':'+input.containerPort,
                type:'proxy'
            }),
            contentType:'application/json',
            success:$.proxy(this.removeProxySuccess, this)
        });

        return false;
    },
    showAddNetworkInterface: function(){
        $('#addNetworkInterfaceModal').modal('show');
//        $('#container').val(_.get(this, 'data.network.eth0.addresses[0].address', '0.0.0.0'));
    },
     removeProxySuccess: function(){
        return window.location.reload();
    },
    addNetworkInterface: function(e) {
        var isValid = $('#addNetworkInterfaceForm')[0].checkValidity();
        if(e){
           e.preventDefault();
        }
        if(!isValid){
            return false;
        }
        var input = $('#addNetworkInterfaceForm').serializeJSON();
        console.log('input', input);
        $.ajax({
            url:App.baseAPI+'container/network/'+this.data.name+'/add',
            type:'POST',
            dataType:'json',
            data: JSON.stringify(input),
            contentType:'application/json',
            success:$.proxy(this.removeProxySuccess, this)
        });

        return false;
    },
    deleteInterface: function(ifaceName){
        $.ajax({
            url: App.baseAPI+'container/network/'+this.data.name+'/remove/'+ifaceName,
            type:'DELETE',
            dataType:'json',
            contentType:'application/json',
            success:$.proxy(this.removeProxySuccess, this)
        });
    }
}
