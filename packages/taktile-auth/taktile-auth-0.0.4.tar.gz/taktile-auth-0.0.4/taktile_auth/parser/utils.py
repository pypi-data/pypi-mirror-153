import typing as t


def parse_body(clauses: t.List[str]) -> t.List[t.Dict[str, t.Any]]:
    parsed_clauses = []
    for clause in clauses:
        if _is_permission(clause):
            parsed_clauses.append(parse_permission(clause))
        else:
            parsed_clauses.append(parse_sub_role(clause))
    return parsed_clauses


def _is_permission(clause: str) -> bool:
    return ":" in clause


def parse_permission(clause: str) -> t.Dict[str, t.Any]:
    action_str, _, resource_str = clause.partition(":")
    actions = action_str.split("+") if action_str else []
    resource_name, _, args_str = resource_str.partition("/")
    resource_args = args_str.split(",") if args_str else []
    return {
        "type": "permission",
        "actions": actions,
        "resource_name": resource_name,
        "resource_args": resource_args,
    }


def parse_sub_role(clause: str) -> t.Dict[str, t.Any]:
    sub_role, sep, sub_role_args_str = clause.partition("/")
    sub_role_args = sub_role_args_str.split(",") if sub_role_args_str else []
    return {
        "type": "role",
        "sub_role_name": sub_role,
        "sub_role_args": sub_role_args,
    }
