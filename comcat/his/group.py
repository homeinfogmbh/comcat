"""ComCat accounts as members in groups."""

from __future__ import annotations

from flask import request

from cmslib import get_group
from comcatlib import GroupMemberUser
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, require_json

from comcat.his.functions import get_group_member_user
from comcat.his.functions import get_group_member_users
from comcat.his.functions import get_groups_tree
from comcat.his.functions import get_user
from comcat.his.grouptree import GroupTree


__all__ = ['ROUTES']


@authenticated
@authorized('comcat')
def list_() -> JSON:
    """Lists group <> user mappings."""

    return JSON([gmu.to_json() for gmu in get_group_member_users()])


@authenticated
@authorized('comcat')
def get(ident: int) -> JSON:
    """Returns the respective group <> user mapping."""

    return JSON(get_group_member_user(ident).to_json())


@authenticated
@authorized('comcat')
def groups_tree() -> JSON:
    """Returns a tree view of the groups."""

    return JSON([tree.to_json() for tree in get_groups_tree()])


@authenticated
@authorized('dscms4')
def groups_subtree(ident: int) -> JSON:
    """Lists the groups."""

    return JSON(
        GroupTree(get_group(ident, CUSTOMER.id)).to_json(recursive=False)
    )


@authenticated
@authorized('comcat')
@require_json(dict)
def add() -> JSONMessage:
    """Adds the ComCat user to the respective group."""

    group = get_group(request.json.pop('group'), CUSTOMER.id)
    user = get_user(request.json.pop('user'))

    try:
        group_member_user = GroupMemberUser.get(
            (GroupMemberUser.group == group)
            & (GroupMemberUser.user == user)
        )
    except GroupMemberUser.DoesNotExist:
        group_member_user = GroupMemberUser(group=group, user=user)
        group_member_user.save()

    return JSONMessage(
        'Group member added.', id=group_member_user.id, status=201)


@authenticated
@authorized('comcat')
def delete(ident: int) -> JSONMessage:
    """Deletes the respective user from the group."""

    get_group_member_user(ident).delete_instance()
    return JSONMessage('Group member user deleted.', status=200)


ROUTES = [
    ('GET', '/group/user', list_),
    ('GET', '/group/user/<int:ident>', get),
    ('GET', '/grouptree', groups_tree),
    ('GET', '/grouptree/<int:ident>', groups_subtree),
    ('POST', '/group/user', add),
    ('DELETE', '/group/user/<int:ident>', delete)
]
