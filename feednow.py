import time
import urllib2
import json
import os
import feeder  # A custom module containing some related functions

print "******************************"
print "feednow.py running..."

while(1):
	feeder_id = feeder.feeder_id # get from the feeder module (feeder.py)
	feednow_url = feeder.feednow_url # get from the feeder module (feeder.py)
	feednow_complete_url = feeder.feednow_complete_url # get from the feeder module (feeder.py)

	print "Current feeder ID: %s" % feeder_id

	# Addresses of folders and files
	feednow_addr = feeder.feednow_addr # get from the feeder module (feeder.py)

	# If folder does not exist, create one
	if not os.path.exists(feednow_addr):
		try:
			os.makedirs(feednow_addr)
		except Exception, e:
			feeder.logError(e)
			
	print "Getting Feed Now data from API..."		
	# Get feed now request data from API in JSON format
	try:
		feednow_json = json.loads(urllib2.urlopen(feednow_url).read())
	except Exception, e:
		feeder.logError(e)
		feednow_json = None

	# If the API returns nothing, raise an alert
	if not feednow_json:
		feeder.logError("API didn't respond to Feed Now request.")
		print "Error: API didn't respond to Feed Now request."
	else:
		print "API returns: %s" % json.dumps(feednow_json, separators=(',', ': '))
	
	if feednow_json is not None:
		if feednow_json['feedNow'] == True:
			print "Feed Now request confirmed. Writing feeding amount to file..."
			if feednow_json['feedAmount']:
				# Write a "feednow.txt" file with the feed amount in it
				feeder.writeFile("%s/feednow.txt" % feednow_addr, feednow_json['feedAmount'])
				# Tell the API the feed now request is done
				try:
					print "Notifying completed Feed Now request to API"
					urllib2.urlopen(feednow_complete_url)
				except Exception, e:
					feeder.logError(e)		
			else:
				feeder.logError("Feed Now Error: Feed amount not set.")
				print "Error: Feed amount not set."		
		else:
			print "'feedNow' value returns false. No need to do anything."
	time.sleep(15)
print "feednow.py done running."
print "******************************"
