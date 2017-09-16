var selectedContainers = [];
var tasks_required = 0;

function checkAll() {
    if ($('.container-check').is(':checked') == true) {
        $('#chk-containers').prop('checked', false)
        $('.container-check').prop('checked', false)
        selectedContainers = [];
    } else {
        var containers = $('.container-check');
        for (var i = 0; i <= $('.container-check').length - 1; i++) {
            selectedContainers.push($(containers[i]).attr('data'));
        }
        $('#chk-containers').prop('checked', true)
        $('.container-check').prop('checked', true)
    }
}

function checkContainer(name) {
    //console.log(name)
    var index = selectedContainers.indexOf(name);
    if (index == -1) {
        selectedContainers.push(name)
    } else {
        selectedContainers.splice(index, 1)
    }
}


function sequential_launchcontainer(naming_pattern_prefix, container_nr, left_to_be_done, image_alias, ACCORDION_ID) {
    if (container_nr == left_to_be_done) {
        $('#loader').show();
        $('#btn-create-container').prop("disabled", true);
        $('#btn-create-container').text(' Spinning up ...');
    }
    if (left_to_be_done > 0) {
        var container_suffix_nr = (container_nr - left_to_be_done) + 1;

        $.post(API + 'launch-container',
            {
                containerName: naming_pattern_prefix + container_suffix_nr,
                img_alias: image_alias
            },
            function (response) {
                if (response.move_next) {
                    if (response.success) {
                        toastr.success(response.payload);
                    }
                    else {
                        toastr.error(response.payload);
                    }

                    left_to_be_done = left_to_be_done - 1;
                    sequential_launchcontainer(naming_pattern_prefix, container_nr, left_to_be_done, image_alias, ACCORDION_ID)
                }
                else {
                    toastr.error(response.payload, "!!! WARNING !!!");
                    $('#accordion [id="' + ACCORDION_ID + '"] ').parent().css("background-color", "rgba(178,34,34,0.1)");
                    $('#loader').hide();

                    tasks_required -= 1;
                    if (tasks_required == 0) {
                        $('#btn-create-container').text(' Bulk process finished !!!');
                        $('#btn-cancel').hide();
                        window.setTimeout(function () { window.location.replace(API + 'containers'); }, 3000);
                    }

                }
            })
    }
    else {
        tasks_required -= 1;
        $('#loader').hide();
        $('#accordion [id="' + ACCORDION_ID + '"] ').parent().fadeOut();
        //toastr.info('Finished BULK PROCESS of INSTANCE CREATION of ['+container_nr+'] containers; with prefix <'+naming_pattern_prefix+'> and LXC Image OS <'+image_alias+'>!');        
    }

    if (tasks_required == 0) {
        $('#btn-create-container').text(' Bulk process finished !!!');
        $('#btn-cancel').hide();
        window.setTimeout(function () { window.location.replace(API + 'containers?auto_refresh'); }, 3000);
    }
}

function start_instancecreation(NAMING_PATTERN_PREFIX, CONTAINER_NR, IMG_ALIAS, ACCORDION_ID) {
    //check if image exists
    $.post(API + 'check-image', { img_alias: IMG_ALIAS },
        function (response) {
            toastr.info('Bulk process of [' + CONTAINER_NR + '] container launching via the naming pattern <' + NAMING_PATTERN_PREFIX + '> targeting the LXC image <' + IMG_ALIAS + '> has just been initiated !');

            if (response.image_exists == false) {
                toastr.warning('Image <' + IMG_ALIAS + '> will be auto-downloaded as a pre-condition !');
            }

            sequential_launchcontainer(NAMING_PATTERN_PREFIX, CONTAINER_NR, CONTAINER_NR, IMG_ALIAS, ACCORDION_ID)
        })
}

function createContainer() {
    tasks_required = selectedImages.length;

    for (var i = 0; i <= (tasks_required - 1); i++) {
        var containerName_pre = $('#accordion [id="' + i + '"] .containerName').val();
        var container_count = parseInt($('#accordion [id="' + i + '"] .cntNrs').val());
        var image_alias = $('#accordion [id="' + i + '"] .img_alias').val();

        setTimeout(start_instancecreation(containerName_pre, container_count, image_alias, i), 1000);
    }
}

function refresh_ipv4_of(container_name) {
    $.get(API + 'container-ip/' + container_name, function (response) {
        $('.ip_' + response.container_name).text(response.IP);
    })
}

//ACTIONS of container
function startContainer() {
    selectedContainers.forEach(function (container) {
        $.post(API + 'start', { containerName: container }, function (response) {
            if (response.success) {
                $('.status_' + response.container_name).text("Running");
                $('.ip_' + container).text(response.ip);
                refresh_ipv4_of(response.container_name);
            }
            else {
                toastr.error(response.message, "CONTAINER ERROR");
            }
        })
    })
}

function stopContainer() {
    selectedContainers.forEach(function (container) {
        $.post(API + 'stop', { containerName: container }, function (response) {
            if (response.success) {
                $('.status_' + response.container_name).text("Stopped");
                $('.ip_' + container).text("N/A");
            }
        })
    })
}

function restartContainer() {
    selectedContainers.forEach(function (container) {

        if($('.status_' + container).text() != "Stopped")
        {
            $('.status_' + container).text("Restarting...");

            document.getElementById("cnt_" + container).style.backgroundColor = "rgba(89,161,255,0.1)";

            $.post(API + 'restart', { containerName: container }, function (response) {
                if (response.success) {
                    $('.status_' + response.container_name).text("Running");
                    document.getElementById("cnt_" + response.container_name).style.backgroundColor = "white";
                }
            })
        }
        else
        {
            toastr.error("Container <"+container+"> can not be restarted because it's a stopped container !");
        }
    })
}

function deleteContainer() {
    selectedContainers.forEach(function (container) {

        $('.status_' + container).text("Deleting...");
        target_cnt = "cnt_" + container;
        document.getElementById(target_cnt).style.backgroundColor = "rgba(178,34,34,0.1)";

        $.post(API + 'delete', { containerName: container }, function (response) { document.getElementById("cnt_" + response.container_name).remove(); })
    })
}