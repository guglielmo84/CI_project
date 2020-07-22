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
        if k == "Date Made Public":
         tt = v.split('/')
         b = datetime.date(int(tt[-1]), int(tt[0]) , int(tt[1]))
         _tmp[k] = b.isoformat()
         _tmp['date'] = b.isoformat()
        elif k in ['Latitude','Longitude']:
         try:
           _tmp[k] = float(v)
         except:
           _tmp[k] = v
        elif k in ['Total Records', "Year of Breach"]:
         try:
           _tmp[k] = int(v.replace(',',''))
         except:
           _tmp[k] = ''
        else:
         _tmp[k] = v.replace('\n', ' ')
      with open(os.path.join(path, "{}.json".format(i)), "w+") as f:
        json.dump(_tmp,f, ensure_ascii=True)
      i += 1
  except Exception as e:
    print(e)
    import ipdb;ipdb.set_trace()
