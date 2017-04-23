function run(method) {

    $('#edit_text_wrapper').show();
    var settings = {
        'endpoint' : server,
        'confidence' : $('#confidence').val(),
        'support' : $('#support').val(),
        'powered_by': 'no',
        'showScores': 'yes',
        'spotter' : "Default",
        'disambiguator' : $('#disambiguator').val(),
        'policy' : getFilterPolicy(),
        'callback' : function callback(response) {lastResponse = response; $('#status_indicator').removeClass("loading");}
    }
    
    settings.sparql = getSPARQLQuery();
    settings.types = getTypes();

// will hide text object and show annotated text
    $('#text').hide();
    $('#text_annotated').remove();
    $('#text_container').prepend('<div id=text_annotated>'+$('#text').val().replace(/\n/g, "<br />\n")+'</div>');
    $('#text_annotated').annotate(settings);//TODO enable annotate(method, settings)
    $('#text_annotated').annotate(method);

    $('#status_indicator').addClass("loading");
    $('#text_container').addClass("annotated loading");

    $(".action_button").attr("disabled", true);
    $.uniform.update(".action_button");

//button to get the editable text box back for the user to modify as needed

    $('#edit_text').click(function() {
        annotated = false;

        $('#text_annotated').cancelAnnotation();

        $('#text').show();
        $('#text_annotated').remove();
        $('#text_container').removeClass("annotated loading");
        $('#status_indicator').removeClass("loading");

        //$("#text_container").unbind('click');
        $(".action_button").attr("disabled", false);
        $('#edit_text_wrapper').hide();
        $.uniform.update(".action_button");
    });

    annotated = true;

//get candidates for the surface form selected
    $("#text_annotated").bind("mouseup", getSuggestions);

}