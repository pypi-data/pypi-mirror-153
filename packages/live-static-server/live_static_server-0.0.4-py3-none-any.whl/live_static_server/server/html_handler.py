import os
from tornado.web import RequestHandler
from bs4 import BeautifulSoup, Comment

def _inject(html_file):
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, features='html.parser')
        head = soup.find('head')
        if head is None:
            soup.append(soup.new_tag('head'))
            head = soup.find('head')

        script_tag = soup.new_tag(name='script', src="/live-static-server.js")
        head.append(Comment('injected by live-static-server'))
        head.append(script_tag)

        return soup.encode()


class HtmlHandler(RequestHandler):
    def initialize(self, path, default_filename=None):
        self.root = path
        self.default_filename = default_filename

    def get(self, captured):
        if captured is None:
            captured = self.default_filename
        try:
            injected_html = _inject(os.path.join(self.root, captured))
            self.write(injected_html)
        except FileNotFoundError:
            self.send_error(404)
