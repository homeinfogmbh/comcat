"""ComCat application backend."""

from hashlib import sha256
from json import dumps
from uuid import UUID

from flask import request, Flask
from flask_cors import CORS

from comcatlib import ACCOUNT
from comcatlib import Account
from comcatlib import Presentation
from comcatlib import Session
from comcatlib import authenticated
from comcatlib import decode_url
from comcatlib import get_facebook_accounts
from comcatlib import get_facebook_posts
from comcatlib import get_session_duration
from comcatlib import proxy_url
from comcatlib.messages import INVALID_CREDENTIALS
from lptlib import get_departures
from wsgilib import Binary, JSON, Response

from comcat.functions.damage_report import get_damage_reports
from comcat.functions.damage_report import submit_damage_report
from comcat.functions.local_news import get_local_news_articles
from comcat.functions.local_news import get_local_news_image


__all__ = ['APPLICATION']


APPLICATION = Flask('comcat')
CORS(APPLICATION)
DOMAIN = 'wohninfo.homeinfo.de'


@APPLICATION.errorhandler(Response)
def _handle_raised_message(message):
    """Returns the respective message."""

    return message


@APPLICATION.route('/login', methods=['POST'])
def _login():
    """Logs in an end user."""

    uuid = request.json.get('uuid')
    passwd = request.json.get('passwd')

    if not uuid or not passwd:
        return INVALID_CREDENTIALS

    try:
        uuid = UUID(uuid)
    except (ValueError, TypeError):
        return INVALID_CREDENTIALS

    try:
        account = Account.get(Account.uuid == uuid)
    except Account.DoesNotExist:
        return INVALID_CREDENTIALS  # Mitigate account sniffing.

    if account.login(passwd):
        session = Session.open(account, duration=get_session_duration())
        response = JSON(session.to_json())
        response.set_cookie('Session', session.token.hex, expires=session.end)
        return response

    return INVALID_CREDENTIALS


@APPLICATION.route('/presentation', methods=['GET'])
@authenticated
def _get_presentation():
    """Returns the presentation for the respective account."""

    account = ACCOUNT.instance  # Get model from LocalProxy.
    presentation = Presentation(account)
    json = presentation.to_json()
    sha256sum = sha256(dumps(json).encode()).hexdigest()

    if sha256sum == request.headers.get('sha256sum'):
        return ('Not Modified', 304)

    json['sha256sum'] = sha256sum
    return JSON(json)


@APPLICATION.route('/facebook', methods=['GET'])
@authenticated
def _list_facebook_posts():
    """Returns a list of sent damage report."""

    accounts = {}

    for account in get_facebook_accounts(ACCOUNT):
        posts = tuple(post.to_json() for post in get_facebook_posts(account))
        accounts[account.facebook_id] = posts

    return JSON(accounts)


@APPLICATION.route('/facebook/image', methods=['POST'])
@authenticated
def _get_facebook_image():
    """Returns the respective facebook image."""

    url = decode_url(request.json)
    return proxy_url(url)


@APPLICATION.route('/damage_report', methods=['GET'])
@authenticated
def _list_damage_reports():
    """Returns a list of sent damage report."""

    return JSON([report.to_dict() for report in get_damage_reports()])


@APPLICATION.route('/damage_report', methods=['POST'])
@authenticated
def _submit_damage_report():
    """Submits a new damage report."""

    submit_damage_report()
    return ('Damage report submitted.', 201)


@APPLICATION.route('/local_news', methods=['GET'])
@authenticated
def _get_local_news_articles():
    """Lists local news."""

    return JSON([
        article.to_json(preview=True) for article
        in get_local_news_articles()])


@APPLICATION.route(
    '/local_news/<int:article_id>/<int:image_id>',
    methods=['GET'])
@authenticated
def _get_local_news_image(article_id, image_id):
    """Returns a local news image."""

    image = get_local_news_image(article_id, image_id)

    try:
        return Binary(image.watermarked)
    except OSError:     # Not an image.
        return Binary(image.data)


@APPLICATION.route('/ltp', methods=['GET'])
@authenticated
def _get_departures():
    """Returns the departures."""

    address = ACCOUNT.address
    stops, source = get_departures(address)
    stops = [stop.to_json() for stop in stops]
    return JSON({'source': source, 'stops': stops})
