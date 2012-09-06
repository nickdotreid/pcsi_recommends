# Create your views here.

def ajax_answer_questions(request):
	if 'person_obj' not in request.session:
		return HttpResponseBadRequest(json.dumps({"message":"No Session"}),
		                mimetype="application/json")
	person_obj = request.session['person_obj']
	post_data = DotExpandedDict(request.POST)
	if 'questions' not in post_data:
		return HttpResponseBadRequest(json.dumps({"message":"No Questions"}),
		                mimetype="application/json")
	QuestionForm = make_question_form(person_obj,{
		'include_question_ids':list(map(int,post_data['questions'].keys())),
	})
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			answers = []
			for question,answer in form.cleaned_data.items():
				answers.append(answer)
			message = ""
			for answer in answers_for_form(form):
				message = render_to_string("questions/answered.html",{
					"answer":answer,
					})
			return HttpResponse(json.dumps({
				"answers":answers,
				"message":message,
				}),
			                mimetype="application/json")
	return HttpResponseBadRequest(json.dumps("answered"),
	                mimetype="application/json")

def ajax_save_answer(request):
	if 'person_obj' not in request.session or request.method != 'POST':
		return HttpResponseBadRequest(json.dumps({"message":"Bad Input"}),
		                mimetype="application/json")
	person_obj = request.session['person_obj']
	post_data = DotExpandedDict(request.POST)
	QuestionForm = make_question_form(person_obj,{
		'include_question_ids':list(map(int,post_data['questions'].keys())),
	})
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			request.session['person_obj'] = person_obj_from_(form.cleaned_data,person_obj)
			return HttpResponse(json.dumps({"message":"Saved"}),
				mimetype="application/json")
	return HttpResponseBadRequest(json.dumps({"message":"Fail"}),
	                mimetype="application/json")
	

def ajax_get_questions(request):
	if 'person_obj' not in request.session:
		return HttpResponseBadRequest(json.dumps({"message":"No Session"}),
		                mimetype="application/json")
	person_obj = request.session['person_obj']
	QuestionForm = make_question_form(person_obj,{
		'exclude_question_ids':person_obj['question_ids'],
		'form_class':'questions ajax',
		'form_tag':False,
	})
	from django.forms.fields import MultipleChoiceField
	questions = []
	form = QuestionForm()
	for name in form.fields:
		field = form.fields[name]
#		import pdb; pdb.set_trace()
		answers = []
		for value,text in field.choices:
			answers.append({
				'value':value,
				'text':text,
			})
		questions.append({
			'answers':answers,
			'label':field.label,
			'name':name,
			'required':field.required,
			'multiple_choice':isinstance(field,MultipleChoiceField)
		})
	if len(questions) < 1:
		return HttpResponseBadRequest(json.dumps({"message":"No More Questions"}),
		                mimetype="application/json")
	return HttpResponse(json.dumps({
		"questions":questions,
		}),
	    mimetype="application/json")

def ajax_get_recommendations(request):
	if 'person_obj' not in request.session:
		return HttpResponseBadRequest(json.dumps({"message":"No Session"}),
		                mimetype="application/json")
	person_obj = request.session['person_obj']
	recommendations = []
	for recommendation in fake_populations_to_recommendations(person_obj):
		_notes = []
		for note in recommendation.screen.select_notes():
			_notes.append({
				'id':note.id,
				'subject':note.subject.title,
				'title':note.title,
			})
		recommendations.append({
			'screen-id':recommendation.screen.id,
			'screen-name':recommendation.screen.name,
			'frequency':recommendation.frequency,
			'not-recommended':recommendation.not_recommended,
			'notes':_notes,
		})
	return HttpResponse(json.dumps({
		'recommendations':recommendations,
	}),mimetype="application/json")