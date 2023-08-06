;(function($){
    $(document).ready(function(){
        var make_select2 = function(){
            var self = $(this);
            var flag = true;
            var form_row = self.parents(".form-row");
            if(form_row.length > 0){
                if(form_row.hasClass("empty-form")){
                    flag = false;
                }
            }
            if(flag){
                self.select2();
            }
        }
        $("select.django_power_admin_select2_widget").each(make_select2);
        $(document).on("formset:added", function(event, $row, formsetName){
            $row.find("select.django_power_admin_select2_widget").each(make_select2);
        });
    });
})(jQuery);
