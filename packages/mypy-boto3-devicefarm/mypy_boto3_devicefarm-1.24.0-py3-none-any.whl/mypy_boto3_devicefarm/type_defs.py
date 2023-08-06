"""
Type annotations for devicefarm service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devicefarm/type_defs/)

Usage::

    ```python
    from mypy_boto3_devicefarm.type_defs import TrialMinutesTypeDef

    data: TrialMinutesTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ArtifactCategoryType,
    ArtifactTypeType,
    BillingMethodType,
    DeviceAttributeType,
    DeviceAvailabilityType,
    DeviceFilterAttributeType,
    DeviceFormFactorType,
    DevicePlatformType,
    DevicePoolTypeType,
    ExecutionResultCodeType,
    ExecutionResultType,
    ExecutionStatusType,
    InstanceStatusType,
    InteractionModeType,
    NetworkProfileTypeType,
    OfferingTransactionTypeType,
    RuleOperatorType,
    SampleTypeType,
    TestGridSessionArtifactCategoryType,
    TestGridSessionArtifactTypeType,
    TestGridSessionStatusType,
    TestTypeType,
    UploadCategoryType,
    UploadStatusType,
    UploadTypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "TrialMinutesTypeDef",
    "ArtifactTypeDef",
    "CPUTypeDef",
    "CountersTypeDef",
    "RuleTypeDef",
    "ResponseMetadataTypeDef",
    "CreateInstanceProfileRequestRequestTypeDef",
    "InstanceProfileTypeDef",
    "CreateNetworkProfileRequestRequestTypeDef",
    "NetworkProfileTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "ProjectTypeDef",
    "CreateRemoteAccessSessionConfigurationTypeDef",
    "TestGridVpcConfigTypeDef",
    "CreateTestGridUrlRequestRequestTypeDef",
    "CreateUploadRequestRequestTypeDef",
    "UploadTypeDef",
    "CreateVPCEConfigurationRequestRequestTypeDef",
    "VPCEConfigurationTypeDef",
    "CustomerArtifactPathsTypeDef",
    "DeleteDevicePoolRequestRequestTypeDef",
    "DeleteInstanceProfileRequestRequestTypeDef",
    "DeleteNetworkProfileRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteRemoteAccessSessionRequestRequestTypeDef",
    "DeleteRunRequestRequestTypeDef",
    "DeleteTestGridProjectRequestRequestTypeDef",
    "DeleteUploadRequestRequestTypeDef",
    "DeleteVPCEConfigurationRequestRequestTypeDef",
    "DeviceFilterTypeDef",
    "DeviceMinutesTypeDef",
    "IncompatibilityMessageTypeDef",
    "ResolutionTypeDef",
    "ExecutionConfigurationTypeDef",
    "GetDeviceInstanceRequestRequestTypeDef",
    "ScheduleRunTestTypeDef",
    "GetDevicePoolRequestRequestTypeDef",
    "GetDeviceRequestRequestTypeDef",
    "GetInstanceProfileRequestRequestTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetNetworkProfileRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "GetOfferingStatusRequestRequestTypeDef",
    "GetProjectRequestRequestTypeDef",
    "GetRemoteAccessSessionRequestRequestTypeDef",
    "GetRunRequestRequestTypeDef",
    "GetSuiteRequestRequestTypeDef",
    "GetTestGridProjectRequestRequestTypeDef",
    "GetTestGridSessionRequestRequestTypeDef",
    "TestGridSessionTypeDef",
    "GetTestRequestRequestTypeDef",
    "GetUploadRequestRequestTypeDef",
    "GetVPCEConfigurationRequestRequestTypeDef",
    "InstallToRemoteAccessSessionRequestRequestTypeDef",
    "ListArtifactsRequestRequestTypeDef",
    "ListDeviceInstancesRequestRequestTypeDef",
    "ListDevicePoolsRequestRequestTypeDef",
    "ListInstanceProfilesRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListNetworkProfilesRequestRequestTypeDef",
    "ListOfferingPromotionsRequestRequestTypeDef",
    "OfferingPromotionTypeDef",
    "ListOfferingTransactionsRequestRequestTypeDef",
    "ListOfferingsRequestRequestTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListRemoteAccessSessionsRequestRequestTypeDef",
    "ListRunsRequestRequestTypeDef",
    "ListSamplesRequestRequestTypeDef",
    "SampleTypeDef",
    "ListSuitesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagTypeDef",
    "ListTestGridProjectsRequestRequestTypeDef",
    "ListTestGridSessionActionsRequestRequestTypeDef",
    "TestGridSessionActionTypeDef",
    "ListTestGridSessionArtifactsRequestRequestTypeDef",
    "TestGridSessionArtifactTypeDef",
    "ListTestGridSessionsRequestRequestTypeDef",
    "ListTestsRequestRequestTypeDef",
    "ListUniqueProblemsRequestRequestTypeDef",
    "ListUploadsRequestRequestTypeDef",
    "ListVPCEConfigurationsRequestRequestTypeDef",
    "LocationTypeDef",
    "MonetaryAmountTypeDef",
    "ProblemDetailTypeDef",
    "PurchaseOfferingRequestRequestTypeDef",
    "RadiosTypeDef",
    "RenewOfferingRequestRequestTypeDef",
    "StopJobRequestRequestTypeDef",
    "StopRemoteAccessSessionRequestRequestTypeDef",
    "StopRunRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDeviceInstanceRequestRequestTypeDef",
    "UpdateInstanceProfileRequestRequestTypeDef",
    "UpdateNetworkProfileRequestRequestTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "UpdateUploadRequestRequestTypeDef",
    "UpdateVPCEConfigurationRequestRequestTypeDef",
    "AccountSettingsTypeDef",
    "CreateDevicePoolRequestRequestTypeDef",
    "DevicePoolTypeDef",
    "UpdateDevicePoolRequestRequestTypeDef",
    "CreateTestGridUrlResultTypeDef",
    "ListArtifactsResultTypeDef",
    "CreateInstanceProfileResultTypeDef",
    "DeviceInstanceTypeDef",
    "GetInstanceProfileResultTypeDef",
    "ListInstanceProfilesResultTypeDef",
    "UpdateInstanceProfileResultTypeDef",
    "CreateNetworkProfileResultTypeDef",
    "GetNetworkProfileResultTypeDef",
    "ListNetworkProfilesResultTypeDef",
    "UpdateNetworkProfileResultTypeDef",
    "CreateProjectResultTypeDef",
    "GetProjectResultTypeDef",
    "ListProjectsResultTypeDef",
    "UpdateProjectResultTypeDef",
    "CreateRemoteAccessSessionRequestRequestTypeDef",
    "CreateTestGridProjectRequestRequestTypeDef",
    "TestGridProjectTypeDef",
    "UpdateTestGridProjectRequestRequestTypeDef",
    "CreateUploadResultTypeDef",
    "GetUploadResultTypeDef",
    "InstallToRemoteAccessSessionResultTypeDef",
    "ListUploadsResultTypeDef",
    "UpdateUploadResultTypeDef",
    "CreateVPCEConfigurationResultTypeDef",
    "GetVPCEConfigurationResultTypeDef",
    "ListVPCEConfigurationsResultTypeDef",
    "UpdateVPCEConfigurationResultTypeDef",
    "DeviceSelectionConfigurationTypeDef",
    "DeviceSelectionResultTypeDef",
    "ListDevicesRequestRequestTypeDef",
    "SuiteTypeDef",
    "TestTypeDef",
    "GetOfferingStatusRequestGetOfferingStatusPaginateTypeDef",
    "ListArtifactsRequestListArtifactsPaginateTypeDef",
    "ListDeviceInstancesRequestListDeviceInstancesPaginateTypeDef",
    "ListDevicePoolsRequestListDevicePoolsPaginateTypeDef",
    "ListDevicesRequestListDevicesPaginateTypeDef",
    "ListInstanceProfilesRequestListInstanceProfilesPaginateTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListNetworkProfilesRequestListNetworkProfilesPaginateTypeDef",
    "ListOfferingPromotionsRequestListOfferingPromotionsPaginateTypeDef",
    "ListOfferingTransactionsRequestListOfferingTransactionsPaginateTypeDef",
    "ListOfferingsRequestListOfferingsPaginateTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListRemoteAccessSessionsRequestListRemoteAccessSessionsPaginateTypeDef",
    "ListRunsRequestListRunsPaginateTypeDef",
    "ListSamplesRequestListSamplesPaginateTypeDef",
    "ListSuitesRequestListSuitesPaginateTypeDef",
    "ListTestsRequestListTestsPaginateTypeDef",
    "ListUniqueProblemsRequestListUniqueProblemsPaginateTypeDef",
    "ListUploadsRequestListUploadsPaginateTypeDef",
    "ListVPCEConfigurationsRequestListVPCEConfigurationsPaginateTypeDef",
    "GetTestGridSessionResultTypeDef",
    "ListTestGridSessionsResultTypeDef",
    "ListOfferingPromotionsResultTypeDef",
    "ListSamplesResultTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ListTestGridSessionActionsResultTypeDef",
    "ListTestGridSessionArtifactsResultTypeDef",
    "RecurringChargeTypeDef",
    "ScheduleRunConfigurationTypeDef",
    "GetAccountSettingsResultTypeDef",
    "CreateDevicePoolResultTypeDef",
    "GetDevicePoolResultTypeDef",
    "ListDevicePoolsResultTypeDef",
    "UpdateDevicePoolResultTypeDef",
    "DeviceTypeDef",
    "GetDeviceInstanceResultTypeDef",
    "ListDeviceInstancesResultTypeDef",
    "UpdateDeviceInstanceResultTypeDef",
    "CreateTestGridProjectResultTypeDef",
    "GetTestGridProjectResultTypeDef",
    "ListTestGridProjectsResultTypeDef",
    "UpdateTestGridProjectResultTypeDef",
    "RunTypeDef",
    "GetSuiteResultTypeDef",
    "ListSuitesResultTypeDef",
    "GetTestResultTypeDef",
    "ListTestsResultTypeDef",
    "OfferingTypeDef",
    "GetDevicePoolCompatibilityRequestRequestTypeDef",
    "ScheduleRunRequestRequestTypeDef",
    "DevicePoolCompatibilityResultTypeDef",
    "GetDeviceResultTypeDef",
    "JobTypeDef",
    "ListDevicesResultTypeDef",
    "ProblemTypeDef",
    "RemoteAccessSessionTypeDef",
    "GetRunResultTypeDef",
    "ListRunsResultTypeDef",
    "ScheduleRunResultTypeDef",
    "StopRunResultTypeDef",
    "ListOfferingsResultTypeDef",
    "OfferingStatusTypeDef",
    "GetDevicePoolCompatibilityResultTypeDef",
    "GetJobResultTypeDef",
    "ListJobsResultTypeDef",
    "StopJobResultTypeDef",
    "UniqueProblemTypeDef",
    "CreateRemoteAccessSessionResultTypeDef",
    "GetRemoteAccessSessionResultTypeDef",
    "ListRemoteAccessSessionsResultTypeDef",
    "StopRemoteAccessSessionResultTypeDef",
    "GetOfferingStatusResultTypeDef",
    "OfferingTransactionTypeDef",
    "ListUniqueProblemsResultTypeDef",
    "ListOfferingTransactionsResultTypeDef",
    "PurchaseOfferingResultTypeDef",
    "RenewOfferingResultTypeDef",
)

TrialMinutesTypeDef = TypedDict(
    "TrialMinutesTypeDef",
    {
        "total": float,
        "remaining": float,
    },
    total=False,
)

ArtifactTypeDef = TypedDict(
    "ArtifactTypeDef",
    {
        "arn": str,
        "name": str,
        "type": ArtifactTypeType,
        "extension": str,
        "url": str,
    },
    total=False,
)

CPUTypeDef = TypedDict(
    "CPUTypeDef",
    {
        "frequency": str,
        "architecture": str,
        "clock": float,
    },
    total=False,
)

CountersTypeDef = TypedDict(
    "CountersTypeDef",
    {
        "total": int,
        "passed": int,
        "failed": int,
        "warned": int,
        "errored": int,
        "stopped": int,
        "skipped": int,
    },
    total=False,
)

RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "attribute": DeviceAttributeType,
        "operator": RuleOperatorType,
        "value": str,
    },
    total=False,
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

_RequiredCreateInstanceProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateInstanceProfileRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateInstanceProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateInstanceProfileRequestRequestTypeDef",
    {
        "description": str,
        "packageCleanup": bool,
        "excludeAppPackagesFromCleanup": Sequence[str],
        "rebootAfterUse": bool,
    },
    total=False,
)


class CreateInstanceProfileRequestRequestTypeDef(
    _RequiredCreateInstanceProfileRequestRequestTypeDef,
    _OptionalCreateInstanceProfileRequestRequestTypeDef,
):
    pass


InstanceProfileTypeDef = TypedDict(
    "InstanceProfileTypeDef",
    {
        "arn": str,
        "packageCleanup": bool,
        "excludeAppPackagesFromCleanup": List[str],
        "rebootAfterUse": bool,
        "name": str,
        "description": str,
    },
    total=False,
)

_RequiredCreateNetworkProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateNetworkProfileRequestRequestTypeDef",
    {
        "projectArn": str,
        "name": str,
    },
)
_OptionalCreateNetworkProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateNetworkProfileRequestRequestTypeDef",
    {
        "description": str,
        "type": NetworkProfileTypeType,
        "uplinkBandwidthBits": int,
        "downlinkBandwidthBits": int,
        "uplinkDelayMs": int,
        "downlinkDelayMs": int,
        "uplinkJitterMs": int,
        "downlinkJitterMs": int,
        "uplinkLossPercent": int,
        "downlinkLossPercent": int,
    },
    total=False,
)


class CreateNetworkProfileRequestRequestTypeDef(
    _RequiredCreateNetworkProfileRequestRequestTypeDef,
    _OptionalCreateNetworkProfileRequestRequestTypeDef,
):
    pass


NetworkProfileTypeDef = TypedDict(
    "NetworkProfileTypeDef",
    {
        "arn": str,
        "name": str,
        "description": str,
        "type": NetworkProfileTypeType,
        "uplinkBandwidthBits": int,
        "downlinkBandwidthBits": int,
        "uplinkDelayMs": int,
        "downlinkDelayMs": int,
        "uplinkJitterMs": int,
        "downlinkJitterMs": int,
        "uplinkLossPercent": int,
        "downlinkLossPercent": int,
    },
    total=False,
)

_RequiredCreateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProjectRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProjectRequestRequestTypeDef",
    {
        "defaultJobTimeoutMinutes": int,
    },
    total=False,
)


class CreateProjectRequestRequestTypeDef(
    _RequiredCreateProjectRequestRequestTypeDef, _OptionalCreateProjectRequestRequestTypeDef
):
    pass


ProjectTypeDef = TypedDict(
    "ProjectTypeDef",
    {
        "arn": str,
        "name": str,
        "defaultJobTimeoutMinutes": int,
        "created": datetime,
    },
    total=False,
)

CreateRemoteAccessSessionConfigurationTypeDef = TypedDict(
    "CreateRemoteAccessSessionConfigurationTypeDef",
    {
        "billingMethod": BillingMethodType,
        "vpceConfigurationArns": Sequence[str],
    },
    total=False,
)

TestGridVpcConfigTypeDef = TypedDict(
    "TestGridVpcConfigTypeDef",
    {
        "securityGroupIds": Sequence[str],
        "subnetIds": Sequence[str],
        "vpcId": str,
    },
)

CreateTestGridUrlRequestRequestTypeDef = TypedDict(
    "CreateTestGridUrlRequestRequestTypeDef",
    {
        "projectArn": str,
        "expiresInSeconds": int,
    },
)

_RequiredCreateUploadRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUploadRequestRequestTypeDef",
    {
        "projectArn": str,
        "name": str,
        "type": UploadTypeType,
    },
)
_OptionalCreateUploadRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUploadRequestRequestTypeDef",
    {
        "contentType": str,
    },
    total=False,
)


class CreateUploadRequestRequestTypeDef(
    _RequiredCreateUploadRequestRequestTypeDef, _OptionalCreateUploadRequestRequestTypeDef
):
    pass


UploadTypeDef = TypedDict(
    "UploadTypeDef",
    {
        "arn": str,
        "name": str,
        "created": datetime,
        "type": UploadTypeType,
        "status": UploadStatusType,
        "url": str,
        "metadata": str,
        "contentType": str,
        "message": str,
        "category": UploadCategoryType,
    },
    total=False,
)

_RequiredCreateVPCEConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateVPCEConfigurationRequestRequestTypeDef",
    {
        "vpceConfigurationName": str,
        "vpceServiceName": str,
        "serviceDnsName": str,
    },
)
_OptionalCreateVPCEConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateVPCEConfigurationRequestRequestTypeDef",
    {
        "vpceConfigurationDescription": str,
    },
    total=False,
)


class CreateVPCEConfigurationRequestRequestTypeDef(
    _RequiredCreateVPCEConfigurationRequestRequestTypeDef,
    _OptionalCreateVPCEConfigurationRequestRequestTypeDef,
):
    pass


VPCEConfigurationTypeDef = TypedDict(
    "VPCEConfigurationTypeDef",
    {
        "arn": str,
        "vpceConfigurationName": str,
        "vpceServiceName": str,
        "serviceDnsName": str,
        "vpceConfigurationDescription": str,
    },
    total=False,
)

CustomerArtifactPathsTypeDef = TypedDict(
    "CustomerArtifactPathsTypeDef",
    {
        "iosPaths": Sequence[str],
        "androidPaths": Sequence[str],
        "deviceHostPaths": Sequence[str],
    },
    total=False,
)

DeleteDevicePoolRequestRequestTypeDef = TypedDict(
    "DeleteDevicePoolRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteInstanceProfileRequestRequestTypeDef = TypedDict(
    "DeleteInstanceProfileRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteNetworkProfileRequestRequestTypeDef = TypedDict(
    "DeleteNetworkProfileRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteProjectRequestRequestTypeDef = TypedDict(
    "DeleteProjectRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteRemoteAccessSessionRequestRequestTypeDef = TypedDict(
    "DeleteRemoteAccessSessionRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteRunRequestRequestTypeDef = TypedDict(
    "DeleteRunRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteTestGridProjectRequestRequestTypeDef = TypedDict(
    "DeleteTestGridProjectRequestRequestTypeDef",
    {
        "projectArn": str,
    },
)

DeleteUploadRequestRequestTypeDef = TypedDict(
    "DeleteUploadRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteVPCEConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteVPCEConfigurationRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeviceFilterTypeDef = TypedDict(
    "DeviceFilterTypeDef",
    {
        "attribute": DeviceFilterAttributeType,
        "operator": RuleOperatorType,
        "values": List[str],
    },
)

DeviceMinutesTypeDef = TypedDict(
    "DeviceMinutesTypeDef",
    {
        "total": float,
        "metered": float,
        "unmetered": float,
    },
    total=False,
)

IncompatibilityMessageTypeDef = TypedDict(
    "IncompatibilityMessageTypeDef",
    {
        "message": str,
        "type": DeviceAttributeType,
    },
    total=False,
)

ResolutionTypeDef = TypedDict(
    "ResolutionTypeDef",
    {
        "width": int,
        "height": int,
    },
    total=False,
)

ExecutionConfigurationTypeDef = TypedDict(
    "ExecutionConfigurationTypeDef",
    {
        "jobTimeoutMinutes": int,
        "accountsCleanup": bool,
        "appPackagesCleanup": bool,
        "videoCapture": bool,
        "skipAppResign": bool,
    },
    total=False,
)

GetDeviceInstanceRequestRequestTypeDef = TypedDict(
    "GetDeviceInstanceRequestRequestTypeDef",
    {
        "arn": str,
    },
)

_RequiredScheduleRunTestTypeDef = TypedDict(
    "_RequiredScheduleRunTestTypeDef",
    {
        "type": TestTypeType,
    },
)
_OptionalScheduleRunTestTypeDef = TypedDict(
    "_OptionalScheduleRunTestTypeDef",
    {
        "testPackageArn": str,
        "testSpecArn": str,
        "filter": str,
        "parameters": Mapping[str, str],
    },
    total=False,
)


class ScheduleRunTestTypeDef(_RequiredScheduleRunTestTypeDef, _OptionalScheduleRunTestTypeDef):
    pass


GetDevicePoolRequestRequestTypeDef = TypedDict(
    "GetDevicePoolRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetDeviceRequestRequestTypeDef = TypedDict(
    "GetDeviceRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetInstanceProfileRequestRequestTypeDef = TypedDict(
    "GetInstanceProfileRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetJobRequestRequestTypeDef = TypedDict(
    "GetJobRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetNetworkProfileRequestRequestTypeDef = TypedDict(
    "GetNetworkProfileRequestRequestTypeDef",
    {
        "arn": str,
    },
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

GetOfferingStatusRequestRequestTypeDef = TypedDict(
    "GetOfferingStatusRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

GetProjectRequestRequestTypeDef = TypedDict(
    "GetProjectRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetRemoteAccessSessionRequestRequestTypeDef = TypedDict(
    "GetRemoteAccessSessionRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetRunRequestRequestTypeDef = TypedDict(
    "GetRunRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetSuiteRequestRequestTypeDef = TypedDict(
    "GetSuiteRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetTestGridProjectRequestRequestTypeDef = TypedDict(
    "GetTestGridProjectRequestRequestTypeDef",
    {
        "projectArn": str,
    },
)

GetTestGridSessionRequestRequestTypeDef = TypedDict(
    "GetTestGridSessionRequestRequestTypeDef",
    {
        "projectArn": str,
        "sessionId": str,
        "sessionArn": str,
    },
    total=False,
)

TestGridSessionTypeDef = TypedDict(
    "TestGridSessionTypeDef",
    {
        "arn": str,
        "status": TestGridSessionStatusType,
        "created": datetime,
        "ended": datetime,
        "billingMinutes": float,
        "seleniumProperties": str,
    },
    total=False,
)

GetTestRequestRequestTypeDef = TypedDict(
    "GetTestRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetUploadRequestRequestTypeDef = TypedDict(
    "GetUploadRequestRequestTypeDef",
    {
        "arn": str,
    },
)

GetVPCEConfigurationRequestRequestTypeDef = TypedDict(
    "GetVPCEConfigurationRequestRequestTypeDef",
    {
        "arn": str,
    },
)

InstallToRemoteAccessSessionRequestRequestTypeDef = TypedDict(
    "InstallToRemoteAccessSessionRequestRequestTypeDef",
    {
        "remoteAccessSessionArn": str,
        "appArn": str,
    },
)

_RequiredListArtifactsRequestRequestTypeDef = TypedDict(
    "_RequiredListArtifactsRequestRequestTypeDef",
    {
        "arn": str,
        "type": ArtifactCategoryType,
    },
)
_OptionalListArtifactsRequestRequestTypeDef = TypedDict(
    "_OptionalListArtifactsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListArtifactsRequestRequestTypeDef(
    _RequiredListArtifactsRequestRequestTypeDef, _OptionalListArtifactsRequestRequestTypeDef
):
    pass


ListDeviceInstancesRequestRequestTypeDef = TypedDict(
    "ListDeviceInstancesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListDevicePoolsRequestRequestTypeDef = TypedDict(
    "_RequiredListDevicePoolsRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalListDevicePoolsRequestRequestTypeDef = TypedDict(
    "_OptionalListDevicePoolsRequestRequestTypeDef",
    {
        "type": DevicePoolTypeType,
        "nextToken": str,
    },
    total=False,
)


class ListDevicePoolsRequestRequestTypeDef(
    _RequiredListDevicePoolsRequestRequestTypeDef, _OptionalListDevicePoolsRequestRequestTypeDef
):
    pass


ListInstanceProfilesRequestRequestTypeDef = TypedDict(
    "ListInstanceProfilesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListJobsRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalListJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListJobsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListJobsRequestRequestTypeDef(
    _RequiredListJobsRequestRequestTypeDef, _OptionalListJobsRequestRequestTypeDef
):
    pass


_RequiredListNetworkProfilesRequestRequestTypeDef = TypedDict(
    "_RequiredListNetworkProfilesRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalListNetworkProfilesRequestRequestTypeDef = TypedDict(
    "_OptionalListNetworkProfilesRequestRequestTypeDef",
    {
        "type": NetworkProfileTypeType,
        "nextToken": str,
    },
    total=False,
)


class ListNetworkProfilesRequestRequestTypeDef(
    _RequiredListNetworkProfilesRequestRequestTypeDef,
    _OptionalListNetworkProfilesRequestRequestTypeDef,
):
    pass


ListOfferingPromotionsRequestRequestTypeDef = TypedDict(
    "ListOfferingPromotionsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

OfferingPromotionTypeDef = TypedDict(
    "OfferingPromotionTypeDef",
    {
        "id": str,
        "description": str,
    },
    total=False,
)

ListOfferingTransactionsRequestRequestTypeDef = TypedDict(
    "ListOfferingTransactionsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

ListOfferingsRequestRequestTypeDef = TypedDict(
    "ListOfferingsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

ListProjectsRequestRequestTypeDef = TypedDict(
    "ListProjectsRequestRequestTypeDef",
    {
        "arn": str,
        "nextToken": str,
    },
    total=False,
)

_RequiredListRemoteAccessSessionsRequestRequestTypeDef = TypedDict(
    "_RequiredListRemoteAccessSessionsRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalListRemoteAccessSessionsRequestRequestTypeDef = TypedDict(
    "_OptionalListRemoteAccessSessionsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListRemoteAccessSessionsRequestRequestTypeDef(
    _RequiredListRemoteAccessSessionsRequestRequestTypeDef,
    _OptionalListRemoteAccessSessionsRequestRequestTypeDef,
):
    pass


_RequiredListRunsRequestRequestTypeDef = TypedDict(
    "_RequiredListRunsRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalListRunsRequestRequestTypeDef = TypedDict(
    "_OptionalListRunsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListRunsRequestRequestTypeDef(
    _RequiredListRunsRequestRequestTypeDef, _OptionalListRunsRequestRequestTypeDef
):
    pass


_RequiredListSamplesRequestRequestTypeDef = TypedDict(
    "_RequiredListSamplesRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalListSamplesRequestRequestTypeDef = TypedDict(
    "_OptionalListSamplesRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListSamplesRequestRequestTypeDef(
    _RequiredListSamplesRequestRequestTypeDef, _OptionalListSamplesRequestRequestTypeDef
):
    pass


SampleTypeDef = TypedDict(
    "SampleTypeDef",
    {
        "arn": str,
        "type": SampleTypeType,
        "url": str,
    },
    total=False,
)

_RequiredListSuitesRequestRequestTypeDef = TypedDict(
    "_RequiredListSuitesRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalListSuitesRequestRequestTypeDef = TypedDict(
    "_OptionalListSuitesRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListSuitesRequestRequestTypeDef(
    _RequiredListSuitesRequestRequestTypeDef, _OptionalListSuitesRequestRequestTypeDef
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

ListTestGridProjectsRequestRequestTypeDef = TypedDict(
    "ListTestGridProjectsRequestRequestTypeDef",
    {
        "maxResult": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListTestGridSessionActionsRequestRequestTypeDef = TypedDict(
    "_RequiredListTestGridSessionActionsRequestRequestTypeDef",
    {
        "sessionArn": str,
    },
)
_OptionalListTestGridSessionActionsRequestRequestTypeDef = TypedDict(
    "_OptionalListTestGridSessionActionsRequestRequestTypeDef",
    {
        "maxResult": int,
        "nextToken": str,
    },
    total=False,
)


class ListTestGridSessionActionsRequestRequestTypeDef(
    _RequiredListTestGridSessionActionsRequestRequestTypeDef,
    _OptionalListTestGridSessionActionsRequestRequestTypeDef,
):
    pass


TestGridSessionActionTypeDef = TypedDict(
    "TestGridSessionActionTypeDef",
    {
        "action": str,
        "started": datetime,
        "duration": int,
        "statusCode": str,
        "requestMethod": str,
    },
    total=False,
)

_RequiredListTestGridSessionArtifactsRequestRequestTypeDef = TypedDict(
    "_RequiredListTestGridSessionArtifactsRequestRequestTypeDef",
    {
        "sessionArn": str,
    },
)
_OptionalListTestGridSessionArtifactsRequestRequestTypeDef = TypedDict(
    "_OptionalListTestGridSessionArtifactsRequestRequestTypeDef",
    {
        "type": TestGridSessionArtifactCategoryType,
        "maxResult": int,
        "nextToken": str,
    },
    total=False,
)


class ListTestGridSessionArtifactsRequestRequestTypeDef(
    _RequiredListTestGridSessionArtifactsRequestRequestTypeDef,
    _OptionalListTestGridSessionArtifactsRequestRequestTypeDef,
):
    pass


TestGridSessionArtifactTypeDef = TypedDict(
    "TestGridSessionArtifactTypeDef",
    {
        "filename": str,
        "type": TestGridSessionArtifactTypeType,
        "url": str,
    },
    total=False,
)

_RequiredListTestGridSessionsRequestRequestTypeDef = TypedDict(
    "_RequiredListTestGridSessionsRequestRequestTypeDef",
    {
        "projectArn": str,
    },
)
_OptionalListTestGridSessionsRequestRequestTypeDef = TypedDict(
    "_OptionalListTestGridSessionsRequestRequestTypeDef",
    {
        "status": TestGridSessionStatusType,
        "creationTimeAfter": Union[datetime, str],
        "creationTimeBefore": Union[datetime, str],
        "endTimeAfter": Union[datetime, str],
        "endTimeBefore": Union[datetime, str],
        "maxResult": int,
        "nextToken": str,
    },
    total=False,
)


class ListTestGridSessionsRequestRequestTypeDef(
    _RequiredListTestGridSessionsRequestRequestTypeDef,
    _OptionalListTestGridSessionsRequestRequestTypeDef,
):
    pass


_RequiredListTestsRequestRequestTypeDef = TypedDict(
    "_RequiredListTestsRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalListTestsRequestRequestTypeDef = TypedDict(
    "_OptionalListTestsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListTestsRequestRequestTypeDef(
    _RequiredListTestsRequestRequestTypeDef, _OptionalListTestsRequestRequestTypeDef
):
    pass


_RequiredListUniqueProblemsRequestRequestTypeDef = TypedDict(
    "_RequiredListUniqueProblemsRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalListUniqueProblemsRequestRequestTypeDef = TypedDict(
    "_OptionalListUniqueProblemsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListUniqueProblemsRequestRequestTypeDef(
    _RequiredListUniqueProblemsRequestRequestTypeDef,
    _OptionalListUniqueProblemsRequestRequestTypeDef,
):
    pass


_RequiredListUploadsRequestRequestTypeDef = TypedDict(
    "_RequiredListUploadsRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalListUploadsRequestRequestTypeDef = TypedDict(
    "_OptionalListUploadsRequestRequestTypeDef",
    {
        "type": UploadTypeType,
        "nextToken": str,
    },
    total=False,
)


class ListUploadsRequestRequestTypeDef(
    _RequiredListUploadsRequestRequestTypeDef, _OptionalListUploadsRequestRequestTypeDef
):
    pass


ListVPCEConfigurationsRequestRequestTypeDef = TypedDict(
    "ListVPCEConfigurationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

LocationTypeDef = TypedDict(
    "LocationTypeDef",
    {
        "latitude": float,
        "longitude": float,
    },
)

MonetaryAmountTypeDef = TypedDict(
    "MonetaryAmountTypeDef",
    {
        "amount": float,
        "currencyCode": Literal["USD"],
    },
    total=False,
)

ProblemDetailTypeDef = TypedDict(
    "ProblemDetailTypeDef",
    {
        "arn": str,
        "name": str,
    },
    total=False,
)

_RequiredPurchaseOfferingRequestRequestTypeDef = TypedDict(
    "_RequiredPurchaseOfferingRequestRequestTypeDef",
    {
        "offeringId": str,
        "quantity": int,
    },
)
_OptionalPurchaseOfferingRequestRequestTypeDef = TypedDict(
    "_OptionalPurchaseOfferingRequestRequestTypeDef",
    {
        "offeringPromotionId": str,
    },
    total=False,
)


class PurchaseOfferingRequestRequestTypeDef(
    _RequiredPurchaseOfferingRequestRequestTypeDef, _OptionalPurchaseOfferingRequestRequestTypeDef
):
    pass


RadiosTypeDef = TypedDict(
    "RadiosTypeDef",
    {
        "wifi": bool,
        "bluetooth": bool,
        "nfc": bool,
        "gps": bool,
    },
    total=False,
)

RenewOfferingRequestRequestTypeDef = TypedDict(
    "RenewOfferingRequestRequestTypeDef",
    {
        "offeringId": str,
        "quantity": int,
    },
)

StopJobRequestRequestTypeDef = TypedDict(
    "StopJobRequestRequestTypeDef",
    {
        "arn": str,
    },
)

StopRemoteAccessSessionRequestRequestTypeDef = TypedDict(
    "StopRemoteAccessSessionRequestRequestTypeDef",
    {
        "arn": str,
    },
)

StopRunRequestRequestTypeDef = TypedDict(
    "StopRunRequestRequestTypeDef",
    {
        "arn": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateDeviceInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDeviceInstanceRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalUpdateDeviceInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDeviceInstanceRequestRequestTypeDef",
    {
        "profileArn": str,
        "labels": Sequence[str],
    },
    total=False,
)


class UpdateDeviceInstanceRequestRequestTypeDef(
    _RequiredUpdateDeviceInstanceRequestRequestTypeDef,
    _OptionalUpdateDeviceInstanceRequestRequestTypeDef,
):
    pass


_RequiredUpdateInstanceProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateInstanceProfileRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalUpdateInstanceProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateInstanceProfileRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "packageCleanup": bool,
        "excludeAppPackagesFromCleanup": Sequence[str],
        "rebootAfterUse": bool,
    },
    total=False,
)


class UpdateInstanceProfileRequestRequestTypeDef(
    _RequiredUpdateInstanceProfileRequestRequestTypeDef,
    _OptionalUpdateInstanceProfileRequestRequestTypeDef,
):
    pass


_RequiredUpdateNetworkProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateNetworkProfileRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalUpdateNetworkProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateNetworkProfileRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "type": NetworkProfileTypeType,
        "uplinkBandwidthBits": int,
        "downlinkBandwidthBits": int,
        "uplinkDelayMs": int,
        "downlinkDelayMs": int,
        "uplinkJitterMs": int,
        "downlinkJitterMs": int,
        "uplinkLossPercent": int,
        "downlinkLossPercent": int,
    },
    total=False,
)


class UpdateNetworkProfileRequestRequestTypeDef(
    _RequiredUpdateNetworkProfileRequestRequestTypeDef,
    _OptionalUpdateNetworkProfileRequestRequestTypeDef,
):
    pass


_RequiredUpdateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateProjectRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalUpdateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateProjectRequestRequestTypeDef",
    {
        "name": str,
        "defaultJobTimeoutMinutes": int,
    },
    total=False,
)


class UpdateProjectRequestRequestTypeDef(
    _RequiredUpdateProjectRequestRequestTypeDef, _OptionalUpdateProjectRequestRequestTypeDef
):
    pass


_RequiredUpdateUploadRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUploadRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalUpdateUploadRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUploadRequestRequestTypeDef",
    {
        "name": str,
        "contentType": str,
        "editContent": bool,
    },
    total=False,
)


class UpdateUploadRequestRequestTypeDef(
    _RequiredUpdateUploadRequestRequestTypeDef, _OptionalUpdateUploadRequestRequestTypeDef
):
    pass


_RequiredUpdateVPCEConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateVPCEConfigurationRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalUpdateVPCEConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateVPCEConfigurationRequestRequestTypeDef",
    {
        "vpceConfigurationName": str,
        "vpceServiceName": str,
        "serviceDnsName": str,
        "vpceConfigurationDescription": str,
    },
    total=False,
)


class UpdateVPCEConfigurationRequestRequestTypeDef(
    _RequiredUpdateVPCEConfigurationRequestRequestTypeDef,
    _OptionalUpdateVPCEConfigurationRequestRequestTypeDef,
):
    pass


AccountSettingsTypeDef = TypedDict(
    "AccountSettingsTypeDef",
    {
        "awsAccountNumber": str,
        "unmeteredDevices": Dict[DevicePlatformType, int],
        "unmeteredRemoteAccessDevices": Dict[DevicePlatformType, int],
        "maxJobTimeoutMinutes": int,
        "trialMinutes": TrialMinutesTypeDef,
        "maxSlots": Dict[str, int],
        "defaultJobTimeoutMinutes": int,
        "skipAppResign": bool,
    },
    total=False,
)

_RequiredCreateDevicePoolRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDevicePoolRequestRequestTypeDef",
    {
        "projectArn": str,
        "name": str,
        "rules": Sequence[RuleTypeDef],
    },
)
_OptionalCreateDevicePoolRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDevicePoolRequestRequestTypeDef",
    {
        "description": str,
        "maxDevices": int,
    },
    total=False,
)


class CreateDevicePoolRequestRequestTypeDef(
    _RequiredCreateDevicePoolRequestRequestTypeDef, _OptionalCreateDevicePoolRequestRequestTypeDef
):
    pass


DevicePoolTypeDef = TypedDict(
    "DevicePoolTypeDef",
    {
        "arn": str,
        "name": str,
        "description": str,
        "type": DevicePoolTypeType,
        "rules": List[RuleTypeDef],
        "maxDevices": int,
    },
    total=False,
)

_RequiredUpdateDevicePoolRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDevicePoolRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalUpdateDevicePoolRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDevicePoolRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "rules": Sequence[RuleTypeDef],
        "maxDevices": int,
        "clearMaxDevices": bool,
    },
    total=False,
)


class UpdateDevicePoolRequestRequestTypeDef(
    _RequiredUpdateDevicePoolRequestRequestTypeDef, _OptionalUpdateDevicePoolRequestRequestTypeDef
):
    pass


CreateTestGridUrlResultTypeDef = TypedDict(
    "CreateTestGridUrlResultTypeDef",
    {
        "url": str,
        "expires": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListArtifactsResultTypeDef = TypedDict(
    "ListArtifactsResultTypeDef",
    {
        "artifacts": List[ArtifactTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateInstanceProfileResultTypeDef = TypedDict(
    "CreateInstanceProfileResultTypeDef",
    {
        "instanceProfile": InstanceProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeviceInstanceTypeDef = TypedDict(
    "DeviceInstanceTypeDef",
    {
        "arn": str,
        "deviceArn": str,
        "labels": List[str],
        "status": InstanceStatusType,
        "udid": str,
        "instanceProfile": InstanceProfileTypeDef,
    },
    total=False,
)

GetInstanceProfileResultTypeDef = TypedDict(
    "GetInstanceProfileResultTypeDef",
    {
        "instanceProfile": InstanceProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInstanceProfilesResultTypeDef = TypedDict(
    "ListInstanceProfilesResultTypeDef",
    {
        "instanceProfiles": List[InstanceProfileTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateInstanceProfileResultTypeDef = TypedDict(
    "UpdateInstanceProfileResultTypeDef",
    {
        "instanceProfile": InstanceProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateNetworkProfileResultTypeDef = TypedDict(
    "CreateNetworkProfileResultTypeDef",
    {
        "networkProfile": NetworkProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetNetworkProfileResultTypeDef = TypedDict(
    "GetNetworkProfileResultTypeDef",
    {
        "networkProfile": NetworkProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListNetworkProfilesResultTypeDef = TypedDict(
    "ListNetworkProfilesResultTypeDef",
    {
        "networkProfiles": List[NetworkProfileTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateNetworkProfileResultTypeDef = TypedDict(
    "UpdateNetworkProfileResultTypeDef",
    {
        "networkProfile": NetworkProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProjectResultTypeDef = TypedDict(
    "CreateProjectResultTypeDef",
    {
        "project": ProjectTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetProjectResultTypeDef = TypedDict(
    "GetProjectResultTypeDef",
    {
        "project": ProjectTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProjectsResultTypeDef = TypedDict(
    "ListProjectsResultTypeDef",
    {
        "projects": List[ProjectTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateProjectResultTypeDef = TypedDict(
    "UpdateProjectResultTypeDef",
    {
        "project": ProjectTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateRemoteAccessSessionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRemoteAccessSessionRequestRequestTypeDef",
    {
        "projectArn": str,
        "deviceArn": str,
    },
)
_OptionalCreateRemoteAccessSessionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRemoteAccessSessionRequestRequestTypeDef",
    {
        "instanceArn": str,
        "sshPublicKey": str,
        "remoteDebugEnabled": bool,
        "remoteRecordEnabled": bool,
        "remoteRecordAppArn": str,
        "name": str,
        "clientId": str,
        "configuration": CreateRemoteAccessSessionConfigurationTypeDef,
        "interactionMode": InteractionModeType,
        "skipAppResign": bool,
    },
    total=False,
)


class CreateRemoteAccessSessionRequestRequestTypeDef(
    _RequiredCreateRemoteAccessSessionRequestRequestTypeDef,
    _OptionalCreateRemoteAccessSessionRequestRequestTypeDef,
):
    pass


_RequiredCreateTestGridProjectRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTestGridProjectRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateTestGridProjectRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTestGridProjectRequestRequestTypeDef",
    {
        "description": str,
        "vpcConfig": TestGridVpcConfigTypeDef,
    },
    total=False,
)


class CreateTestGridProjectRequestRequestTypeDef(
    _RequiredCreateTestGridProjectRequestRequestTypeDef,
    _OptionalCreateTestGridProjectRequestRequestTypeDef,
):
    pass


TestGridProjectTypeDef = TypedDict(
    "TestGridProjectTypeDef",
    {
        "arn": str,
        "name": str,
        "description": str,
        "vpcConfig": TestGridVpcConfigTypeDef,
        "created": datetime,
    },
    total=False,
)

_RequiredUpdateTestGridProjectRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTestGridProjectRequestRequestTypeDef",
    {
        "projectArn": str,
    },
)
_OptionalUpdateTestGridProjectRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTestGridProjectRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "vpcConfig": TestGridVpcConfigTypeDef,
    },
    total=False,
)


class UpdateTestGridProjectRequestRequestTypeDef(
    _RequiredUpdateTestGridProjectRequestRequestTypeDef,
    _OptionalUpdateTestGridProjectRequestRequestTypeDef,
):
    pass


CreateUploadResultTypeDef = TypedDict(
    "CreateUploadResultTypeDef",
    {
        "upload": UploadTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetUploadResultTypeDef = TypedDict(
    "GetUploadResultTypeDef",
    {
        "upload": UploadTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstallToRemoteAccessSessionResultTypeDef = TypedDict(
    "InstallToRemoteAccessSessionResultTypeDef",
    {
        "appUpload": UploadTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUploadsResultTypeDef = TypedDict(
    "ListUploadsResultTypeDef",
    {
        "uploads": List[UploadTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateUploadResultTypeDef = TypedDict(
    "UpdateUploadResultTypeDef",
    {
        "upload": UploadTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVPCEConfigurationResultTypeDef = TypedDict(
    "CreateVPCEConfigurationResultTypeDef",
    {
        "vpceConfiguration": VPCEConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetVPCEConfigurationResultTypeDef = TypedDict(
    "GetVPCEConfigurationResultTypeDef",
    {
        "vpceConfiguration": VPCEConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVPCEConfigurationsResultTypeDef = TypedDict(
    "ListVPCEConfigurationsResultTypeDef",
    {
        "vpceConfigurations": List[VPCEConfigurationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVPCEConfigurationResultTypeDef = TypedDict(
    "UpdateVPCEConfigurationResultTypeDef",
    {
        "vpceConfiguration": VPCEConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeviceSelectionConfigurationTypeDef = TypedDict(
    "DeviceSelectionConfigurationTypeDef",
    {
        "filters": Sequence[DeviceFilterTypeDef],
        "maxDevices": int,
    },
)

DeviceSelectionResultTypeDef = TypedDict(
    "DeviceSelectionResultTypeDef",
    {
        "filters": List[DeviceFilterTypeDef],
        "matchedDevicesCount": int,
        "maxDevices": int,
    },
    total=False,
)

ListDevicesRequestRequestTypeDef = TypedDict(
    "ListDevicesRequestRequestTypeDef",
    {
        "arn": str,
        "nextToken": str,
        "filters": Sequence[DeviceFilterTypeDef],
    },
    total=False,
)

SuiteTypeDef = TypedDict(
    "SuiteTypeDef",
    {
        "arn": str,
        "name": str,
        "type": TestTypeType,
        "created": datetime,
        "status": ExecutionStatusType,
        "result": ExecutionResultType,
        "started": datetime,
        "stopped": datetime,
        "counters": CountersTypeDef,
        "message": str,
        "deviceMinutes": DeviceMinutesTypeDef,
    },
    total=False,
)

TestTypeDef = TypedDict(
    "TestTypeDef",
    {
        "arn": str,
        "name": str,
        "type": TestTypeType,
        "created": datetime,
        "status": ExecutionStatusType,
        "result": ExecutionResultType,
        "started": datetime,
        "stopped": datetime,
        "counters": CountersTypeDef,
        "message": str,
        "deviceMinutes": DeviceMinutesTypeDef,
    },
    total=False,
)

GetOfferingStatusRequestGetOfferingStatusPaginateTypeDef = TypedDict(
    "GetOfferingStatusRequestGetOfferingStatusPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListArtifactsRequestListArtifactsPaginateTypeDef = TypedDict(
    "_RequiredListArtifactsRequestListArtifactsPaginateTypeDef",
    {
        "arn": str,
        "type": ArtifactCategoryType,
    },
)
_OptionalListArtifactsRequestListArtifactsPaginateTypeDef = TypedDict(
    "_OptionalListArtifactsRequestListArtifactsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListArtifactsRequestListArtifactsPaginateTypeDef(
    _RequiredListArtifactsRequestListArtifactsPaginateTypeDef,
    _OptionalListArtifactsRequestListArtifactsPaginateTypeDef,
):
    pass


ListDeviceInstancesRequestListDeviceInstancesPaginateTypeDef = TypedDict(
    "ListDeviceInstancesRequestListDeviceInstancesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListDevicePoolsRequestListDevicePoolsPaginateTypeDef = TypedDict(
    "_RequiredListDevicePoolsRequestListDevicePoolsPaginateTypeDef",
    {
        "arn": str,
    },
)
_OptionalListDevicePoolsRequestListDevicePoolsPaginateTypeDef = TypedDict(
    "_OptionalListDevicePoolsRequestListDevicePoolsPaginateTypeDef",
    {
        "type": DevicePoolTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDevicePoolsRequestListDevicePoolsPaginateTypeDef(
    _RequiredListDevicePoolsRequestListDevicePoolsPaginateTypeDef,
    _OptionalListDevicePoolsRequestListDevicePoolsPaginateTypeDef,
):
    pass


ListDevicesRequestListDevicesPaginateTypeDef = TypedDict(
    "ListDevicesRequestListDevicesPaginateTypeDef",
    {
        "arn": str,
        "filters": Sequence[DeviceFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListInstanceProfilesRequestListInstanceProfilesPaginateTypeDef = TypedDict(
    "ListInstanceProfilesRequestListInstanceProfilesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "_RequiredListJobsRequestListJobsPaginateTypeDef",
    {
        "arn": str,
    },
)
_OptionalListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "_OptionalListJobsRequestListJobsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListJobsRequestListJobsPaginateTypeDef(
    _RequiredListJobsRequestListJobsPaginateTypeDef, _OptionalListJobsRequestListJobsPaginateTypeDef
):
    pass


_RequiredListNetworkProfilesRequestListNetworkProfilesPaginateTypeDef = TypedDict(
    "_RequiredListNetworkProfilesRequestListNetworkProfilesPaginateTypeDef",
    {
        "arn": str,
    },
)
_OptionalListNetworkProfilesRequestListNetworkProfilesPaginateTypeDef = TypedDict(
    "_OptionalListNetworkProfilesRequestListNetworkProfilesPaginateTypeDef",
    {
        "type": NetworkProfileTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListNetworkProfilesRequestListNetworkProfilesPaginateTypeDef(
    _RequiredListNetworkProfilesRequestListNetworkProfilesPaginateTypeDef,
    _OptionalListNetworkProfilesRequestListNetworkProfilesPaginateTypeDef,
):
    pass


ListOfferingPromotionsRequestListOfferingPromotionsPaginateTypeDef = TypedDict(
    "ListOfferingPromotionsRequestListOfferingPromotionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOfferingTransactionsRequestListOfferingTransactionsPaginateTypeDef = TypedDict(
    "ListOfferingTransactionsRequestListOfferingTransactionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOfferingsRequestListOfferingsPaginateTypeDef = TypedDict(
    "ListOfferingsRequestListOfferingsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "ListProjectsRequestListProjectsPaginateTypeDef",
    {
        "arn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListRemoteAccessSessionsRequestListRemoteAccessSessionsPaginateTypeDef = TypedDict(
    "_RequiredListRemoteAccessSessionsRequestListRemoteAccessSessionsPaginateTypeDef",
    {
        "arn": str,
    },
)
_OptionalListRemoteAccessSessionsRequestListRemoteAccessSessionsPaginateTypeDef = TypedDict(
    "_OptionalListRemoteAccessSessionsRequestListRemoteAccessSessionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListRemoteAccessSessionsRequestListRemoteAccessSessionsPaginateTypeDef(
    _RequiredListRemoteAccessSessionsRequestListRemoteAccessSessionsPaginateTypeDef,
    _OptionalListRemoteAccessSessionsRequestListRemoteAccessSessionsPaginateTypeDef,
):
    pass


_RequiredListRunsRequestListRunsPaginateTypeDef = TypedDict(
    "_RequiredListRunsRequestListRunsPaginateTypeDef",
    {
        "arn": str,
    },
)
_OptionalListRunsRequestListRunsPaginateTypeDef = TypedDict(
    "_OptionalListRunsRequestListRunsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListRunsRequestListRunsPaginateTypeDef(
    _RequiredListRunsRequestListRunsPaginateTypeDef, _OptionalListRunsRequestListRunsPaginateTypeDef
):
    pass


_RequiredListSamplesRequestListSamplesPaginateTypeDef = TypedDict(
    "_RequiredListSamplesRequestListSamplesPaginateTypeDef",
    {
        "arn": str,
    },
)
_OptionalListSamplesRequestListSamplesPaginateTypeDef = TypedDict(
    "_OptionalListSamplesRequestListSamplesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSamplesRequestListSamplesPaginateTypeDef(
    _RequiredListSamplesRequestListSamplesPaginateTypeDef,
    _OptionalListSamplesRequestListSamplesPaginateTypeDef,
):
    pass


_RequiredListSuitesRequestListSuitesPaginateTypeDef = TypedDict(
    "_RequiredListSuitesRequestListSuitesPaginateTypeDef",
    {
        "arn": str,
    },
)
_OptionalListSuitesRequestListSuitesPaginateTypeDef = TypedDict(
    "_OptionalListSuitesRequestListSuitesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSuitesRequestListSuitesPaginateTypeDef(
    _RequiredListSuitesRequestListSuitesPaginateTypeDef,
    _OptionalListSuitesRequestListSuitesPaginateTypeDef,
):
    pass


_RequiredListTestsRequestListTestsPaginateTypeDef = TypedDict(
    "_RequiredListTestsRequestListTestsPaginateTypeDef",
    {
        "arn": str,
    },
)
_OptionalListTestsRequestListTestsPaginateTypeDef = TypedDict(
    "_OptionalListTestsRequestListTestsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTestsRequestListTestsPaginateTypeDef(
    _RequiredListTestsRequestListTestsPaginateTypeDef,
    _OptionalListTestsRequestListTestsPaginateTypeDef,
):
    pass


_RequiredListUniqueProblemsRequestListUniqueProblemsPaginateTypeDef = TypedDict(
    "_RequiredListUniqueProblemsRequestListUniqueProblemsPaginateTypeDef",
    {
        "arn": str,
    },
)
_OptionalListUniqueProblemsRequestListUniqueProblemsPaginateTypeDef = TypedDict(
    "_OptionalListUniqueProblemsRequestListUniqueProblemsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListUniqueProblemsRequestListUniqueProblemsPaginateTypeDef(
    _RequiredListUniqueProblemsRequestListUniqueProblemsPaginateTypeDef,
    _OptionalListUniqueProblemsRequestListUniqueProblemsPaginateTypeDef,
):
    pass


_RequiredListUploadsRequestListUploadsPaginateTypeDef = TypedDict(
    "_RequiredListUploadsRequestListUploadsPaginateTypeDef",
    {
        "arn": str,
    },
)
_OptionalListUploadsRequestListUploadsPaginateTypeDef = TypedDict(
    "_OptionalListUploadsRequestListUploadsPaginateTypeDef",
    {
        "type": UploadTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListUploadsRequestListUploadsPaginateTypeDef(
    _RequiredListUploadsRequestListUploadsPaginateTypeDef,
    _OptionalListUploadsRequestListUploadsPaginateTypeDef,
):
    pass


ListVPCEConfigurationsRequestListVPCEConfigurationsPaginateTypeDef = TypedDict(
    "ListVPCEConfigurationsRequestListVPCEConfigurationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetTestGridSessionResultTypeDef = TypedDict(
    "GetTestGridSessionResultTypeDef",
    {
        "testGridSession": TestGridSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTestGridSessionsResultTypeDef = TypedDict(
    "ListTestGridSessionsResultTypeDef",
    {
        "testGridSessions": List[TestGridSessionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOfferingPromotionsResultTypeDef = TypedDict(
    "ListOfferingPromotionsResultTypeDef",
    {
        "offeringPromotions": List[OfferingPromotionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSamplesResultTypeDef = TypedDict(
    "ListSamplesResultTypeDef",
    {
        "samples": List[SampleTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

ListTestGridSessionActionsResultTypeDef = TypedDict(
    "ListTestGridSessionActionsResultTypeDef",
    {
        "actions": List[TestGridSessionActionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTestGridSessionArtifactsResultTypeDef = TypedDict(
    "ListTestGridSessionArtifactsResultTypeDef",
    {
        "artifacts": List[TestGridSessionArtifactTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RecurringChargeTypeDef = TypedDict(
    "RecurringChargeTypeDef",
    {
        "cost": MonetaryAmountTypeDef,
        "frequency": Literal["MONTHLY"],
    },
    total=False,
)

ScheduleRunConfigurationTypeDef = TypedDict(
    "ScheduleRunConfigurationTypeDef",
    {
        "extraDataPackageArn": str,
        "networkProfileArn": str,
        "locale": str,
        "location": LocationTypeDef,
        "vpceConfigurationArns": Sequence[str],
        "customerArtifactPaths": CustomerArtifactPathsTypeDef,
        "radios": RadiosTypeDef,
        "auxiliaryApps": Sequence[str],
        "billingMethod": BillingMethodType,
    },
    total=False,
)

GetAccountSettingsResultTypeDef = TypedDict(
    "GetAccountSettingsResultTypeDef",
    {
        "accountSettings": AccountSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDevicePoolResultTypeDef = TypedDict(
    "CreateDevicePoolResultTypeDef",
    {
        "devicePool": DevicePoolTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDevicePoolResultTypeDef = TypedDict(
    "GetDevicePoolResultTypeDef",
    {
        "devicePool": DevicePoolTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDevicePoolsResultTypeDef = TypedDict(
    "ListDevicePoolsResultTypeDef",
    {
        "devicePools": List[DevicePoolTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDevicePoolResultTypeDef = TypedDict(
    "UpdateDevicePoolResultTypeDef",
    {
        "devicePool": DevicePoolTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeviceTypeDef = TypedDict(
    "DeviceTypeDef",
    {
        "arn": str,
        "name": str,
        "manufacturer": str,
        "model": str,
        "modelId": str,
        "formFactor": DeviceFormFactorType,
        "platform": DevicePlatformType,
        "os": str,
        "cpu": CPUTypeDef,
        "resolution": ResolutionTypeDef,
        "heapSize": int,
        "memory": int,
        "image": str,
        "carrier": str,
        "radio": str,
        "remoteAccessEnabled": bool,
        "remoteDebugEnabled": bool,
        "fleetType": str,
        "fleetName": str,
        "instances": List[DeviceInstanceTypeDef],
        "availability": DeviceAvailabilityType,
    },
    total=False,
)

GetDeviceInstanceResultTypeDef = TypedDict(
    "GetDeviceInstanceResultTypeDef",
    {
        "deviceInstance": DeviceInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeviceInstancesResultTypeDef = TypedDict(
    "ListDeviceInstancesResultTypeDef",
    {
        "deviceInstances": List[DeviceInstanceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDeviceInstanceResultTypeDef = TypedDict(
    "UpdateDeviceInstanceResultTypeDef",
    {
        "deviceInstance": DeviceInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTestGridProjectResultTypeDef = TypedDict(
    "CreateTestGridProjectResultTypeDef",
    {
        "testGridProject": TestGridProjectTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTestGridProjectResultTypeDef = TypedDict(
    "GetTestGridProjectResultTypeDef",
    {
        "testGridProject": TestGridProjectTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTestGridProjectsResultTypeDef = TypedDict(
    "ListTestGridProjectsResultTypeDef",
    {
        "testGridProjects": List[TestGridProjectTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTestGridProjectResultTypeDef = TypedDict(
    "UpdateTestGridProjectResultTypeDef",
    {
        "testGridProject": TestGridProjectTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RunTypeDef = TypedDict(
    "RunTypeDef",
    {
        "arn": str,
        "name": str,
        "type": TestTypeType,
        "platform": DevicePlatformType,
        "created": datetime,
        "status": ExecutionStatusType,
        "result": ExecutionResultType,
        "started": datetime,
        "stopped": datetime,
        "counters": CountersTypeDef,
        "message": str,
        "totalJobs": int,
        "completedJobs": int,
        "billingMethod": BillingMethodType,
        "deviceMinutes": DeviceMinutesTypeDef,
        "networkProfile": NetworkProfileTypeDef,
        "parsingResultUrl": str,
        "resultCode": ExecutionResultCodeType,
        "seed": int,
        "appUpload": str,
        "eventCount": int,
        "jobTimeoutMinutes": int,
        "devicePoolArn": str,
        "locale": str,
        "radios": RadiosTypeDef,
        "location": LocationTypeDef,
        "customerArtifactPaths": CustomerArtifactPathsTypeDef,
        "webUrl": str,
        "skipAppResign": bool,
        "testSpecArn": str,
        "deviceSelectionResult": DeviceSelectionResultTypeDef,
    },
    total=False,
)

GetSuiteResultTypeDef = TypedDict(
    "GetSuiteResultTypeDef",
    {
        "suite": SuiteTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSuitesResultTypeDef = TypedDict(
    "ListSuitesResultTypeDef",
    {
        "suites": List[SuiteTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTestResultTypeDef = TypedDict(
    "GetTestResultTypeDef",
    {
        "test": TestTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTestsResultTypeDef = TypedDict(
    "ListTestsResultTypeDef",
    {
        "tests": List[TestTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OfferingTypeDef = TypedDict(
    "OfferingTypeDef",
    {
        "id": str,
        "description": str,
        "type": Literal["RECURRING"],
        "platform": DevicePlatformType,
        "recurringCharges": List[RecurringChargeTypeDef],
    },
    total=False,
)

_RequiredGetDevicePoolCompatibilityRequestRequestTypeDef = TypedDict(
    "_RequiredGetDevicePoolCompatibilityRequestRequestTypeDef",
    {
        "devicePoolArn": str,
    },
)
_OptionalGetDevicePoolCompatibilityRequestRequestTypeDef = TypedDict(
    "_OptionalGetDevicePoolCompatibilityRequestRequestTypeDef",
    {
        "appArn": str,
        "testType": TestTypeType,
        "test": ScheduleRunTestTypeDef,
        "configuration": ScheduleRunConfigurationTypeDef,
    },
    total=False,
)


class GetDevicePoolCompatibilityRequestRequestTypeDef(
    _RequiredGetDevicePoolCompatibilityRequestRequestTypeDef,
    _OptionalGetDevicePoolCompatibilityRequestRequestTypeDef,
):
    pass


_RequiredScheduleRunRequestRequestTypeDef = TypedDict(
    "_RequiredScheduleRunRequestRequestTypeDef",
    {
        "projectArn": str,
        "test": ScheduleRunTestTypeDef,
    },
)
_OptionalScheduleRunRequestRequestTypeDef = TypedDict(
    "_OptionalScheduleRunRequestRequestTypeDef",
    {
        "appArn": str,
        "devicePoolArn": str,
        "deviceSelectionConfiguration": DeviceSelectionConfigurationTypeDef,
        "name": str,
        "configuration": ScheduleRunConfigurationTypeDef,
        "executionConfiguration": ExecutionConfigurationTypeDef,
    },
    total=False,
)


class ScheduleRunRequestRequestTypeDef(
    _RequiredScheduleRunRequestRequestTypeDef, _OptionalScheduleRunRequestRequestTypeDef
):
    pass


DevicePoolCompatibilityResultTypeDef = TypedDict(
    "DevicePoolCompatibilityResultTypeDef",
    {
        "device": DeviceTypeDef,
        "compatible": bool,
        "incompatibilityMessages": List[IncompatibilityMessageTypeDef],
    },
    total=False,
)

GetDeviceResultTypeDef = TypedDict(
    "GetDeviceResultTypeDef",
    {
        "device": DeviceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "arn": str,
        "name": str,
        "type": TestTypeType,
        "created": datetime,
        "status": ExecutionStatusType,
        "result": ExecutionResultType,
        "started": datetime,
        "stopped": datetime,
        "counters": CountersTypeDef,
        "message": str,
        "device": DeviceTypeDef,
        "instanceArn": str,
        "deviceMinutes": DeviceMinutesTypeDef,
        "videoEndpoint": str,
        "videoCapture": bool,
    },
    total=False,
)

ListDevicesResultTypeDef = TypedDict(
    "ListDevicesResultTypeDef",
    {
        "devices": List[DeviceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProblemTypeDef = TypedDict(
    "ProblemTypeDef",
    {
        "run": ProblemDetailTypeDef,
        "job": ProblemDetailTypeDef,
        "suite": ProblemDetailTypeDef,
        "test": ProblemDetailTypeDef,
        "device": DeviceTypeDef,
        "result": ExecutionResultType,
        "message": str,
    },
    total=False,
)

RemoteAccessSessionTypeDef = TypedDict(
    "RemoteAccessSessionTypeDef",
    {
        "arn": str,
        "name": str,
        "created": datetime,
        "status": ExecutionStatusType,
        "result": ExecutionResultType,
        "message": str,
        "started": datetime,
        "stopped": datetime,
        "device": DeviceTypeDef,
        "instanceArn": str,
        "remoteDebugEnabled": bool,
        "remoteRecordEnabled": bool,
        "remoteRecordAppArn": str,
        "hostAddress": str,
        "clientId": str,
        "billingMethod": BillingMethodType,
        "deviceMinutes": DeviceMinutesTypeDef,
        "endpoint": str,
        "deviceUdid": str,
        "interactionMode": InteractionModeType,
        "skipAppResign": bool,
    },
    total=False,
)

GetRunResultTypeDef = TypedDict(
    "GetRunResultTypeDef",
    {
        "run": RunTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRunsResultTypeDef = TypedDict(
    "ListRunsResultTypeDef",
    {
        "runs": List[RunTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ScheduleRunResultTypeDef = TypedDict(
    "ScheduleRunResultTypeDef",
    {
        "run": RunTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopRunResultTypeDef = TypedDict(
    "StopRunResultTypeDef",
    {
        "run": RunTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOfferingsResultTypeDef = TypedDict(
    "ListOfferingsResultTypeDef",
    {
        "offerings": List[OfferingTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OfferingStatusTypeDef = TypedDict(
    "OfferingStatusTypeDef",
    {
        "type": OfferingTransactionTypeType,
        "offering": OfferingTypeDef,
        "quantity": int,
        "effectiveOn": datetime,
    },
    total=False,
)

GetDevicePoolCompatibilityResultTypeDef = TypedDict(
    "GetDevicePoolCompatibilityResultTypeDef",
    {
        "compatibleDevices": List[DevicePoolCompatibilityResultTypeDef],
        "incompatibleDevices": List[DevicePoolCompatibilityResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobResultTypeDef = TypedDict(
    "GetJobResultTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobsResultTypeDef = TypedDict(
    "ListJobsResultTypeDef",
    {
        "jobs": List[JobTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopJobResultTypeDef = TypedDict(
    "StopJobResultTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UniqueProblemTypeDef = TypedDict(
    "UniqueProblemTypeDef",
    {
        "message": str,
        "problems": List[ProblemTypeDef],
    },
    total=False,
)

CreateRemoteAccessSessionResultTypeDef = TypedDict(
    "CreateRemoteAccessSessionResultTypeDef",
    {
        "remoteAccessSession": RemoteAccessSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRemoteAccessSessionResultTypeDef = TypedDict(
    "GetRemoteAccessSessionResultTypeDef",
    {
        "remoteAccessSession": RemoteAccessSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRemoteAccessSessionsResultTypeDef = TypedDict(
    "ListRemoteAccessSessionsResultTypeDef",
    {
        "remoteAccessSessions": List[RemoteAccessSessionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopRemoteAccessSessionResultTypeDef = TypedDict(
    "StopRemoteAccessSessionResultTypeDef",
    {
        "remoteAccessSession": RemoteAccessSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetOfferingStatusResultTypeDef = TypedDict(
    "GetOfferingStatusResultTypeDef",
    {
        "current": Dict[str, OfferingStatusTypeDef],
        "nextPeriod": Dict[str, OfferingStatusTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OfferingTransactionTypeDef = TypedDict(
    "OfferingTransactionTypeDef",
    {
        "offeringStatus": OfferingStatusTypeDef,
        "transactionId": str,
        "offeringPromotionId": str,
        "createdOn": datetime,
        "cost": MonetaryAmountTypeDef,
    },
    total=False,
)

ListUniqueProblemsResultTypeDef = TypedDict(
    "ListUniqueProblemsResultTypeDef",
    {
        "uniqueProblems": Dict[ExecutionResultType, List[UniqueProblemTypeDef]],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOfferingTransactionsResultTypeDef = TypedDict(
    "ListOfferingTransactionsResultTypeDef",
    {
        "offeringTransactions": List[OfferingTransactionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PurchaseOfferingResultTypeDef = TypedDict(
    "PurchaseOfferingResultTypeDef",
    {
        "offeringTransaction": OfferingTransactionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RenewOfferingResultTypeDef = TypedDict(
    "RenewOfferingResultTypeDef",
    {
        "offeringTransaction": OfferingTransactionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
