from datetime import date, datetime
from typing import List

import pytest

from covid.domain.model import User, Article, Tag, Comment, make_comment
from covid.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_article_count(in_memory_repo):
    number_of_articles = in_memory_repo.get_number_of_articles()

    # Check that the query returned 6 Articles.
    assert number_of_articles == 6


def test_repository_can_add_article(in_memory_repo):
    article = Article(
        date.fromisoformat('2020-03-09'),
        'Second US coronavirus cruise tests negative amid delays and cancellations',
        'It was revealed ...',
        'https://www.nzherald.co.nz/travel/news/article.cfm?c_id=7&objectid=12315024',
        'https://www.nzherald.co.nz/resizer/ix7hy3lzkMWUkD8hE6kdZ-8oaOM=/620x349/smart/filters:quality(70)/arc-anglerfish-syd-prod-nzme.s3.amazonaws.com/public/7VFOBLCBCNDHLICBY3CTPFR2L4.jpg',
        7
    )
    in_memory_repo.add_article(article)

    assert in_memory_repo.get_article(7) is article


def test_repository_can_retrieve_article(in_memory_repo):
    article = in_memory_repo.get_article(1)

    # Check that the Article has the expected title.
    assert article.title == 'Coronavirus: First case of virus in New Zealand'

    # Check that the Article is commented as expected.
    comment_one = [comment for comment in article.comments if comment.comment == 'Oh no, COVID-19 has hit New Zealand'][
        0]
    comment_two = [comment for comment in article.comments if comment.comment == 'Yeah Freddie, bad news'][0]

    assert comment_one.user.username == 'fmercury'
    assert comment_two.user.username == "thorke"

    # Check that the Article is tagged as expected.
    assert article.is_tagged_by(Tag('Health'))
    assert article.is_tagged_by(Tag('New Zealand'))


def test_repository_does_not_retrieve_a_non_existent_article(in_memory_repo):
    article = in_memory_repo.get_article(101)
    assert article is None


def test_repository_can_retrieve_articles_by_date(in_memory_repo):
    articles = in_memory_repo.get_articles_by_date(date(2020, 3, 1))

    # Check that the query returned 3 Articles.
    assert len(articles) == 3


def test_repository_does_not_retrieve_an_article_when_there_are_no_articles_for_a_given_date(in_memory_repo):
    articles = in_memory_repo.get_articles_by_date(date(2020, 3, 8))
    assert len(articles) == 0


def test_repository_can_retrieve_tags(in_memory_repo):
    tags: List[Tag] = in_memory_repo.get_tags()

    assert len(tags) == 4

    tag_one = [tag for tag in tags if tag.tag_name == 'New Zealand'][0]
    tag_two = [tag for tag in tags if tag.tag_name == 'Health'][0]
    tag_three = [tag for tag in tags if tag.tag_name == 'World'][0]
    tag_four = [tag for tag in tags if tag.tag_name == 'Politics'][0]

    assert tag_one.number_of_tagged_articles == 3
    assert tag_two.number_of_tagged_articles == 2
    assert tag_three.number_of_tagged_articles == 3
    assert tag_four.number_of_tagged_articles == 1


def test_repository_can_get_first_article(in_memory_repo):
    article = in_memory_repo.get_first_article()
    assert article.title == 'Coronavirus: First case of virus in New Zealand'


def test_repository_can_get_last_article(in_memory_repo):
    article = in_memory_repo.get_last_article()
    assert article.title == 'Coronavirus: Death confirmed as six more test positive in NSW'


def test_repository_can_get_articles_by_ids(in_memory_repo):
    articles = in_memory_repo.get_articles_by_id([2, 5, 6])

    assert len(articles) == 3
    assert articles[
               0].title == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'
    assert articles[1].title == "Australia's first coronavirus fatality as man dies in Perth"
    assert articles[2].title == 'Coronavirus: Death confirmed as six more test positive in NSW'


def test_repository_does_not_retrieve_article_for_non_existent_id(in_memory_repo):
    articles = in_memory_repo.get_articles_by_id([2, 9])

    assert len(articles) == 1
    assert articles[
               0].title == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    articles = in_memory_repo.get_articles_by_id([0, 9])

    assert len(articles) == 0


def test_repository_returns_article_ids_for_existing_tag(in_memory_repo):
    article_ids = in_memory_repo.get_article_ids_for_tag('New Zealand')

    assert article_ids == [1, 3, 4]


def test_repository_returns_an_empty_list_for_non_existent_tag(in_memory_repo):
    article_ids = in_memory_repo.get_article_ids_for_tag('United States')

    assert len(article_ids) == 0


def test_repository_returns_date_of_previous_article(in_memory_repo):
    article = in_memory_repo.get_article(6)
    previous_date = in_memory_repo.get_date_of_previous_article(article)

    assert previous_date.isoformat() == '2020-03-01'


def test_repository_returns_none_when_there_are_no_previous_articles(in_memory_repo):
    article = in_memory_repo.get_article(1)
    previous_date = in_memory_repo.get_date_of_previous_article(article)

    assert previous_date is None


def test_repository_returns_date_of_next_article(in_memory_repo):
    article = in_memory_repo.get_article(3)
    next_date = in_memory_repo.get_date_of_next_article(article)

    assert next_date.isoformat() == '2020-03-05'


def test_repository_returns_none_when_there_are_no_subsequent_articles(in_memory_repo):
    article = in_memory_repo.get_article(6)
    next_date = in_memory_repo.get_date_of_next_article(article)

    assert next_date is None


def test_repository_can_add_a_tag(in_memory_repo):
    tag = Tag('Motoring')
    in_memory_repo.add_tag(tag)

    assert tag in in_memory_repo.get_tags()


def test_repository_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    article = in_memory_repo.get_article(2)
    comment = make_comment("Trump's onto it!", user, article)

    in_memory_repo.add_comment(comment)

    assert comment in in_memory_repo.get_comments()


def test_repository_does_not_add_a_comment_without_a_user(in_memory_repo):
    article = in_memory_repo.get_article(2)
    comment = Comment(None, article, "Trump's onto it!", datetime.today())

    with pytest.raises(RepositoryException):
        in_memory_repo.add_comment(comment)


def test_repository_does_not_add_a_comment_without_an_article_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    article = in_memory_repo.get_article(2)
    comment = Comment(None, article, "Trump's onto it!", datetime.today())

    user.add_comment(comment)

    with pytest.raises(RepositoryException):
        # Exception expected because the Article doesn't refer to the Comment.
        in_memory_repo.add_comment(comment)


def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_comments()) == 2



