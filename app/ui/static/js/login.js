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
    },
    doLoginSuccess: function(response){
        sessionStorage.setItem('authToken', response.access_token);
        sessionStorage.setItem('user', JSON.stringify({
            username:$('#username').val(),
            password:$('#password').val()
        }));
        window.location = App.baseWEB + 'containers';
    },
    doLoginError: function(error){
        if(!$('.error-div').hasClass('hidden')) {
            $('.error-div').addClass('hidden');
        }
        if(error.status == 401) {
            $('.msg').text('Check username and password');
            var parent = $('.msg').parent().parent().removeClass('hidden');
        }
    },
    doLogout: function() {
        sessionStorage.removeItem('authToken');
        window.location = App.baseWEB;
    }
}