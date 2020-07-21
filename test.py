import fileinput
import json

def enrichContent(data):
  res = dict()
  for k,v in data.items():
    res[k.lower().replace(' ','_')] = v
  return res

# Read all data coming from stdin. Infinite loop.
for line in fileinput.input():

    # Parse JSON data.
    parsedJson = json.loads(line)

    # Clean tweet text.
    enrichedData = enrichContent(parsedJson)
    if enrichedData is None:
        continue

    enrichedJson = json.dumps(enrichedData)
    print(enrichedJson)
