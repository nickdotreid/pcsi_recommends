$(document).ready(function(){
	// remove current question form  // remove recommendations form
	$(".recommendations,.questions.ajax").html("")
	
	// set up event triggers for question form input click
	$("#content").delegate(".questions.ajax input","click",function(){
		var input = $(this);
		var question = input.parents(".question:first");
		var container = input.parents(".question:first");
		if(input.attr("type")=="checkbox"){
			container = input.parents("label:first");
		}
		timeout = setTimeout(function(){
			container.remove();
			$(".answers").append(a);
		},2000);
		var a = $("#question-answered-template .question").clone();
		$(".label",a).html($(".control-label",question).html());
		$(".answer",a).html($("span",input.parents("label:first")).html());
		timeout = setTimeout(function(){
			var _data = {}
			_data[input.attr("name")] = input.attr("value");
			container.remove();
			$(".answers").append(a);
			$(".undo",a).remove();
			if(input.attr("type")=="checkbox"){
				if($(".controls .checkbox,.controls .question",question).length < 1){
					question.hide();
				}
			}
			$.ajax({
				url:"/ajax/save",
				data:_data,
				type:"POST",
				success:function(data){
					$.ajax({
						url:"/ajax/questions",
						type:"POST",
						success:function(data){
							load_questions(data['questions'],after=question);
						},
						error:handle_error
					});
					$.ajax({
						url:"/ajax/update",
						type:"POST",
						success:function(data){
							load_recommendations(data['recommendations']);
						},
						error:handle_error
					});
				},
				error:handle_error
			});
		},2000);
		container.hide().after(a);
		$(".undo",a).click(function(event){
			event.preventDefault();
			clearTimeout(timeout);
			container.show();
			a.remove();
		})
	});
	
	$.ajax({
		url:"/ajax/update",
		type:"POST",
		success:function(data){
			load_recommendations(data['recommendations']);
		},
		error:handle_error
	});
	
	$.ajax({
		url:"/ajax/questions",
		type:"POST",
		success:function(data){
			load_questions(data['questions'],after=false);
		},
		error:handle_error
	});
	
	$("form").trigger("display");
});

function handle_error(data){
	
}

function load_recommendations(recommendations){
	for( index in recommendations ){
		if(!add_recommendation(recommendations[index])){
			update_recommendation(recommendations[index]);
		}
	}
}
function add_recommendation(recommendation){
	if($("#recommendation-"+recommendation['screen-id']).length>0){
		return false;
	}
	var r = $("#recommendation-template .recommendation").clone();
	r.attr("id","recommendation-"+recommendation['screen-id']);
	$(".screen",r).html(recommendation['screen-name']);
	$(".frequency",r).html(recommendation['frequency']);
	if(recommendation['not-recommended']){
		r.hide();
	}
	$(".recommendations").append(r);
	return true;
}

function update_recommendation(recommendation){
	var r = $("#recommendation-"+recommendation['screen-id']);
	if(recommendation['frequency'] != $(".frequency",r).html()){
		$(".frequency",r).html(recommendation['frequency']);
	}
	if(recommendation['not-recommended']){
		r.hide();
	}else{
		r.show();
	}
}

function load_questions(questions,after){
	for( index in questions){
		add_question(questions[index],after);
	}
}
function add_question(question,after){
	var question_id = question['name'].replace(".","-");
	if($("#"+question_id).length>0){
		return;
	}
	var q = $("#question-template .question").clone();
	q.attr("id",question_id);
	$(".control-label",q).html(question['label']);
	for( i in question['answers']){
		var answer = question['answers'][i];
		if(question.multiple_choice){
			var a = $("#checkbox-template .checkbox").clone();
		}else{
			var a = $("#radio-template .radio").clone();
		}
		$("input",a).attr("name",question['name']).attr("value",answer['value']);
		a.append('<span>'+answer['text']+'</span>');
		$(".controls",q).append(a);
	}
	if(after){
		after.after(q);
	}else{
		$(".questions").append(q);
	}
}