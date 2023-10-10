$(document).ready(function() {
	$('.like-form').submit(function(e){
		e.preventDefault();
		const post_id = $(this).attr('id');
		const likeText = $(`.like-btn${post_id}`).text();
		const trim = $.trim(likeText)
		const url = $(this).attr('action');
		let res;
		const likes = $(`.like-count${post_id}`).text();
		const trimcount = parseInt(likes);
		$.ajax({
			type:'POST',
			url:url,
			data:{
				'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
				'post_id':post_id,

			},
			success:function(response){
					if(trim==='Unlike'){
						$(`.like-btn${post_id}`).text('Like');
						res = trimcount-1
					}else{
						$(`.like-btn${post_id}`).text('Unlike');
						res = trimcount+1
					}
					$(`.like-count${post_id}`).text(res)

			},
			error:function(response){
				console.log('error', response);
		}
		})
	});
	$(".search").on("keyup", function () {
    var v = $(this).val();
    $(".lead").removeClass("lead");
    var re = new RegExp("\\b" + v + "\\b","g")
    $(".card").each(function () {
			
        if (v != "" && $(this).text().search(re) != -1) {
					$(this).removeClass("none");
            $(this).addClass("lead");
        }
				else{
					$(this).addClass("none");
				}
    });
});

})