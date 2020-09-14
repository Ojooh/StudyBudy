jQuery(document).ready(function( $ ) {
    var error               = $('.error');
    var loginBtn            = $('.loginBtn');
    var oldPassword         = $("#password-old");
    var newPassword         = $("#password-new");
    var confirmPassowrd     = $("#password-confirm");
    var change              = $('#changeBtn');





    loginBtn.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        error.html("");
        var url                        = $(this).attr("data-url");
        var username                   = $('#username').val();
        var password                   = $('#password').val();
        var emailRegex                 = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i;
        var usernameRegex              = /^[A-Z]+[-]+[0-9]+[0-9]$/i;
        var msg                        = "";
    
        if (username == "" || password == ""){
            msg = "<span class='alert alert-success'>Please enter a valid username and passsword</span>";
            error.html(msg);
        }
        else if (usernameRegex.test(username) == false && emailRegex.test(username) == false){
            msg = "<span class='alert alert-success'>Enter a valid username</span>";
            error.html(msg);
        }
        else{
            error.html("");
            var data = {
                'username': username,
                'password': password,
            }
            
            $.ajax({
                url: url,
                data: data,
                success: function (data) {
                    if ("url" in data){
                        Swal.fire("Login Details Correct, Welcome", "Click OK to proceed to Dashoboard", "success").then(
                            function(){
                                window.location = data.url;
                            }
                        )
                    }
                    else{
                        msg = "<span class='alert alert-success'>" + data.error + "</span>";
                        error.html(msg);
                    }
                    
                }
             });
        }
    });


    change.on("click", function(e) {
        var old       = oldPassword.val();
        var nw        = newPassword.val();
        var confirm   = confirmPassowrd.val();
        var url       = $(this).attr("data-url");

        if(old == "" || nw == "" || confirm == ""){
            msg = "<span class='alert alert-success'>All fields are compulsory</span>";
            error.html(msg);
        }
        else if (nw.length <= 6){
            msg = "<span class='alert alert-success'>Passowrd character length must be more than 6</span>";
            error.html(msg);
        }
        else if(nw == old){
            msg = "<span class='alert alert-success'>Please enter a new password</span>";
            error.html(msg);
        }
        else if (nw != confirm){
            console.log(nw)
            console.log(confirm)
            msg = "<span class='alert alert-success'>Confirm New password Field does not match</span>";
            error.html(msg);
        } else {
            error.html("")
            var data = {
                'old': old,
                'new': confirm,
            };

            $.ajax({
                url: url,
                data: data,
                success: function (data) {
                    if ("url" in data){
                        Swal.fire("Password Details Changed, Welcome", "Click OK to proceed to Dashoboard", "success").then(
                            function(){
                                window.location = data.url;
                            }
                        )
                    }
                    else{
                        msg = "<span class='alert alert-success'>" + data.error + "</span>";
                        error.html(msg);
                    }
                    
                }
             });
        }
        

    });
    


});







