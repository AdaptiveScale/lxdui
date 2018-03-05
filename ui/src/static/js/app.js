const API = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '')+"/";

function formatBytes(bytes){
  var kb = 1024;
  var ndx = Math.floor( Math.log(bytes) / Math.log(kb) );
  var fileSizeTypes = ["BYTES", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
  return (bytes / kb / kb).toFixed(2) + ' '+ fileSizeTypes[ndx];
}

function changeNumberOfContainers(index, val){
    var n = parseInt($(val).val());
    var ndz = "Node";
    if (n > 1)
    {
        ndz = "Nodes";
    }

    $('.nrOfNodes_'+index).text($(val).val() + ' '+ ndz);
}


function showContainers(){
    var html = '';
    $.post(API + 'containers-list', function (response) {
        if(response.success)
        { 
            response.payload.forEach(function (container) {
            html+=`<tr id="cnt_${container.name}"><td><input type="checkbox" data="${container.name}" class="container-check" onchange="checkContainer('${container.name}')"></td>`
                  +`<td><a href="/container/${container.name}" style="cursor:pointer">${container.name}</td>`
                  +`<td class="status_${container.name}">${container.status}</td>`
                  +`<td class="ip_${container.name}">${container.ipaddress}</td>`
                  +`<td>${container.OS.name} ${container.OS.release} (${container.OS.architecture})</td>`
                  +`<td>${container.created_at}</td>`
                +`</tr>`;
            })
            $('#tbl-containers tbody').html(html);
        }
        else
        {
            $('#tbl-containers tbody').parent().parent().append('<div class="alert alert-danger" role="alert">'+response.payload+'</div>');
        }
    })
}

function showContainerDetails(name) {
        HTML.set('containers-set-id', 'cmp-container-details', function (cb) {
            $.post(API + 'container-details/'+name, function (response) {
                $('#name').text(response.hostname)
                $('#architecture').text(response.architecture)
                $('#created_at').text(response.created_at)
                $('#status').text(response.status)
                $('#profiles').text(response.profiles[0])
                if(response.network){
                    $('#inet').text(response.network['eth0']['addresses'][0].address || 'N/A')
                    $('#inet6').text(response.network['eth0']['addresses'][1].address)
                    $('#inet6-1').text(response.network['eth0']['addresses'][2].address)
                    $('#lo-inet').text(response.network['lo']['addresses'][0].address)
                    $('#lo-inet6').text(response.network['lo']['addresses'][1].address)
                    $('#pid').text(response.pid)
                    $('#processes').text(response.processes)
                }else{
                    $('.running').text('N/A')
                }
            });
        })
}