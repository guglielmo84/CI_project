import json
import os
import csv
import datetime
#import ipdb;ipdb.set_trace()
i = 1
path = "data/"
with open("PRC Data Breach Chronology - 1.13.20.csv", 'r') as f:
  red = csv.reader(f)
  head = next(red)
  try:
    for l in red:
      _tmp=dict()
      for k,v in zip(head, l):
        if not k:
          continue
        _tmp[k] = v
      with open(os.path.join(path, "{}.json".format(i)), "w+") as f:
        json.dump(_tmp,f, ensure_ascii=True)
      i += 1
  except Exception as e:
    print(e)