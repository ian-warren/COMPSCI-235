import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from covid.domain.model import User, Article, Comment, Tag
from covid.adapters.repository import AbstractRepository

tags = None


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_username=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_article(self, article: Article):
        with self._session_cm as scm:
            scm.session.add(article)
            scm.commit()

    def get_article(self, id: int) -> Article:
        article = None
        try:
            article = self._session_cm.session.query(Article).filter(Article._id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return article

    def get_articles_by_date(self, target_date: date) -> List[Article]:
        if target_date is None:
            articles = self._session_cm.session.query(Article).all()
            return articles
        else:
            # Return articles matching target_date; return an empty list if there are no matches.
            articles = self._session_cm.session.query(Article).filter(Article._date == target_date).all()
            return articles

    def get_number_of_articles(self):
        number_of_articles = self._session_cm.session.query(Article).count()
        return number_of_articles

    def get_first_article(self):
        article = self._session_cm.session.query(Article).first()
        return article

    def get_last_article(self):
        article = self._session_cm.session.query(Article).order_by(desc(Article._id)).first()
        return article

    def get_articles_by_id(self, id_list):
        articles = self._session_cm.session.query(Article).filter(Article._id.in_(id_list)).all()
        return articles

    def get_article_ids_for_tag(self, tag_name: str):
        article_ids = []

        # Use native SQL to retrieve article ids, since there is no mapped class for the article_tags table.
        row = self._session_cm.session.execute('SELECT id FROM tags WHERE name = :tag_name', {'tag_name': tag_name}).fetchone()

        if row is None:
            # No tag with the name tag_name - create an empty list.
            article_ids = list()
        else:
            tag_id = row[0]

            # Retrieve article ids of articles associated with the tag.
            article_ids = self._session_cm.session.execute(
                    'SELECT article_id FROM article_tags WHERE tag_id = :tag_id ORDER BY article_id ASC',
                    {'tag_id': tag_id}
            ).fetchall()
            article_ids = [id[0] for id in article_ids]

        return article_ids

    def get_date_of_previous_article(self, article: Article):
        result = None
        prev = self._session_cm.session.query(Article).filter(Article._date < article.date).order_by(desc(Article._date)).first()

        if prev is not None:
            result = prev.date

        return result

    def get_date_of_next_article(self, article: Article):
        result = None
        next = self._session_cm.session.query(Article).filter(Article._date > article.date).order_by(asc(Article._date)).first()

        if next is not None:
            result = next.date

        return result

    def get_tags(self) -> List[Tag]:
        tags = self._session_cm.session.query(Tag).all()
        return tags

    def add_tag(self, tag: Tag):
        with self._session_cm as scm:
            scm.session.add(tag)
            scm.commit()

    def get_comments(self) -> List[Comment]:
        comments = self._session_cm.session.query(Comment).all()
        return comments

    def add_comment(self, comment: Comment):
        super().add_comment(comment)
        with self._session_cm as scm:
            scm.session.add(comment)
            scm.commit()

def article_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:

            article_data = row
            article_key = article_data[0]

            # Strip any leading/trailing white space from data read.
            article_data = [item.strip() for item in article_data]

            number_of_tags = len(article_data) - 6
            article_tags = article_data[-number_of_tags:]

            # Add any new tags; associate the current article with tags.
            for tag in article_tags:
                if tag not in tags.keys():
                    tags[tag] = list()
                tags[tag].append(article_key)

            del article_data[-number_of_tags:]

            yield article_data


def get_tag_records():
    tag_records = list()
    tag_key = 0

    for tag in tags.keys():
        tag_key = tag_key + 1
        tag_records.append((tag_key, tag))
    return tag_records


def article_tags_generator():
    article_tags_key = 0
    tag_key = 0

    for tag in tags.keys():
        tag_key = tag_key + 1
        for article_key in tags[tag]:
            article_tags_key = article_tags_key + 1
            yield article_tags_key, article_key, tag_key


def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]

            if post_process is not None:
                row = post_process(row)
            yield row


def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    global tags
    tags = dict()

    insert_articles = """
        INSERT INTO articles (
        id, date, title, first_para, hyperlink, image_hyperlink)
        VALUES (?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_articles, article_record_generator(os.path.join(data_path, 'news_articles.csv')))

    insert_tags = """
        INSERT INTO tags (
        id, name)
        VALUES (?, ?)"""
    cursor.executemany(insert_tags, get_tag_records())

    insert_article_tags = """
        INSERT INTO article_tags (
        id, article_id, tag_id)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_article_tags, article_tags_generator())

    insert_users = """
        INSERT INTO users (
        id, username, password)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))

    insert_comments = """
        INSERT INTO comments (
        id, user_id, article_id, comment, timestamp)
        VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_comments, generic_generator(os.path.join(data_path, 'comments.csv')))

    conn.commit()
    conn.close()

