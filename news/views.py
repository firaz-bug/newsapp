from django.shortcuts import render
from newsapi import NewsApiClient
import requests
import datetime

# Create your views here.
def homepage(request):
	newsapi = NewsApiClient(api_key='03ade69b781c491cba7f02354aeca357')
	category = request.GET.get('category')
	query=request.GET.get('query')
	if query:
		top_headlines = newsapi.get_top_headlines(q=query)
	else:
		top_headlines = newsapi.get_top_headlines(category=category)

	weatherurl = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=ffd655841cd5d3d0cd0e8a2ec46391a8"
	
	city=request.GET.get('location')

	if city == None:
		city = 'delhi'

	if category == None:
		category = 'General'

	report = requests.get(weatherurl.format(city)).json()

	weather_report = {
		'city': city,
		'temperature':report['main']['temp'] - 273.15,
		'description':report['weather'][0]['description'],
		'icon':report['weather'][0]['icon'],
	}

	today = datetime.datetime.now()


	date = today.strftime("%B %d, %Y")
	day = today.strftime("%A")
	time_p = today.strftime("%p")
	time = today.strftime("%I")
	context = {
		'category' : category,
		'headlines' : top_headlines,
		'report' : weather_report,
		'date':date,
		'day':day,
		'time':time,
		'time_p':time_p
	}
	return render(request,"index.html",context)
