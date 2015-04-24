$(document).ready(function(){
	$(".form-show").click(function(){
		current_id = $(this).attr('id').split("-")[0];
		$("#"+current_id+"-form").slideToggle();
	});
	$(".student-show").click(function(){
		current_id = $(this).attr('id').split("-")[0];
		$("#"+current_id+"-students").slideToggle();
	});
	$(".group-form-show").click(function(){
		$("#group-form").slideToggle();
	});
	$(".group-tab").click(function(){
		current_id = $(this).attr('id').split("-")[0];
		$("#"+current_id+"-content").slideToggle();
	})
});