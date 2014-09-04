from requests.auth import HTTPDigestAuth
from os import makedirs
from os.path import expanduser, exists, join
import requests
import json
class BadRequest(Exception): pass
class Change(object):
    def __init__(self, json):
        self.fields = dict(json)

    def shorten_string(self, s, l=15, reverse=False):
        cut = "..."
        l = l - len(cut)
        if len(s) > l:
            if reverse:
                return cut + s[len(s) - l:]
            else:
                return s[:l] + cut
        else:
            return s

    def __getattr__(self, name):
        if name in self.fields:
            return self.fields[name]
        else:
            return None

    def __str__(self):
        return "%s (%s)" % (
                self.shorten_string(self.subject),
                self.shorten_string(self.project, reverse=True)
                )

class GerritNotify(object):
    _cache_dir = expanduser('~/.cache/gerrit-notify')
    _icon_path = join(_cache_dir, 'icon')

    def __init__(self, url, username = None, password = None):
        self.url = url
        self.endpoint = self.url + "/"
        self.auth = None
        if username and password:
            self.endpoint += 'a/' #prefix for authenticated access
            self.auth = HTTPDigestAuth(username, password)

        if not exists(self._cache_dir):
            makedirs(self._cache_dir)


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

    @property
    def icon(self):
        iconfile = self._icon_path
        if not exists(iconfile):
            resp = requests.get(self.url + '/' + 'favicon.ico')
            icondata = resp.content
            with open(iconfile, 'wb') as f:
                f.write(icondata)
        return iconfile
