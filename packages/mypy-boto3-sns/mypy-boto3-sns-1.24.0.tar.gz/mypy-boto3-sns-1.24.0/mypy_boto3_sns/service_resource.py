"""
Type annotations for sns service ServiceResource

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_sns.service_resource import SNSServiceResource
    import mypy_boto3_sns.service_resource as sns_resources

    session = Session()
    resource: SNSServiceResource = session.resource("sns")

    my_platform_application: sns_resources.PlatformApplication = resource.PlatformApplication(...)
    my_platform_endpoint: sns_resources.PlatformEndpoint = resource.PlatformEndpoint(...)
    my_subscription: sns_resources.Subscription = resource.Subscription(...)
    my_topic: sns_resources.Topic = resource.Topic(...)
```
"""
from typing import Dict, Iterator, List, Mapping, Sequence

from boto3.resources.base import ResourceMeta
from boto3.resources.base import ServiceResource as Boto3ServiceResource
from boto3.resources.collection import ResourceCollection

from .client import SNSClient
from .type_defs import MessageAttributeValueTypeDef, PublishResponseTypeDef, TagTypeDef

__all__ = (
    "SNSServiceResource",
    "PlatformApplication",
    "PlatformEndpoint",
    "Subscription",
    "Topic",
    "ServiceResourcePlatformApplicationsCollection",
    "ServiceResourceSubscriptionsCollection",
    "ServiceResourceTopicsCollection",
    "PlatformApplicationEndpointsCollection",
    "TopicSubscriptionsCollection",
)


class ServiceResourcePlatformApplicationsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourceplatformapplicationscollection)
    """

    def all(self) -> "ServiceResourcePlatformApplicationsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """

    def filter(  # type: ignore
        self, *, NextToken: str = ...
    ) -> "ServiceResourcePlatformApplicationsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """

    def limit(self, count: int) -> "ServiceResourcePlatformApplicationsCollection":
        """
        Return at most this many PlatformApplications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """

    def page_size(self, count: int) -> "ServiceResourcePlatformApplicationsCollection":
        """
        Fetch at most this many PlatformApplications per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """

    def pages(self) -> Iterator[List["PlatformApplication"]]:
        """
        A generator which yields pages of PlatformApplications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """

    def __iter__(self) -> Iterator["PlatformApplication"]:
        """
        A generator which yields PlatformApplications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """


class ServiceResourceSubscriptionsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcesubscriptionscollection)
    """

    def all(self) -> "ServiceResourceSubscriptionsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcesubscriptionscollection)
        """

    def filter(  # type: ignore
        self, *, NextToken: str = ...
    ) -> "ServiceResourceSubscriptionsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcesubscriptionscollection)
        """

    def limit(self, count: int) -> "ServiceResourceSubscriptionsCollection":
        """
        Return at most this many Subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcesubscriptionscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceSubscriptionsCollection":
        """
        Fetch at most this many Subscriptions per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcesubscriptionscollection)
        """

    def pages(self) -> Iterator[List["Subscription"]]:
        """
        A generator which yields pages of Subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcesubscriptionscollection)
        """

    def __iter__(self) -> Iterator["Subscription"]:
        """
        A generator which yields Subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcesubscriptionscollection)
        """


class ServiceResourceTopicsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcetopicscollection)
    """

    def all(self) -> "ServiceResourceTopicsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcetopicscollection)
        """

    def filter(self, *, NextToken: str = ...) -> "ServiceResourceTopicsCollection":  # type: ignore
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcetopicscollection)
        """

    def limit(self, count: int) -> "ServiceResourceTopicsCollection":
        """
        Return at most this many Topics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcetopicscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceTopicsCollection":
        """
        Fetch at most this many Topics per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcetopicscollection)
        """

    def pages(self) -> Iterator[List["Topic"]]:
        """
        A generator which yields pages of Topics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcetopicscollection)
        """

    def __iter__(self) -> Iterator["Topic"]:
        """
        A generator which yields Topics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#serviceresourcetopicscollection)
        """


class PlatformApplicationEndpointsCollection(ResourceCollection):
    def all(self) -> "PlatformApplicationEndpointsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, NextToken: str = ...
    ) -> "PlatformApplicationEndpointsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "PlatformApplicationEndpointsCollection":
        """
        Return at most this many PlatformEndpoints.
        """

    def page_size(self, count: int) -> "PlatformApplicationEndpointsCollection":
        """
        Fetch at most this many PlatformEndpoints per service request.
        """

    def pages(self) -> Iterator[List["PlatformEndpoint"]]:
        """
        A generator which yields pages of PlatformEndpoints.
        """

    def __iter__(self) -> Iterator["PlatformEndpoint"]:
        """
        A generator which yields PlatformEndpoints.
        """


