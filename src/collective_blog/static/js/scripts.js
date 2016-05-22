$('textarea.expand').focus(function () {
    $(this).animate({ height: "4em" }, 500);
});

$('#post_rating_up').click(function(){
    var post_id;
    post_id = $(this).attr("post_id");
    $.get('/new_like/', {post_id: post_id}, function(data){
        $('#rating').html(data['rating']);
        $('#like_errors').html(data['result']);
    });
});

$('#post_rating_down').click(function(){
    var post_id;
    post_id = $(this).attr("post_id");
    $.get('/new_dislike/', {post_id: post_id}, function(data){
        $('#rating').html(data['rating']);
        $('#like_errors').html(data['result']);
    });
});