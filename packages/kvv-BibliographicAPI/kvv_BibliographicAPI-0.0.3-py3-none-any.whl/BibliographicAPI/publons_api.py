import requests
import json
from StoredObjects import Author, Publication

_token = None
_baseUrl = 'https://publons.com/api/v2/'

def setToken(token):
    global _token
    _token = token

def _request(url):
    if _token == None:
        print("Publons token was not provided")
        return
    headers = {'Authorization': 'Token ' + _token, 'Content-Type': 'application/json'}
    url = url.removeprefix(_baseUrl)
    r = requests.get(_baseUrl + url, headers=headers)
    if r.status_code != 200:
        raise Exception("Publons returned an error:\n" + r.text)
    try:
        r = r.json()
        if "detail" in r:
            if (r['detail'] == 'Invalid token.'):
                print("Publons token is invalid")
        else:
            return r
    except:
        print('There was an error communiating with the Publons API')

def _getID(author: Author):
    id = author.publonsID
    if id is None:
        id = author.researcherID
    if id is None:
        id = author.orcID
    return id

def addAuthorIDs(author: Author):
    id = _getID(author)
    if id is None:
        return False
    url = 'academic/' + id
    json_obj = _request(url)
    ids = json_obj['ids']
    author.publonsID = ids['id']
    author.researcherID = ids['rid']
    author.orcid = ids['orcid']
    return True


def getPublicationsOfAuthor(author: Author):
    id = _getID(author)
    if id is None:
        return None
    url = 'academic/publication/?academic=' + id
    json_obj = _request(url)
    publications = []
    while True:
        results = json_obj['results']
        for res in results:
            info = res['publication']
            
            pub = Publication()
            pub.title = info['title']
            if info['ids'] is not None:
                ids = info['ids']
                pub.doi = ids['doi']
                pub.ut = ids['ut']
                existingPub = author.searchPublicationByDOI(pub.doi)
                if existingPub is not None:
                    existingPub.mergeIDs(pub)
                else:
                    publications.append(pub)
                    author.publications.append(pub)

        
        url = json_obj['next']
        if url is None:
            break
        json_obj = _request(url)
    return publications


def getAuthorsOfUniversity():
    inst = 'Murmansk State Technical University'
    url = 'academic/?institution=' + inst
    json_obj = _request(url)
    while True:
        print(json_obj['count'])

        url = json_obj['next']
        if url is None:
            break
        json_obj = _request(url)
    
