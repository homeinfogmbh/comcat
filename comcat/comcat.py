"""ComCat application backend."""

from hashlib import sha256
from json import dumps

from flask import request, Flask

from comcatlib import ACCOUNT
from comcatlib import Account
from comcatlib import AccountDamageReport
from comcatlib import Presentation
from comcatlib import Session
from comcatlib import authenticated
from comcatlib import decode_url
from comcatlib import get_facebook_posts as _get_facebook_posts
from comcatlib import get_session_duration
from comcatlib import proxy_url
from comcatlib.messages import INVALID_CREDENTIALS
from comcatlib.messages import NO_ADDRESS_CONFIGURED
from damage_report import DamageReport
from wsgilib import JSON


__all__ = ['APPLICATION']


APPLICATION = Flask('comcat')


@APPLICATION.route('/login', methods=['POST'])
def login():
    """Logs in an end user."""

    account = request.json.get('account')
    passwd = request.json.get('passwd')

    if not account or not passwd:
        return INVALID_CREDENTIALS

    try:
        account = Account.get(Account.name == account)
    except Account.DoesNotExist:
        return INVALID_CREDENTIALS  # Mitigate account sniffing.

    if account.login(passwd):
        session = Session.open(account, duration=get_session_duration())
        return JSON(session.to_json())

    return INVALID_CREDENTIALS


@APPLICATION.route('/presentation', methods=['GET'])
@authenticated
def get_presentation():
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
def get_facebook_posts():
    """Returns a list of sent damage report."""

    facebook_posts = _get_facebook_posts(ACCOUNT)
    return JSON([facebook_post.to_json() for facebook_post in facebook_posts])


@APPLICATION.route('/facebook/image', methods=['POST'])
@authenticated
def get_facebook_image():
    """Returns the respective facebook image."""

    url = decode_url(request.json)
    return proxy_url(url)


@APPLICATION.route('/damage_report', methods=['GET'])
@authenticated
def list_damage_reports():
    """Returns a list of sent damage report."""

    damage_reports = DamageReport.select().join(AccountDamageReport).where(
        AccountDamageReport.account == ACCOUNT.id)
    return JSON([damage_report.to_dict() for damage_report in damage_reports])


@APPLICATION.route('/damage_report', methods=['POST'])
@authenticated
def submit_damage_report():
    """Submits a new damage report."""

    address = ACCOUNT.address

    if address is None:
        return NO_ADDRESS_CONFIGURED

    damage_report = DamageReport.from_json(
        request.json, ACCOUNT.customer, address)
    damage_report.save()
    account_damage_report = AccountDamageReport(ACCOUNT.id, damage_report)
    account_damage_report.save()
    return ('Damage report submitted.', 201)
