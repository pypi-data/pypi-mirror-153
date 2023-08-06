;(function($){
    $(document).ready(function(){
        var onTextInputFieldFilterChange = function(theform){
            var input = theform.find(".TextInputFieldFilterInput");
            var params = parseParam(window.location.query || "");
            params[input.attr("name")] = input.val();
            var new_querystring = $.param(params);
            var new_url = window.location.origin + window.location.pathname + "?" + new_querystring;
            window.location.href = new_url;
        };

        $(".TextInputFieldFilter .TextInputFieldFilterResetButton").click(function(){
            var theform = $(this).parents("form");
            var input = theform.find(".TextInputFieldFilterInput");
            input.val("");
            onTextInputFieldFilterChange(theform);
            return false;
        });

        $(".TextInputFieldFilter .TextInputFieldFilterSubmitButton").click(function(){
            var theform = $(this).parents("form");
            onTextInputFieldFilterChange(theform);
            return false;
        });
    });
})(jQuery);
