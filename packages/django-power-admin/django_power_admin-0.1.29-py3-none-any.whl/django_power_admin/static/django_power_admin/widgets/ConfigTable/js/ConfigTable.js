;(function($){    
    $.fn.ConfigTable = function(){
        $.each($(this), function(){
            var wrapper = $(this);
            var django_power_admin_widgets_config_table = wrapper.find(".django_power_admin_widgets_config_table");
            var insert_before_item = wrapper.find(".django_power_admin_widgets_config_table_add_another_config");  
            var config_item_template = wrapper.find(".django_power_admin_widgets_config_table_item_template");
            var textarea = wrapper.find("textarea");

            var remove_config_item = function(e){
                e.preventDefault();
                $(this).parents("tr").remove();
                update_textarea_value();
                return false;
            };
            var update_textarea_value = function(){
                var items = {};
                var keys = [];
                $.each(wrapper.find(".django_power_admin_widgets_config_table_item"), function(){
                    var item = $(this);
                    var key = item.find(".django_power_admin_widgets_config_table_item_key input").val();
                    var value = item.find(".django_power_admin_widgets_config_table_item_value input").val();
                    if(key){
                        items[key] = value;
                        keys.push(key);
                    }
                });
                var config_text = JSON.stringify(items);
                textarea.val(config_text);
            };
            var make_new_item = function(key, value){
                var new_item = config_item_template.clone();
                new_item.find(".django_power_admin_widgets_config_table_item_key input").val(key);
                new_item.find(".django_power_admin_widgets_config_table_item_value input").val(value);
                new_item.removeClass("django_power_admin_widgets_config_table_item_template");
                new_item.addClass("django_power_admin_widgets_config_table_item");
                new_item.appendTo(django_power_admin_widgets_config_table);
                new_item.insertBefore(insert_before_item);
                new_item.show();
                new_item.find(".django_power_admin_widgets_config_table_item_remove a").click(remove_config_item);
                new_item.find("input").change(update_textarea_value);
                new_item.find("input").blur(update_textarea_value);
                return new_item;
            };
            var load_textarea_value = function(){
                wrapper.find(".django_power_admin_widgets_config_table_item").remove(); // remove all items
                var textarea_text = textarea.val();
                var items = {};
                var keys = [];
                if(textarea_text){
                    items = $.parseJSON(textarea_text);
                }
                $.each(items, function(key, _){
                    if(key!="_django_power_admin_widgets_config_table_keys"){
                        keys.push(key);
                    }
                });
                for(var i=0; i<keys.length; i++){
                    var key = keys[i];
                    var value = items[key];
                    make_new_item(key, value);
                }
                if(keys.length < 1){
                    make_new_item("", "");
                }
            };
    
            wrapper.find(".django_power_admin_widgets_config_table_item input").change(update_textarea_value);
            wrapper.find(".django_power_admin_widgets_config_table_item input").blur(update_textarea_value);
            wrapper.find(".django_power_admin_widgets_config_table_item .django_power_admin_widgets_config_table_item_remove a").click(remove_config_item);
            wrapper.find(".django_power_admin_widgets_config_table_add_another_config_button").click(function(e){
                e.preventDefault();
                make_new_item("", "");
                return false;
            });

            // init...
            load_textarea_value();
            update_textarea_value();
        });
        return $(this);
    };

    $(document).ready(function(){
        $(".django_power_admin_widgets_config_table_wrapper").ConfigTable();
        $(document).on("formset:added", function(event, $row, formsetName){
            $row.find(".django_power_admin_widgets_config_table_wrapper").ConfigTable();
        });
    });
})(jQuery);
