#Written by Jake Schultz
#TODO Add more lang support, limit number of results returned
import re
from urllib2 import Request, urlopen, URLError, quote
import urllib
import json
from jasper import plugin

class WikiPlugin(plugin.SpeechHandlerPlugin):
	def get_priority(self):
            return 1

	def get_phrases(self):
	    return [self.gettext("WIKI"), self.gettext("WICKY")]

	def handle(self, text, mic):
	    try:
                lang = self.profile['language'].split('-')[0]
	    except KeyError:
                lang = 'en'
	    
	    # method to get the wiki summary
	    self.get_wiki(lang, text, mic)


	def get_wiki(self, lang, text, mic):
	    mic.say(self.gettext("What would you like to learn about?"))
	    # get the user voice input as string
	    article_title = mic.active_listen()
	    # make a call to the Wikipedia API
	    print 'Making request to : '+'https://'+lang+'.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+article_title[0].title()
	    request = Request('https://'+lang+'.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+quote(article_title[0].title()))
	    try:
		mic.say(self.gettext("Loading."))
		response = urlopen(request)
		data = json.load(response)
		# Parse the JSON to just get the extract. Always get the first summary.
		output = data["query"]["pages"]
		final = output[output.keys()[0]]["extract"]
		mic.say(final)
	    except URLError, e:
		mic.say(self.gettext("Unable to reach dictionary API."))


	def is_valid(self, text):
	    return any((word.upper() in text.upper()) for word in
                   (self.gettext("WIKI"), self.gettext("WICKY")))

