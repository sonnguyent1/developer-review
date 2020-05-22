import json
import requests
import datetime
import sys
import os
import uuid
import re
import time
import pytz
from flask import g, Markup
from flask import (Blueprint, render_template, make_response,
                   redirect, url_for, abort, request, Response)
from tw33t import app, app_search_logger
from functools import wraps
from flask import jsonify
from twitter import Twitter, OAuth, api


twit = Twitter(auth=OAuth(
    os.environ.get('TWITTER_TOKEN'),
    os.environ.get('TWITTER_TOKEN_SECRET'),
    os.environ.get('TWITTER_CONSUMER_KEY'),
    os.environ.get('TWITTER_CONSUMER_SECRET')
))


@ app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


'''

Introduce a "Get tweets" route for the client and log relevant info from each search into a file.

'''
@ app.route('/tweets', methods=['GET'])
def get_tweets():
    response_data = []
    handle = request.args.get('handle', '')
    try:
        data = twit.statuses.user_timeline(
            screen_name=handle, count=3)
        response_data = [{
            'created_at': datetime.datetime.strptime(t['created_at'],'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC),
            'text': t['text'],
            'photo': t['user']['profile_image_url_https'],
            'name': t['user']['name']
        } for t in data]
    except api.TwitterHTTPError as ex:
        response_data = ex.response_data
    app_search_logger.info('\nSearch tweets by handle: {}\nResult: {}\n'.format(handle, json.dumps(response_data, default=str)))
    return jsonify(response_data)
