import time
import urllib
import urllib2
import json
import os
import feeder  # A custom module containing some related functions

print "******************************"
print "data_logging.py running..."

while(1):
  feeder_id = feeder.feeder_id # get from the feeder module (feeder.py)
  logging_url = feeder.logging_url # get from the feeder module (feeder.py)
  tank_empty_url = feeder.tank_empty_url # get from the feeder module (feeder.py)
  tank_full_url = feeder.tank_full_url # get from the feeder module (feeder.py)
  
  # Addresses of folders and files
  tank_stat_addr = feeder.tank_stat_addr # get from the feeder module (feeder.py)
  log_data_addr = feeder.log_data_addr # get from the feeder module (feeder.py)
  
  # If folder does not exist, create one
  if not os.path.exists(tank_stat_addr):
    try:
      os.makedirs(tank_stat_addr)
    except Exception, e:
      feeder.logError(e)
  if not os.path.exists(log_data_addr):
    try:
      os.makedirs(log_data_addr)
    except Exception, e:
      feeder.logError(e)
      
  # Check if tank_empty.txt exists. If yes, notify API and delete tank_empty.txt
  print "Checking if tank_empty.txt exists..."
  if os.path.isfile("%stank_empty.txt" % tank_stat_addr):
    print "tank_empty.txt exists. Notifying API..."
    try:
      urllib2.urlopen(tank_empty_url)
    except Exception, e:
      feeder.logError(e)
    print "Deleting tank_empty.txt..."
    try:
      os.unlink("%stank_empty.txt" % tank_stat_addr)
    except Exception,e:
      feeder.logError(e)
  else:
    print "tank_empty.txt does not exist."
    
  # Check if tank_full.txt exists. If yes, notify API and delete tank_full.txt
  print "Checking if tank_full.txt exists..."
  if os.path.isfile("%stank_full.txt" % tank_stat_addr):
    print "tank_full.txt exists. Notifying API..."
    try:
      urllib2.urlopen(tank_full_url)
    except Exception, e:
      feeder.logError(e)
    print "Deleting tank_full.txt..."
    try:
      os.unlink("%stank_full.txt" % tank_stat_addr)
    except Exception,e:
      feeder.logError(e)
  else:
    print "tank_full.txt does not exist."
  
  # Get logging data from files
  print "Checking log data..."
  for file in os.listdir(log_data_addr):
    if os.path.isfile("%s%s" % (log_data_addr,file)):
      print "Found a log file: %s Parsing..." % file
      try:
        data = feeder.readFile("%s%s" % (log_data_addr,file)).split(',')
      except Exception, e:
        feeder.logError(e)
      print data
      # Send logging data to API via POST
      values = {"feederid": feeder_id,
        "function": "log_data",
        "tagid": data[0],
        "time": data[1],
		"eatenWeight": data[3],
		"amtFedWeight": data[2],
		"petWeight": data[4]}
      print values
      data = urllib.urlencode(values)   # Encode values for POST request
      req = urllib2.Request(logging_url, data)
      try:
        urllib2.urlopen(req)
      except Exception, e:
        feeder.logError(e)
      print "Deleting reported log file..."
      try:
        os.unlink("%s%s" % (log_data_addr,file))
      except Exception,e:
        feeder.logError(e)

  time.sleep(15)
  
print "data_logging.py done running."
print "******************************"