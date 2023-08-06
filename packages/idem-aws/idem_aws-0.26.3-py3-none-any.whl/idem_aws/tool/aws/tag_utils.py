import copy
from typing import Dict
from typing import List
from typing import Tuple


def convert_tag_list_to_dict(hub, tags: List):
    result = {}
    for tag in tags:
        if "Key" in tag:
            result[tag["Key"]] = tag.get("Value")
        else:
            hub.log.warning(
                f"tag {tag} is not in the proper format of 'Key', 'Value' pair"
            )
    return result


def convert_tag_dict_to_list(hub, tags: Dict) -> List:
    if tags is None:
        tags = {}
    return [{"Key": key, "Value": value} for key, value in tags.items()]


def diff_tags_list(hub, old_tags: List, new_tags: List) -> Tuple:
    """

    Args:
        hub:
        old_tags:
        new_tags:

    Returns:

    """
    if old_tags is None:
        old_tags = []
    if new_tags is None:
        new_tags = []
    old_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(old_tags)
    new_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(new_tags)
    tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
        old_tags, new_tags
    )
    return [{"Key": key, "Value": value} for key, value in tags_to_remove.items()], [
        {"Key": key, "Value": value} for key, value in tags_to_add.items()
    ]


def diff_tags_dict(hub, old_tags: Dict[str, str], new_tags: Dict[str, str]) -> Tuple:
    """

    Args:
        hub:
        old_tags:
        new_tags:

    Returns:

    """
    tags_to_add = {}
    tags_to_remove = {}
    new_tags = copy.deepcopy(new_tags)
    if old_tags is None:
        old_tags = {}
    if new_tags is None:
        new_tags = {}
    for key, value in old_tags.items():
        if key in new_tags:
            if old_tags[key] != new_tags[key]:
                tags_to_remove.update({key: old_tags[key]})
                tags_to_add.update({key: new_tags[key]})
            new_tags.pop(key)
        else:
            tags_to_remove.update({key: old_tags[key]})
    tags_to_add.update(new_tags)
    return tags_to_remove, tags_to_add
