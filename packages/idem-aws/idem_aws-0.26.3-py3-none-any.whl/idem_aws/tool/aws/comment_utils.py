from typing import Tuple


def create_comment(hub, resource_type: str, name: str) -> Tuple:
    return (f"Created {resource_type} '{name}'",)


def would_create_comment(hub, resource_type: str, name: str) -> Tuple:
    return (f"Would create {resource_type} '{name}'",)


def update_comment(hub, resource_type: str, name: str) -> Tuple:
    return (f"Updated {resource_type} '{name}'",)


def would_update_comment(hub, resource_type: str, name: str) -> Tuple:
    return (f"Would update {resource_type} '{name}'",)


def delete_comment(hub, resource_type: str, name: str) -> Tuple:
    return (f"Deleted {resource_type} '{name}'",)


def would_delete_comment(hub, resource_type: str, name: str) -> Tuple:
    return (f"Would delete {resource_type} '{name}'",)


def already_absent_comment(hub, resource_type: str, name: str) -> Tuple:
    return (f"{resource_type} '{name}' already absent",)


def already_exists_comment(hub, resource_type: str, name: str) -> Tuple:
    return (f"{resource_type} '{name}' already exists",)


def update_tags_comment(hub, tags_to_remove, tags_to_add) -> Tuple:
    return (
        f"Update tags: Add keys {tags_to_add.keys()} Remove keys {tags_to_remove.keys()}",
    )


def would_update_tags_comment(hub, tags_to_remove, tags_to_add) -> Tuple:
    return (
        f"Would update tags: Add keys {tags_to_add.keys()} Remove keys {tags_to_remove.keys()}",
    )
