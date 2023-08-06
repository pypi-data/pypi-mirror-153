import logging
import csv
import re
import os
from pathlib import Path
from enum import Enum, auto
from qary.etl.netutils import download_if_necessary
from qary.etl.news import get_news_stories_text
from joblib import load, dump
from time import time
from sklearn.linear_model import SGDClassifier
from numpy import argmax, mean, append
from qary.skills.base import BotReply
from qary.config import DATA_DIR

log = logging.getLogger(__name__)


class State(Enum):
    WELCOME = auto()
    PULSE = auto()
    SELECT = auto()
    FEEDBACK = auto()


RE_STORY_SELECT = r"\d+"  # only digits in statement (headline select)
RE_USER_FEEDBACK = r"like|dislike|good|bad|positive|negative|more|less"


class Skill:
    """Skill to give users personalized prosocial local news"""

    def __init__(self, display_stories=21, refresh_interval=3600):
        self.display_stories = display_stories
        self.refresh_interval = refresh_interval  # seconds

        self.model_dir = DATA_DIR + "/pulse/allusers/"
        self.history_path = DATA_DIR + "/pulse/allusers/reading_history.csv"

        self.last_intent = None

        # list of stories, each story is dictionary with story title, article urls, article contents and probability scores
        self.stories = []
        self.previous_news_fetch_time = 0

        log.info("Loading models...")
        self.fb_model = load(download_if_necessary(
            "https://static-proai-org.nyc3.digitaloceanspaces.com/qary/data/fb_content_regressor.joblib"))
        self.fb_vectorizer = load(download_if_necessary(
            "https://static-proai-org.nyc3.digitaloceanspaces.com/qary/data/fb_vectorizer.joblib"))

        # fb_reactions_scaler = load(self.MODEL_DIRECTORY + "fb_reactions_scaler.joblib")
        # maybe needed in future, docs say to scale before SGDclassifier

        Path(self.model_dir).mkdir(parents=True, exist_ok=True)

        # creates a model with seed examples if not already there
        if not os.path.isfile(self.model_dir + "user_model.joblib"):
            self.user_model = SGDClassifier(random_state=3, warm_start=True, loss="log")
            self.user_model.fit([[0, 0.25, 0.75, 0, 0.5, 0, 1], [0.5, 0.1, 0.5, 1, 0.1, 1, 0]], [1, 0])
        else:
            self.user_model = load(self.model_dir + "user_model.joblib")

    def recognize_intent(self, statement):
        if not isinstance(statement, str):
            self.last_intent = State.WELCOME
        elif statement == "pulse":
            self.last_intent = State.PULSE
        elif re.fullmatch(RE_STORY_SELECT, statement) is not None and (
                self.last_intent == State.PULSE or
                self.last_intent == State.SELECT or
                self.last_intent == State.FEEDBACK):  # read multiple articles
            self.last_intent = State.SELECT
        elif self.last_intent == State.SELECT and re.search(RE_USER_FEEDBACK, statement):
            self.last_intent = State.FEEDBACK
        return self.last_intent

    def reply(self, statement, context=None):
        """Suggest responses to a user statement string with [(score, reply_string)..]"""
        self.update_news()

        if self.last_intent == State.SELECT:    # won't do time and feedback based training for same article
            self.time_adjust_user_model()

        intent = self.recognize_intent(statement)

        if intent == State.WELCOME:
            return [BotReply(0, "The `pulse` skill is loaded. To fetch the current news, enter \"pulse\". To choose a "
                                "news story, enter a number corresponding to a headline. To give feedback after reading "
                                "an article, tell me if you liked what you read.")]

        elif intent == State.PULSE:
            mean_story_score = mean([mean(story["scores"]) for story in self.stories])
            return [BotReply(mean_story_score, self.headlines())]

        elif intent == State.SELECT:
            story_selection = int(statement)

            if not 0 <= story_selection < self.display_stories:
                return [BotReply(1, "Must enter number in range 0 to {} for `pulse` headline selection".format(
                    self.display_stories))]

            # selects highest scored article in selected news story
            article = self.stories[story_selection]["articles"][argmax(self.stories[story_selection]["scores"])]
            self.last_article = article
            self.last_article_reading_start_time = time()
            return [(1, '\n' + article)]

        elif intent == State.FEEDBACK:
            self.feedback_adjust_user_model(
                re.search(RE_USER_FEEDBACK, statement).group())  # only uses first feedback word
            return [(1, "Your preferences have been adjusted.")]

        else:
            return [BotReply(0.05, "I don't think that's a pulse command")]

    def headlines(self):
        """Formats headlines with selection number"""
        headlines = "\n\n"

        for story_index in range(self.display_stories):
            headlines += "{} {}\n".format(story_index, self.stories[story_index]["title"])

        return headlines

    def update_news(self):
        """Fetches and scores current news stories if last updated longer ago than refresh interval"""
        if time() - self.previous_news_fetch_time > self.refresh_interval:
            log.info("Fetching news...")
            self.stories = get_news_stories_text()

            log.info("Analyzing news stories...")
            for story in self.stories:
                story["scores"] = [self.score_article(self.article_inference(article)) for article in story["articles"]]

            # sometimes scraper fails to get articles, need to give empty stories 0 score
            self.stories.sort(key=lambda story: mean(story["scores"]) if len(story["scores"]) > 0 else 0, reverse=True)
            self.stories = self.stories[:self.display_stories]

    def article_inference(self, article):
        """Creates vector for given article"""
        return self.fb_model.predict(self.fb_vectorizer.transform([article]))  # fb_reactions_scaler.transform(

    def score_article(self, article_vector):
        """Scores article vector on user preferences"""
        return self.user_model.predict_proba(article_vector)[0][1]

    def time_adjust_user_model(self):
        """Updates user model with estimate of whether user liked the article based on reading speed"""
        expected_reading_time = len(self.last_article) / 22  # using 22 characters/sec reading speed
        reading_time = time() - self.last_article_reading_start_time

        if reading_time < expected_reading_time / 2:
            self.user_model.partial_fit(self.article_inference(self.last_article), [0])
        elif reading_time > expected_reading_time * 10:
            return  # unlikely that user actually read the article
        else:
            self.user_model.partial_fit(self.article_inference(self.last_article), [1])

        self.record_article(reading_time)

    def feedback_adjust_user_model(self, feedback):
        """Updates user model with direct user feedback"""
        if feedback == "like" or feedback == "good" or feedback == "positive" or feedback == "more":
            self.user_model.partial_fit(self.article_inference(self.last_article), [1])
        else:
            self.user_model.partial_fit(self.article_inference(self.last_article), [0])

        self.record_article()

    def record_article(self, reading_time=-1):
        has_header = os.path.isfile(self.history_path)
        with open(self.history_path, "a+") as history_csv:
            writer = csv.writer(history_csv)
            if not has_header:
                writer.writerow(
                    ["fb_wow", "fb_haha", "fb_like", "fb_sad", "fb_care", "fb_angry", "fb_love", "reading_time",
                     "predicted_probability"])
            article_vector = self.article_inference(self.last_article)
            writer.writerow(
                append(article_vector, [reading_time, self.score_article(article_vector)]))

        dump(self.user_model, self.model_dir + "user_model.joblib")
