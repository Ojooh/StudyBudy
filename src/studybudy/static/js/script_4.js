jQuery(document).ready(function( $ ) {
    var error                   = $('.error');
    var toggleNav               = $('.toggle-nav');
    var sideMenuToggler         = $(".sideMenuToggler");
    var window_width            = $(window).width();
    var minimize                = $('.btn-minimize');
    var queNav                  = $('.navis');
    var currentQues             = [];
    var answers                 = [];
    var timey                   = [];
    var failed                  = [];
    var nextQuestion            = $('.next-question');
    var previousQuestion        = $('.previous-question');
    var timeModal               = $('#timerModal');
    var modalQuizSummary        = $('#QuizSummaryModal');
    var setTime                 = $('.set-time');
    var submitAnswers           = $('.submit-answers');
    var tryAgain                = $('.try-again');
    var Failed                  = $('.failed-questions');
    var failedList              = $('.failed-list');
    var saveQuiz                = $('.savish');
    var Qtype;
    var interval;

    console.log(questionAnswer);
    // <div class="answered"></div>

    var navhtml = "";
    for (var i = 1; i <= questionAnswer.length; i++){
        navhtml  += `<div class="col-3 my-3">
                        <div class="question-navigation text-center">
                            <span>` + i + `.</span>
                        </div>
                    </div>`
    }
    queNav.html(navhtml);
    currentQues.push(0);
    answers.push("");

    if (currentQues[0] > 0){
        previousQuestion.removeClass("deactivated");
    } else {
        previousQuestion.addClass("deactivated");
    }



    

    function displayQuestionTag(quesNumber){
        quesNumber += 1
        var ht      = "<span>Question <strong>" + quesNumber + ".</strong></span>"
        $('.question-number').html(ht);
    }

    function displayQuestions(question_text){
        $('.questions').html(question_text)
    }

    function displayOptions(options){
        $('.quiz-label').addClass("deactivated");
        $('.quiz-label').html("");
        if (options.length == 2){
            $('.quiz-label').eq(0).html(options[0]);
            $('#Radio1').val(options[0]);
            $('.quiz-label').eq(1).html(options[1]);
            $('#Radio2').val(options[1]);
            $('.quiz-label').eq(0).removeClass("deactivated");
            $('.quiz-label').eq(1).removeClass("deactivated");
            $('.quiz-label').eq(2).addClass("deactivated");
            $('.quiz-label').eq(3).addClass("deactivated");
        } else if (options.length > 2){
            $('.quiz-label').eq(0).html(options[0]);
            $('#Radio1').val(options[0]);
            $('.quiz-label').eq(1).html(options[1]);
            $('#Radio2').val(options[1]);
            $('.quiz-label').eq(2).html(options[2]);
            $('#Radio3').val(options[2]);
            $('.quiz-label').eq(3).html(options[3]);
            $('#Radio4').val(options[3]);
            $('.quiz-label').eq(0).removeClass("deactivated");
            $('.quiz-label').eq(1).removeClass("deactivated");
            $('.quiz-label').eq(2).removeClass("deactivated");
            $('.quiz-label').eq(3).removeClass("deactivated");
        }
    }

    function getTimeRemaining(endtime) {
        const total     = Date.parse(endtime) - Date.parse(new Date());
        const seconds   = Math.floor((total / 1000) % 60);
        const minutes   = Math.floor((total / 1000 / 60) % 60);
        const hours     = Math.floor((total / (1000 * 60 * 60)) % 24);
        const days      = Math.floor(total / (1000 * 60 * 60 * 24));
        
        return {
          total,
          days,
          hours,
          minutes,
          seconds
        };
    }

    function initializeClock(id, endtime) {
        var rt              = "#" + id
        const clock         = $(rt);
        const hoursSpan     = $('.hours');
        const minutesSpan   = $('.minutes');
        const secondsSpan   = $('.seconds');
      
        function updateClock() {
          const t = getTimeRemaining(endtime);
      
        //   daysSpan.innerHTML = t.days;
          hoursSpan.html(('0' + t.hours).slice(-2));
          minutesSpan.html(('0' + t.minutes).slice(-2));
          secondsSpan.html(('0' + t.seconds).slice(-2));
      
          if (t.total <= 0) {
            clearInterval(timeinterval);
            Grade()
            alert("Your time is up, quiz will submit in the next 5 seconds, click okay to see result");
            
            // setTimeout(Grade(answers), 5000);
            
          }
        }
      
        updateClock();
        var timeinterval = setInterval(updateClock, 1000);
    }

    function giveComment(perc){
        var cmmt = "";
        if (perc >= 0 && perc <= 45){
            cmmt = "Sorry you need to work and study harder, your grades are really bad";
        } else if (perc >= 46 && perc <= 65){
            cmmt = "You performed average, but you are not quite there yet, put in a lttile more effort";
        } else if (perc >= 66 && perc <= 85){
            cmmt = "Wow Congrats you did really good, keep up the good work you are an A student";
        } else {
            cmmt = "WOOP WOOP BADOOH YOU SMASHED THIS THING A ++ STUDENT, KEEP IT UP";
        }

        return cmmt;
    }

    function Grade() {
        var score   = 0;
        var overall = questionAnswer.length;
        timey.push(new Date());

        for (var k = 0; k < questionAnswer.length; k++){
            
            if(answers[k] == questionAnswer[k].Answer){
                score += 1;
            } else {
                failed.push(k);
            }
        }

        var points  = score
        var perc    = Math.round((score/overall) * 100 );
        var comment = giveComment(perc);

        $('.start-timey').html("Quiz Attempt started at : " + timey[0].toDateString());    
        $('.end-timey').html("Quiz Attempt ended at : " + timey[1].toDateString());
        $('.score').html("<strong> Score : " + points.toString() + "/" + overall.toString() + "</strong>");
        $('.percentage').html("<strong> Percentage : " + perc.toString() + " % </strong>");
        $('.Comment').html(comment);
        $('.prep').addClass("deactivated");
        $('.start').addClass("deactivated");
        $('.submit').addClass("deactivated");
        $('.result').removeClass("deactivated");
    }

    

    
    displayQuestionTag(currentQues[0]);
    displayQuestions(questionAnswer[0].Full_qus);
    displayOptions(questionAnswer[0].options);

    $(document).on("click", function(e){
        var listItems = $('.question-navigation');
        if ($(e.target).hasClass("question-navigation") || $(e.target).parent().hasClass("question-navigation")){
            var indx    = listItems.index( $(e.target) );
            var indx_1  = listItems.index( $(e.target).parent());
            var tip;
            if (indx != -1){
                tip = indx;
            } else {
                tip = indx_1;
            }

            if (!$(".start").hasClass("deactivated")){
                currentQues = [];
                currentQues.push(tip);
                if (currentQues[0] > 0){
                    previousQuestion.removeClass("deactivated");
                } else {
                    previousQuestion.addClass("deactivated");
                }
                displayQuestionTag(currentQues[0]);
                displayQuestions(questionAnswer[tip].Full_qus);
                displayOptions(questionAnswer[tip].options);
            }
            
        }
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

    $('input[name="customMode"]').on("change", function(e){
        if ($(this).val() == "timeless"){
            $('.prep').addClass("deactivated");
            $('.start').removeClass("deactivated");
            timey.push(new Date());
            Qtype = $(this).val();
        } else{
            timeModal.modal("show");
            Qtype = $(this).val()
        }
    });

    nextQuestion.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();

        var que_no      = currentQues[0];
        var selected    = $("input[name='customOptions']:checked"). val();
        que_no          += 1;
        currentQues     = [];

        currentQues.push(que_no);
        $(".custom-control-input").prop("checked", false);

        if (currentQues[0] > 0){
            previousQuestion.removeClass("deactivated");
        } else {
            previousQuestion.addClass("deactivated");
        }

        if (que_no > 0 && que_no < questionAnswer.length){
            var indx = que_no - 1
            if (selected != "" && selected != undefined){
                answers[indx] = selected;
                $('.question-navigation').eq(que_no - 1).html(`<span>` + que_no.toString() + `.</span><div class="answered"></div>`);
            } else {
                answers[indx] = "";
            }
            displayQuestionTag(que_no);
            displayQuestions(questionAnswer[que_no].Full_qus);
            displayOptions(questionAnswer[que_no].options);
            
        } else {
            var indx = que_no - 1
            if (selected != "" && selected != undefined){
                answers[indx] = selected;
                console.log(answers)
                $('.question-navigation').eq(que_no - 1).html(`<span>` + que_no.toString() + `.</span><div class="answered"></div>`);
            } else {
                answers[indx] = "";
            }
            que_no          -= 1;
            currentQues     = [];
            currentQues.push(que_no);

            $('.prep').addClass("deactivated");
            $('.start').addClass("deactivated");
            $('.submit').removeClass("deactivated");

        }

    });

    previousQuestion.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();

        var que_no      = currentQues[0];
        que_no          -= 1;
        currentQues     = [];

        currentQues.push(que_no);
        $(".custom-control-input").prop("checked", false);

        if (currentQues[0] > 0){
            previousQuestion.removeClass("deactivated");
        } else {
            previousQuestion.addClass("deactivated");
        }

        if (que_no >= 0 && que_no < questionAnswer.length){
            var indx = que_no - 1
            $('.question-navigation').eq(indx).html(`<span>` + que_no.toString() + `.</span>`);
            displayQuestionTag(que_no);
            displayQuestions(questionAnswer[que_no].Full_qus);
            displayOptions(questionAnswer[que_no].options);
            $('.prep').addClass("deactivated");
            $('.start').removeClass("deactivated");
            $('.submit').addClass("deactivated");
        } else {
            var indx = que_no - 1
            $('.question-navigation').eq(indx).html(`<span>` + que_no.toString() + `.</span>`);
            displayQuestionTag(que_no);
            displayQuestions(questionAnswer[que_no].Full_qus);
            displayOptions(questionAnswer[que_no].options);
            console.log(answers);
            $('.prep').addClass("deactivated");
            $('.start').removeClass("deactivated");
            $('.submit').addClass("deactivated");
        }

    });

    setTime.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();

        var quizTime = 1

        error.html("");
        var hour_ent        = parseInt($("#hour").val());
        var minutes_ent     = parseInt($("#minute").val());
        var seconds_ent     = parseInt($("#second").val());

        if (hour_ent <= 0 && minutes_ent <= 0 && seconds_ent <= 0){
            msg = "<span class='alert alert-success'>Enter an appropriate time to complete quiz.</span>";
            error.html(msg);
        } else {
            error.html("");
            if (hour_ent > 0){
                quizTime = quizTime * hour_ent *60 *60;
            }

            if (minutes_ent > 0){
                quizTime = quizTime * minutes_ent * 60;
            }

            if (seconds_ent > 0){
                quizTime = quizTime * seconds_ent;
            }

            const deadline = new Date(Date.parse(new Date()) +  quizTime * 1000);
            initializeClock("clockdiv", deadline);
            $('.prep').addClass("deactivated");
            $('.start').removeClass("deactivated");
            $('.timer').removeClass("deactivated");
            timeModal.modal("hide");
            timey.push(new Date());
        }
    });

    submitAnswers.on("click", Grade);


    tryAgain.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();

        window.location.reload();
    });

    Failed.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var htmll = "";
        

        for(var m = 0; m < failed.length; m++){
            var indx = failed[m];

            var quizD = questionAnswer[indx];
            htmll += "<li class='text-center'>" + quizD.Full_qus + "<br><strong>" + quizD.Answer + "</strong></li><br>";
        }

        failedList.html(htmll);
        failedList.removeClass("deactivated");
    });

    saveQuiz.on("click", function(e){
        e.preventDefault();
        e.stopPropagation();

        var url         = $(this).attr("data-url");
        var fileName    = $(this).attr("data-name");
        var ID          = $(this).attr("data-id");
        var info        = $(this).attr("data-info");
        var taken       = $(this).attr("data-taken");

        var c = timey[0];
        var d = timey[1];
        var dy_s = c.getDate();
        var dy_e = d.getDate();
        var m_s  = c.getMonth();
        var m_e  = d.getMonth();
        var y_s  = c.getFullYear();
        var y_e  = d.getFullYear();
        var h_S  = c.getHours();
        var h_e  = d.getHours();
        var mi_s = c.getMinutes();
        var mi_e = d.getMinutes();
        var se_s = c.getSeconds();
        var se_e = d.getSeconds();
        m_s += 1;
        m_e += 1;
        
        var data        = {
                            "note_id" : ID, 
                            "note_name" : fileName, 
                            "quiz_type" : Qtype, 
                            "start_date": y_s + "-" + m_s + "-" + dy_s + " " + h_S + ":" + mi_s + ":" + se_s, 
                            "end_date"  : y_e + "-" + m_e + "-" + dy_e + " " + h_e + ":" + mi_e + ":" + se_e, 
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