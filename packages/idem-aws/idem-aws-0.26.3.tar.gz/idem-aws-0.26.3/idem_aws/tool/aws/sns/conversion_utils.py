import json
from collections import OrderedDict
from json import JSONDecodeError
from typing import Any
from typing import Dict


def convert_raw_subscription_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """
    Util functions to convert raw resource state to present input format for SNS topic_subscription.

    """
    raw_attributes = raw_resource.get("Attributes")
    resource_id = raw_attributes.get("SubscriptionArn")
    resource_parameters = OrderedDict(
        {
            "TopicArn": "topic_arn",
            "Protocol": "protocol",
            "Endpoint": "endpoint",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource.get("Attributes"):
            resource_translated[parameter_present] = raw_resource.get("Attributes").get(
                parameter_raw
            )

    attribute_params = [
        "DeliveryPolicy",
        "FilterPolicy",
        "RawMessageDelivery",
        "RedrivePolicy",
    ]

    attributes = {}
    for param in attribute_params:
        value = raw_attributes.get(param, None)
        if value:
            attributes[param] = standardise_json(hub, value)
    resource_translated["attributes"] = attributes

    return resource_translated


def convert_raw_topic_to_present(
    hub,
    raw_resource: Dict[str, Any],
    raw_resource_tags: Dict[str, Any],
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    """
    Util functions to convert raw resource state to present input format for SNS topic.

    """
    raw_attributes = raw_resource.get("Attributes")
    resource_id = raw_attributes.get("TopicArn")
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    attribute_params = [
        "DeliveryPolicy",
        "DisplayName",
        "FifoTopic",
        "Policy",
        "KmsMasterKeyId",
        "ContentBasedDeduplication",
    ]

    attributes = {}
    for param in attribute_params:
        value = raw_attributes.get(param, None)
        if value:
            if isinstance(value, str):
                try:
                    attributes[param] = json.loads(value)
                except JSONDecodeError:
                    attributes[param] = value
            else:
                attributes[param] = standardise_json(hub, value)
    resource_translated["attributes"] = attributes

    if raw_resource_tags.get("ret") and raw_resource_tags.get("ret").get("Tags"):
        resource_translated["tags"] = raw_resource_tags.get("ret").get("Tags")

    return resource_translated


def convert_raw_topic_policy_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """
    Util functions to convert raw resource state to present input format for SNS topic_policy.

    """
    raw_attributes = raw_resource["ret"].get("Attributes")
    resource_id = raw_attributes.get("TopicArn") + "-policy"
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "topic_arn": raw_attributes.get("TopicArn"),
        "policy": standardise_json(hub, raw_attributes.get("Policy")),
    }

    return resource_translated


def standardise_json(hub, value: str):
    """
    Utils function for standardising the json string format for SNS resources
    """
    if value is None:
        return None

    if isinstance(value, str):
        try:
            json_dict = json.loads(value)
        except JSONDecodeError:
            json_dict = value
    else:
        json_dict = value
    return json.dumps(json_dict, separators=(", ", ": "))
