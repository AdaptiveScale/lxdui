App.containers = App.containers || {
    data:[],
    error:false,
    errorMessage:'',
    loading:false,
    selectedContainers: [],

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
    init: function(){
        console.log('Containers init');
        this.dataTable = $('#tableContainers').DataTable(this.tableSettings);
        $('#refreshContainers').on('click', $.proxy(this.refreshContainers, this));
        $('#buttonStart').on('click', $.proxy(this.startContainer, this));
        $('#buttonStop').on('click', $.proxy(this.stopContainer, this));
        $('#buttonRestart').on('click', $.proxy(this.restartContainer, this));
        $('#buttonDelete').on('click', $.proxy(this.deleteContainer, this));
        this.dataTable.on('select', $.proxy(this.onRowSelected, this));
        this.dataTable.on('deselect', $.proxy(this.onRowSelected, this));
        this.getData();
    },
    refreshContainers: function(e){
        console.log('refreshContainers');
        e.preventDefault();
        console.log('dataTable', this.dataTable);
        this.getData();
    },
    setLoading: function(state){
        this.loading=true;
    },
    getData: function(){
        this.setLoading(true);
        $.get(App.baseAPI+'container', $.proxy(this.getDataSuccess, this));
    },
    getDataSuccess: function(response){
        console.log('success', response.data);
        this.setLoading(false);
        this.data = response.data;
        if(!this.initiated)
            return this.initiated = true;
        this.dataTable.clear();
        this.dataTable.destroy();
        this.dataTable=$('#tableContainers').DataTable(App.mergeProps(this.tableSettings, {
            data:this.data,
            columns : [
                { title:'Select', data: null, defaultContent:''},
                { title:'Name', data : 'name'},
                { title:'Status', data : 'status' },
                { title:'IP Address', data : 'ipaddress', defaultContent:''},
                { title:'OS Image', data : 'config',
                    render:function(field){
                        return field['image.distribution'];
                    }
                },
                { title:'Create at', data : 'created_at' }
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
        $('.success-msg').text('Container ' + name + 'has been started')
        var parent = $('.success-msg').parent().toggleClass('hidden');
        setTimeout(function(){
          parent.toggleClass('hidden');
        }, 10000)
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
        $('.success-msg').text('Container ' + name + ' has been stopped');
        var parent = $('.success-msg').parent().toggleClass('hidden');

        setTimeout(function(){
          parent.toggleClass('hidden');
        }, 10000);
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
        $('.success-msg').text('Container ' + name + ' has been restarted');
        var parent = $('.success-msg').parent().toggleClass('hidden');

        setTimeout(function(){
          parent.toggleClass('hidden');
        }, 10000);
    },
    deleteContainer: function() {
        this.dataTable.rows( { selected: true } ).data().map(function(row){
            $.ajax({
                url: App.baseAPI+'container/' + row['name'],
                type: 'DELETE',
                success: $.proxy(this.onDeleteSuccess, this, row['name'])
            });
        }.bind(this));
    },

    onDeleteSuccess: function(name){
        this.dataTable.row("#"+name).remove().draw();
        $('.success-msg').text('Container ' + name + ' has been removed');
        var parent = $('.success-msg').parent().toggleClass('hidden');

        setTimeout(function(){
          parent.toggleClass('hidden');
        }, 10000);

    },
}

//var selectedContainers = [];
//var tasks_required = 0;
//
//jQuery.each( [ "put", "delete" ], function( i, method ) {
//  jQuery[ method ] = function( url, data, callback, type ) {
//    if ( jQuery.isFunction( data ) ) {
//      type = type || callback;
//      callback = data;
//      data = undefined;
//    }
//
//    return jQuery.ajax({
//      url: url,
//      type: method,
//      dataType: type,
//      data: data,
//      success: callback
//    });
//  };
//});
//
//function checkAll() {
//    if ($('.container-check').is(':checked') == true) {
//        $('#chk-containers').prop('checked', false)
//        $('.container-check').prop('checked', false)
//        selectedContainers = [];
//    } else {
//        var containers = $('.container-check');
//        for (var i = 0; i <= $('.container-check').length - 1; i++) {
//            selectedContainers.push($(containers[i]).attr('data'));
//        }
//        $('#chk-containers').prop('checked', true)
//        $('.container-check').prop('checked', true)
//    }
//}
//
//function checkContainer(name) {
//    //console.log(name)
//    var index = selectedContainers.indexOf(name);
//    if (index == -1) {
//        selectedContainers.push(name)
//    } else {
//        selectedContainers.splice(index, 1)
//    }
//}
//
//
//function sequential_launchcontainer(naming_pattern_prefix, container_nr, left_to_be_done, image_alias, ACCORDION_ID) {
//    if (container_nr == left_to_be_done) {
//        $('#loader').show();
//        $('#btn-create-container').prop("disabled", true);
//        $('#btn-create-container').text(' Spinning up ...');
//    }
//    if (left_to_be_done > 0) {
//        var container_suffix_nr = (container_nr - left_to_be_done) + 1;
//
//        $.post(API + 'launch-container',
//            {
//                containerName: naming_pattern_prefix + container_suffix_nr,
//                img_alias: image_alias
//            },
//            function (response) {
//                if (response.move_next) {
//                    if (response.success) {
//                        toastr.success(response.payload);
//                    }
//                    else {
//                        toastr.error(response.payload);
//                    }
//
//                    left_to_be_done = left_to_be_done - 1;
//                    sequential_launchcontainer(naming_pattern_prefix, container_nr, left_to_be_done, image_alias, ACCORDION_ID)
//                }
//                else {
//                    toastr.error(response.payload, "!!! WARNING !!!");
//                    $('#accordion [id="' + ACCORDION_ID + '"] ').parent().css("background-color", "rgba(178,34,34,0.1)");
//                    $('#loader').hide();
//
//                    tasks_required -= 1;
//                    if (tasks_required == 0) {
//                        $('#btn-create-container').text(' Bulk process finished !!!');
//                        $('#btn-cancel').hide();
//                        window.setTimeout(function () { window.location.replace(API + 'containers'); }, 3000);
//                    }
//
//                }
//            })
//    }
//    else {
//        tasks_required -= 1;
//        $('#loader').hide();
//        $('#accordion [id="' + ACCORDION_ID + '"] ').parent().fadeOut();
//        //toastr.info('Finished BULK PROCESS of INSTANCE CREATION of ['+container_nr+'] containers; with prefix <'+naming_pattern_prefix+'> and LXC Image OS <'+image_alias+'>!');
//    }
//
//    if (tasks_required == 0) {
//        $('#btn-create-container').text(' Bulk process finished !!!');
//        $('#btn-cancel').hide();
//        window.setTimeout(function () { window.location.replace(API + 'containers?auto_refresh'); }, 3000);
//    }
//}
//
//function start_instancecreation(NAMING_PATTERN_PREFIX, CONTAINER_NR, IMG_ALIAS, ACCORDION_ID) {
//    //check if image exists
//    $.post(API + 'check-image', { img_alias: IMG_ALIAS },
//        function (response) {
//            toastr.info('Bulk process of [' + CONTAINER_NR + '] container launching via the naming pattern <' + NAMING_PATTERN_PREFIX + '> targeting the LXC image <' + IMG_ALIAS + '> has just been initiated !');
//
//            if (response.image_exists == false) {
//                toastr.warning('Image <' + IMG_ALIAS + '> will be auto-downloaded as a pre-condition !');
//            }
//
//            sequential_launchcontainer(NAMING_PATTERN_PREFIX, CONTAINER_NR, CONTAINER_NR, IMG_ALIAS, ACCORDION_ID)
//        })
//}
//
//function createContainer() {
//    tasks_required = selectedImages.length;
//
//    for (var i = 0; i <= (tasks_required - 1); i++) {
//        var containerName_pre = $('#accordion [id="' + i + '"] .containerName').val();
//        var container_count = parseInt($('#accordion [id="' + i + '"] .cntNrs').val());
//        var image_alias = $('#accordion [id="' + i + '"] .img_alias').val();
//
//        setTimeout(start_instancecreation(containerName_pre, container_count, image_alias, i), 1000);
//    }
//}
//
//function refresh_ipv4_of(container_name) {
//    $.get(API + 'container-ip/' +  { containerName: container }, function (response) {
//        $('.ip_' + response.container_name).text(response.IP);
//    })
//}
//
////ACTIONS of container
//function startContainer() {
//    selectedContainers.forEach(function (container) {
//    console.log('container', container);
//    console.log('selected containers', selectedContainers)
//        $.put(API + 'container/start/'+ container, function (response) {
//        console.log('data', data);
//            if(response.status==200) {
//                $('.status_' + response.container_name).text("Running");
//                $('.ip_' + container).text(response.ip);
//                refresh_ipv4_of(response.container_name);
//                toastr.success(response.message);
//            }
//            else {
//                toastr.error(response.message, "CONTAINER ERROR");
//            }
//        })
//    })
//}
//
//function stopContainer() {
//    selectedContainers.forEach(function (container) {
//        $.post(API + 'container/stop' + { containerName: container }, function (response) {
//            if (response.success) {
//                $('.status_' + response.container_name).text("Stopped");
//                $('.ip_' + container).text("N/A");
//            }
//        })
//    })
//}
//
//function restartContainer() {
//    selectedContainers.forEach(function (container) {
//
//        if($('.status_' + container).text() != "Stopped")
//        {
//            $('.status_' + container).text("Restarting...");
//
//            document.getElementById("cnt_" + container).style.backgroundColor = "rgba(89,161,255,0.1)";
//
//            $.post(API + 'container/restart'+ { containerName: container }, function (response) {
//                if (response.success) {
//                    $('.status_' + response.container_name).text("Running");
//                    document.getElementById("cnt_" + response.container_name).style.backgroundColor = "white";
//                }
//            })
//        }
//        else
//        {
//            toastr.error("Container <"+container+"> can not be restarted because it's a stopped container !");
//        }
//    })
//}
//
//function deleteContainer() {
//    selectedContainers.forEach(function (container) {
//
//        $('.status_' + container).text("Deleting...");
//        target_cnt = "cnt_" + container;
//        document.getElementById(target_cnt).style.backgroundColor = "rgba(178,34,34,0.1)";
//
//        $.post(API + 'container/delete', { container }, function (response) { document.getElementById("cnt_" + response.container_name).remove(); })
//    })
//}
//$(function(){
//    showContainers();
//});