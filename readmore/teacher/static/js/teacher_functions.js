$(document).ready(function(){
	$(".form-show").click(function(){
		current_id = $(this).attr('id').split("-")[0];
		console.log(current_id);
		$("#"+current_id+"-form").slideToggle();
	});
	$(".student-show").click(function(){
		current_id = $(this).attr('id').split("-")[0];
		console.log(current_id);
		$("#"+current_id+"-students").slideToggle();
	})
});