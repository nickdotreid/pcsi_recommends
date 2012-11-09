var Question = Backbone.Model.extend({
	defaults:{
		text: false,
		value: false
	},
	initialize:function(options){
		
	}
});

var QuestionCollection = Backbone.Collection.extend({
	initialize:function(options){
		
	}
});

var JustAskView = Backbone.View.extend({
	events:{
		'submit form.questions':'save_questions'
	},
	initialize:function(options){
		
	},
	render: function(options){
		
	},
	save_questions: function(event){
		event.preventDefault();
		var justAsk = this;
		var form = $(event.currentTarget);
		$.ajax({
			url:form.attr("action"),
			type:form.attr("method"),
			data:form.serialize(),
			success:function(data){
				// add all items to questions
				// render questionsList view
			}
		});
	}
});

$(document).ready(function(event){
	new JustAskView({
		el:$("#content")[0]
	});
});