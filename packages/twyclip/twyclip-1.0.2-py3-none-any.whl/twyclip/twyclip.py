import requests

def clipData(clip_url):
	clip_response = requests.get(f"https://twiclips.com/twitch-download/clip?clip_url={clip_url}")
	clip_json = clip_response.json()
	return {
		'title': clip_json['data']['title'],
		'author': clip_json['data']['info']['author'],
		'category': clip_json['data']['info']['category'],
		'clip_author': clip_json['data']['info']['clip_author'],
		'date': clip_json['data']['info']['date'],
		'views': clip_json['data']['info']['views'],
		'download_link': clip_json['data']['info']['play_url']
	}