class TopicSubscriptionsCollection(ResourceCollection):
    def all(self) -> "TopicSubscriptionsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(self, *, NextToken: str = ...) -> "TopicSubscriptionsCollection":  # type: ignore
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "TopicSubscriptionsCollection":
        """
        Return at most this many Subscriptions.
        """

    def page_size(self, count: int) -> "TopicSubscriptionsCollection":
        """
        Fetch at most this many Subscriptions per service request.
        """

    def pages(self) -> Iterator[List["Subscription"]]:
        """
        A generator which yields pages of Subscriptions.
        """

    def __iter__(self) -> Iterator["Subscription"]:
        """
        A generator which yields Subscriptions.
        """


class PlatformEndpoint(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.PlatformEndpoint)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformendpoint)
    """

    attributes: Dict[str, str]
    arn: str

    def delete(self) -> None:
        """
        Deletes the endpoint for a device and mobile app from Amazon SNS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.delete)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformendpointdelete-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformendpointget_available_subresources-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_endpoint_attributes` to update the attributes of
        the PlatformEndpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.load)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformendpointload-method)
        """

    def publish(
        self,
        *,
        Message: str,
        TopicArn: str = ...,
        PhoneNumber: str = ...,
        Subject: str = ...,
        MessageStructure: str = ...,
        MessageAttributes: Mapping[str, MessageAttributeValueTypeDef] = ...,
        MessageDeduplicationId: str = ...,
        MessageGroupId: str = ...
    ) -> PublishResponseTypeDef:
        """
        Sends a message to an Amazon SNS topic, a text message (SMS message) directly to
        a phone number, or a message to a mobile platform endpoint (when you specify the
        `TargetArn` ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.publish)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformendpointpublish-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_endpoint_attributes` to update the attributes of
        the PlatformEndpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.reload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformendpointreload-method)
        """

    def set_attributes(self, *, Attributes: Mapping[str, str]) -> None:
        """
        Sets the attributes for an endpoint for a device on one of the supported push
        notification services, such as GCM (Firebase Cloud Messaging) and APNS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.set_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformendpointset_attributes-method)
        """


_PlatformEndpoint = PlatformEndpoint


class Subscription(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.Subscription)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#subscription)
    """

    attributes: Dict[str, str]
    arn: str

    def delete(self) -> None:
        """
        Deletes a subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Subscription.delete)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#subscriptiondelete-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Subscription.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#subscriptionget_available_subresources-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_subscription_attributes` to update the attributes
        of the Subscription resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Subscription.load)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#subscriptionload-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_subscription_attributes` to update the attributes
        of the Subscription resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Subscription.reload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#subscriptionreload-method)
        """

    def set_attributes(self, *, AttributeName: str, AttributeValue: str = ...) -> None:
        """
        Allows a subscription owner to set an attribute of the subscription to a new
        value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Subscription.set_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#subscriptionset_attributes-method)
        """


_Subscription = Subscription


