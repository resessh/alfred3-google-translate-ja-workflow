from plistlib import readPlist
import requests
import json
from HTMLParser import HTMLParser

API_TOKEN = readPlist('info.plist')['variables']['token']

def fetch_language_of_query(query):
	params = {
		'q': query,
		'key': API_TOKEN,
	}
	response = requests.get('https://translation.googleapis.com/language/translate/v2/detect/', params = params)
	return json.loads(response.text)['data']['detections'][0][0]['language']

def fetch_translation(query, source_lang, target_lang):
	params = {
		'q': query,
		'source': source_lang,
		'target': target_lang,
		'key': API_TOKEN,
	}
	response = requests.get('https://translation.googleapis.com/language/translate/v2/', params = params)
	h = HTMLParser()
	return map(
		lambda translation: h.unescape(translation['translatedText']),
		json.loads(response.text)['data']['translations']
	)

def generate_json_for_alfred_response(words):
	return json.dumps({
		"items": map(
			lambda word: {
				"title": word,
				"arg": word,
			},
			words
		)
	})

def translate(query):
	source_lang = fetch_language_of_query(query)
	target_lang = 'ja' if source_lang == 'en' else 'en'
	translations = fetch_translation(query, source_lang, target_lang)
	return generate_json_for_alfred_response(translations)
