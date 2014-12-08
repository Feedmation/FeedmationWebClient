import urllib2
import json
import os
import datetime
#import feeder  # A custom module containing some related functions

# Function for logging errors
def logError(error):
	# Get the current date and time
	i = datetime.datetime.now()
	# Log the date, time and error
	error = open(error_log, 'a') 
	error.write("%s: %s\n" % (i, error))
	error.close
  
# Function for writing files
def writeFile(address, content):
	try:
		file = open(address, 'w')
	except Exception, e:
		logError(e)
	file.write(content)
	file.close()

# Function for reading files
def readFile(address):
	try:
		file = open(address, 'r')
	except Exception, e:
		logError(e)
	content = file.read()
	file.close()
	return content
	
# Pull settings in JSON format from the API
#feeder_id = "meow1234"  # My feeder
#feeder_id = "df34f"  # Josh's feeder
feeder_id = "12345" # Josh's other feeder
settings_url = "http://feedmation.com/api/v1/sync_data.php?feederid=%s&function=pull_settings" % feeder_id
settings_json = json.loads(urllib2.urlopen(settings_url).read())

#print json.dumps(settings_json, sort_keys=True,indent=0, separators=(',', ': '))
#print settings_json

# Addresses of folders and files
addr = "/feedmation/settings/"  # Note that this address might be different from the one on the board
error_log = "/feedmation/log/error_log.txt"  # Note that this address might be different from the one on the board

# Check each folder in the settings directory
for folder in os.listdir(addr):
	# If an existing tag in the folders no longer exists in the json object, it has been deleted by the user.
	# In this case, wipe out everything in the corresponding folder and leave a file "deleted.txt" with the tagID of the deleted tag in it.
	# Check if a tag slot number in the settings directory exists in the json object
	# If not, the corresponding tag has been deleted. Wipe out files and leave "deleted.txt"
	if settings_json[folder] is None:
		# Get the tagID of the deleted tag
		deletedID = None
		if os.path.isfile("%s%s/tagID.txt" % (addr, folder)):
			deletedID = readFile("%s%s/tagID.txt" % (addr, folder))
		# Delete every file in the folder
		for the_file in os.listdir(addr+folder):
			file_path = os.path.join(addr+folder, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
			except Exception, e:
				logError(e)
		# Leave the "deleted.txt" file with the deleted tagID
		if not deletedID is None:
			writeFile("%s%s/deleted.txt" % (addr, folder), deletedID)
    
for tagNo in settings_json:
	# If folder does not exist, create one
	if not os.path.exists(addr+tagNo):
		try:
			os.makedirs(addr+tagNo)
		except Exception, e:
			logError(e)
	if settings_json[tagNo]:
		# If file does not exist, create file
		# OR
		# If 'tagUpdate' is true, a change of settings has occurred to the tag. Rewrite the corresponding files.
		if (not os.listdir("%s%s" % (addr,tagNo))) or (os.listdir("%s%s" % (addr,tagNo)) == [u'deleted.txt']) or (settings_json[tagNo]['tagUpdate'] == True):
			print tagNo
			# If a "deleted.txt" exists, delete it
			try:
				if os.path.isfile("%s%s/deleted.txt" % (addr,tagNo)):
					os.unlink("%s%s/deleted.txt" % (addr,tagNo))
			except Exception, e:
				logError(e)
			for key in settings_json[tagNo]:
				# We don't need a "tagUpdate.txt"
				if not key == "tagUpdate":
					writeFile("%s%s/%s.txt" % (addr,tagNo,key), settings_json[tagNo][key])
			if settings_json[tagNo]['tagUpdate'] == True:
				# Tell the API the update is done
				tag_complete_url = "http://feedmation.com/api/v1/sync_data.php?feederid=%s&tagid=%s&function=tag_complete" % (feeder_id, settings_json[tagNo]['tagID'])
				urllib2.urlopen(tag_complete_url)
				# Leave an empty file called "updated.txt" indicating an occurred update
				writeFile("%s%s/updated.txt" % (addr,tagNo), "")	
