/*
*	Request
*	AJAX post request script for feedme
*	
*	Requires jQuery library (http://www.jquery.com)
*	
*	Taylan Pince (taylanpince at gmail dot com) - May 15, 2010
*/

$.namespace("core.Request");

core.Request = $.Class.extend({
    selector : null,
    container : null,
    valid : true,
    processing : false,
    
    media_url : '',
    error_template : '<p class="errors padded low-margin">All fields are required.</p>',
    loader_template : '<p class="center">Hold on, this might take a while</p><p class="center"><img src="{{ MEDIA_URL }}images/ajax-loader.gif" alt="Loader" /></p>',
    
    submit_done : function(data, status, request) {
        this.processing = false;

        $(this.container).html(data);
    },
    
    submit : function() {
        if (!this.processing) {
            this.processing = true;
            this.valid = true;
        
            $(this.selector).find("input").each(this.validate.bind(this));
        
            if (this.valid) {
                $(this.container).html(this.loader_template.replace("{{ MEDIA_URL }}", this.media_url));
                $("#PanelBackground, #PanelContainer").fadeIn();
                $("#CloseButton").click(this.cancel.bind());
                $.post($(this.selector).attr("action"), $(this.selector).serialize(), this.submit_done.bind(this));
            } else if (!$(this.selector).hasClass("has-errors")) {
                $(this.selector).addClass("has-errors").prepend(this.error_template);
            }
            
            this.processing = this.valid;
        }
        
        return false;
    },
    
    validate : function(index, elem) {
        if ($(elem).val() == "") {
            this.valid = false;
        }
    },
    
    cancel : function() {
        this.processing = false;
        
        $("#PanelBackground, #PanelContainer").fadeOut();
        $("#CloseButton").unbind();
    },
    
    init : function(selector, container, media_url) {
        this.selector = selector;
        this.container = container;
        this.media_url = media_url;
        
        $(this.selector).submit(this.submit.bind(this));
    }
});
