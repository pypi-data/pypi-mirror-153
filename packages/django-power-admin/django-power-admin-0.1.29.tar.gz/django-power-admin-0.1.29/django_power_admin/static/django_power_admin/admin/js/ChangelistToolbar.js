;(function($){
    $(document).ready(function(){
        $(".PowerAdminChangelistToolbarDropDown").click(function(){
            var content = $(this).find(".PowerAdminChangelistToolbarDropDownContent");
            if(content.css("visibility") == "hidden"){
                content.css("visibility", "visible");
            }else{
                content.css("visibility", "hidden");
            }
        });
        $(".PowerAdminChangelistToolbarDropDownContent").mouseleave(function(event){
            console.log(event);            
            if($(this).find(".PowerAdminChangelistToolbarDropDownItem:hover").length < 1){
                $(this).css("visibility", "hidden");
            }
        });
    });
})(jQuery);
