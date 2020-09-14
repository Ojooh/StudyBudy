jQuery(document).ready(function( $ ) {
    var level        = $('#los');
    var cos          = $('#class');
    var json        = {
        "levels": [
          {
            "level": "Primary",
            "class": ["1st grade", "2nd grade", "3rd grade", "4th grade", "5th grade", "6th grade"]
          },
          {
            "level": "Secondary",
            "class": ["7th grade (jss1)", "8th grade (jss2)", "9th grade (jss3)", "10th grade (ss1)", "11th grade (ss2)", "12th grade (ss3)"]
          },
          {
            "level": "Tertiary",
            "class": ["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "6th Year", "7th Year", "Matsers/PHD"]
          }
        ]
    };

    var levels = json.levels
    var html_lvl = "";
    var html_class = "";

    for (var t = 0; t < levels.length; t++){
        var lvl = levels[t].level;
        var lvl_val = lvl + "-" + t
        html_lvl += "<option value='" + lvl_val + "'>" + lvl + "</option>";    
    }
    level.append(html_lvl);

    $("#los").change(function fillStates() {
        var cix = $(this).val();
        var valls = cix.split("-");
        var classes = levels[valls[1]].class;
        cos.empty();
        html_class = "<option value=''><!-----choose----></option>";
        for (var u = 0; u < classes.length; u++){
             var ste = classes[u];
             html_class += "<option value='" + ste + "'>" + ste + "</option>";
        }
        cos.append(html_class);   
    });
    
});