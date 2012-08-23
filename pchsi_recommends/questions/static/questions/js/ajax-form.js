$(document).ready(function(){
	// remove current question form  // remove recommendations form
	$(".recommendations,.questions.ajax").html("")
	
	// set up event triggers for question form input click
	$("#content").delegate(".questions.ajax .question input[type='submit']","click",function(event){
		event.preventDefault();
		var input = $(this);
		var question = input.parents(".question:first");
		question.trigger("question-loading");
		_data = {}
		$("input:checked,input:selected",question).each(function(){
			_data[this.name] = this.value;
		})
		$.ajax({
			url:"/ajax/save",
			data:_data,
			type:"POST",
			success:function(data){
				question.hide();
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
	for(var i=0;i<recommendation['notes'].length;i++){
		var note = recommendation['notes'][i];
		$(".nav",r).append('<a id="note-'+note['id']+'" href="#">'+note['subject']+'</a>');
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
	$(".nav a",r).remove();
	for(var i=0;i<recommendation['notes'].length;i++){
		var note = recommendation['notes'][i];
		$(".nav",r).append('<a id="note-'+note['id']+'" href="#">'+note['subject']+'</a>');
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
	q.append('<div class="controls"><input type="submit" value="Update Recommendations" /></div>');
	if(after){
		after.after(q);
	}else{
		$(".questions").append(q);
	}
}