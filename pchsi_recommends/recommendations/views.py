# Create your views here.
from pchsi_recommends.recommendations.models import *

def populations_to_recomendations(populations):
	recommendations = []
	if len(populations) > 0:
		for screen in Screen.objects.all():
			recommend = False
			for recommendation in screen.recommendation_set.all():
				for population in recommendation.populations.all():
					if population in populations:
						if not recommend or recommend.weight > recommendation.weight:
							recommend = recommendation
			if recommend:
				recommendations.append(recommend)
	return recommendations