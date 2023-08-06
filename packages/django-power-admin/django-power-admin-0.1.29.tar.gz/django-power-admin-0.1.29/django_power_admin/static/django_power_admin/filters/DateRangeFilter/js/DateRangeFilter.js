
;(function($){
    $(document).ready(function(){

        var onDateRangeFilterChange = function(theform){
            var input_start = theform.find(".DateRangeFilterStartInput");
            var input_end = theform.find(".DateRangeFilterEndInput");
            var params = parseParam(window.location.query || "");
            params[input_start.attr("name")] = input_start.val();
            params[input_end.attr("name")] = input_end.val()
            var new_querystring = $.param(params);
            var new_url = window.location.origin + window.location.pathname + "?" + new_querystring;
            window.location.href = new_url;
        };

        $(".DateRangeFilter .DateRangeFilterResetButton").click(function(){
            var theform = $(this).parents("form");
            var input_start = theform.find(".DateRangeFilterStartInput");
            var input_end = theform.find(".DateRangeFilterEndInput");
            input_start.val("");
            input_end.val("");

            onDateRangeFilterChange(theform);
            return false;
        });

        $(".DateRangeFilter .DateRangeFilterSubmitButton").click(function(){
            var theform = $(this).parents("form");
            onDateRangeFilterChange(theform);
            return false;
        });

        $(".DateRangeFilterInput").datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: "yy-mm-dd"
          });
    });
})(jQuery);
