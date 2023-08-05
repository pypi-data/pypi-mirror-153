import typing as t
from collections import defaultdict

import pydantic

from taktile_auth.entities.permission import Permission, PermissionDefinition
from taktile_auth.entities.resource import Resource
from taktile_auth.enums import Action


class Role(pydantic.BaseModel):
    name: str
    args: t.Dict[str, str]
    arg_list: t.List[str]
    permissions: t.List[Permission]
    sub_roles: t.List["Role"]

    def __contains__(self, query: Permission) -> bool:
        for permission in self.permissions:
            if query in permission:
                return True
        return False

    def _get_all_permissions(self) -> t.Set[str]:
        return {repr(perm) for perm in self.permissions}

    def __repr__(self) -> str:
        return self.name + "/" + ",".join(self.args[x] for x in self.arg_list)


Role.update_forward_refs()


class RoleDefinition(pydantic.BaseModel):
    name: str
    permission_definitions: t.List[
        t.Tuple[t.Set[Action], PermissionDefinition]
    ]
    args: t.List[str]
    sub_role_definitions: t.List["RoleDefinition"]

    def build(self, **kwargs: str) -> Role:
        assert set(kwargs.keys()) == set(self.args)
        # Flattening Permissions to include those from sub_role
        perm_map: t.Dict[Resource, t.Set[Action]] = defaultdict(set)
        for actions, permission_definition in self.permission_definitions:
            perm = permission_definition.build(actions=actions, **kwargs)
            perm_map[perm.resource] = perm_map[perm.resource].union(
                perm.actions
            )
        sub_roles = []
        for sub_role_definition in self.sub_role_definitions:
            extra_args = {
                arg: "*"
                for arg in set(sub_role_definition.args).difference(self.args)
            }
            sub_role = sub_role_definition.build(**kwargs, **extra_args)
            sub_roles.append(sub_role)
            for perm in sub_role.permissions:
                perm_map[perm.resource] = perm_map[perm.resource].union(
                    perm.actions
                )
        permissions = []
        for resource, actions in perm_map.items():
            permissions.append(
                Permission(
                    actions=actions,
                    resource=resource,
                    resource_name=type(resource).__name__,
                )
            )
        return Role(
            name=self.name,
            arg_list=self.args,
            args=kwargs,
            permissions=permissions,
            sub_roles=sub_roles,
        )


RoleDefinition.update_forward_refs()
