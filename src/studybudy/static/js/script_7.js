jQuery(document).ready(function( $ ) {
    var oldPassword         = $("#password-old");
    var newPassword         = $("#password-new");
    var confirmPassowrd     = $("#password-confirm");
    var error               = $('.error');
    var change              = $('#changeBtn');




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
