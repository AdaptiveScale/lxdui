//function LoginScreen(){
//    return {
//        loading: false,
//        username: '',
//        password: '',
//        error:false,
//        errorMessage: '',
//        init: function(){
//            $('.btn-login').on('click', $.proxy(this.onLogin, this));
//        },
//        onLogin: function(event){
//            console.log('args', arguments);
//        }
//    }
//});

//$(function(){
//    $('.btn-login').on('click', function(e){
//        e.preventDefault();
//        $.ajax({
//            url:API+'user/login',
//            method:'POST',
//            contentType: "application/json; charset=utf-8",
//            dataType:'json',
//            data:JSON.stringify({
//               username:$('#username').val(),
//               password:$('#password').val()
//            }),
//            success: function (response) {
//                localStorage.setItem('authToken', response.access_token);
//                window.location = WEB + 'containers'
//            },
//            error:function(response){
//                console.log('err', response);
//            }
//        });
//    });
//});

App.login = App.login || {
    init: function(){
        console.log('Login initialized');
        $('.btn-login').on('click',$.proxy(this.doLogin, this));
    },
    doLogin: function(e){
        e.preventDefault();
        var data = JSON.stringify({
            username:$('#username').val(),
            password:$('#password').val()
        });
        $.ajax({
            url:App.baseAPI+'user/login',
            method:'POST',
            contentType: "application/json; charset=utf-8",
            dataType:'json',
            data:data,
            success: $.proxy(this.doLoginSuccess, this),
            error:$.proxy(this.doLoginError, this)
        });
//        $.post(App.baseAPI+'user/login', data, $.proxy(this.doLoginSuccess, this), 'json');
    },
    doLoginSuccess: function(response){
        console.log('loginSuccess', response, this, App);
        localStorage.setItem('authToken', response.access_token);

        window.location = App.baseWEB + 'containers';
    },
    doLoginError: function(error){
        if(!$('.alert').hasClass('hidden')) {
            $('.alert').addClass('hidden');
        }
        if(error.status == 401) {
            $('.msg').text('Check username and password');
            var parent = $('.msg').parent().removeClass('hidden');
        }
    },
    doLogout: function() {
        localStorage.removeItem('authToken');
        window.location = App.baseWEB;
    }
}