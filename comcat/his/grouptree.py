"""Group tree views."""

from __future__ import annotations
from typing import Iterator

from cmslib.orm.group import Group
from comcatlib import GroupMemberUser, User


__all__ = ['GroupTree']


class GroupTree:
    """Represents content of a group."""

    def __init__(self, group: Group):
        """Sets the respective group."""
        self.group = group

    @property
    def children(self) -> Iterator[GroupTree]:
        """Yields children of this group."""
        for group in Group.select(cascade=True).where(
                Group.parent == self.group):
            yield type(self)(group)

    @property
    def users(self) -> Iterator[User]:
        """Yields users of this group."""
        for group_member_user in GroupMemberUser.select(cascade=True).where(
                GroupMemberUser.group == self.group):
            yield group_member_user.user

    def to_json(self, recursive: bool = True) -> dict:
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
