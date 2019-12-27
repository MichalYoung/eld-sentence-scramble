"""
Display poetry with dynamically revealed translation.
Poetry source is marked up in a simple plain-text format,
which is converted when the page is served.
"""
import config

import flask
from flask import request
from flask import session
from flask import jsonify
from flask import g
import random
import logging

from typing import List

###
# Globals
###
app = flask.Flask(__name__)

# Some resources are located relative to the
# script directory (i.e., to this file)
import os
scriptdir = os.path.dirname(__file__)

import uuid

app.secret_key = str(uuid.uuid4())
app.debug = config.DEBUG
app.logger.setLevel(logging.DEBUG)

##############
# URL routing
###############

@app.route("/")
def index():
    app.logger.debug("Entering index")
    level = session.get("level")
    if not level:
        app.logger.debug(f"session.get('level') returned {level}")
        app.logger.debug("Level not set, redirecting to level chooser")
        return flask.redirect(flask.url_for("choose_level"))

    app.logger.debug(f"Level was set to '{level}'")
    sentence = random.choice(session["sentences"])
    app.logger.debug(f"Selected sentence: {sentence}")
    g.sentence = "".join(sentence)
    g.scrambled = scramble(sentence)
    app.logger.debug(f"Rendering scramble as {g.scrambled}")
    return flask.render_template("scramble.html")

@app.route("/choose")
def choose_level():
    return flask.render_template("choose_level.html")

@app.route("/_choose")
def _choose():
    """Pick a level (== a list of sentences to scramble)"""
    app.logger.debug("Entering '_choose'")
    level=request.args.get("level")
    data = open(f"{scriptdir}/static/data/{level}.txt").readlines()
    session["sentences"] = [s.split() for s in data if not s.startswith("#")]
    session["level"] = level
    app.logger.debug(f"Redirecting to index, level={level}")
    return flask.redirect(flask.url_for("index"))







###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_suggest_completions")
def suggest_completions():
    """
    Up to k suggestions for completing a word
    """
    app.logger.debug("Got a JSON request")
    prefix = request.args.get('prefix', "default", type=str)
    app.logger.debug(f"Prefix: '{prefix}")
    app.logger.debug(f"The request object: {request}")
    app.logger.debug(f"The arguments: '{request.args}")
    if prefix:
        app.logger.debug(f"Looking up '{prefix}' in {len(WORDLIST)} words")
        # completions = get_completions(prefix, 5)
        app.logger.debug(f"Found completions {completions}")
    else:
        app.logger.debug("Didn't have a prefix to look up")
        completions = []
    return jsonify(suggestions=completions)


#############
# Used by request handlers
#############

def scramble(sentence: List[str]) -> List[str]:
    scrambled = sentence.copy()
    while (len(scrambled) > 1 and scrambled == sentence):
        random.shuffle(scrambled)
    return scrambled


#############
#  Startup
#############

if __name__ == "__main__":
    import uuid

    app.secret_key = str(uuid.uuid4())
    app.debug = config.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=config.PORT)


