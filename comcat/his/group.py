"""ComCat accounts as members in groups."""

from cmslib.messages.group import MEMBER_ADDED
from cmslib.messages.group import MEMBER_DELETED
from cmslib.messages.group import NO_SUCH_MEMBER
from cmslib.orm.group import Group
from cmslib.functions.group import get_group
from comcatlib import GroupMemberAccount
from his import CUSTOMER, JSON_DATA, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


def get_groups_tree():
    """Returns the management tree."""

    for root_group in Group.select().where(
            (Group.customer == CUSTOMER.id) & (Group.parent >> None)):
        yield GroupContent(root_group)


@authenticated
@authorized('comcat')
def get(gid):
    """Returns the group's mamber mappings for ComCat accounts."""

    group = get_group(gid)
    group_members = []

    for group_member_account in GroupMemberAccount.select().where(
            GroupMemberAccount.group == group):
        group_members.append(group_member_account.to_json())

    return JSON(group_members)


@authenticated
@authorized('comcat')
def groups_tree():
    """Returns a tree view of the groups."""

    return JSON([group.to_json() for group in get_groups_tree()])


@authenticated
@authorized('dscms4')
def groups_subtree(gid):
    """Lists the groups."""

    group_content = GroupContent(get_group(gid))
    return JSON(group_content.to_json(recursive=False))


@authenticated
@authorized('comcat')
def add(gid):
    """Adds the ComCat account to the respective group."""

    group = get_group(gid)
    group_member_account = GroupMemberAccount.from_json(JSON_DATA, group)
    group_member_account.save()
    return MEMBER_ADDED.update(id=group_member_account.id)


@authenticated
@authorized('comcat')
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


class GroupContent:
    """Represents content of a group."""

    def __init__(self, group):
        """Sets the respective group."""
        self.group = group

    @property
    def children(self):
        """Yields children of this group."""
        for group in Group.select().where(Group.parent == self.group):
            yield GroupContent(group)

    @property
    def accounts(self):
        """Yields terminals of this group."""
        for group_member_account in GroupMemberAccount.select().where(
                GroupMemberAccount.group == self.group):
            yield group_member_account.member

    def to_json(self, recursive=True):
        """Recursively converts the group content into a JSON-ish dict."""
        json = self.group.to_json(parent=False, skip=('customer',))

        if recursive:
            children = [
                group.to_json(recursive=True) for group in self.children]
        else:
            children = [
                group.group.to_json(parent=False, skip=('customer',))
                for group in self.children]

        json['children'] = children
        json['accounts'] = [account.to_json() for account in self.accounts]
        return json


ROUTES = (
    ('GET', '/group/<int:gid>/account', get, 'get_group_members'),
    ('GET', '/grouptree', groups_tree, 'groups_tree'),
    ('GET', '/grouptree/<int:gid>', groups_subtree, 'groups_subtree'),
    ('POST', '/group/<int:gid>/account', add, 'add_group_member'),
    ('DELETE', '/group/<int:gid>/account/<int:member_id>',
     delete, 'delete_group_member'))
