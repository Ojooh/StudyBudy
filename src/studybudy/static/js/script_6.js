jQuery(document).ready(function( $ ) {
    var error                   = $('.error');
    var toggleNav               = $('.toggle-nav');
    var sideMenuToggler         = $(".sideMenuToggler");
    var window_width            = $(window).width();
    var minimize                = $('.btn-minimize');
    var reminderDrop            = $('.drop-trigger-options');
    var editTask                = $('.edit_task');
    var editform                = $('#taskForm');
    var deleteTask              = $('.delet_task');
    var trashMove               = $('.yep');
    var modalWarning            = $('#warningModal');
    var complete                = $('.custom-control-input');

    if ((editform.attr("data-task") != undefined || editform.attr("data-task") != "") && (editform.attr("data-date") != undefined || editform.attr("data-date") != "") && (editform.attr("data-time") != undefined || editform.attr("data-time") != "") ){
        var task = editform.attr("data-task");
        var date = editform.attr("data-date");
        var time = editform.attr("data-time");

        $('#task').val(task);
        $('#date_scheduled').val(date);
        $('#time').val(time);
    }


    $(document).on("click", function(e){    

        $('.drop-meny').addClass("deactivated");

    });

    toggleNav.on('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
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
        e.stopPropagation();
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

    minimize.on("click", function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        var id      = $(this).attr("id");
        var heed    = ".body-" + id;
        var jip    = ".flip-" + id;
        var flip    = $(jip);
        $(heed).toggleClass("deactivated");

        if (flip.hasClass("fa-chevron-up")){
            console.log("okay");
            flip.removeClass("fa-chevron-up");
            flip.addClass("fa-chevron-down");
        } else {
            flip.removeClass("fa-chevron-down");
            flip.addClass("fa-chevron-up");
        }

    });

    reminderDrop.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var others      = $('.drop-meny');
        var id          = $(this).attr("id");
        var seed        = id.split("-");
        var jigi        = ".opy-" + seed[seed.length - 1];
        var slip        = $(jigi);
        var scrollTop   = $(window).scrollTop();
        
        var windowHeight = $(window).height();

        $.each(others, function(ky, vl){
            if ($(vl).attr("class") != slip.attr("class")){
                $(vl).addClass("deactivated");
            }
        });

        var topOffset   = slip.offset().top;
        var reloffset = topOffset-scrollTop;
        // if(reloffset < windowHeight/2){
        //     slip.addClass("reverse");
        // }
        // else{
        //     slip.removeClass("reverse");
        // }
        console.log(slip.attr("class"));
        slip.toggleClass("deactivated");
         
    });

    editTask.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var url = $(this).attr("data-url");
        console.log(url);

        window.location.href = url;
    });

    deleteTask.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var url = $(this).attr("data-url");
        var ID  = $(this).attr("data-id");
        var fileName = $(this).attr("data-name");
        trashMove.attr("data-url", url);
        trashMove.attr("data-id", ID);
        $('.modal-title').html("Delete " + fileName);
        $('.content-warning').html("<h4>Are you sure you want to Delete " + fileName + "</h4>");
        modalWarning.modal("show");
    });

    trashMove.on("click", function(e){
        var url  = $(this).attr("data-url");
        var ID   = $(this).attr("data-id");
        var data = {"ID": ID}

        $.ajax({                       
            url: url,                    
            data: data,
            success: function (data) {
                    if ("error" in data){
                        Swal.fire(data.error , "Click OK to proceed", "success").then(
                            function(){
                        });
    
                    }else {
                        Swal.fire(data.success , "Click OK to proceed", "success").then(
                            function(){
                            location.reload();
                        });
    
                    }   
            }
        });
    });

    complete.on("change", function(e){
        
        var url  = $(this).attr("data-url");
        var ID   = $(this).attr("data-id");
        var stat = $(this).val();
        var data = {"ID": ID, "status" : stat};

        $.ajax({                       
            url: url,                    
            data: data,
            success: function (data) {
                    if ("error" in data){
                        Swal.fire(data.error , "Click OK to proceed", "success").then(
                            function(){
                        });
    
                    }else {
                        Swal.fire(data.success , "Click OK to proceed", "success").then(
                            function(){
                            location.reload();
                        });
    
                    }   
            }
        });
    });


});