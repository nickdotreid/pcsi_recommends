from django.core.exceptions import ObjectDoesNotExist
from annoying.functions import get_object_or_None

from pchsi_recommends.recommendations.models import *
from pchsi_recommends.questions.models import *
from pchsi_recommends.populations.models import Population

def get_gender(answers):
	if 'birth_sex' in answers and 'current_sex' in answers:
		sex = determine_sex(answers['current_sex'],answers['birth_sex'])
		if sex:
			return sex
	if 'current_sex' in answers:
		sex = determine_sex(answers['current_sex'])
		if sex:
			return sex
	return False

def get_country(answers):
	if 'country' in answers:
		return answers['country']
	if 'birth_country' in answers:
		return answers['birth_country']
	return False

def get_age(answers):
	if 'age' in answers:
		return answers['age']
	if 'birth_year' in answers:
		from datetime import datetime
		current_year = datetime.now().timetuple().tm_year
		return current_year - int(answers['birth_year'])
	return False

def get_if_population_from_(pdict):
	populations = []
	for index in pdict:
		population = pdict[index]
		try:
			pop = Population.objects.get(short=population)
			populations.append(pop)
		except ObjectDoesNotExist:
			population = False
	return populations

def get_populations(answers):
	populations = []
	sex = get_gender(answers)
	if sex:
		populations.append(sex)
	if sex and 'sex_partners' in answers and answers['sex_partners']:
		pop = determine_sexual_orientation(sex,answers['sex_partners'])
		if pop:
			populations.append(pop)
	for key in answers:
		question = False
		try:
			question_id = int(key)
			question = get_object_or_None(Question,id=question_id)
		except ValueError:
			pass
		if question:
			answer_id_list = answers[question_id]
			if type(answer_id_list) != type([]):
				answer_id_list = [answer_id_list]
			for answer_id in answer_id_list:
				answer = get_object_or_None(Answer,id=answer_id)
				if answer:
					for population in answer.populations.all():
						if population not in populations and not population_is_sex(population):
							populations.append(population)
	return populations

def get_population_sex_dict():
	sex_dict = {}
	try:
		sex_dict['male'] = Population.objects.get(short__iexact='male')
	except ObjectDoesNotExist:
		sex_dict['male'] = False
	try:
		sex_dict['female'] = Population.objects.get(short__iexact='female')
	except ObjectDoesNotExist:
		sex_dict['female'] = False
	try:
		sex_dict['transmale'] = Population.objects.get(short__iexact='transmale')
	except ObjectDoesNotExist:
		sex_dict['transmale'] = False
	try:
		sex_dict['transfemale'] = Population.objects.get(short__iexact='transfemale')
	except ObjectDoesNotExist:
		sex_dict['transfemale'] = False
	return sex_dict

def population_is_sex(population):
	sex_dict = get_population_sex_dict()
	for sex_index in sex_dict:
		sex = sex_dict[sex_index]
		if population.id == sex.id:
			return True
	return False

def determine_sex(current_sex,birth_sex=False):
	if current_sex and not birth_sex:
		pop = get_object_or_None(Population, short__iexact=current_sex)
		if pop:
			return pop
	if current_sex == 'other':
		return 'other'
	sex_dict = get_population_sex_dict()
	if birth_sex == 'male' and current_sex == 'male' and sex_dict['male']:
		return sex_dict['male']
	if birth_sex == 'female' and current_sex == 'female' and sex_dict['female']:
		return sex_dict['female']
	if sex_dict['transfemale'] and (current_sex == 'transfemale' or (current_sex == 'female' and birth_sex == 'male')):
		return sex_dict['transfemale']
	if sex_dict['transmale'] and (current_sex == 'transmale' or (current_sex == 'male' and birth_sex == 'female')):
		return sex_dict['transmale']
	return False

def determine_sexual_orientation(sex,sex_partners={}):
	sex_dict = get_population_sex_dict()
	if sex in [sex_dict['male'],sex_dict['transfemale'],sex_dict['transmale']] and ('male' in sex_partners or 'transmale' in sex_partners or 'transfemale' in sex_partners):
		try:
			pop = Population.objects.get(short__iexact='msm')
			if pop:
				return pop
		except ObjectDoesNotExist:
			return False
	return False