;(function($){

    $(document).ready(function(){
        $("#result_list tr").hover(function(){
            if($(this).hasClass("highlight_hover_row_enabled")){
                $(this).addClass("highlight_hover_row_active");
            }
        }, function(){
            $(this).removeClass("highlight_hover_row_active");
        });

        $("#result_list tr").click(function(event){
            if($(this).hasClass("highlight_clicked_row_enabled")){
                if($(event.target).hasClass("action-select")){
                    $("#result_list tr").removeClass("highlight_hover_row_active_forever");
                }else{
                    $("#result_list tr").removeClass("highlight_hover_row_active_forever");
                    $(this).addClass("highlight_hover_row_active_forever");
                }
            }
        });
    });

})(jQuery);