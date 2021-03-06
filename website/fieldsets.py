#!/usr/bin/python
# -*- coding: utf-8 -*-

class DummyException:
	"""usable as stand-in when one want to disable excp catching"""
	pass
	
def unicodeField( field ):
	return unicode(field, 'utf-8', 'replace')

def getFieldsByPrefix( prefix, request ):
	filtered = dict()
	for k in request.GET.keys():
		if k.startswith( prefix ):
			filtered[k] = unicodeField(request.GET[k])
	return filtered

def getAllFields( prefix, request ):
	filtered = dict()
	for k in request.GET.keys():
		filtered[k] = unicodeField(request.GET[key])
	return filtered

def getSingleField( key, request, default=None ):
	if key in request.GET.keys():
		return unicodeField(request.GET[key])
	else:
		return default

def getSingleFieldPOST( key, request, default=None ):
	if key in request.POST.keys():
		return request.POST[key]
	else:
		return default

def getFieldsByPrefixPOST( prefix, request ):
	filtered = dict()
	for k in request.POST.keys():
		if k.startswith( prefix ):
			filtered[k] = request.POST[k]
	return filtered

def SortAsc( condition, ascending = 'True' ):
	if ascending == 'True':
		return condition.asc()
	else:
		return condition.desc()

class LadderInfoToTableAdapter:
	def __init__(self,ladder):
		self.ladder = ladder
		self.rows 	= []
		self.rows.append( [ 'min amount of AIs' 		, ladder.min_ai_count 	] )
		self.rows.append( [ 'max amount of AIs' 		, ladder.max_ai_count 	] )
		self.rows.append( [ 'min amount players sharing control (controlTeam size)' 	, ladder.min_team_size ] )
		self.rows.append( [ 'max amount of players sharing control (controlTeam size)' 	, ladder.max_team_size ] )
		self.rows.append( [ 'min amount of starting positions (controlTeam count)' 	, ladder.min_team_count ] )
		self.rows.append( [ 'max amount of starting positions (controlTeam count)' 	, ladder.max_team_count ] )
		self.rows.append( [ 'min amount of controlTeams allied' 	, ladder.min_ally_size ] )
		self.rows.append( [ 'max amount of controlTeams allied' 	, ladder.max_ally_size ] )
		self.rows.append( [ 'min amount of ally sides' 	, ladder.min_ally_count ] )
		self.rows.append( [ 'max amount of ally sides' 	, ladder.max_ally_count ] )
		self.rows.append( [ 'ranking algorythm' 	, ladder.ranking_algo_id ] )

class LadderOptionsAdapter:
	def __init__(self,options,ladder):
		self.ladder		= ladder
		self.options 	= options
		self.optheaders	= ['key','value']
		self.bloptions 	= []
		self.wloptions 	= []
		self.admins		= []
		for opt in self.options:
			if opt.key == 'ladderadmin':
				self.admins.append( opt.value )
			else:
				if opt.key == 'modname' or opt.key == 'mapname':
					continue
				if opt.is_whitelist:
					self.wloptions.append( {'key': opt.key, 'value': opt.value } )
				else:
					self.bloptions.append( {'key': opt.key, 'value': opt.value } )

class MatchInfoToTableAdapter:
	def __init__(self, match ):
		self.match = match
		self.rows = []
		self.rows.append( [ 'date'		, match.date] )
		self.rows.append( [ 'modname'	, match.modname] )
		self.rows.append( [ 'mapname'	, match.mapname] )
		self.rows.append( [ 'replay'	, '<a href="%s" >%s</a>'%(match.replay,match.replay.split('/')[-1]) ] )
		self.rows.append( [ 'duration'	, match.duration] )
