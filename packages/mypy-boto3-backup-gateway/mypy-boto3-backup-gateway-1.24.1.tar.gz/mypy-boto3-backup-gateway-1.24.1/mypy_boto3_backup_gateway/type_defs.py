"""
Type annotations for backup-gateway service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/type_defs/)

Usage::

    ```python
    from mypy_boto3_backup_gateway.type_defs import AssociateGatewayToServerInputRequestTypeDef

    data: AssociateGatewayToServerInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import HypervisorStateType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssociateGatewayToServerInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "DeleteGatewayInputRequestTypeDef",
    "DeleteHypervisorInputRequestTypeDef",
    "DisassociateGatewayFromServerInputRequestTypeDef",
    "GatewayDetailsTypeDef",
    "GatewayTypeDef",
    "GetGatewayInputRequestTypeDef",
    "HypervisorTypeDef",
    "PaginatorConfigTypeDef",
    "ListGatewaysInputRequestTypeDef",
    "ListHypervisorsInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListVirtualMachinesInputRequestTypeDef",
    "VirtualMachineTypeDef",
    "PutMaintenanceStartTimeInputRequestTypeDef",
    "TestHypervisorConfigurationInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateGatewayInformationInputRequestTypeDef",
    "UpdateGatewaySoftwareNowInputRequestTypeDef",
    "UpdateHypervisorInputRequestTypeDef",
    "AssociateGatewayToServerOutputTypeDef",
    "CreateGatewayOutputTypeDef",
    "DeleteGatewayOutputTypeDef",
    "DeleteHypervisorOutputTypeDef",
    "DisassociateGatewayFromServerOutputTypeDef",
    "ImportHypervisorConfigurationOutputTypeDef",
    "PutMaintenanceStartTimeOutputTypeDef",
    "TagResourceOutputTypeDef",
    "UntagResourceOutputTypeDef",
    "UpdateGatewayInformationOutputTypeDef",
    "UpdateGatewaySoftwareNowOutputTypeDef",
    "UpdateHypervisorOutputTypeDef",
    "CreateGatewayInputRequestTypeDef",
    "ImportHypervisorConfigurationInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "TagResourceInputRequestTypeDef",
    "GetGatewayOutputTypeDef",
    "ListGatewaysOutputTypeDef",
    "ListHypervisorsOutputTypeDef",
    "ListGatewaysInputListGatewaysPaginateTypeDef",
    "ListHypervisorsInputListHypervisorsPaginateTypeDef",
    "ListVirtualMachinesInputListVirtualMachinesPaginateTypeDef",
    "ListVirtualMachinesOutputTypeDef",
)

AssociateGatewayToServerInputRequestTypeDef = TypedDict(
    "AssociateGatewayToServerInputRequestTypeDef",
    {
        "GatewayArn": str,
        "ServerArn": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

DeleteGatewayInputRequestTypeDef = TypedDict(
    "DeleteGatewayInputRequestTypeDef",
    {
        "GatewayArn": str,
    },
)

DeleteHypervisorInputRequestTypeDef = TypedDict(
    "DeleteHypervisorInputRequestTypeDef",
    {
        "HypervisorArn": str,
    },
)

DisassociateGatewayFromServerInputRequestTypeDef = TypedDict(
    "DisassociateGatewayFromServerInputRequestTypeDef",
    {
        "GatewayArn": str,
    },
)

GatewayDetailsTypeDef = TypedDict(
    "GatewayDetailsTypeDef",
    {
        "GatewayArn": str,
        "GatewayDisplayName": str,
        "GatewayType": Literal["BACKUP_VM"],
        "HypervisorId": str,
        "LastSeenTime": datetime,
        "NextUpdateAvailabilityTime": datetime,
        "VpcEndpoint": str,
    },
    total=False,
)

GatewayTypeDef = TypedDict(
    "GatewayTypeDef",
    {
        "GatewayArn": str,
        "GatewayDisplayName": str,
        "GatewayType": Literal["BACKUP_VM"],
        "HypervisorId": str,
        "LastSeenTime": datetime,
    },
    total=False,
)

GetGatewayInputRequestTypeDef = TypedDict(
    "GetGatewayInputRequestTypeDef",
    {
        "GatewayArn": str,
    },
)

HypervisorTypeDef = TypedDict(
    "HypervisorTypeDef",
    {
        "Host": str,
        "HypervisorArn": str,
        "KmsKeyArn": str,
        "Name": str,
        "State": HypervisorStateType,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListGatewaysInputRequestTypeDef = TypedDict(
    "ListGatewaysInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListHypervisorsInputRequestTypeDef = TypedDict(
    "ListHypervisorsInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ListVirtualMachinesInputRequestTypeDef = TypedDict(
    "ListVirtualMachinesInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

VirtualMachineTypeDef = TypedDict(
    "VirtualMachineTypeDef",
    {
        "HostName": str,
        "HypervisorId": str,
        "LastBackupDate": datetime,
        "Name": str,
        "Path": str,
        "ResourceArn": str,
    },
    total=False,
)

_RequiredPutMaintenanceStartTimeInputRequestTypeDef = TypedDict(
    "_RequiredPutMaintenanceStartTimeInputRequestTypeDef",
    {
        "GatewayArn": str,
        "HourOfDay": int,
        "MinuteOfHour": int,
    },
)
_OptionalPutMaintenanceStartTimeInputRequestTypeDef = TypedDict(
    "_OptionalPutMaintenanceStartTimeInputRequestTypeDef",
    {
        "DayOfMonth": int,
        "DayOfWeek": int,
    },
    total=False,
)


class PutMaintenanceStartTimeInputRequestTypeDef(
    _RequiredPutMaintenanceStartTimeInputRequestTypeDef,
    _OptionalPutMaintenanceStartTimeInputRequestTypeDef,
):
    pass


_RequiredTestHypervisorConfigurationInputRequestTypeDef = TypedDict(
    "_RequiredTestHypervisorConfigurationInputRequestTypeDef",
    {
        "GatewayArn": str,
        "Host": str,
    },
)
_OptionalTestHypervisorConfigurationInputRequestTypeDef = TypedDict(
    "_OptionalTestHypervisorConfigurationInputRequestTypeDef",
    {
        "Password": str,
        "Username": str,
    },
    total=False,
)


class TestHypervisorConfigurationInputRequestTypeDef(
    _RequiredTestHypervisorConfigurationInputRequestTypeDef,
    _OptionalTestHypervisorConfigurationInputRequestTypeDef,
):
    pass


UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateGatewayInformationInputRequestTypeDef = TypedDict(
    "_RequiredUpdateGatewayInformationInputRequestTypeDef",
    {
        "GatewayArn": str,
    },
)
_OptionalUpdateGatewayInformationInputRequestTypeDef = TypedDict(
    "_OptionalUpdateGatewayInformationInputRequestTypeDef",
    {
        "GatewayDisplayName": str,
    },
    total=False,
)


class UpdateGatewayInformationInputRequestTypeDef(
    _RequiredUpdateGatewayInformationInputRequestTypeDef,
    _OptionalUpdateGatewayInformationInputRequestTypeDef,
):
    pass


UpdateGatewaySoftwareNowInputRequestTypeDef = TypedDict(
    "UpdateGatewaySoftwareNowInputRequestTypeDef",
    {
        "GatewayArn": str,
    },
)

_RequiredUpdateHypervisorInputRequestTypeDef = TypedDict(
    "_RequiredUpdateHypervisorInputRequestTypeDef",
    {
        "HypervisorArn": str,
    },
)
_OptionalUpdateHypervisorInputRequestTypeDef = TypedDict(
    "_OptionalUpdateHypervisorInputRequestTypeDef",
    {
        "Host": str,
        "Name": str,
        "Password": str,
        "Username": str,
    },
    total=False,
)


class UpdateHypervisorInputRequestTypeDef(
    _RequiredUpdateHypervisorInputRequestTypeDef, _OptionalUpdateHypervisorInputRequestTypeDef
):
    pass


AssociateGatewayToServerOutputTypeDef = TypedDict(
    "AssociateGatewayToServerOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGatewayOutputTypeDef = TypedDict(
    "CreateGatewayOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGatewayOutputTypeDef = TypedDict(
    "DeleteGatewayOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteHypervisorOutputTypeDef = TypedDict(
    "DeleteHypervisorOutputTypeDef",
    {
        "HypervisorArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateGatewayFromServerOutputTypeDef = TypedDict(
    "DisassociateGatewayFromServerOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportHypervisorConfigurationOutputTypeDef = TypedDict(
    "ImportHypervisorConfigurationOutputTypeDef",
    {
        "HypervisorArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutMaintenanceStartTimeOutputTypeDef = TypedDict(
    "PutMaintenanceStartTimeOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceOutputTypeDef = TypedDict(
    "TagResourceOutputTypeDef",
    {
        "ResourceARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UntagResourceOutputTypeDef = TypedDict(
    "UntagResourceOutputTypeDef",
    {
        "ResourceARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGatewayInformationOutputTypeDef = TypedDict(
    "UpdateGatewayInformationOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGatewaySoftwareNowOutputTypeDef = TypedDict(
    "UpdateGatewaySoftwareNowOutputTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateHypervisorOutputTypeDef = TypedDict(
    "UpdateHypervisorOutputTypeDef",
    {
        "HypervisorArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateGatewayInputRequestTypeDef = TypedDict(
    "_RequiredCreateGatewayInputRequestTypeDef",
    {
        "ActivationKey": str,
        "GatewayDisplayName": str,
        "GatewayType": Literal["BACKUP_VM"],
    },
)
_OptionalCreateGatewayInputRequestTypeDef = TypedDict(
    "_OptionalCreateGatewayInputRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateGatewayInputRequestTypeDef(
    _RequiredCreateGatewayInputRequestTypeDef, _OptionalCreateGatewayInputRequestTypeDef
):
    pass


_RequiredImportHypervisorConfigurationInputRequestTypeDef = TypedDict(
    "_RequiredImportHypervisorConfigurationInputRequestTypeDef",
    {
        "Host": str,
        "Name": str,
    },
)
_OptionalImportHypervisorConfigurationInputRequestTypeDef = TypedDict(
    "_OptionalImportHypervisorConfigurationInputRequestTypeDef",
    {
        "KmsKeyArn": str,
        "Password": str,
        "Tags": Sequence[TagTypeDef],
        "Username": str,
    },
    total=False,
)


class ImportHypervisorConfigurationInputRequestTypeDef(
    _RequiredImportHypervisorConfigurationInputRequestTypeDef,
    _OptionalImportHypervisorConfigurationInputRequestTypeDef,
):
    pass


ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "ResourceArn": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

GetGatewayOutputTypeDef = TypedDict(
    "GetGatewayOutputTypeDef",
    {
        "Gateway": GatewayDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGatewaysOutputTypeDef = TypedDict(
    "ListGatewaysOutputTypeDef",
    {
        "Gateways": List[GatewayTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListHypervisorsOutputTypeDef = TypedDict(
    "ListHypervisorsOutputTypeDef",
    {
        "Hypervisors": List[HypervisorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGatewaysInputListGatewaysPaginateTypeDef = TypedDict(
    "ListGatewaysInputListGatewaysPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListHypervisorsInputListHypervisorsPaginateTypeDef = TypedDict(
    "ListHypervisorsInputListHypervisorsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListVirtualMachinesInputListVirtualMachinesPaginateTypeDef = TypedDict(
    "ListVirtualMachinesInputListVirtualMachinesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListVirtualMachinesOutputTypeDef = TypedDict(
    "ListVirtualMachinesOutputTypeDef",
    {
        "NextToken": str,
        "VirtualMachines": List[VirtualMachineTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
