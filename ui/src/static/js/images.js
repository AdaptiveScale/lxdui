var selectedImages = [];
var display_img_names = [];

var LOCAL_IMAGES = {};
var LOCAL_IMG_TOTAL = 0;
var LOCAL_PAGE = true;


function loadImages(lxd_host){
    $("#btn-launch").hide();
    $("#btn-delete").hide();
    selectedImages = [];
    display_img_names = [];
    

    if(lxd_host != 'local')
    {
        LOCAL_PAGE = false;
        $('#chk-images').hide();
        $('#btn-update-remote').show();
        $.get(API + 'remote-images', displayImages);
        
    }
    else
    {
        LOCAL_PAGE = true;
        $('#chk-images').show();
        $('#btn-update-remote').hide();
        $.get(API + 'local-images', displayImages);
    }
}
function capitalize(s)
{
    return s && s[0].toUpperCase() + s.slice(1);
}

function displayImages(response){
    var html = '';
    response.payload.forEach(function (image) {

        var d_name = capitalize(image.properties.distribution);

        html+=`<tr id="img_${image.aliases.name}"><td><input type="checkbox" class="images-check" data="${image.aliases.name}" display_name='${d_name} ${image.properties.release} (${image.properties.architecture})' onchange="selectImage('${image.aliases.name}', '${d_name} ${image.properties.release} (${image.properties.architecture})')"></td>`
        + `<td><a style="cursor:pointer" onclick="selectImage('${image.aliases.name}', '${d_name} ${image.properties.release} (${image.properties.architecture})'), showCreateContainer()">${image.properties.distribution}</a></td>`
        + `<td>${image.properties.description}</td>`
        + `<td>${image.aliases.name}</td>`
        + `<td>${image.properties.release}</td>`
        + `<td>${image.properties.architecture}</td>`
        + `<td>${formatBytes(`${image.size}`)}</td></tr>`;
    })
    $('#tbl-images tbody').html(html);
}

function selectAllImages()
{
    selectedImages = [];
    display_img_names = [];

    if($('.images-check').is(':checked') == true)
    {
        $('#chk-images').prop('checked', false)
        $('.images-check').prop('checked', false)
        //hide the buttons
        $("#btn-launch").hide();
        if (LOCAL_PAGE) $("#btn-delete").hide(); 
    }
    else
    {   
        $('#chk-images').prop('checked', true);
        $('.images-check').prop('checked', true);

        var images = $('.images-check');
        for (var i = 0; i <= $('.images-check').length - 1; i++)
        {
            var alias = $(images[i]).attr('data');
            var dp_img_name = $(images[i]).attr('display_name');
            selectImage(alias, dp_img_name);
        }
    }
}


var imagesData = {};

function selectImage(alias, display_name)
{
    var indexOfArr = selectedImages.indexOf(alias);
    if(indexOfArr == -1)
    {
        selectedImages.push(alias);
        display_img_names.push(display_name);
    }
    else
    {  
        selectedImages.splice(indexOfArr, 1);
        display_img_names.splice(indexOfArr, 1);
    }  
    //console.log(display_img_names.join())

    if(selectedImages.length > 0)
    {
        $("#btn-launch").show();
        if (LOCAL_PAGE) $("#btn-delete").show();
    }
    else
    {
        $("#btn-launch").hide();
        if (LOCAL_PAGE) $("#btn-delete").hide(); 
    }

}

function deleteLocalImage(){
    selectedImages.forEach(function (img) {
        var target_img = 'img_'+img;
        document.getElementById(target_img).style.backgroundColor = "rgba(178,34,34,0.1)";
        //we are deleting it in the backend
        $.post(API + 'delete-image', { image_alias: img}, function (response) {
            if(response.success)
            {   
                LOCAL_IMG_TOTAL = LOCAL_IMG_TOTAL - 1;
                var indexOfArr = selectedImages.indexOf(img);
                //remove from list
                selectedImages.splice(indexOfArr, 1);
                display_img_names.splice(indexOfArr, 1);

                //needs refactoring
                if(selectedImages.length < 1)
                {
                    $("#btn-launch").hide();
                    if (LOCAL_PAGE) $("#btn-delete").hide(); 
                }
                else
                {
                    $("#btn-launch").show();
                    if (LOCAL_PAGE) $("#btn-delete").show();
                }
                
                setTimeout(function () { 
                    $('#local_img_nr').html('local <span class="badge">'+LOCAL_IMG_TOTAL+'</span>');
                    document.getElementById("img_"+response.img_alias).remove(); }, 1500);
            }
        })
    })
}

function update_remote_image_list()
{
    $("#loader-update-img").show();
    toastr.warning("Updating the linux official REMOTE IMAGE list is a LONG-PROCESS which usually takes more than 2 minutes (depending on your internet connection) !", "! UPDATE INITIATED !");
    
    $.get(API + 'update-remote-images', function (response) {
        toastr.success(response.payload);
        $("#loader-update-img").hide();
        loadImages('remote');
    });
}