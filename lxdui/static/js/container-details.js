function single_container_manager(container_name, status_running)
{
    var obj = {};
    obj.container_name = container_name;
    obj.status_running = (status_running == "RUNNING") ? true : false;
    obj.buttons_div = "container_details_buttons";

    obj.render_buttons = function (){
        var this_content = ""
        if (this.status_running) {
            this_content += '<button class="btn btn-default btn-stop_container" onclick="cm_this_container.stop_container()"> <span class="glyphicon glyphicon-stop"> </span> Stop</button> ';
            this_content += '<button class="btn btn-default btn-restart_container" onclick="cm_this_container.restart_container()"> <span class="glyphicon glyphicon-repeat"> </span> Restart </button> '
        }
        else {
            this_content += '<button class="btn btn-default btn-start_container" onclick="cm_this_container.start_container()"><span class="glyphicon glyphicon-play"> </span> Start </button> ';
        }
        this_content += '<button class="btn btn-default btn-delete_container" onclick="cm_this_container.delete_container()"><span class="glyphicon glyphicon-remove-sign"> </span> Delete</button> ';

        $('#' + this.buttons_div).html(this_content);
    }
    obj.start_container = function () {
        $('.btn-stop_container').text("Starting...").prop('disabled', true);
        $.post(API + 'start', { containerName: this.container_name }, function (response) {
            if (response.success) {
                window.location.replace(API + 'container/'+response.container_name+'?auto_refresh');
            }
            else {
                toastr.error(response.message, "CONTAINER ERROR");
            }
        })
    };
    obj.stop_container = function () {
        $('.btn-stop_container').text("Stopping...").prop('disabled', true);
        $.post(API + 'stop', { containerName: this.container_name }, function (response) {
            
            if (response.success) {
                location.reload(); 
            }
            else {
                toastr.error(response.message, "CONTAINER ERROR");
            }
        })
    };
    obj.restart_container = function () {
        $('.btn-restart_container').text("Restarting...").prop('disabled', true);
        $('.status_' + this.container_name).removeClass("label-success").text("RESTARTING").addClass("label-info");

        $.post(API + 'restart', { containerName: this.container_name }, function (response) {
            if (response.success) {
                $('.status_' + response.container_name).removeClass("label-info").text("RUNNING").addClass("label-success");
                $('.btn-restart_container').prop('disabled', false).text("Restart");
            }
            else {
                toastr.error(response.message, "CONTAINER ERROR");
            }
        })
    }
    obj.delete_container = function () {
        $('.btn-delete_container').text("Deleting...").css('backgroundColor', 'rgba(178,34,34,0.1)');
        $('.btn-delete_container').prop('disabled', true);
        $.post(API + 'delete', { containerName: this.container_name }, function (response) { window.location.replace(API + 'containers'); })
    };
    
    return obj;
}
