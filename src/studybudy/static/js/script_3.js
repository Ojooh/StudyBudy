jQuery(document).ready(function( $ ) {
    var error                   = $('.error');
    var toggleNav               = $('.toggle-nav');
    var sideMenuToggler         = $(".sideMenuToggler");
    var window_width            = $(window).width();
    var minimize                = $('.btn-minimize');
    var nameFile                = $('#name-file');
    var renameFile              = $('.rename-file');
    var nameFolder              = $('#name-folder');
    var renameFolder            = $('.rename-folder');
    var fileUpload              = $('.upload-choice');
    var fileBlank               = $('.blank-choice');
    var myModal                 = $('#FileAttrModal');
    var modalTitle              = $('#FileAttrModalLabel');
    var modalEDITOR             = $('#ediitViewFileModal');
    var modalFINFO              = $('#FileInfoModal');
    var modalWarning            = $('#warningModal');
    var modalQuizSummary        = $('#QuizSummaryModal');
    var modal_lbl               = $('.modal-label');
    var backyDacky              = $(".backy-dacky");
    var uploadArea              = $('.upload-area');
    var uploadNote              = $('#upload-note');
    var mode                    = $('.mode');
    var createFile              = $('.create-file');
    var noteActions             = $('.options-icon');
    var recNoteActions          = $('.options-rec-icon');
    var folderActions           = $('.options-icon-fd');
    var folderFilter            = $('.folder-filter-class');
    var fileFilter              = $('.file-filter-class');
    var filterFolder            = $('.filters-folder');
    var filterFile              = $('.filters-file');
    var tableDrop               = $('.drop-trigger-options');
    var noteEditViewArea        = $('.editModal-trigger');
    var ckayForm                = $('#editor-form');
    var Trash                   = $('.delete-trigger');
    var trashMove               = $('.yep');
    var share                   = $('.share-file');
    var recipient               = $('#recipients');
    var shareFile               = $('.sharey');
    var moveList                = $('.move-list');
    var fileDetails             = $('.details');
    var downloadFile            = $('.download_file');
    var makePublic              = $('.custom-control-input');
    var editDesc                = $('.edit-description');
    var okay                    = $('#okay');
    var newTab                  = $('.open-new-tab');
    var summary                 = $('.summary-file');
    var smzy                    = $('.summary-action');
    var starIt                  = $('.star');
    var tableFolderDrop         = $('.drop-trigger-1');
    var tableNoteDrop           = $('.drop-trigger-2');
    var quizFile                = $('.quiz-file');
    var quizTry                 = $(".quiz-try");
    var ckeeditorArea           = CKEDITOR.instances.editor2
    var elementState            = false;
    var elementFocus            = [];
    var saveQuiz                = $('.savish');

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
    } else {
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
    }

    function uploadData(formdata, url){
        console.log(formdata);
        $.ajax({
            url: url,
            type: 'post',
            data: formdata,
            contentType: false,
            processData: false,
            dataType: 'json',
            success: function(data){
                if ("error" in data){
                    $(".upload-label").text(data.error);
                } else {
                    Swal.fire("File Upload Successful", "Click OK to proceed to Dashoboard", "success").then(
                        function(){
                            window.location = data.url;
                        }
                    )
                }
            }
        });
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
                            location.reload();
                        }
                    )
                }
            }
        });
    }

    function move(url, moving, move_to){
        var data = {'moving' : moving, 'move_to' : move_to}
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
    }

    if ( $('.szl').html() != "" && $('.szl').html() != undefined ){
        $.each($('.szl'),function(ky,val){
            var value  = parseInt($('.szl').eq(ky).html().trim());
            $('.szl').eq(ky).html(convertSize(value));
        });
        
        // var value  = parseInt($('.szl').html().trim());
        // console.log(value);
        // $('.szl').html(convertSize(value));
    }


    $(document).on("click", function(e){    
        $('.other-options-menu').addClass("deactivated");
        
        $('.filter-options-menu').addClass("deactivated");

        $('.folder-options-menu').addClass("deactivated");

        $('.folder-Drop').addClass("deactivated");

        $('.file-Drop').addClass("deactivated");

        $('.drop-meny').addClass("deactivated");

        // console.log(e.target);

        if ($(e.target).hasClass("cke_button__save") || $(e.target).hasClass("cke_button__save_icon")){
            var new_data = ckeeditorArea.getData();
            
            if (new_data.length != elementFocus[0] || elementState){
                var url = ckayForm.attr("data-url");
                var ID  = ckayForm.attr("data-id");
                var fd  = new FormData();
                fd.append('file_id', ID );
                fd.append('file_data', new_data);
                
                saveNoteData(fd, url, new_data.length);    
            }
        }

        if($(e.target).hasClass("mf")  || $(e.target).hasClass("fa-arrow-right")){
            var url         = $('.move-store').attr("data-url");
            var moving      = $('.move-store').attr("data-id");
            if($(e.target).hasClass("mf")){
                var move_to = $(e.target).attr("data-id");
            } else{
                var move_to = $(e.target).parent().attr("data-id");
            }

            move(url, moving, move_to);
        }



        // $('.edit-modal').addClass("deactivated");
    });

    toggleNav.on('click', function (e) {
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

    minimize.on("click", function(e) {
        e.preventDefault()
        
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

    nameFile.on("click", function(e) {
        modalTitle.html("File Action");
        myModal.modal('show');
        $(".file-action-choice").removeClass("deactivated");
        $(".file-naming").addClass("deactivated");
        $(".file-upload") .addClass("deactivated");
    });

    renameFile.on("click", function(e) {
        e.preventDefault();
        var ID          = $(this).attr("id");
        var fileName    = $(this).attr("data-name");
        var description = $(this).attr("data-description");

        myModal.modal('show');
        backyDacky.addClass("deactivated");
        $(".file-action-choice").addClass("deactivated");
        $(".file-naming").removeClass("deactivated");
        $(".file-upload") .addClass("deactivated");
        modalTitle.html("File ReName");
        modal_lbl.html("Enter a New File Name");
        mode.attr("data-type", "file");
        mode.attr("data-id", ID);
        $("#file-name").val(fileName);
        $("#description-field").val(description);
        createFile.html("Rename");
    });

    nameFolder.on("click", function(e) {
        modalTitle.html("Folder Name");  
        myModal.modal('show');
        $(".file-action-choice").addClass("deactivated");
        $(".file-naming").removeClass("deactivated");
        $(".file-upload").addClass("deactivated");
        modal_lbl.html("Enter a Folder Name");
        backyDacky.addClass("deactivated");
        mode.attr("data-type", "folder");
    });

    renameFolder.on("click", function(e) {
        e.preventDefault();
        var ID          = $(this).attr("id");
        var fileName    = $(this).attr("data-name");
        var description = $(this).attr("data-description");

        myModal.modal('show');
        backyDacky.addClass("deactivated");
        $(".file-action-choice").addClass("deactivated");
        $(".file-naming").removeClass("deactivated");
        $(".file-upload") .addClass("deactivated");
        modalTitle.html("Folder ReName");
        modal_lbl.html("Enter a New Folder Name");
        mode.attr("data-type", "folder");
        mode.attr("data-id", ID);
        $("#file-name").val(fileName);
        $("#description-field").val(description);
        createFile.html("Rename");
    });

    fileUpload.on("click", function(e){
        modalTitle.html("New File Upload");
        $(".file-action-choice").addClass("deactivated");
        $(".file-naming").addClass("deactivated");
        $(".file-upload") .removeClass("deactivated");
    });

    fileBlank.on("click", function(e){
        modalTitle.html("Create Blank File");
        $(".file-action-choice").addClass("deactivated");
        $(".file-naming").removeClass("deactivated");
        $(".file-upload") .addClass("deactivated");
        modal_lbl.html("Enter a File Name");
        mode.attr("data-type", "file");
    });

    backyDacky.on("click", function(e){
        $(".file-action-choice").removeClass("deactivated");
        $(".file-naming").addClass("deactivated");
        $(".file-upload") .addClass("deactivated");
        modalTitle.html("File Action");
    });

    $("html").on("dragover", function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(".uploaded-label").text("Drag here");
    });

    $("html").on("drop", function(e) {
        e.preventDefault();
        e.stopPropagation(); 
    });

    uploadArea.on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
        $(".upload-label").text("Drop");
    });

    uploadArea.on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
        $(".upload-label").text("Drop");
    });

    uploadArea.on('drop', function (e) {
        e.stopPropagation();
        e.preventDefault();

        $(".upload-label").text("Uploading.......");

        var file = e.originalEvent.dataTransfer.files;
        var fd  = new FormData();
        var url = $("#upload-file").attr("data-url");
        var fold= mode.attr("data-fold");

        if(fold != undefined || fold != ""){
            fd.append('fold', fold)
        }

        for(var y= 0; y < files.length; y++){
            fd.append('file',files[y]);
        }

        uploadData(fd, url);
    });

    uploadNote.change(function(){
        $(".upload-label").text("Uploading.......");
        var fd = new FormData();

        var files = uploadNote[0].files;
        console.log(files.length)
        var url = $("#upload-file").attr("data-url");
        var fold= mode.attr("data-fold");

        if(fold != undefined || fold != ""){
            fd.append('fold', fold)
        }

        for(var y= 0; y < files.length; y++){
            fd.append('file',files[y]);
        }

        uploadData(fd, url);
    });

    createFile.on("click", function(){
        error.html("");
        var fileName    = $("#file-name").val();
        var description = $("#description-field").val();
        var fileType    = mode.attr("data-type");
        var url         = mode.attr("data-url");
        var ID          = mode.attr("data-id");
        var fold        = mode.attr("data-fold");

        if(fileName != ""){
            if(ID === undefined || ID == ""){
                if(fold === undefined || fold == ""){
                    var data = {'fileName': fileName, 'description' : description, 'fileType' : fileType};
                } else {
                    var data = {'fileName': fileName, 'description' : description, 'fileType' : fileType, 'fold' : fold};
                }
    
    
                $.ajax({                       
                    url: url,                    
                    data: data,
                    success: function (data) {
                            if ("error" in data){
                                $('.modal-title').html("Error");
                                error.removeClass("deactivated");
                                msg = "<span class='alert alert-success'>" + data.error + "</span>";
                                error.html(msg);
            
                            }else {
                                Swal.fire(data.msg , "Click OK to proceed", "success").then(
                                    function(){
                                    location.reload();
                                });
            
                            }   
                    }
                });
    
            } else {
                var url = mode.attr("data-url3");
                var data = {'fileName': fileName, 'description' : description, 'fileType' : fileType, 'ID' : ID};
    
                $.ajax({                       
                    url: url,                    
                    data: data,
                    success: function (data) {
                            if ("error" in data){
                                $('.modal-title').html("Error");
                                error.removeClass("deactivated");
                                msg = "<span class='alert alert-success'>" + data.error + "</span>";
                                error.html(msg);
            
                            }else {
                                Swal.fire(data.msg , "Click OK to proceed", "success").then(
                                    function(){
                                    location.reload();
                                });
            
                            }   
                    }
                });
            }
        } else {
            $('.modal-title').html("Error");
            error.removeClass("deactivated");
            msg = "<span class='alert alert-success'>Please enter an appropriate Name</span>";
            error.html(msg);
        }    
    });

    recNoteActions.on("click", function(e) {
        e.stopPropagation();
        e.preventDefault();
        var others      = $('.other-options-menu');
        var id          = $(this).attr("id");
        var seed        = id.split("-");
        var jigi        = ".option-rec-" + seed[seed.length - 1];
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
        if(reloffset < windowHeight/2){
            slip.addClass("reverse");
        }
        else{
            slip.removeClass("reverse");
        }
        slip.toggleClass("deactivated");
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

    noteEditViewArea.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var url         = $(this).attr("data-url");
        var ID          = $(this).attr("data-file");
        var view_status = $(this).attr("data-view");
        var fileName    = $(this).attr("data-filename")
        var data         = {"ID" : ID};
        elementFocus     = [];
        console.log(view_status);
        // modalEDITOR.modal("show");

        $.ajax({
            url: url,
            data: data,
            beforeSend: function(){
                modalEDITOR.modal("show");
                $("#ediitViewFileModalLabel").html("LOADING........");
                $(".loading-bar").removeClass("deactivated");
            },
            success: function (data) {
    
                if (data.error){
                    $(".loading-bar").addClass("deactivated");
                    $("#ediitViewFileModalLabel").html("Error");
                    error.removeClass("deactivated");
                    msg = "<span class='alert alert-success'>" + data.error + "</span>";
                    error.html(msg)
                }
                else{  
                    elementFocus.push(data.length);
                    console.log(elementFocus);
                    $(".loading-bar").addClass("deactivated");
                    $("#ediitViewFileModalLabel").html(fileName);
                    $(".ckay").removeClass("deactivated");

                    if ( view_status == "view"){
                        $("#cke_1_top").css({
                            'display': 'none',
                        });
                        ckeeditorArea.setData(data);
                        
                    }
                    else{
                        $("#cke_1_top").css({
                            'display': 'block',
                        });
                        ckayForm.attr("data-id", ID);
                        ckeeditorArea.setData(data);
                    }
                }
            }
        });

    });

    ckeeditorArea.on("change", function(e){
        elementState = true;
    });

    Trash.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var url = $(this).attr("data-url");
        var ID  = $(this).attr("data-id");
        var fileName = $(this).attr("data-filename");
        trashMove.attr("data-url", url);
        trashMove.attr("data-id", ID);
        $('.modal-title').html("Delete " + fileName);
        $('.content-warning').html("<h4>Are you sure you want to Delete " + fileName + "</h4>");
        modalWarning.modal("show");
    });

    trashMove.on("click", function(e){
        var url  = $(this).attr("data-url");
        var ID   = $(this).attr("data-id");
        var data = {"file_id": ID}

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

    share.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var ID          = $(this).attr("data-id");
        var fileName    = $(this).attr("data-name");

        modalFINFO.modal("show");
        $('.modal-title').html("Share " + fileName);
        $('.file-details').addClass("deactivated");
        $('.share-file-menu').removeClass("deactivated");
        $('.util').attr("data-id", ID);
        recipient.focus();
    });

    $(document).on('click','.after ul li a', function(e){
        e.preventDefault();
        e.stopPropagation();
        $(this).parents('li').remove();
        var indx  = $(this).parents('li').index();
        elementFocus.splice(parseInt(indx) - 1, 1);
    });

    recipient.on("keyup", function(e){
        var  toList  = $('.reci-list');
        var html     = toList.html();
        $('.notify').removeClass("deactivated");
        if(e.which == 32 || e.which == 44){
            var recValue       = recipient.val();
            elementFocus.push(recValue);
            html += "<li class='user-list'>" + recValue + "<a href='#'>×</a></li>";
            toList.html(html);
            $(this).val('');
        }
    });

    shareFile.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();

        var url = $('.util').attr("data-url");
        var ID  = $('.util').attr("data-id");
        var ms  = recipient.val();
        if (ms != "" || ms != undefined){
            elementFocus.push(ms);
        }
        var note    = $("#rec-msg").val();
        var email = elementFocus;
        var data  = new  FormData();
        data.append('ID', ID);
        data.append('emails', email);
        data.append('note', note);

        $.ajax({
            url: url,
            type: 'post',
            data: data,
            contentType: false,
            processData: false,
            dataType: 'json',
            success: function(data){
                if ("error" in data){
                    error.removeClass("deactivated");
                    msg = "<span class='alert alert-success'>" + data.error + "</span>";
                    error.html(msg);
                } else {
                    Swal.fire("File Share Successful", "Click OK to proceed to Dashoboard", "success").then(
                        function(){
                            window.location = data.url;
                        }
                    )
                }
            }
        });
    });

    moveList.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var ID = $(this).attr("data-id");
        var url = $(this).attr("data-url");
        $('.move-store').attr("data-id", ID);
        var data = {"ID" : ID};
        $.ajax({
            url: url,
            data: data,
            success: function(data){
                modalFINFO.modal("show");
                $('.file-details').addClass("deactivated");
                $('.share-file-menu').addClass("deactivated");
                $('.move-list-meny').removeClass("deactivated");
                $(".modal-title").html("Pick a Folder to move to");
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
                            html_1 += "<h5 class='text-info my-3'><i class='far fa-folder'></i> " + folder.name + "</h5>";
                            html_2 += "<h5 data-id='" + folder.id + "'class='text-primary my-3 mf'><i class='fas fa-arrow-right'></i> Move Here</h5>"
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

    fileDetails.on("click", function(e){
        var url = $(this).attr("data-url");
        var ID  = $(this).attr("data-id");
        var name = $(this).attr("data-name");

        var data = {'ID' : ID};

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
                    okay.attr("data-id", data.id);
                    $("#desc").val(data.description);
                }
            }
        });
    });

    editDesc.on("click", function(e){
        $('.room').addClass("deactivated");
        $('.have-mercy').addClass("deactivated");
        $('.woundy').removeClass("deactivated");
    });

    okay.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var url = $(this).attr("data-url");
        var ID = $(this).attr("data-id");
        var desc = $('#desc').val();

        if(desc != "" && desc != undefined){
            var data = {'ID' : ID, 'desc' : desc };

            $.ajax({                       
                url: url,                    
                data: data,
                success: function (data) {
                        if ("error" in data){
                            Swal.fire(data.error , "Click OK to proceed", "success").then(
                                function(){
                            });
        
                        }else {
                            Swal.fire(data.msg, "Click OK to proceed", "success").then(
                                function(){
                                location.reload();
                            });
        
                        }   
                }
            });


        } else{
            $('.room').removeClass("deactivated");
        $('.have-mercy').removeClass("deactivated");
            $('.woundy').addClass("deactivated");
        }
    });

    downloadFile.on("click", function(e){
        var url = $(this).attr("data-url");
        window.location = url;
    });

    makePublic.on("change", function(e){
        var funke = $(this).val().split("-");
        var url = $(this).parent().attr("data-url");
        var ID  = funke[1];
        var status = funke[0];

        var data = {'ID' : ID, 'status' : status};

        $.ajax({                       
            url: url,                    
            data: data,
            success: function (data) {
                    if ("error" in data){
                        Swal.fire(data.error , "Click OK to proceed", "success").then(
                            function(){
                        });
    
                    }else {
                        Swal.fire(data.msg, "Click OK to proceed", "success").then(
                            function(){
                            location.reload();
                        });
    
                    }   
            }
        });


    });

    newTab.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var url         = $(this).attr("data-url");
        window.open(url, '_blank'); 
        // modalEDITOR.modal("show");


    });

    summary.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var url = $(this).attr("data-url");
        var ID  = $(this).attr("data-id");
        var fileName = $(this).attr("data-name");
        smzy.attr("data-id", ID);
        smzy.attr("data-url", url);
        $(".modal-title").html("Summarize " + fileName);
        modalQuizSummary.modal("show");
        $('.quizy-part').addClass("deactivated");
        $('.summary-part').removeClass("deactivated");
        $('.loading-sum').addClass("deactivated");
        $('.get-number').removeClass("deactivated");
        $('.summarized').addClass("deactivated");
        $("#number").val("");

    });

    smzy.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var url = $(this).attr("data-url");
        var ID  = $(this).attr("data-id");
        var num = $("#number").val();
        error.html("");

        if (num != "" && num != undefined && num != 0){
            var data = {"ID" : ID, "number" : num};

            $.ajax({
                url: url,
                data: data,
                beforeSend: function(){
                    $('.loading-sum').removeClass("deactivated");
                    $('.get-number').addClass("deactivated");
                    $('.summarized').addClass("deactivated");
                },
                success: function(data){
                    console.log(data.summary);
                    $('.loading-sum').addClass("deactivated");
                    $('.get-number').addClass("deactivated");
                    $('.summarized').removeClass("deactivated");
                    $('.smmry').html(data.summary);
                }
            });


        } else{
            error.removeClass("deactivated");
            msg = "<span class='alert alert-success'> Please enter a valid number of retirn sentences.</span>";
            error.html(msg);
        }


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

    starIt.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var funke = $(this).attr("data-value").split("-");
        var url = $(this).attr("data-url");
        var ID  = funke[1];
        var status = funke[0];

        var data = {'ID' : ID, 'status' : status};

        $.ajax({                       
            url: url,                    
            data: data,
            success: function (data) {
                    if ("error" in data){
                        Swal.fire(data.error , "Click OK to proceed", "success").then(
                            function(){
                        });
    
                    }else {
                        Swal.fire(data.msg, "Click OK to proceed", "success").then(
                            function(){
                            location.reload();
                        });
    
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

    quizFile.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        error.html("");

        var url         = $(this).attr("data-url");
        var fileName    = $(this).attr("data-name");
        var ID          = $(this).attr("data-id");
        var data        = {"ID" : ID}
        // console.log(url);
        // console.log(data);
        
        $.ajax({
            url: url,
            data: data,
            beforeSend: function(){
                
                $('.modal-title').html("Quizing " + fileName + "...........");
                $('.quizy-part').removeClass("deactivated");
                $('.summary-part').addClass("deactivated");
                $('.loading-quiz').removeClass("deactivated");
                $('.get-number').addClass("deactivated");
                $('.summarized').addClass("deactivated");
                $('.quiz-summary').addClass("deactivated");
                saveQuiz.addClass("deactivated");
                quizTry.addClass("deactivated");
                modalQuizSummary.modal("show");
            },
            success: function(data){
                console.log(data)
                if ("error" in data){
                    error.removeClass("deactivated");
                    msg = "<span class='alert alert-success'>" + data.error + ".</span>";
                    error.html(msg);
                } else {
                    $('.modal-title').html("Quiz Result for " + fileName );
                    $('.quizy-part').removeClass("deactivated");
                    $('.summary-part').addClass("deactivated");
                    $('.loading-quiz').addClass("deactivated");
                    $('.get-number').addClass("deactivated");
                    $('.summarized').addClass("deactivated");
                    $('.quiz-summary').removeClass("deactivated");
                    $('.words').html("Word Coount : " + data.words)
                    $('.binary') .html("Binary Question(s) : " + data.result[0])
                    $('.wh').html("Wh Questions(s) : " + data.result[3]);
                    $('.time-taken').html("Total Time Taken : " + Math.round(data.time)); 
                    $('.fill-gaps') .html("Fill in the gaps : " + data.result[2]);
                    $('.total-ques').html("Total Questions Generated : " + data.total);
                    quizTry.attr("data-id", data.file_id);
                    saveQuiz.removeClass("deactivated");
                    quizTry.removeClass("deactivated");
                    saveQuiz.attr("data-id", data.file_id);
                    saveQuiz.attr("data-name", fileName);
                    saveQuiz.attr("data-info", data.result.toString());

                    if (data.saved == "True"){
                        $('.savish').addClass("deactivated");
                    }
                }
                
            }
        });
    });

    quizTry.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var oldUrl      = $(this).attr("data-url");
        var id          = $(this).attr("data-id");
        var splity      = oldUrl.split("/");
        splity[2]       = id
        var newUrl      = splity.join("/");
        window.location = newUrl

    });

    saveQuiz.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();

        var url         = $(this).attr("data-url");
        var fileName    = $(this).attr("data-name");
        var ID          = $(this).attr("data-id");
        var info        = $(this).attr("data-info");
        var taken       = $(this).attr("data-taken");
        var data        = {
                            "note_id" : ID, 
                            "note_name" : fileName, 
                            "quiz_type" : "", 
                            "start_date": "", 
                            "end_date"  : "",
                            "info"      : info,
                            "taken"     : taken
                        };
        $.ajax({
            url: url,
            data: data,
            beforeSend: function(){
                
                $('.modal-title').html("Quizing " + fileName + "...........");
                $('.quizy-part').removeClass("deactivated");
                $('.summary-part').addClass("deactivated");
                $('.loading-quiz').removeClass("deactivated");
                $('.get-number').addClass("deactivated");
                $('.summarized').addClass("deactivated");
                $('.quiz-summary').addClass("deactivated");
                modalQuizSummary.modal("show");
                $('.loading-quiz').html("Please wait, Saving Quiz......");
            },
            success: function(data){     
                if ("error" in data){
                    error.removeClass("deactivated");
                    msg = "<span class='alert alert-success'>" + data.error + ".</span>";
                    error.html(msg);
                } else {
                    Swal.fire(data.msg, "Click OK to proceed", "success").then(
                        function(){
                        window.location = data.url;
                    });             
                }                         
            }
        });
    });






});