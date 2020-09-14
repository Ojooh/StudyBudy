jQuery(document).ready(function( $ ) {
    var error                   = $('.error');
    var toggleNav               = $('.toggle-nav');
    var sideMenuToggler         = $(".sideMenuToggler");
    var window_width            = $(window).width();
    var ckeeditorArea           = CKEDITOR.instances.editor2;
    var elementFocus            = [];
    var elementState            = false
    var ckayForm                = $('#editor-form');
    var saveFile                = $('.save-file');


    elementFocus.push(data.length);
    $(".loading-bar").addClass("deactivated");
    $(".ckay").removeClass("deactivated");
    var view_status = "edit";

    if ( view_status == "view"){
        $("#cke_1_top").css({
            'display': 'none',
        });
        ckayForm.attr("data-id", data[1]);
        ckeeditorArea.setData(data[0]);
        
    }
    else{
        $("#cke_1_top").css({
            'display': 'block',
        });
        ckayForm.attr("data-id", data[1]);
        ckeeditorArea.setData(data[0]);
    }

    function saveNoteData(formdata, url, new_length){
        $.ajax({
            url: url,
            type: 'post',
            data: formdata,
            contentType: false,
            processData: false,
            dataType: 'json',
            success: function(data){
                if ("error" in data){
                    $(".loading-bar").addClass("deactivated");
                    $("#ediitViewFileModalLabel").html("Error");
                    error.removeClass("deactivated");
                    msg = "<span class='alert alert-success'>" + data.error + "</span>";
                    error.html(msg);
                } else {
                    elementFocus[0] = new_length;
                    Swal.fire(data.success, "Click OK to proceed to Dashoboard", "success").then(
                        function(){
                            console.log("SUccesss");
                            // location.reload();
                        }
                    )
                }
            }
        });
    }

    $(document).on("click", function(e){
        e.target;
    });

    toggleNav.on('click', function () {
        if ($("#sidebar").hasClass("reduce")){
            if ($('#sidebar > ul').is(":visible") === true) {
                $('#main-content').css({
                    'margin-left': '0px'
                });
                $('#sidebar').css({
                    'margin-left': '-80px',
                    'z-index'       : '9'
                });
                $('#sidebar > ul').hide();
                $("#container").addClass("sidebar-closed");
            } else {
                if (window_width < 1025) {
                    $('#main-content').css({
                        'margin-left'   :'0px',
                       
                    });
                } else {
                    $('#main-content').css({
                        'margin-left': '80px'
                    });
                }
                
                $('#sidebar > ul').show();
                $('#sidebar').css({
                    'margin-left'   : '0',
                    'z-index'       : '9'
                });
                $("#container").removeClass("sidebar-closed");
            }
        }
        else {
            if ($('#sidebar > ul').is(":visible") === true) {
                $('#main-content').css({
                    'margin-left': '0px'
                });
                $('#sidebar').css({
                    'margin-left'   : '-250px',
                    'z-index'       : '9'
                });
                $('#sidebar > ul').hide();
                $("#container").addClass("sidebar-closed");
            } else {
                if (window_width < 1025) {
                    $('#main-content').css({
                        'margin-left'   : '0px',
                    });
                } else {
                    $('#main-content').css({
                        'margin-left': '250px'
                    });
                }
                
                $('#sidebar > ul').show();
                $('#sidebar').css({
                    'margin-left'   : '0',
                    'z-index'       : '9'
                });
                $("#container").removeClass("sidebar-closed");
            }
        }
        
    });

    sideMenuToggler.on("click", function(e) {
        e.preventDefault();
        $("#sidebar").toggleClass("reduce");
        if ( $(".fas").hasClass("fa-angle-double-left")){
            $(".fas").removeClass("fa-angle-double-left");
            $(".fas").addClass("fa-angle-double-right");
            
            if (window_width < 1025) {
                $('#sidebar').css({
                    'z-index'       : '9'
                });
                $('#main-content').css({
                    'margin-left'   : '0px',
                });
            } else {
                $('#main-content').css({
                    'margin-left': '80px'
                });
            }
        } else {
            $(".fas").removeClass("fa-angle-double-right");
            $(".fas").addClass("fa-angle-double-left");
            
            if (window_width < 1025) {
                $('#sidebar').css({
                    'z-index'       : '9'
                });
                $('#main-content').css({
                    'margin-left'   : '0px',
                    
                });
            } else {
                $('#main-content').css({
                    'margin-left': '250px'
                });
            }
        }
           
    });

    ckeeditorArea.on("change", function(e){
        elementState = true;
    });

    saveFile.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();

        var new_data = ckeeditorArea.getData();
        
        if (new_data.length != elementFocus[0] || elementState){
            var url = ckayForm.attr("data-url");
            var ID  = ckayForm.attr("data-id");
            var fd  = new FormData();
            fd.append('file_id', ID );
            fd.append('file_data', new_data);
            console.log(ID);
            console.log(new_data);
            
            saveNoteData(fd, url, new_data.length);    
        }

    });



});