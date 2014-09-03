from requests.auth import HTTPDigestAuth
import requests
import json
class Change(object):
    def __init__(self, json):
        self.fields = dict(json)

    def __getattr__(self, name):
        if name in self.fields:
            return self.fields[name]
        else:
            return None

    def __str__(self):
        return str(self.fields)

class GerritNotify(object):
    def __init__(self, url, username = None, password = None):
        self.endpoint = url + "/"
        self.auth = None
        if username and password:
            self.endpoint += 'a/' #prefix for authenticated access
            self.auth = HTTPDigestAuth("alofgren", "/P4ODk67pGp0")



    def incoming_changes(self):
        query = '?q=status:open'
        uri = self.endpoint + 'changes/' + query
        resp = requests.get(uri, auth=self.auth)
        if resp.ok:
            return [Change(d) for d in json.loads(resp.text[resp.text.find('\n'):])]
        else:
            raise BadRequest("Failed to fetch incoming changes (%d: %s)" %
                    (resp.status_code, resp.reason))
