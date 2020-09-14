jQuery(document).ready(function( $ ) {
    var error               = $('.error');
    var inptArr             = []
    var form_Box            = $('.form-box');
    var regBtn1             = $('.registerBtn');
    var regBtn2             = $('.registerBtn2');
    var regBtn3             = $('.registerBtn3');
    var backBtn             = $('.backBtn');
    var county_code_inpt    = $('#county_code')
    var user_Category       = $('.user-category');
    var day                 = $('#day');
    var month               = $('#month')
    var year                = $('#year');
    var tele                = $('#telephone');
    var d                   = new Date();
    var currentmonth        = d.getMonth() + 1;
    var currentyear         = d.getFullYear();
    var monthDays           = 31 
    var content_1, 
    content_2, content_3    = ""
    const monthNames        =   [
                                    "January", "February", "March", "April", "May", "June",
                                    "July", "August", "September", "October", "November", "December"
                                ];


    for(var j = 0; j < monthNames.length; j++){
        var vee = j + 1
        content_1 += "<option value='" + vee + "'>" + monthNames[j] + "</option>"
    }
    month.append(content_1)


    for(var i = 1; i <= monthDays; i++){
        content_2 += "<option value='" + i + "'>" + i + "</option>"
    }
    day.append(content_2)


    for(var k = 1900; k <= currentyear; k++){
        content_3 += "<option value='" + k + "'>" + k + "</option>"
    }
    year.append(content_3)


    function setCode(country, countryCodeArray) { 
        for (var y = 0; y < countryCodeArray.length; y++){
            if(countryCodeArray[y].name == country){
                return countryCodeArray[y].dial_code;
            }

        }
        return "N/A";
    }


    function cleanInput(inputArray){
        for(var r = 0; r < inputArray.length; r++){
            if($.inArray( inputArray[r], inptArr)  == -1){
                inptArr.push(inputArray[r])
            }
        }
    }
                            
                            
    month.on("change", function (){
        content_1 = ""
        $('#day option').remove()
        content_1 = "<option value=''><!---choose-----></option>"
        monthDays = new Date(currentyear, parseInt(month.val()), 0).getDate(); 
        for(var i = 1; i <= monthDays; i++){
            content_1 += "<option value='" + i + "'>" + i + "</option>"
        }
        day.html(content_1)
    }); 

    regBtn1.on('click', function () {
        error.html("");
        var current_fs = $(this).parent();
        var next_fs = $(this).parent().next();
        var category = user_Category.val();
        var msg = ""

        if (category == ""){
            msg = "<span class='alert alert-success'>Please select a category</span>"
            error.html(msg)
        }
        else{
            if(category == "student"){
                error.html("");
                inptArr.push(category);

                $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
                next_fs.show();
                current_fs.css({
                    'display'       : 'none'
                });
                form_Box.css({
                    'top'       : '60%'
                });
            }
        }
    });

    regBtn2.on('click', function () {
        error.html("");
        var current_fs              = $(this).parent().parent();
        var next_fs                 = $(this).parent().parent().next();
        var fname                   = $('#f-name').val();
        var lname                   = $('#l-name').val();
        var dob_day                 = day.val();
        var dob_mnth                = month.val();
        var dob_year                = year.val();
        var sex                     = $('#sex').val();
        var country                 = $('#country').val();
        var ffname, flname, ctry    = "";
        var state                   = $('#state').val();
        var msg                     = ""
        var nameRegex               = /^[A-Za-z.\s_-]*$/

        if (fname == "" || lname == "" || nameRegex.test(fname) == false || nameRegex.test(lname) == false){
            msg = "<span class='alert alert-success'>First and last name Entered Incorrectly, only letters, whitespcae and hyphens Allowed</span>";
            error.html(msg);
        }
        else if (dob_day == "" || dob_mnth == "" || dob_year == ""){
            if (dob_mnth == 2 && dob_day > 29) { 
                msg += "<span class='alert alert-success'>Febuary does not have more than 29 days <br></span>";
            } 
            else if ((dob_mnth == 4 || dob_mnth == 6 || dob_mnth == 9 || dob_mnth == 11) && (dob_day > 30)) {
                msg += "<span class='alert alert-success'>Please Enter the right date, Month selected does not match with available day <br></span>";
            }
            else{
                msg += "<span class='alert alert-success'>Please Enter Date of birth information correctly <br></span>"
            }
            
            error.html(msg)
        }
        else if (sex == ""){
            msg += "<span class='alert alert-success'>Please choose the appropriate geneder you belong too <br></span>"
            error.html(msg)
        }
        else if (country == "" || state == ""){
            msg = "<span class='alert alert-success'>Please select the country and state from the list of options that you belong to</span>";
            error.html(msg);
        }
        else {
            error.html("")
            ctry = country.split("-");
            ffname = fname.toLowerCase().replace(/\b[a-z]/g, function(letter) {
                return letter.toUpperCase();
            });
            flname = lname.toLowerCase().replace(/\b[a-z]/g, function(letter) {
                return letter.toUpperCase();
            });
            

            inptArr.push(ffname, flname, dob_day, dob_mnth, dob_year, sex, ctry[0], state)
    
            var code = setCode(ctry[0], cc);
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
            next_fs.show();
            current_fs.css({
                'display'       : 'none'
            });
            form_Box.css({
                'top'       : '60%'
            });
            county_code_inpt.val(code);
        }
       
    });

    regBtn3.on('click', function () {
        error.html("");
        var los                                 = $('#los').val();
        var class_study                         = $('#class').val();
        var school                              = $('#school').val();
        var email                               = $('#email').val();
        var cry_code                            = county_code_inpt.val();
        var telephone                           = tele.val();
        var facebook                            = $('#fb').val();
        var twitter                             = $('#twitter').val();
        var IG                                  = $('#IG').val();
        var fschool, ftel                       = "";
        var msg                                 = ""
        var emailRegex                          = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i;
        var telRegex                            = /^[\s()+-]*([0-9][\s()+-]*){6,20}$/;
        var schoolRegex                         = /^[A-Za-z.\s_-]*$/;
        var fbRegex                             = /^[a-z\d\s.]{5,}$/i;
        var twitterRegex                        = /^@?(\w){1,15}$/;
        var IGRegex                             = /^([A-Za-z0-9._](?:(?:[A-Za-z0-9._]|(?:\.(?!\.))){2,28}(?:[A-Za-z0-9._]))?)$/;



        if (los == "" || class_study == ""){
            msg = "<span class='alert alert-success'>Please select a level of study and the appropriate class you belong too</span>";
            error.html(msg);
        }
        else if (email == "" || emailRegex.test(email) == false){
            msg = "<span class='alert alert-success'>Please Enter an appropraite email address</span>";
            error.html(msg);
        }
        else if (school != "" && schoolRegex.test(school) == false){
            msg = "<span class='alert alert-success'>Please Enter an appropraite name of school, Only letters, whitespace and hyphens allowed</span>";
            error.html(msg);
        }
        else if ((telephone != "") && (telRegex.test(telephone) == false || $.isNumeric(telephone) == false)){
            msg = "<span class='alert alert-success'>Please Enter an appropraite phone number</span>";
            error.html(msg);
        }
        else if (facebook != "" && fbRegex.test(facebook) == false){
            msg = "<span class='alert alert-success'>Please Enter an appropriate facebook handle</span>";
            error.html(msg);
        }
        else if (twitter != "" && twitterRegex.test(twitter) == false){
            msg = "<span class='alert alert-success'>Please Enter an appropriate twitter handle</span>";
            error.html(msg);
        }
        else if (IG != "" && IGRegex.test(IG) == false){
            msg = "<span class='alert alert-success'>Please Enter an appropriate Instagram handle</span>"
            error.html(msg);
        }
        else {
            var tos = los.split("-");
            error.html("");
            if(school != ""){
                    fschool = school.toLowerCase().replace(/\b[a-z]/g, function(letter) {
                        return letter.toUpperCase();
                    });
            }
            if(telephone != ""){
                ftel = cry_code + telephone;
            }
            
            inptArr.push(tos[0], class_study, fschool, email, ftel, facebook, twitter, IG)
            var url = "/register_user";

            $.ajax({
                url: url,
                data: {
                    'user_category'     : inptArr[0],
                    'fname'             : inptArr[1],
                    'lname'             : inptArr[2], 
                    'dob_day'           : inptArr[3], 
                    'dob_mnth'          : inptArr[4], 
                    'dob_year'          : inptArr[5], 
                    'sex'               : inptArr[6], 
                    'ctry'              : inptArr[7], 
                    'state'             : inptArr[8],
                    'tos'               : inptArr[9], 
                    'class_study'       : inptArr[10], 
                    'school'            : inptArr[11], 
                    'email'             : inptArr[12], 
                    'tel'               : inptArr[13], 
                    'facebook'          : inptArr[14], 
                    'twitter'           : inptArr[15], 
                    'IG'                : inptArr[16]
                },
                success: function (data) {
                    if ("url" in data){
                        Swal.fire("User Account Successfully created, refer to your email for verification and change of password in order to login", "Click OK to proceed", "success").then(
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

    backBtn.on('click', function () {
        error.html("");
        var current_fs              = $(this).parent().parent();
        var previous_fs                 = $(this).parent().parent().prev();
        
        $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
        var indx = current_fs.index();

        if(indx == 1 ){
            inptArr.pop()
        }
        if(indx == 2 || indx == 3){
            var t = 8;
            while(t != 0){
                inptArr.pop();
                t--;
            }
        }
        previous_fs.show(); 

        current_fs.css({
            'display'       : 'none'
        });

    });

                            
});