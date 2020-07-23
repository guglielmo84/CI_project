import fileinput
import json
import datetime
import re
import string

stopwords = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"])
    

def removeURLs(text):
    cleanText = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    return cleanText

# Remove all special chars from text.
def removeSpecialChars(text):
    cleanText = re.sub(r'[\r\n]+', ' ', text, flags=re.MULTILINE)
    cleanText = cleanText.replace("RT", "")
    return cleanText

def removeAllPuntuaction(text):
    ret = ""
    for c in text:
        if c in string.punctuation:
            ret = ret + " "
        else:
            ret = ret + c
    tokens = re.compile(r"\s+").split(ret.strip())
    return " ".join(tokens)

def clean_text(text, toLower=True, mustRemoveURLs=True):
    if toLower:
        textRet = text.lower()
    else:
        textRet = text
    if mustRemoveURLs:
        textRet = removeURLs(textRet)
    textRet = removeSpecialChars(textRet)
    textRet = removeAllPuntuaction(textRet)
    tokens = re.compile(r"\s+").split(textRet)
    filtered_words = [w for w in tokens if w if not w in stopwords]
    return " ".join(filtered_words).strip()


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
    if k == "Description of incident":
      _tmp[kk] = clean_text(v)
    elif k == "Date Made Public":
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
