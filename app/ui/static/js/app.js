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
    network: null,
    loading: false,
    notInitialized:['containers', 'images', 'network'],
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
        console.log('App initialized');
        this.getInfo();
    },
    getInfo: function(){
        $.ajax({
            url: this.baseAPI+'lxd/config',
            method:'GET',
            success: $.proxy(this.getInfoSuccess, this)
        });
    },
    getInfoSuccess:function(response){
        this.info = response.data;
        $('#stamplike').text('LXD Version: ' + this.info.environment.server_version);
    },
    setDefaultHeaders: function(){
        console.log('locaiton', window.location.href, WEB);
        if(!localStorage.getItem('authToken') && window.location.href!==WEB){
            console.log('Not Logged In/Token Expired - Redirecting to login');
            return window.location = WEB;
        }
        if(window.location.href!==WEB){
            console.log('Setting Authorization header', localStorage.getItem('authToken'));
            $.ajaxSetup({
                headers:{
                    Authorization:'JWT '+localStorage.getItem('authToken')
                },
                complete: function(response){
                    if(response.status == 401 && window.location!== WEB){
                        window.location = WEB;
                    }
                }
            });
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
    }
};

$(function(){
    App.init();
});