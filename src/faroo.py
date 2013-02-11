#!/usr/bin/env python
# faroo.py
import datetime
import urllib
import json




#{{{ Faroo request class
class FarooRequest:

#{{{ Constructor
	def __init__(self, template={}):
		self.q       = template.get('q', None)
		self.start   = template.get('start', 1)
		self.length  = template.get('length', 10)
		self.rlength = template.get('rlength', 20)
		self.l       = template.get('l', 'en')
		self.src     = template.get('src', 'web')
		self.kwic    = template.get('kwic', 'true')
		self.i       = template.get('i', 'false')
		self.f       = template.get('f', 'json')
#}}}

#}}}


#{{{ Faroo response class
class FarooResponse:

#{{{ Constructor
	def __init__(self, template={}):
		self.query       = template.get('query', None)
		self.count       = template.get('count', None)
		self.start       = template.get('start', None)
		self.length      = template.get('length', None)
		self.time        = template.get('time', None)
		self.suggestions = template.get('suggestions', None)

		# Create a list of Faroo results
		results          = template.get('results', None)
		self.results     = list(map(FarooResult, results)) if results else None
#}}}

#}}}


#{{{ Faroo result class
class FarooResult:

#{{{ Constructor
	def __init__(self, template={}):
		self.title   = template.get('title', None)
		self.kwic    = template.get('kwic', None)
		self.url     = template.get('url', None)
		self.iurl    = template.get('iurl', None)
		self.domain  = template.get('domain', None)
		self.author  = template.get('author', None)
		self.news    = template.get('news', None)

		# Create a list of Faroo related results
		related      = template.get('related', None)
		self.related = list(map(FarooRelated, related)) if related else None

		# Create a datetime object
		date         = template.get('date', None)
		self.date    = datetime.datetime.fromtimestamp(int(date)/1000) if date else None
#}}}

#}}}


#{{{ Faroo related class
class FarooRelated:

#{{{ Constructor
	def __init__(self, template={}):
		self.title  = template.get('title', None)
		self.url    = template.get('url', None)
		self.domain = template.get('domain', None)
#}}}

#}}}


#{{{ Perform a Faroo request
def FarooPerformRequest(freq):
	base       = 'http://www.faroo.com/api'
	parameters = {
		'q'      : freq.q,
		'start'  : freq.start,
		'length' : freq.length,
		'rlength': freq.rlength,
		'l'      : freq.l,
		'src'    : freq.src,
		'kwic'   : freq.kwic,
		'i'      : freq.i,
		'f'      : 'json'
	}

	try:
		# Attempt to urlencode parameters
		parameters = urllib.parse.urlencode(parameters)
		url        = '?'.join([base, parameters])
	except:
		return None

	try:
		# Attempt to perform web request
		response   = urllib.request.urlopen(url)
		data       = response.read().decode('utf-8')
	except:
		return None

	try:
		# Attempt to parse json
		data       = json.loads(data)
	except:
		return None

	return FarooResponse(data)
#}}}


#{{{ Faroo API helper
class Faroo:

#{{{ Constructor
	def __init__(self):
		self.parameters = None
#}}}

#{{{ Modify a parameter
	def param(self, key, value):
		"""Modify a single query parameter"""
		if self.parameters is None:
			self.parameters = {}
		self.parameters[str(key)] = str(value)
		return self
#}}}

#{{{ Modify several parameters
	def params(self, pairs={}):
		"""Modify several query parameter"""
		for key, val in pairs.items():
			self.param(key, val)
		return self
#}}}

#{{{ Perform query
	def query(self, q=None):
		"""Perform a query"""
		self.param('q', q)
		freq = FarooRequest(self.parameters)

		return FarooPerformRequest(freq)
#}}}

#}}}
