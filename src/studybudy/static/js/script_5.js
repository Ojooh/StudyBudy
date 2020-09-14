jQuery(document).ready(function( $ ) {
    var error                   = $('.error');
    var toggleNav               = $('.toggle-nav');
    var sideMenuToggler         = $(".sideMenuToggler");
    var window_width            = $(window).width();
    var minimize                = $('.btn-minimize');
    var noteActions             = $('.options-icon');
    var folderActions           = $('.options-icon-fd');
    var folderFilter            = $('.folder-filter-class');
    var fileFilter              = $('.file-filter-class');
    var filterFolder            = $('.filters-folder');
    var filterFile              = $('.filters-file');
    var tableDrop               = $('.drop-trigger-options');
    var Trash                   = $('.delete-trigger');
    var trashMove               = $('.yep');
    var tableFolderDrop         = $('.drop-trigger-1');
    var tableNoteDrop           = $('.drop-trigger-2');
    var modalFINFO              = $('#FileInfoModal');
    var modalWarning            = $('#warningModal');
    var fileDetails             = $('.details');
    var recycleList                = $('.recycle');

    if ($('.folder-filter-class').length != 0){
        if ($('.folder-filter-class').html().trim() == $('.folder-filt-1').html().trim()){
            var ht = $('.folder-filt-1').html().trim();
            $('.folder-filt-1').html('<i class="fas fa-check"></i> ' + ht);
        } 
        else if ($('.folder-filter-class').html().trim() == $('.folder-filt-2').html().trim()){
            var ht = $('.folder-filt-2').html().trim();
            $('.folder-filt-2').html('<i class="fas fa-check"></i> ' + ht);
        }
        else if ($('.folder-filter-class').html().trim() == $('.folder-filt-3').html().trim()){
            var ht = $('.folder-filt-3').html().trim();
            $('.folder-filt-3').html('<i class="fas fa-check"></i> ' + ht);
        }


        if ($('.file-filter-class').html().trim() == $('.file-filt-1').html().trim()){
            var ht = $('.file-filt-1').html().trim();
            $('.file-filt-1').html('<i class="fas fa-check"></i> ' + ht);
        } 
        else if ($('.file-filter-class').html().trim() == $('.file-filt-2').html().trim()){
            var ht = $('.file-filt-2').html().trim();
            $('.file-filt-2').html('<i class="fas fa-check"></i> ' + ht);
        }
        else if ($('.file-filter-class').html().trim() == $('.file-filt-3').html().trim()){
            var ht = $('.file-filt-3').html().trim();
            $('.file-filt-3').html('<i class="fas fa-check"></i> ' + ht);
        }
    } 
    else {
        if ($('.folder-filt-2').length != 0){

            if ($('.table-filter-mode').html().trim() ==  $('.folder-filt-2').html().trim()){
                var ht = $('.folder-filt-2').html().trim();
                $('.folder-filt-2').html('<i class="fas fa-check"></i> ' + ht);
            }
            else if ($('.table-filter-mode').html().trim() ==  $('.folder-filt-3').html().trim()){
                var ht = $('.folder-filt-3').html().trim();
                $('.folder-filt-3').html('<i class="fas fa-check"></i> ' + ht);
            }

        }
        if ($('.file-filt-2').length != 0) {
            if ($('.table-filter-mode').html().trim() ==  $('.file-filt-2').html().trim()){
                var ht = $('.file-filt-2').html().trim();
                $('.file-filt-2').html('<i class="fas fa-check"></i> ' + ht);
            }
            else if ($('.table-filter-mode').html().trim() ==  $('.file-filt-3').html().trim()){
                var ht = $('.file-filt-3').html().trim();
                $('.file-filt-3').html('<i class="fas fa-check"></i> ' + ht);
            }
        }
        
    }

    function convertSize(size) {
        var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        if (size == 0) return '0 Byte';
        var i = parseInt(Math.floor(Math.log(size) / Math.log(1024)));
        return Math.round(size / Math.pow(1024, i), 2) + ' ' + sizes[i];
    };

    function Restore(url, restoring, type){
        var data = {'ID' : restoring, 'typey' : type}
        $.ajax({
            url: url,
            data: data,
            beforeSend: function(){
                $('.folder-move-list').addClass("deactivated");
                $('.folder-move-icon').addClass("deactivated");
                $('.waiting').removeClass("deactivated");

            },
            success: function(data){
                if ("error" in data){
                    $(".modal-title").html("Error");
                    error.removeClass("deactivated");
                    msg = "<span class='alert alert-success'>" + data.error + "</span>";
                    error.html(msg);
                } else {
                    Swal.fire(data.success, "Click OK to proceed to Dashoboard", "success").then(
                        function(){
                            location.reload();
                        }
                    )
                }
            }
        });
    };

    if ( $('.szl').html() != "" && $('.szl').html() != undefined ){
        $.each($('.szl'),function(ky,val){
            var value  = parseInt($('.szl').eq(ky).html().trim());
            $('.szl').eq(ky).html(convertSize(value));
        });
        
    }

    $(document).on("click", function(e){    
        $('.other-options-menu').addClass("deactivated");
        
        $('.filter-options-menu').addClass("deactivated");

        $('.folder-options-menu').addClass("deactivated");

        $('.folder-Drop').addClass("deactivated");

        $('.file-Drop').addClass("deactivated");

        $('.drop-meny').addClass("deactivated");


        if($(e.target).hasClass("rf")  || $(e.target).hasClass("fa-recycle")){
            var url         = $('.move-store').attr("data-url");
            if($(e.target).hasClass("rf")){
                var restoring   = $(e.target).attr("data-id");
                var typey       = $(e.target).attr("data-type");
            } else{
                var restoring   = $(e.target).parent().attr("data-id");
                var typey       = $(e.target).parent().attr("data-type");
            }

            Restore(url, restoring, typey);
        }



        // $('.edit-modal').addClass("deactivated");
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

    noteActions.on("click", function(e) {
        e.stopPropagation();
        e.preventDefault();
        var others      = $('.other-options-menu');
        var id          = $(this).attr("id");
        var seed        = id.split("-");
        var jigi        = ".option-" + seed[seed.length - 1];
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
        slip.toggleClass("deactivated");
    });

    folderFilter.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        $('.option-folder-filter').toggleClass("deactivated");
    });

    fileFilter.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        $('.option-file-filter').toggleClass("deactivated");
    });

    folderActions.on("click", function(e) {
        e.stopPropagation();
        e.preventDefault();
        var others      = $('.folder-options-menu');
        var id          = $(this).attr("id");
        var seed        = id.split("-");
        var jigi        = ".fd-op-" + seed[seed.length - 1];
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
        slip.toggleClass("deactivated");
    });

    filterFolder.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var url     = $(this).attr("data-url");
        var filter  = $(this).attr("data-hml");

        var data    = {'filter' : filter, 'type' : "folder"}

        $.ajax({                       
            url: url,                    
            data: data,
            success: function (data) {
                    if ("error" in data){
                        Swal.fire(data.error , "Click OK to proceed", "success").then(
                            function(){
                        });
    
                    }else {
                        location.reload();
                    }   
            }
        });


    });

    filterFile.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var url     = $(this).attr("data-url");
        var filter  = $(this).attr("data-hml");

        var data    = {'filter' : filter, 'type' : "file"}

        $.ajax({                       
            url: url,                    
            data: data,
            success: function (data) {
                    if ("error" in data){
                        Swal.fire(data.error , "Click OK to proceed", "success").then(
                            function(){
                        });
    
                    }else {
                        location.reload();
                    }   
            }
        });


    });

    tableFolderDrop.on("click", function(e){
        console.log("yep");
        e.preventDefault();
        e.stopPropagation();
        $('.folder-Drop').toggleClass("deactivated");
    });

    tableNoteDrop.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        $('.file-Drop').toggleClass("deactivated");
    });

    tableDrop.on("click", function(e){
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

    fileDetails.on("click", function(e){
        var url = $(this).attr("data-url");
        var ID  = $(this).attr("data-id");
        var name = $(this).attr("data-name");
        var type = $(this).attr("data-type");

        var data = {'ID' : ID, 'typey' : type};
        console.log(data);

        $.ajax({
            url: url,
            data: data,
            beforeSend: function(){
                modalFINFO.modal("show");
                $('.file-details').removeClass("deactivated");
                $('.share-file-menu').addClass("deactivated");
                $('.move-list-meny').addClass("deactivated");
                $(".modal-title").html(name + " Details");
                $(".loading-details").removeClass("deactivated")
                $(".file-details").addClass("deactivated");

            },
            success: function(data){
                $(".loading-details").addClass("deactivated");
                $(".file-details").removeClass("deactivated");
                if ("error" in data){
                    $(".modal-title").html("Error");
                    error.removeClass("deactivated");
                    msg = "<span class='alert alert-success'>" + data.error + "</span>";
                    error.html(msg);
                } else {
                    
                    $('.fl-name').html(data.file_name);
                    $('.fl-name').attr("title", data.file_name);
                    if (data.file_type == "PDF file"){
                        $('.fl-type').html("TYPE : <br><i class='far fa-file-pdf'></i> " + data.file_type);
                        $('.fl-type').attr("title", data.file_type);
                    } else if (data.file_type == "JSON file"){
                        $('.fl-type').html("TYPE : <br><i class='fab fa-js'></i> " + data.file_type);
                        $('.fl-type').attr("title", data.file_type);
                        
                    } else {
                        $('.fl-type').html("TYPE : <br><i class='far fa-folder'></i> " + data.file_type);
                        $('.fl-type').attr("title", data.file_type);
                    }
                    $('.fl-size').html("SIZE : <br><i class='fas fa-memory'></i> " + convertSize(data.size));
                    $('.fl-size').attr("title", data.size);
                    $('.fl-owner').html("OWNER : <br><i class='far fa-user'></i> " + data.owner);
                    $('.fl-owner').attr("title", data.owner);
                    $('.fl-location').html("LOCATION : <br><i class='fas fa-location-arrow'></i> " + data.location);
                    $('.fl-location').attr("title", data.location);
                    $('.fl-created').html("CREATED : <br><i class='far fa-calendar-alt'></i> " + data.created);
                    $('.fl-created').attr("title", data.created);
                    $('.fl-modified').html("LAST MODIFIED : <br><i class='far fa-calendar-alt'></i> " + data.last_modified);
                    $('.fl-modified').attr("title", data.last_modified);
                    $('.fl-opened').html("LAST OPENED : <br><i class='far fa-calendar-alt'></i> " + data.last_opened);
                    $('.fl-opened').attr("title", data.lats_opened);
                    $('.fl-editted').html("LAST EDITTED BY : <br><i class='fas fa-user-friends'></i> " + data.editted_by);
                    $('.fl-editted').attr("title", data.editted_by);
                    $('.fl-desc').html("Description : <br>" + data.description);
                    $('.fl-desc').attr("title", data.description);
                }
            }
        });
    });

    Trash.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var url = $(this).attr("data-url");
        var ID  = $(this).attr("data-id");
        var type = $(this).attr("data-type");
        var fileName = $(this).attr("data-filename");
        trashMove.attr("data-url", url);
        trashMove.attr("data-id", ID);
        trashMove.attr("data-type", type);
        $('.modal-title').html("Delete " + fileName);
        $('.content-warning').html("<h4>Are you sure you want to Permanently Delete " + fileName + "</h4>");
        modalWarning.modal("show");
    });

    trashMove.on("click", function(e){
        var url  = $(this).attr("data-url");
        var ID   = $(this).attr("data-id");
        var type = $(this).attr("data-type");
        var data = {"file_id": ID, 'typey' : type}

        $.ajax({                       
            url: url,                    
            data: data,
            success: function (data) {
                    if ("error" in data){
                        Swal.fire(data.error , "Click OK to proceed", "success").then(
                            function(){
                        });
    
                    }else {
                        Swal.fire(data.msg , "Click OK to proceed", "success").then(
                            function(){
                            location.reload();
                        });
    
                    }   
            }
        });
    });

    recycleList.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var ID = $(this).attr("data-id");
        var url = $(this).attr("data-url");
        var fileName = $(this).attr("data-name");
        var type = $(this).attr("data-type");
        $('.move-store').attr("data-id", ID);

        var data = {"ID" : ID, 'typey' : type};

        $.ajax({
            url: url,
            data: data,
            success: function(data){
                modalFINFO.modal("show");
                $('.file-details').addClass("deactivated");
                $('.share-file-menu').addClass("deactivated");
                $('.move-list-meny').removeClass("deactivated");
                $(".modal-title").html("Restore " + fileName);
                if ("error" in data){
                    $(".modal-title").html('error');
                    error.removeClass("deactivated");
                    msg = "<span class='alert alert-success'>" + data.error + "</span>";
                    error.html(msg);
                } else {
                    var folders = data.src;
                    if (folders.length > 0){
                        var html_1  = "";
                        var html_2 = "";
                        for(var e = 0; e < folders.length; e++){
                            var folder = folders[e];
                            if (folder.f_type == "folder"){
                                html_1 += "<h5 class='text-info my-3'><i class='far fa-folder'></i> " + folder.f_name + "</h5>";
                            } else if  (folder.f_type == "file"){
                                html_1 += "<h5 class='text-info my-3'><i class='far fa-file-pdf'></i> " + folder.f_name + "</h5>";
                            } else {
                                html_1 += "<h5 class='text-info my-3'><i class='fab fa-js'></i> " + folder.f_name + "</h5>";
                            }
                            
                            html_2 += "<h5 data-id='" + folder.f_id + "' data-type='" + folder.f_type + "' class='text-primary my-3 rf'><i class='fas fa-recycle'></i> Restore</h5>"
                        }
                    } else {
                        html_1 = `<div class='text-center text-danger'>
                                    <span class='alert alert-success'>No Folders available to move to</span>
                                </div>`;
                    }

                    $('.folder-move-list').html(html_1);
                    $('.folder-move-icon').html(html_2);
                }
            }
        });


    });

});