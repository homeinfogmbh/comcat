"""Smartphone app endpoints."""

from comcat.app.common import APPLICATION
from comcat.app.damage_report import list_damage_reports, submit_damage_report
from comcat.app.file import delete as delete_file
from comcat.app.file import get as get_file
from comcat.app.file import post as post_file
from comcat.app.local_news import get_local_news_articles, get_local_news_image
from comcat.app.lpt import get_departures
from comcat.app.presentation import get_presentation


__all__ = ['APPLICATION']


# Damage report.
APPLICATION.route('/damage-report', methods=['GET'])(list_damage_reports)
APPLICATION.route('/damage-report', methods=['POST'])(submit_damage_report)
# Files.
APPLICATION.route('/file/<name>', methods=['POST'])(post_file)
APPLICATION.route('/file/<int:file>', methods=['DELETE'])(delete_file)
APPLICATION.route('/file/<int:file>', methods=['GET'])(get_file)
# Local news.
APPLICATION.route('/local-news', methods=['GET'])(get_local_news_articles)
APPLICATION.route(
    '/local-news/<int:article_id>/<int:image_id>', methods=['GET']
)(get_local_news_image)
# Local public transport.
APPLICATION.route('/ltp', methods=['GET'])(get_departures)
APPLICATION.route('/presentation', methods=['GET'])(get_presentation)
