"""
imdb.py - Phenny IMDB Module
Author: Gaganpreet, http://gaganpreet.in
"""
from lxml.html import parse
import urllib, re

def imdb(phenny, input):
    origterm = input.groups()[1]
    if not origterm:
       return phenny.say('Perhaps you meant ".wik Zen"?')
    origterm = origterm.encode('utf-8')

    doc = parse("http://m.imdb.com/find?q=" + urllib.quote(origterm));
    try:
        first_result = doc.xpath("/html/body/section/div/div/div")[0];
        movie_name = first_result.text_content().strip();
        movie_url = first_result.xpath("a")[0].get("href");
    except:
        return phenny.say("No result");

    re_uri = re.compile("\/title\/tt[0-9]*\/");

    if re_uri.match(movie_url):
        doc = parse("http://m.imdb.com" + movie_url).getroot();

        details = doc.cssselect("section.details")[0];

        for i in details.xpath('div/h1'):
            if i.text == "Genre":
                genre = i.getnext().text;

        try:
            rating = doc.xpath("/html/body/section/a/p/strong")[0].text; #Unreleased movies have no rating
        except:
            rating = "";
    else:
        return phenny.say("No result");
    return phenny.say(movie_name + " - " + genre + " - " + rating + "/10 - http://imdb.com" + movie_url);

    phenny.say(movie_name + " " + movie_url);
imdb.commands = ["imdb"];

if __name__ == '__main__':
   print __doc__.strip()

