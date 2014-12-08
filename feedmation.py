import urllib2
import json
import sqlite3

#Pull settings in JSON format from the API
settings_url = "http://feedmation.com/api/v1/sync_data.php?feederid=df34f&function=pull_settings"
settings_json = json.loads(urllib2.urlopen(settings_url).read())

#print json.dumps(settings_json, sort_keys=True,indent=0, separators=(',', ': '))
#print settings_json

#Connect to the SQLite database
dbAddr = '/feedmation/feedmation.db' 
conn = sqlite3.connect(dbAddr)

#Create a cursor for executing SQL statements
c = conn.cursor()

#Create a settings table if it doesn't exist
c.execute("CREATE TABLE IF NOT EXISTS settings(tagNo INT, tagID TEXT PRIMARY KEY, amount REAL, slot1Start INT, slot1End INT, slot2Start INT, slot2End INT)");

for val in settings_json:
  #Check every tag and see if it exists in the settings table
  c.execute("SELECT EXISTS(SELECT * FROM settings WHERE tagID = ?)", (settings_json[val]["tagID"],))
  #If the tag doesn't exist (i.e the fetchone() function fetches no returning row)
  if c.fetchone()[0] == 0:
    #Insert values into database
    c.execute("INSERT INTO settings VALUES (?,?,?,?,?,?,?)", (val, settings_json[val]["tagID"], settings_json[val]["amount"], settings_json[val]["slot1Start"], settings_json[val]["slot1End"], settings_json[val]["slot2Start"], settings_json[val]["slot2End"]))
  else:
      if settings_json[val]["tagUpdate"] == True:
        #Update settings of the corresponding tag
        c.execute("UPDATE settings SET amount = ?, slot1Start = ?, slot1End = ?, slot2Start = ?, slot2End = ? WHERE tagID = ?", (settings_json[val]["amount"], settings_json[val]["slot1Start"], settings_json[val]["slot1End"], settings_json[val]["slot2Start"], settings_json[val]["slot2End"], settings_json[val]["tagID"]))
        #Change the tagUpdate value back to false
        ################################
        #DO SOMETHING WITH THE API HERE#
        ################################
                                                          
#Save changes to the database
conn.commit()
#Close database connection
conn.close()