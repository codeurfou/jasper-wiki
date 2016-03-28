#Written by Jake Schultz
#TODO Add more lang support, limit number of results returned
import re
from urllib2 import Request, urlopen, URLError
import json

from jasper import plugin

WORDS = [self.gettext("WIKI"), self.gettext("WICKY")]

PRIORITY = 1

class WikiPlugin(plugin.SpeechHandlerPlugin):
	def get_phrases(self)
	    return WORDS

	def handle(self, text, mic):
	    try:
                lang = self.profile['language'].split('-')[0]
	    except KeyError:
                lang = 'en'
	    
	    # method to get the wiki summary
	    get_wiki(lang, text, mic)


	def get_wiki(lang, text, mic):
	    mic.say(self.gettext("What would you like to learn about?"))
	    # get the user voice input as string
	    article_title = mic.activeListen()
	    # make a call to the Wikipedia API
	    request = Request('https://'+lang+'.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+article_title)
	    try:
		response = urlopen(request)
		data = json.load(response)
		# Parse the JSON to just get the extract. Always get the first summary.
		output = data["query"]["pages"]
		final = output[output.keys()[0]]["extract"]
		mic.say(final)
	    except URLError, e:
		mic.say(self.gettext("Unable to reach dictionary API."))


	def isValid(self, text):
	    return any((word.upper() in text.upper()) for word in
                   (self.gettext("WIKI"), self.gettext("WICKY")))

