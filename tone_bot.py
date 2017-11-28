from __future__ import unicode_literals
import json, time, tweepy
from watson_developer_cloud import ToneAnalyzerV3
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from tone_bot_config import username, password, consumer_key, consumer_secret, access_token, access_token_secret

plotly.tools.set_credentials_file(username='thisisntarealaccounttho', api_key='cCKpwZQn1jlYNkDfGeQL')


tone_analyzer = ToneAnalyzerV3(
   username=username,
   password=password,
   version='2016-05-19')
   
#tweepy keys (I might not need this part idk)
consumer_key=              consumer_key
consumer_secret=        consumer_secret
access_token=              access_token
access_token_secret=access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def add_to_array(arr, value):
	x=0
	for num in arr:
		if(x < 23):
			arr[x] = arr[x+1]
		x = x + 1
	arr[23] = value
	return arr
	
def get_tone(dump, choice):
	parsed_json = json.loads(dump)
	
	document_tone =       parsed_json['document_tone']
	tone_categories = document_tone['tone_categories']

	emotion_tone =                  tone_categories[0]
	emotion_tones =              emotion_tone['tones']

	language_tone =                 tone_categories[1]
	language_tones =            language_tone['tones']

	social_tone =                   tone_categories[2]
	social_tones =                social_tone['tones']

	#emotion tones
	anger =   emotion_tones[0]
	disgust = emotion_tones[1]
	fear =    emotion_tones[2] 
	joy =     emotion_tones[3]
	sadness = emotion_tones[4]


	#emotion scores
	anger_score =     float(anger['score']) * 100
	disgust_score = float(disgust['score']) * 100
	fear_score =       float(fear['score']) * 100
	joy_score =         float(joy['score']) * 100
	sadness_score = float(sadness['score']) * 100 


	#language tones
	analytical = language_tones[0]
	confident =  language_tones[1]
	tenative =   language_tones[2]


	#language scores
	analytical_score = float(analytical['score']) * 100
	confident_score =   float(confident['score']) * 100
	tenative_score =     float(tenative['score']) * 100

	#social tones
	openness =        social_tones[0]
	confident =       social_tones[1]
	extraversion =    social_tones[2]
	agreeableness =   social_tones[3]
	emotional_range = social_tones[4]

	#social scores
	openness_score =               float(openness['score']) * 100
	confident_score =             float(confident['score']) * 100
	extraversion_score =       float(extraversion['score']) * 100
	agreeableness_score =     float(agreeableness['score']) * 100
	emotional_range_score = float(emotional_range['score']) * 100
	
	if(choice ==1):
		return anger_score
	elif(choice == 2):
		return disgust_score
	elif(choice == 3):
		return fear_score
	elif(choice == 4):
		return joy_score
	elif(choice == 5):
		return sadness_score
	else:
		return -1
		
		
anger_values =   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
disgust_values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
fear_values =    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
joy_values =     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sadness_values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

value_arrays = ([anger_values,disgust_values,fear_values,joy_values,sadness_values])

def run_bot(allarrays):
	x = [23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
	tweet_list = ""
	
	anger_values =   allarrays[0]
	disgust_values = allarrays[1]
	fear_values =    allarrays[2]
	joy_values =     allarrays[3]
	sadness_values = allarrays[4]
	print('starting run_bot')
	for tweet in api.search(q="trump", rpp = 100, page = '	50'):
	
		if len(tweet_list + tweet.text)< 100000:
			print(repr(tweet.text.encode("utf-8")))
			tweet_list = tweet_list + tweet.text
		else:
			break
	print('Getting scores from Watson')
	dump = json.dumps(tone_analyzer.tone(text=tweet_list), indent=2)
	
	anger_score =   round(get_tone(dump, 1))
	disgust_score = round(get_tone(dump, 2))
	fear_score =    round(get_tone(dump, 3))
	joy_score =     round(get_tone(dump, 4))
	sadness_score = round(get_tone(dump, 5))
	
	anger_values =       add_to_array(anger_values, anger_score)
	disgust_values = add_to_array(disgust_values, disgust_score)
	fear_values =          add_to_array(fear_values, fear_score)
	joy_values =             add_to_array(joy_values, joy_score)
	sadness_values =  add_to_array(sadness_values,sadness_score)
	
	anger_scatter = go.Scatter(   
			name = 'anger',
            x=x,
            y=anger_values)
			
	disgust_scatter = go.Scatter(
			name = 'disgust',
            x=x,
            y= disgust_values )
	
	fear_scatter = go.Scatter(
			name = 'fear',
            x=x,
            y=fear_values)
	
	joy_scatter = go.Scatter(
			name = 'joy',
            x=x,
            y=joy_values)
			
	sadness_scatter = go.Scatter(
			name = 'sadness',
            x=x,
            y=sadness_values)
	
	data = [anger_scatter,disgust_scatter,fear_scatter,joy_scatter,sadness_scatter]
	
	
	layout = go.Layout(xaxis = dict(
				   range = [23,0],
				   title = 'Hours ago'
    ), 
	yaxis = dict(
		title = 'Percent likeliness',
		range = [0,100]	
	)
	)
	
	print('Plotting graph')
	fig = go.Figure(data = data, layout = layout)
	plot_url = py.plot(fig, filename = 'Tweets about Trump', url = 'https://plot.ly/~HBake/18/', auto_open = True)
	
	return([anger_values,disgust_values,fear_values,joy_values,sadness_values])
	
while True:
	b=Run_Bot(value_arrays)
	value_arrays=b
	print('Time to sleep :)')
	time.sleep(60 * 60)
