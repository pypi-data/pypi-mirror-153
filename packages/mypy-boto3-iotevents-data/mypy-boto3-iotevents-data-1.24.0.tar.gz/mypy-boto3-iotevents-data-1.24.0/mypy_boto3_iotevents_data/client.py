"""
Type annotations for iotevents-data service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iotevents_data.client import IoTEventsDataClient

    session = Session()
    client: IoTEventsDataClient = session.client("iotevents-data")
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    AcknowledgeAlarmActionRequestTypeDef,
    BatchAcknowledgeAlarmResponseTypeDef,
    BatchDeleteDetectorResponseTypeDef,
    BatchDisableAlarmResponseTypeDef,
    BatchEnableAlarmResponseTypeDef,
    BatchPutMessageResponseTypeDef,
    BatchResetAlarmResponseTypeDef,
    BatchSnoozeAlarmResponseTypeDef,
    BatchUpdateDetectorResponseTypeDef,
    DeleteDetectorRequestTypeDef,
    DescribeAlarmResponseTypeDef,
    DescribeDetectorResponseTypeDef,
    DisableAlarmActionRequestTypeDef,
    EnableAlarmActionRequestTypeDef,
    ListAlarmsResponseTypeDef,
    ListDetectorsResponseTypeDef,
    MessageTypeDef,
    ResetAlarmActionRequestTypeDef,
    SnoozeAlarmActionRequestTypeDef,
    UpdateDetectorRequestTypeDef,
)

__all__ = ("IoTEventsDataClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class IoTEventsDataClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTEventsDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#exceptions)
        """

    def batch_acknowledge_alarm(
        self, *, acknowledgeActionRequests: Sequence[AcknowledgeAlarmActionRequestTypeDef]
    ) -> BatchAcknowledgeAlarmResponseTypeDef:
        """
        Acknowledges one or more alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.batch_acknowledge_alarm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#batch_acknowledge_alarm)
        """

    def batch_delete_detector(
        self, *, detectors: Sequence[DeleteDetectorRequestTypeDef]
    ) -> BatchDeleteDetectorResponseTypeDef:
        """
        Deletes one or more detectors that were created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.batch_delete_detector)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#batch_delete_detector)
        """

    def batch_disable_alarm(
        self, *, disableActionRequests: Sequence[DisableAlarmActionRequestTypeDef]
    ) -> BatchDisableAlarmResponseTypeDef:
        """
        Disables one or more alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.batch_disable_alarm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#batch_disable_alarm)
        """

    def batch_enable_alarm(
        self, *, enableActionRequests: Sequence[EnableAlarmActionRequestTypeDef]
    ) -> BatchEnableAlarmResponseTypeDef:
        """
        Enables one or more alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.batch_enable_alarm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#batch_enable_alarm)
        """

    def batch_put_message(
        self, *, messages: Sequence[MessageTypeDef]
    ) -> BatchPutMessageResponseTypeDef:
        """
        Sends a set of messages to the IoT Events system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.batch_put_message)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#batch_put_message)
        """

    def batch_reset_alarm(
        self, *, resetActionRequests: Sequence[ResetAlarmActionRequestTypeDef]
    ) -> BatchResetAlarmResponseTypeDef:
        """
        Resets one or more alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.batch_reset_alarm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#batch_reset_alarm)
        """

    def batch_snooze_alarm(
        self, *, snoozeActionRequests: Sequence[SnoozeAlarmActionRequestTypeDef]
    ) -> BatchSnoozeAlarmResponseTypeDef:
        """
        Changes one or more alarms to the snooze mode.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.batch_snooze_alarm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#batch_snooze_alarm)
        """

    def batch_update_detector(
        self, *, detectors: Sequence[UpdateDetectorRequestTypeDef]
    ) -> BatchUpdateDetectorResponseTypeDef:
        """
        Updates the state, variable values, and timer settings of one or more detectors
        (instances) of a specified detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.batch_update_detector)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#batch_update_detector)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#can_paginate)
        """

    def describe_alarm(
        self, *, alarmModelName: str, keyValue: str = ...
    ) -> DescribeAlarmResponseTypeDef:
        """
        Retrieves information about an alarm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.describe_alarm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#describe_alarm)
        """

    def describe_detector(
        self, *, detectorModelName: str, keyValue: str = ...
    ) -> DescribeDetectorResponseTypeDef:
        """
        Returns information about the specified detector (instance).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.describe_detector)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#describe_detector)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#generate_presigned_url)
        """

    def list_alarms(
        self, *, alarmModelName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListAlarmsResponseTypeDef:
        """
        Lists one or more alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.list_alarms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#list_alarms)
        """

    def list_detectors(
        self,
        *,
        detectorModelName: str,
        stateName: str = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListDetectorsResponseTypeDef:
        """
        Lists detectors (the instances of a detector model).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client.list_detectors)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents_data/client/#list_detectors)
        """
