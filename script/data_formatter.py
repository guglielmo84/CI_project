import fileinput
import json

def enrichContent(data):
  res = dict()
  res['geo'] = dict()
  for k,v in data.items():
    if k.lower() in ['latitude', 'longitude']:
      res['geo'][k[:3].lower()] = v
      continue
    res[k.lower().replace(' ','_')] = v
  return res

# Read all data coming from stdin. Infinite loop.
for line in fileinput.input():

    # Parse JSON data.
    parsedJson = json.loads(line)

    enrichedData = enrichContent(parsedJson)
    if enrichedData is None:
        continue

    enrichedJson = json.dumps(enrichedData)
    print(enrichedJson)