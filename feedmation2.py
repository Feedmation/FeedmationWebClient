import time
import urllib2
import json
import os
import feeder  # A custom module containing some related functions

print "******************************"
print "feedmation2.py running..."
while(1):
	feeder_id = feeder.feeder_id # get from the feeder module (feeder.py)
	settings_url = feeder.settings_url # get from the feeder module (feeder.py)

	print "Current feeder ID: %s" % feeder_id

	#print json.dumps(settings_json, sort_keys=True,indent=0, separators=(',', ': '))
	#print settings_json

	# Addresses of folders and files
	settings_addr = feeder.settings_addr # get from the feeder module (feeder.py)

	# If folder does not exist, create one
	if not os.path.exists(settings_addr):
		try:
			os.makedirs(settings_addr)
		except Exception, e:
			feeder.logError(e)
			
	print "Getting feeder settings from API..."		

	# Get feeder settings from API in JSON format
	try:
		settings_json = json.loads(urllib2.urlopen(settings_url).read())
	except Exception, e:
		feeder.logError(e)
		settings_json = None
		
	# If the API returns nothing, raise an alert
	if not settings_json:
		feeder.logError("API didn't respond to pull_settings request.")
		print "Error: API didn't respond to pull_settings request."
	else:
		print "API returns: %s" % json.dumps(settings_json, separators=(',', ': '))
		
	# Check each folder in the settings directory
	for folder in os.listdir(settings_addr):
		# If an existing tag in the folders no longer exists in the json object, it has been deleted by the user.
		# In this case, wipe out everything in the corresponding folder and leave a file "deleted.txt" with the tagID of the deleted tag in it.
		# Check if a tag slot number in the settings directory exists in the json object
		# If not, the corresponding tag has been deleted. Wipe out files and leave "deleted.txt"
		if settings_json is not None:
			if settings_json[folder] is None:
				# Get the tagID of the deleted tag
				deletedID = None
				if os.path.isfile("%s%s/tagID.txt" % (settings_addr, folder)):
					deletedID = feeder.readFile("%s%s/tagID.txt" % (settings_addr, folder))
					print "Tag %s has been deleted." % folder
					print "Emptying the corresponding folder..."
					# Delete every file in the folder
					for the_file in os.listdir(settings_addr+folder):
						file_path = os.path.join(settings_addr+folder, the_file)
						try:
							if os.path.isfile(file_path):
								os.unlink(file_path)
						except Exception, e:
							feeder.logError(e)
					# Leave the "deleted.txt" file with the deleted tagID
					if not deletedID is None:
						feeder.writeFile("%s%s/deleted.txt" % (settings_addr, folder), deletedID)
						print "deleted.txt created"
	if settings_json is not None:	
		for tagNo in settings_json:
			# If folder does not exist, create one
			if not os.path.exists(settings_addr+tagNo):
				try:
					os.makedirs(settings_addr+tagNo)
				except Exception, e:
					feeder.logError(e)
					
			if settings_json[tagNo]:
				# If file does not exist, create file
				# OR
				# If 'tagUpdate' is true, a change of settings has occurred to the tag. Rewrite the corresponding files.
				if (not os.listdir("%s%s" % (settings_addr,tagNo))) or (os.listdir("%s%s" % (settings_addr,tagNo)) == [u'deleted.txt']) or (settings_json[tagNo]['tagUpdate'] == True):
					print "Tag %s is updated. Creating files..." % tagNo
					# If a "deleted.txt" exists, delete it
					try:
						if os.path.isfile("%s%s/deleted.txt" % (settings_addr,tagNo)):
							os.unlink("%s%s/deleted.txt" % (settings_addr,tagNo))
					except Exception, e:
						feeder.logError(e)
						
					for key in settings_json[tagNo]:
						# We don't need a "tagUpdate.txt"
						if not key == "tagUpdate":
							feeder.writeFile("%s%s/%s.txt" % (settings_addr,tagNo,key), settings_json[tagNo][key])
							print "File created: %s%s/%s.txt" % (settings_addr,tagNo,key)
					if settings_json[tagNo]['tagUpdate'] == True:
						# Tell the API the update is done
						print "Notifying successful tag update to API"
						tag_complete_url = "http://feedmation.com/api/v1/sync_data.php?feederid=%s&tagid=%s&function=tag_complete" % (feeder_id, settings_json[tagNo]['tagID'])
						try:
							urllib2.urlopen(tag_complete_url)
						except Exception, e:
							feeder.logError(e)
						# Leave an empty file called "updated.txt" indicating an occurred update
						feeder.writeFile("%s%s/updated.txt" % (settings_addr,tagNo), "")
						print "File created: %s%s/updated.txt" % (settings_addr,tagNo)
				
				else:
					print "Tag %s hasn't been updated. No need to do anything." % tagNo
	time.sleep(15)		
print "feedmation2.py done running."
print "******************************"
