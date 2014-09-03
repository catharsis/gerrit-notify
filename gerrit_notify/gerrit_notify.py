from requests.auth import HTTPDigestAuth
import requests
import json
class BadRequest(Exception): pass
class Change(object):
    def __init__(self, json):
        self.fields = dict(json)

    def __getattr__(self, name):
        if name in self.fields:
            return self.fields[name]
        else:
            return None

    def __str__(self):
        return "%s... (%s)" % (self.subject[:15], self.project)

class GerritNotify(object):
    def __init__(self, url, username = None, password = None):
        self.endpoint = url + "/"
        self.auth = None
        if username and password:
            self.endpoint += 'a/' #prefix for authenticated access
            self.auth = HTTPDigestAuth(username, password)

    def open_changes(self):
        query = '?q=status:open'
        return self.changes(query)

    def incoming_changes(self):
        query = '?q=status:open+reviewer:self'
        return self.changes(query)

    def changes(self, query):
        uri = self.endpoint + 'changes/' + query
        resp = requests.get(uri, auth=self.auth,
                headers={'Accept': 'application/json'} # have Gerrit send compacted JSON, gotta preserve those bytes
                )
        if resp.ok:
            #we skip the first line, because Gerrit includes a XSSI prevention prefix there
            return [Change(d) for d in json.loads(resp.text[resp.text.find('\n'):])]
        else:
            raise BadRequest("Failed to fetch incoming changes (%d: %s)" %
                    (resp.status_code, resp.reason))
