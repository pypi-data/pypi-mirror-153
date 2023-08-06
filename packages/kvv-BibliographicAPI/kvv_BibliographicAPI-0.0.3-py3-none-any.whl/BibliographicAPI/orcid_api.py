import requests
import json
from StoredObjects import Author, Publication

_baseUrl = 'https://pub.orcid.org/v3.0/'
_expandedSearch = _baseUrl + 'expanded-search/?q='

def getOrcidByName(author: Author):
    finalUrl = _expandedSearch + '"' + author.engName + '"'

    headers = {'content-type': 'application/json'}
    response = requests.get(finalUrl, headers=headers)
    json_str = response.text

    x = json.loads(json_str)
    result = x['expanded-result']
    for field in result:
        affils = field['institution-name']
        for inst in affils:
            if inst.startswith("Murmansk State"):
                return field['orcid-id']
    return None
