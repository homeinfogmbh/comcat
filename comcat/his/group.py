"""ComCat accounts as members in groups."""

from flask import request

from cmslib.messages.group import MEMBER_ADDED
from cmslib.messages.group import MEMBER_DELETED
from cmslib.messages.group import NO_SUCH_MEMBER
from cmslib.orm.group import Group
from cmslib.functions.group import get_group
from comcatlib import GroupMemberUser
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON

from comcat.his.functions import get_user


__all__ = ['ROUTES']


def get_groups_tree():
    """Returns the management tree."""

    for root_group in Group.select().where(
            (Group.customer == CUSTOMER.id) & (Group.parent >> None)):
        yield GroupContent(root_group)


@authenticated
@authorized('comcat')
def get(gid):
    """Returns the group's mamber mappings for ComCat users."""

    group = get_group(gid)
    group_members = []

    for group_member_user in GroupMemberUser.select().where(
            GroupMemberUser.group == group):
        group_members.append(group_member_user.to_json())

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
    """Adds the ComCat user to the respective group."""

    group = get_group(gid)
    user = get_user(request.json['user'])

    try:
        group_member_user = GroupMemberUser.get(
            (GroupMemberUser.group == group)
            & (GroupMemberUser.user == user))
    except GroupMemberUser.DoesNotExist:
        group_member_user = GroupMemberUser(group=group, user=user)
        group_member_user.save()

    return MEMBER_ADDED.update(id=group_member_user.id)


@authenticated
@authorized('comcat')
def delete(gid, user):
    """Deletes the respective user from the group."""

    try:
        group_member_user = GroupMemberUser.get(
            (GroupMemberUser.group == get_group(gid))
            & (GroupMemberUser.user == user))
    except GroupMemberUser.DoesNotExist:
        raise NO_SUCH_MEMBER

    group_member_user.delete_instance()
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
    def users(self):
        """Yields users of this group."""
        for group_member_user in GroupMemberUser.select().where(
                GroupMemberUser.group == self.group):
            yield group_member_user.user

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
        json['users'] = [user.to_json() for user in self.users]
        return json


ROUTES = (
    ('GET', '/group/<int:gid>/user', get),
    ('GET', '/grouptree', groups_tree),
    ('GET', '/grouptree/<int:gid>', groups_subtree),
    ('POST', '/group/<int:gid>/user', add),
    ('DELETE', '/group/<int:gid>/user/<int:user>', delete)
)
