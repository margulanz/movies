from django.shortcuts import render
from django.http import HttpResponse
from .models import movies
from django.template import loader
import pickle
import os
import pandas as pd 


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


import requests
import json
url_poster = "https://imdb8.p.rapidapi.com/title/find"
headers = {
    'x-rapidapi-host': "imdb8.p.rapidapi.com",
    'x-rapidapi-key': ""
    }


def index(request):
	max_film = 10000
	films = movies.objects.values_list('overview',flat = True)[:max_film]
	poster = {}
	template = loader.get_template('recommend/index.html')
	result = []

	if request.method == 'POST':
		name = request.POST.get('textfield',None)
		try:
			tf = TfidfVectorizer(stop_words = 'english')
			matrix = tf.fit_transform(films)
			cosine_simil = linear_kernel(matrix,matrix)


			movie_title = movies.objects.values_list('original_title',flat = True)[:max_film]
			indices = pd.Series(movies.objects.values_list('id',flat = True)[:max_film],index = movie_title)

			idx = indices[name] - 1
			sim_scores = list(enumerate(cosine_simil[idx]))
			sim_scores = sorted(sim_scores,key = lambda x:x[1],reverse = True)
			sim_scores = sim_scores[1:6]
			movie_indices = [i[0] for i in sim_scores]
			
			for i in movie_indices:
				querystring = {"q":movie_title[i]}
				response = requests.request("GET", url_poster, headers=headers, params=querystring)
				data = json.loads(response.text)
				url = data['results'][0]['image']['url']
				poster[i] = url

			
			
			





			result = [[movie_title[x],films[x],poster[x]] for x in movie_indices]

		except (KeyError,ValueError):
			return HttpResponse(template.render({'result':result},request))
	
	return HttpResponse(template.render({'result':result},request))
