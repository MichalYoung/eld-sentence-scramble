"""
A simple game for English language development students in
primary school.   English sentences are presented with a
scrambled word order.  Students click each word to put it in
correct English order (e.g., adjectives come before nouns).


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

app.secret_key = config.get("app_key")
app.debug = config.get("debug")
if app.debug:
    app.logger.setLevel(logging.DEBUG)
else:
    app.logger.setLevel(logging.INFO)

##############
# URL routing
###############

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Entering index")
    level = session.get("level")
    if not level:
        app.logger.debug(f"session.get('level') returned {level}")
        app.logger.debug("Level not set, redirecting to level chooser")
        return flask.redirect(flask.url_for("choose_level"))

    app.logger.debug(f"Level was set to '{level}'")
    sentence = load_sentence(level).split()
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
    try:
        level=request.args.get("level")
        session["level"] = level
        app.logger.debug(f"Redirecting to index, level={level}")
        return flask.redirect(flask.url_for("index"))
    except:
        return flask.redirect(flask.url_for("choose_level"))


#############
# Used by request handlers
#############

def scramble(sentence: List[str]) -> List[str]:
    scrambled = sentence.copy()
    while (len(scrambled) > 1 and scrambled == sentence):
        random.shuffle(scrambled)
    return scrambled

def load_sentence(level: str) -> str:
    """Selects a random sentence from the levels
    file.
    Note we read the whole file on each
    interaction, in preference to making the session
    object large.   If this becomes a performance issue,
    we can interpose a database and read a single sentence
    from it.  It is unlikely to be a problem for level files
    under several kilobytes.
    """
    data = open(f"{scriptdir}/static/data/{level}.txt").readlines()
    limit = 1000
    attempts = 1
    sentence = random.choice(data)
    while sentence.startswith("#"):
        attempts += 1
        assert attempts < limit, "Did not find non-comment line in level file"
        sentence = random.choice(data)
    return sentence



#############
#  Startup
#############

if __name__ == "__main__":
    import uuid

    app.secret_key = str(uuid.uuid4())
    app.debug = config.get("debug")
    app.logger.setLevel(logging.DEBUG)
    app.run(port=config.PORT)