class PlatformApplication(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.PlatformApplication)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformapplication)
    """

    attributes: Dict[str, str]
    arn: str
    endpoints: PlatformApplicationEndpointsCollection

    def create_platform_endpoint(
        self, *, Token: str, CustomUserData: str = ..., Attributes: Mapping[str, str] = ...
    ) -> _PlatformEndpoint:
        """
        Creates an endpoint for a device and mobile app on one of the supported push
        notification services, such as GCM (Firebase Cloud Messaging) and APNS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformApplication.create_platform_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformapplicationcreate_platform_endpoint-method)
        """

    def delete(self) -> None:
        """
        Deletes a platform application object for one of the supported push notification
        services, such as APNS and GCM (Firebase Cloud Messaging).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformApplication.delete)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformapplicationdelete-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformApplication.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformapplicationget_available_subresources-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_platform_application_attributes` to update the
        attributes of the PlatformApplication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformApplication.load)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformapplicationload-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_platform_application_attributes` to update the
        attributes of the PlatformApplication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformApplication.reload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformapplicationreload-method)
        """

    def set_attributes(self, *, Attributes: Mapping[str, str]) -> None:
        """
        Sets the attributes of the platform application object for the supported push
        notification services, such as APNS and GCM (Firebase Cloud Messaging).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformApplication.set_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#platformapplicationset_attributes-method)
        """


_PlatformApplication = PlatformApplication


class Topic(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.Topic)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#topic)
    """

    attributes: Dict[str, str]
    arn: str
    subscriptions: TopicSubscriptionsCollection

    def add_permission(
        self, *, Label: str, AWSAccountId: Sequence[str], ActionName: Sequence[str]
    ) -> None:
        """
        Adds a statement to a topic's access control policy, granting access for the
        specified Amazon Web Services accounts to the specified actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.add_permission)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#topicadd_permission-method)
        """

    def confirm_subscription(
        self, *, Token: str, AuthenticateOnUnsubscribe: str = ...
    ) -> _Subscription:
        """
        Verifies an endpoint owner's intent to receive messages by validating the token
        sent to the endpoint by an earlier `Subscribe` action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.confirm_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#topicconfirm_subscription-method)
        """

    def delete(self) -> None:
        """
        Deletes a topic and all its subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.delete)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#topicdelete-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#topicget_available_subresources-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_topic_attributes` to update the attributes of the
        Topic resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.load)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#topicload-method)
        """

    def publish(
        self,
        *,
        Message: str,
        TargetArn: str = ...,
        PhoneNumber: str = ...,
        Subject: str = ...,
        MessageStructure: str = ...,
        MessageAttributes: Mapping[str, MessageAttributeValueTypeDef] = ...,
        MessageDeduplicationId: str = ...,
        MessageGroupId: str = ...
    ) -> PublishResponseTypeDef:
        """
        Sends a message to an Amazon SNS topic, a text message (SMS message) directly to
        a phone number, or a message to a mobile platform endpoint (when you specify the
        `TargetArn` ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.publish)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#topicpublish-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_topic_attributes` to update the attributes of the
        Topic resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.reload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#topicreload-method)
        """

    def remove_permission(self, *, Label: str) -> None:
        """
        Removes a statement from a topic's access control policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.remove_permission)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#topicremove_permission-method)
        """

    def set_attributes(self, *, AttributeName: str, AttributeValue: str = ...) -> None:
        """
        Allows a topic owner to set an attribute of the topic to a new value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.set_attributes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#topicset_attributes-method)
        """

    def subscribe(
        self,
        *,
        Protocol: str,
        Endpoint: str = ...,
        Attributes: Mapping[str, str] = ...,
        ReturnSubscriptionArn: bool = ...
    ) -> _Subscription:
        """
        Subscribes an endpoint to an Amazon SNS topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.subscribe)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#topicsubscribe-method)
        """


_Topic = Topic


class SNSResourceMeta(ResourceMeta):
    client: SNSClient


class SNSServiceResource(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/)
    """

    meta: "SNSResourceMeta"
    platform_applications: ServiceResourcePlatformApplicationsCollection
    subscriptions: ServiceResourceSubscriptionsCollection
    topics: ServiceResourceTopicsCollection

    def PlatformApplication(self, arn: str) -> _PlatformApplication:
        """
        Creates a PlatformApplication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.PlatformApplication)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#snsserviceresourceplatformapplication-method)
        """

    def PlatformEndpoint(self, arn: str) -> _PlatformEndpoint:
        """
        Creates a PlatformEndpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.PlatformEndpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#snsserviceresourceplatformendpoint-method)
        """

    def Subscription(self, arn: str) -> _Subscription:
        """
        Creates a Subscription resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.Subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#snsserviceresourcesubscription-method)
        """

    def Topic(self, arn: str) -> _Topic:
        """
        Creates a Topic resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.Topic)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#snsserviceresourcetopic-method)
        """

    def create_platform_application(
        self, *, Name: str, Platform: str, Attributes: Mapping[str, str]
    ) -> _PlatformApplication:
        """
        Creates a platform application object for one of the supported push notification
        services, such as APNS and GCM (Firebase Cloud Messaging), to which devices and
        mobile apps may register.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.create_platform_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#snsserviceresourcecreate_platform_application-method)
        """

    def create_topic(
        self, *, Name: str, Attributes: Mapping[str, str] = ..., Tags: Sequence[TagTypeDef] = ...
    ) -> _Topic:
        """
        Creates a topic to which notifications can be published.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.create_topic)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#snsserviceresourcecreate_topic-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sns/service_resource/#snsserviceresourceget_available_subresources-method)
        """
