# File: CheckTags.py
"""
This program checks that tags are properly matched in an HTML file.
This version of the program runs in Python; the checktags version runs
directly from the command line.
"""

import html.parser
import urllib.request

def CheckTags():
    """Reads a URL from the user and then checks it for tag matching."""
    url = input("URL: ")
    checkURL(url)

def checkURL(url):
    """Checks whether the tags are balanced in the specified URL."""
    try:
        response = urllib.request.urlopen(url)
        parser = BrokenLinks(url)
        parser.checkTags(response.read().decode("UTF-8"))
        if response.status in range(400,500):
            print(f"{response.status}: {url} at line {parser.getpos()[0]}")
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason} at line {parser.getpos()[0]}")
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code}: {e.reason} at line {parser.getpos()[0]}")
    except urllib.error.ContentTooShortError as e:
        print(f"ContentTooShort: {e.code}: {e.reason} at line {parser.getpos()[0]}")
    except ValueError:
        print(f"UrlError: {url} is not a valid url")


class HTMLTagParser(html.parser.HTMLParser):

    """
    This class extends the standard HTML parser and overrides the
    callback methods used for start and end tags.
    """

    def __init__(self):
        """Creates a new HTMLTagParser object."""
        html.parser.HTMLParser.__init__(self)

    def checkTags(self, text):
        """Checks that the tags are balanced in the supplied text."""
        self._stack = [ ]
        self.feed(text)
        while len(self._stack) > 0:
            startTag,startLine = self._stack.pop()
            print("Missing </" + startTag + "> for <" + startTag +
                  "> at line " + str(startLine))

    def handle_starttag(self, startTag, attributes):
        """Overrides the callback function for start tags."""
        startLine,_ = self.getpos()
        self._stack.append((startTag, startLine))

    def handle_endtag(self, endTag):
        """Overrides the callback function for end tags."""
        endLine,_ = self.getpos()
        if len(self._stack) == 0:
            print("No <" + endTag + "> for </" + endTag +
                  "> at line " + str(endLine))
        else:
            while len(self._stack) > 0:
                startTag,startLine = self._stack.pop()
                if startTag == endTag:
                    break;
                print("Missing </" + startTag + "> for <" + startTag +
                      "> at line " + str(startLine))

# Startup code
class BrokenLinks(HTMLTagParser):
    def __init__(self, url):
        """Creates a new HTMLTagParser object."""
        super().__init__()
        self.url = url

    def handle_starttag(self, startTag, attributes):
        """Overrides the callback function for start tags."""
        for i in attributes:
            if i[0] in ['src','href']:
                if "mailto:" and "@" in i[1]:
                    pass # don't try to visit email
                elif '://' in i[1]:
                    self.verifyURL(i[1], startTag)
                else:
                    self.verifyURL(self.url + (i[1] if '/' in i[1] else f'/{i[1]}'), startTag)
        startLine,_ = self.getpos()
        self._stack.append((startTag, startLine))

    def verifyURL(self, url, tag):
        try:
            response = urllib.request.urlopen(url)
        except urllib.error.URLError as e:
            startLine,_ = self.getpos()
            print(f"Broken link {url} in {tag} tag at line {startLine} {e}")

if __name__ == "__main__":
    CheckTags()
