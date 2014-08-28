#!/usr/bin/python

import re
import csv
import json

def isDate(str):
	segs = str.split("/")
	if len(segs) != 3:
		return False
	for seg in segs:
		if seg.isdigit() == False:
			return False
	return True

weightPattern = re.compile('.*?(\d+)\s*lb\s*(\d+\.\d+)\s*oz')
def weightInOunces(str):
	m = weightPattern.match(str)
	if m:
		g = m.groups()
		# return weight in ounces
		return float(g[0]) * 16 + float(g[1])
	return False

timePattern = re.compile('(\d+):(\d+)\s+(A|P)M')
def getTime(timeStr):
	m = timePattern.match(timeStr)
	if m:
		g = m.groups()
		hour = int(g[0]) % 12
		if g[2] == 'P':
			hour = hour + 12
		return {'HH': '%02d' % int(hour), 'MM': '%02d' % int(g[1])}
	return False

datePattern = re.compile('(\d+)/(\d+)/(\d+)')
def getDate(dateStr):
	m = datePattern.match(dateStr)
	if m:
		g = m.groups()
		return {'MM': '%02d' % int(g[0]), 'DD':'%02d' % int(g[1]), 'YYYY':'%04d' % int(g[2])}
	return False

# Creates a sqlite3 datetime string
def getDateTimeStr(date, time):
	return date['YYYY'] + '-'\
		+ date['MM'] + '-'\
		+ date['DD'] + ' '\
		+ time['HH'] + ':'\
		+ time['MM']

def isAmount(str):
	try:
		float(str)
		return True
	except ValueError:
		return False

def parseFile():
	with open('./in.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		_date = ""
		_dailyTotals = []
		_weights = []
		_events = []
		for row in reader:
			if isDate(row[0]):
				_date = row[0]
				_dailyTotals.append((_date, row[2]))
			w = weightInOunces(row[2])
			if w:
				_weights.append((_date, w))
			time = getTime(row[0])
			if time and isAmount(row[1]):
				_events.append({'datetime': getDateTimeStr(getDate(_date), time), 'amount':float(row[1])})
		return {'dailyIntakeInOz':_dailyTotals, 'bodyWeightsInOz':_weights, 'feedingsInOz':_events}

print json.dumps(parseFile(), indent=4)
