from typing import Iterable
import random

from covid.adapters.repository import AbstractRepository
from covid.domain.model import Article


def get_tag_names(repo: AbstractRepository):
    tags = repo.get_tags()
    tag_names = [tag.tag_name for tag in tags]

    return tag_names


def get_random_articles(quantity, repo: AbstractRepository):
    article_count = repo.get_number_of_articles()

    if quantity >= article_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of articles.
        quantity = article_count - 1

    # Pick distinct and random articles.
    random_ids = random.sample(range(1, article_count), quantity)
    articles = repo.get_articles_by_id(random_ids)

    return articles_to_dict(articles)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def article_to_dict(article: Article):
    article_dict = {
        'date': article.date,
        'title': article.title,
        'image_hyperlink': article.image_hyperlink
    }
    return article_dict


def articles_to_dict(articles: Iterable[Article]):
    return [article_to_dict(article) for article in articles]
