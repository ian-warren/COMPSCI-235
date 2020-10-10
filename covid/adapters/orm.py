from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from covid.domain import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

comments = Table(
    'comments', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('article_id', ForeignKey('articles.id')),
    Column('comment', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

articles = Table(
    'articles', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('date', Date, nullable=False),
    Column('title', String(255), nullable=False),
    Column('first_para', String(1024), nullable=False),
    Column('hyperlink', String(255), nullable=False),
    Column('image_hyperlink', String(255), nullable=False)
)

tags = Table(
    'tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

article_tags = Table(
    'article_tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('article_id', ForeignKey('articles.id')),
    Column('tag_id', ForeignKey('tags.id'))
)


def map_model_to_tables():
    mapper(model.User, users, properties={
        '_username': users.c.username,
        '_password': users.c.password,
        '_comments': relationship(model.Comment, backref='_user')
    })
    mapper(model.Comment, comments, properties={
        '_comment': comments.c.comment,
        '_timestamp': comments.c.timestamp
    })
    articles_mapper = mapper(model.Article, articles, properties={
        '_id': articles.c.id,
        '_date': articles.c.date,
        '_title': articles.c.title,
        '_first_para': articles.c.first_para,
        '_hyperlink': articles.c.hyperlink,
        '_image_hyperlink': articles.c.image_hyperlink,
        '_comments': relationship(model.Comment, backref='_article')
    })
    mapper(model.Tag, tags, properties={
        '_tag_name': tags.c.name,
        '_tagged_articles': relationship(
            articles_mapper,
            secondary=article_tags,
            backref="_tags"
        )
    })
