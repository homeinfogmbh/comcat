"""ComCat accounts as members in groups."""

from cmslib.messages.group import MEMBER_ADDED
from cmslib.messages.group import MEMBER_DELETED
from cmslib.messages.group import NO_SUCH_MEMBER
from cmslib.functions.group import get_group
from comcatlib import GroupMemberAccount
from his import JSON_DATA, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns the group's ComCat accounts."""

    group = get_group(gid)
    accounts = []

    for group_member_account in GroupMemberAccount.select().where(
            GroupMemberAccount.group == group):
        accounts.append(group_member_account.member.to_json())

    return JSON(accounts)


@authenticated
@authorized('dscms4')
def add(gid):
    """Adds the ComCat account to the respective group."""

    group = get_group(gid)
    group_member_account = GroupMemberAccount.from_json(JSON_DATA, group)
    group_member_account.save()
    return MEMBER_ADDED.update(id=group_member_account.id)


@authenticated
@authorized('dscms4')
def delete(gid, member_id):
    """Deletes the respective terminal from the group."""

    try:
        group_member_account = GroupMemberAccount.get(
            (GroupMemberAccount.group == get_group(gid))
            & (GroupMemberAccount.id == member_id))
    except GroupMemberAccount.DoesNotExist:
        raise NO_SUCH_MEMBER

    group_member_account.delete_instance()
    return MEMBER_DELETED


ROUTES = (
    ('GET', '/group/<int:gid>/account', get, 'get_group_members'),
    ('POST', '/group/<int:gid>/account', add, 'add_group_member'),
    ('DELETE', '/group/<int:gid>/account/<int:member_id>',
     delete, 'delete_group_member'))
