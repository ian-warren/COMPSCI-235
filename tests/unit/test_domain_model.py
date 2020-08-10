from datetime import date

from covid.domain.model import User, Article, Tag, make_comment, make_tag_association, ModelException

import pytest


@pytest.fixture()
def article():
    return Article(
        date.fromisoformat('2020-03-15'),
        'Coronavirus travel restrictions: Self-isolation deadline pushed back to give airlines breathing room',
        'The self-isolation deadline has been pushed back',
        'https://www.nzherald.co.nz/business/news/article.cfm?c_id=3&objectid=12316800',
        'https://th.bing.com/th/id/OIP.0lCxLKfDnOyswQCF9rcv7AHaCz?w=344&h=132&c=7&o=5&pid=1.7'
    )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def tag():
    return Tag('New Zealand')


def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for comment in user.comments:
        # User should have an empty list of Comments after construction.
        assert False


def test_article_construction(article):
    assert article.id is None
    assert article.date == date.fromisoformat('2020-03-15')
    assert article.title == 'Coronavirus travel restrictions: Self-isolation deadline pushed back to give airlines breathing room'
    assert article.first_para == 'The self-isolation deadline has been pushed back'
    assert article.hyperlink == 'https://www.nzherald.co.nz/business/news/article.cfm?c_id=3&objectid=12316800'
    assert article.image_hyperlink == 'https://th.bing.com/th/id/OIP.0lCxLKfDnOyswQCF9rcv7AHaCz?w=344&h=132&c=7&o=5&pid=1.7'

    assert article.number_of_comments == 0
    assert article.number_of_tags == 0

    assert repr(
        article) == '<Article 2020-03-15 Coronavirus travel restrictions: Self-isolation deadline pushed back to give airlines breathing room>'


def test_article_less_than_operator():
    article_1 = Article(
        date.fromisoformat('2020-03-15'), None, None, None, None
    )

    article_2 = Article(
        date.fromisoformat('2020-04-20'), None, None, None, None
    )

    assert article_1 < article_2


def test_tag_construction(tag):
    assert tag.tag_name == 'New Zealand'

    for article in tag.tagged_articles:
        assert False

    assert not tag.is_applied_to(Article(None, None, None, None, None, None))


def test_make_comment_establishes_relationships(article, user):
    comment_text = 'COVID-19 in the USA!'
    comment = make_comment(comment_text, user, article)

    # Check that the User object knows about the Comment.
    assert comment in user.comments

    # Check that the Comment knows about the User.
    assert comment.user is user

    # Check that Article knows about the Comment.
    assert comment in article.comments

    # Check that the Comment knows about the Article.
    assert comment.article is article


def test_make_tag_associations(article, tag):
    make_tag_association(article, tag)

    # Check that the Article knows about the Tag.
    assert article.is_tagged()
    assert article.is_tagged_by(tag)

    # check that the Tag knows about the Article.
    assert tag.is_applied_to(article)
    assert article in tag.tagged_articles


def test_make_tag_associations_with_article_already_tagged(article, tag):
    make_tag_association(article, tag)

    with pytest.raises(ModelException):
        make_tag_association(article, tag)
