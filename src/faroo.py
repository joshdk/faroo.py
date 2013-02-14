#!/usr/bin/env python
# faroo.py

"""
Python dindings to the FAROO web search API.

This module aims to provide Python bindings to the FAROO web search API.

Full FAROO API documentation can be found at http://www.faroo.com/hp/api/api.html
"""

import datetime
import sys
import urllib
import json

__author__ = 'Josh Komoroske'




#{{{ Faroo request class
class FarooRequest:
	"""
	Encapsulates an individual request to the FAROO API.

	>>> FarooRequest()
	>>> FarooRequest({'q': 'lolcats'})
	>>> FarooRequest({'q': 'lolcats', 'length': 8})
	"""

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
	"""
	Encapsulates an individual response from the FAROO API.

	>>> FarooResponse(json...)
	"""

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
	"""
	Encapsulates an individual result returned from the FAROO API.

	>>> FarooResult(json...)
	"""

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
	"""
	Encapsulates an individual related result from the FAROO API.

	>>> FarooRelated(json...)
	"""

#{{{ Constructor
	def __init__(self, template={}):
		self.title  = template.get('title', None)
		self.url    = template.get('url', None)
		self.domain = template.get('domain', None)
#}}}

#}}}


#{{{ Perform a Faroo request
def FarooPerformRequest(freq):
	"""
	Performs a FAROO API request.

	Takes a FarooRequest, and returns a FarooResponse

	>>> FarooPerformRequest(faroorequest)
	"""

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

	# Attempt to urlencode parameters
	import urllib.parse
	parameters = urllib.parse.urlencode(parameters)
	url = '?'.join([base, parameters])

	# Attempt to perform web request
	import urllib.request
	response = urllib.request.urlopen(url)
	data = response.read().decode('utf-8')

	# Attempt to parse json
	data = json.loads(data)

	return FarooResponse(data)
#}}}


#{{{ Faroo API helper
class Faroo:
	"""
	Streamlines the creation of FAROO API requests.

	>>> Faroo().param('length', 8).query('lolcats')
	>>> Faroo().param('src', 'news').query()
	"""

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
