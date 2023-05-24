$(function () {
    $('.like-post').on('click', function () {
        let url = $(this).data('url');
        let post_slug = $(this).data('post-id');
        $.ajax(
        {
            type:"POST",
            url: url,
            data:{
                post_id: 1,
                post_slug:post_slug
            },
            success: function( data ) 
            {
                if(data.success){
                    if(data.is_liked){
                        $("#"+post_slug).children('i').css("color", "blue");
                    }
                    else{
                        $("#"+post_slug).children('i').removeAttr("style");
                    }
                    $("#"+data.slug+"_total-like").html(data.total_likes)
                }
            }
        });
    })
});