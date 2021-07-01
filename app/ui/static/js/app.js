const API = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '')+"/api/";
const WEB = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '')+"/ui/";

var App = App || {
    baseAPI: API,
    baseWEB: WEB,
    info:null,
    lxdVersion: 'NO LXC INSTALLED',
    login:null,
    containers: null,
    images: null,
    ongoingOperation: 0,
    network: null,
    location: null,
    loading: false,
    tokenRefreshing: false,
    notInitialized:['containers', 'images', 'network', 'containerDetails', 'storagePool'],
    init: function(){
        console.log('App initializing');
        this.setDefaultHeaders();

        if(this.login && window.location == WEB)
            this.login.init();
        if(this.containers && window.location.href.startsWith(WEB +'containers'))
            this.containers.init();
        if(this.containers && window.location.href.startsWith(WEB +'images'))
            this.images.init();
        if(this.containers && window.location.href.startsWith(WEB +'profiles'))
            this.profiles.init();
        if(this.containers && window.location.href.startsWith(WEB +'network'))
            this.network.init();
        if(this.containers && window.location.href.startsWith(WEB +'containers/'))
            this.containerDetails.init();
        if(this.containers && window.location.href.startsWith(WEB +'storage-pools'))
            this.storagePool.init();

        console.log('App initialized');
        this.getInfo();
        $('.buttonLogout').on('click', $.proxy(this.login.doLogout, this.login));

    },
    getInfo: function(){
        $.ajax({
            url: this.baseAPI+'lxd/config',
            method:'GET',
            success: $.proxy(this.getInfoSuccess, this),
            error: $.proxy(this.getInfoError, this),
        });
    },
    getInfoSuccess:function(response){
        this.info = response.data;
        this.lxdVersion = this.info.environment.server_version;
        $('#stamplike').text('LXD Version: ' + this.lxdVersion);
        $('#stamplike').removeClass('label-danger').addClass('label-success');
    },
    getInfoError:function(response) {
        $('#stamplike').text('LXD is not Installed').removeClass('label-success').addClass('label-danger');
    },
    setDefaultHeaders: function(){
        if(!sessionStorage.getItem('authToken') && window.location.href!==WEB){
            console.log('Not Logged In/Token Expired - Redirecting to login');
            return window.location = WEB;
        }
        if(window.location.href!==WEB){
            $.ajaxSetup({
                headers:{
                    Authorization:'Bearer '+sessionStorage.getItem('authToken'),
//                    'Content-Type':'application/json' //commented for file upload as temporary workaround
                },
                beforeSend: function(xhr, settings) {
                    App.ongoingOperation +=1;
                    $('.loader').show();
                },
                complete: function(response){
                    App.ongoingOperation -=1;
                    if(response.status == 401 && window.location!== WEB){
                        window.location = WEB;
                    }
                    if((App.helpers.parseJwt(sessionStorage.getItem('authToken')).exp-App.helpers.currentAppTime())<120){
                        if(!App.tokenRefreshing){
                            App.updateTokenExpiration.call(App);
                        }
                    }
                    if(App.ongoingOperation ==0)
                        $('.loader').hide();
                    if(App.tokenRefreshing){
                        return;
                    }
                    if(window.location!== WEB){
                        App.triggerAlert(response, this.type, this.url);
                    }
                }
            });
        }
    },
    updateTokenExpiration: function(){
        App.tokenRefreshing = true;
        $.ajax({
            url:App.baseAPI+'user/refresh',
            method:'POST',
            contentType: "application/json; charset=utf-8",
            dataType:'json',
            data:sessionStorage.getItem('user'),
            success: $.proxy(this.tokenUpdateSuccess, this)
        });
    },
    tokenUpdateSuccess:function(response){
        sessionStorage.removeItem('authToken');
        document.cookie = 'access_token_cookie' + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        sessionStorage.setItem('authToken', response.access_token);
        document.cookie = "access_token_cookie" + "=" + response.access_token + ";path=/";
        App.tokenRefreshing=false;
    },
    setActiveLink: function(name) {
        $('.nav li').removeClass('active');
        $('.'+name+'-menu').addClass('active');
    },
    triggerAlert: function(response, method, url){
        if(url.endsWith('login')){
            return;
        }
        if([undefined, 'GET'].indexOf(method)>-1)
            return;
        var tempResp = response.responseJSON || response;
        if(response.status !== 200){
            toastr.error(response.responseJSON.message || 'Unknown error', response.statusText||'Error');
        }else{
            toastr.success(response.responseJSON.message, 'Success');
        }
    },
    formatBytes:function(bytes){
      var kb = 1024;
      var ndx = Math.floor( Math.log(bytes) / Math.log(kb) );
      var fileSizeTypes = ["BYTES", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
      return (bytes / kb / kb).toFixed(2) + ' '+ fileSizeTypes[ndx];
    },
    mergeProps:function(source, destination){
         for(var prop in source){
             destination[prop]=source[prop]
         }
         return destination;
    },
    helpers:{
        capitalizeFirstLetter: function(value){
            return value.charAt(0).toUpperCase() + value.slice(1);
        },
        currentAppTime: function(){
            return Math.floor(new Date().getTime()+new Date().getTimezoneOffset())/1000;
        },
        parseJwt: function(token) {
            var base64Url = token.split('.')[1];
            var base64 = base64Url.replace('-', '+').replace('_', '/');
            return JSON.parse(window.atob(base64));
        },
        extractIP(value){
            result = value.match(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/);
            return (result)?result[0]:'N/A';
        },
        extractPort(value){
            result = value.substring(value.lastIndexOf(':')+1, value.length);
            return result || 'N/A';
        }
    }
};

$(function(){
    App.init();
});
