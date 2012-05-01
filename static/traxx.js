function postParent(thing){
    $.post($(thing).parents('form').attr("data-update") + "?" + $(thing).parents('form').serialize())
}