import datetime
import os
import hashlib

# Feeder ID
feeder_id = "5df06ab0ed3a16bd4a12ffb15542eea4c18625bc"

# Settings urls
settings_url = "http://feedmation.com/api/v1/sync_data.php?feederid=%s&function=pull_settings" % feeder_id
# Settings local folder address
settings_addr = "/feedmation/settings/"  # Note that this address might be different from the one on the board

# Feed Now urls
feednow_url = "http://feedmation.com/api/v1/sync_data.php?feederid=%s&function=feed_now" % feeder_id
feednow_complete_url = "http://feedmation.com/api/v1/sync_data.php?feederid=%s&function=feednow_complete" % feeder_id
# Feed Now local folder address
feednow_addr = "/feedmation/feednow/"  # Note that this address might be different from the one on the board

# Data logging urls
logging_url = "http://feedmation.com/api/v1/sync_data.php"
tank_empty_url = "http://www.feedmation.com/api/v1/sync_data.php?feederid=%s&function=tank_empty" % feeder_id
tank_full_url = "http://www.feedmation.com/api/v1/sync_data.php?feederid=%s&function=tank_full" % feeder_id
# Data logging local folder addresses
tank_stat_addr = "/feedmation/tank_status/"  # Note that this tank_stat_address might be different from the one on the board
log_data_addr = "/feedmation/log_data/"  # Note that this tank_stat_address might be different from the one on the board

# Function for logging errors
def logError(error):
  error_log = "/feedmation/log/"  # Note that this address might be different from the one on the board
  if not os.path.exists(error_log):
		os.makedirs(error_log)
	# Get the current date and time
  i = datetime.datetime.now()
	# Log the date, time and error
  log = open("%serror_log.txt" % error_log, 'a') 
  log.write("%s: %s\n" % (i, error))
  log.close
  print "Error: %s" % error
  
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