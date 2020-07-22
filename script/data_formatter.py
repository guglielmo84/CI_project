import fileinput
import json
import datetime

#clean data
def format_data(data):
  keys = data.keys()
  _tmp = dict()
  # create custom object for geo data
  _tmp['geo'] = dict()
  for k in keys:
    v = data[k]
    # delete space from json keys
    kk = k.lower().replace(' ','_')
    if k == "Date Made Public":
      # format data to ISO format
      tt = v.split('/')
      b = datetime.date(int(tt[-1]), int(tt[0]) , int(tt[1]))
      _tmp[kk] = b.isoformat()
      _tmp['date'] = b.isoformat()
    elif k in ['Latitude','Longitude']:
      try:
       _tmp['geo'][kk[:3].lower()] = float(v)
      except:
       _tmp['geo'][kk[:3].lower()] = v
    elif k in ['Total Records', "Year of Breach"]:
      try:
       _tmp[kk] = int(v.replace(',',''))
      except:
       _tmp[kk] = ''
    else:
      _tmp[kk] = v.replace('\n', ' ').replace('\u00a0', '')
  return _tmp

# Read all data coming from stdin. Infinite loop.
for line in fileinput.input():

    # Parse JSON data.
    parsedJson = json.loads(line)

    enrichedData = format_data(parsedJson)
    if enrichedData is None:
        continue

    enrichedJson = json.dumps(enrichedData)
    print(enrichedJson)