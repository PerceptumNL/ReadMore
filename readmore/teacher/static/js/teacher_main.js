$(document).ready(function(){
    $(".group-block.info-block").each(function(){
       initialize_group($(this).attr('pk'));
    });
});

function initialize_group(group_id){
    $.get( "api/group/"+group_id+"?stats=engagement", function( data ) {
        $( "#groupsize_"+group_id ).html( data.student_count );
		if(data.student_count > 0){
			$( "#group_activity_"+group_id).attr('src',
				'/static/img/engagement-0'+data.engagement+'.png');
		}
    });
}
