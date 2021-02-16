import feedparser

"""
The render_template function is the magic which takes a Jinja template as input
and produces pure HTML, capable of being read by any browser, as the output
"""
from flask import Flask

from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'hackernews': 'http://feeds.feedburner.com/TheHackersNews',
            'welivesecurity': 'http://feeds.feedburner.com/eset/blog',
            'krebsonsecurity': 'http://feeds.feedburner.com/krebsonsecurity.com/',
            'threatpost': 'http://feeds.feedburner.com/threatpost',
             'nakedsecurity':'http://feeds.feedburner.com/nakedsecurity'}

# app route for default and bbc
@app.route("/", methods=['GET','POST'])
def publish_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "hackernews"
        pass
    else:
        publication = query.lower()
    return get_news(publication)
    # rest of code unchanged
    pass


# function that calls the publications
def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    #first_article = feed['entries'][0]
    return render_template("home.html", articles=feed['entries'])

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
