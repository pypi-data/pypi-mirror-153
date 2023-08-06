"""
Type annotations for network-firewall service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_network_firewall/type_defs/)

Usage::

    ```python
    from mypy_boto3_network_firewall.type_defs import AddressTypeDef

    data: AddressTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AttachmentStatusType,
    ConfigurationSyncStateType,
    EncryptionTypeType,
    FirewallStatusValueType,
    GeneratedRulesTypeType,
    LogDestinationTypeType,
    LogTypeType,
    PerObjectSyncStatusType,
    ResourceManagedStatusType,
    ResourceManagedTypeType,
    ResourceStatusType,
    RuleGroupTypeType,
    RuleOrderType,
    StatefulActionType,
    StatefulRuleDirectionType,
    StatefulRuleProtocolType,
    TargetTypeType,
    TCPFlagType,
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
    "AddressTypeDef",
    "AssociateFirewallPolicyRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "SubnetMappingTypeDef",
    "AttachmentTypeDef",
    "EncryptionConfigurationTypeDef",
    "TagTypeDef",
    "SourceMetadataTypeDef",
    "DeleteFirewallPolicyRequestRequestTypeDef",
    "DeleteFirewallRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteRuleGroupRequestRequestTypeDef",
    "DescribeFirewallPolicyRequestRequestTypeDef",
    "DescribeFirewallRequestRequestTypeDef",
    "DescribeLoggingConfigurationRequestRequestTypeDef",
    "DescribeResourcePolicyRequestRequestTypeDef",
    "DescribeRuleGroupMetadataRequestRequestTypeDef",
    "StatefulRuleOptionsTypeDef",
    "DescribeRuleGroupRequestRequestTypeDef",
    "DimensionTypeDef",
    "DisassociateSubnetsRequestRequestTypeDef",
    "FirewallMetadataTypeDef",
    "FirewallPolicyMetadataTypeDef",
    "StatefulEngineOptionsTypeDef",
    "StatelessRuleGroupReferenceTypeDef",
    "HeaderTypeDef",
    "IPSetTypeDef",
    "PaginatorConfigTypeDef",
    "ListFirewallPoliciesRequestRequestTypeDef",
    "ListFirewallsRequestRequestTypeDef",
    "ListRuleGroupsRequestRequestTypeDef",
    "RuleGroupMetadataTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "LogDestinationConfigTypeDef",
    "PortRangeTypeDef",
    "TCPFlagFieldTypeDef",
    "PerObjectStatusTypeDef",
    "PortSetTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "RuleOptionTypeDef",
    "RulesSourceListTypeDef",
    "StatefulRuleGroupOverrideTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFirewallDeleteProtectionRequestRequestTypeDef",
    "UpdateFirewallDescriptionRequestRequestTypeDef",
    "UpdateFirewallPolicyChangeProtectionRequestRequestTypeDef",
    "UpdateSubnetChangeProtectionRequestRequestTypeDef",
    "AssociateFirewallPolicyResponseTypeDef",
    "DescribeResourcePolicyResponseTypeDef",
    "UpdateFirewallDeleteProtectionResponseTypeDef",
    "UpdateFirewallDescriptionResponseTypeDef",
    "UpdateFirewallPolicyChangeProtectionResponseTypeDef",
    "UpdateSubnetChangeProtectionResponseTypeDef",
    "AssociateSubnetsRequestRequestTypeDef",
    "AssociateSubnetsResponseTypeDef",
    "DisassociateSubnetsResponseTypeDef",
    "UpdateFirewallEncryptionConfigurationRequestRequestTypeDef",
    "UpdateFirewallEncryptionConfigurationResponseTypeDef",
    "CreateFirewallRequestRequestTypeDef",
    "FirewallPolicyResponseTypeDef",
    "FirewallTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "RuleGroupResponseTypeDef",
    "DescribeRuleGroupMetadataResponseTypeDef",
    "PublishMetricActionTypeDef",
    "ListFirewallsResponseTypeDef",
    "ListFirewallPoliciesResponseTypeDef",
    "ListFirewallPoliciesRequestListFirewallPoliciesPaginateTypeDef",
    "ListFirewallsRequestListFirewallsPaginateTypeDef",
    "ListRuleGroupsRequestListRuleGroupsPaginateTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListRuleGroupsResponseTypeDef",
    "LoggingConfigurationTypeDef",
    "MatchAttributesTypeDef",
    "SyncStateTypeDef",
    "RuleVariablesTypeDef",
    "StatefulRuleTypeDef",
    "StatefulRuleGroupReferenceTypeDef",
    "CreateFirewallPolicyResponseTypeDef",
    "DeleteFirewallPolicyResponseTypeDef",
    "UpdateFirewallPolicyResponseTypeDef",
    "CreateRuleGroupResponseTypeDef",
    "DeleteRuleGroupResponseTypeDef",
    "UpdateRuleGroupResponseTypeDef",
    "ActionDefinitionTypeDef",
    "DescribeLoggingConfigurationResponseTypeDef",
    "UpdateLoggingConfigurationRequestRequestTypeDef",
    "UpdateLoggingConfigurationResponseTypeDef",
    "RuleDefinitionTypeDef",
    "FirewallStatusTypeDef",
    "CustomActionTypeDef",
    "StatelessRuleTypeDef",
    "CreateFirewallResponseTypeDef",
    "DeleteFirewallResponseTypeDef",
    "DescribeFirewallResponseTypeDef",
    "FirewallPolicyTypeDef",
    "StatelessRulesAndCustomActionsTypeDef",
    "CreateFirewallPolicyRequestRequestTypeDef",
    "DescribeFirewallPolicyResponseTypeDef",
    "UpdateFirewallPolicyRequestRequestTypeDef",
    "RulesSourceTypeDef",
    "RuleGroupTypeDef",
    "CreateRuleGroupRequestRequestTypeDef",
    "DescribeRuleGroupResponseTypeDef",
    "UpdateRuleGroupRequestRequestTypeDef",
)

AddressTypeDef = TypedDict(
    "AddressTypeDef",
    {
        "AddressDefinition": str,
    },
)

_RequiredAssociateFirewallPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateFirewallPolicyRequestRequestTypeDef",
    {
        "FirewallPolicyArn": str,
    },
)
_OptionalAssociateFirewallPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateFirewallPolicyRequestRequestTypeDef",
    {
        "UpdateToken": str,
        "FirewallArn": str,
        "FirewallName": str,
    },
    total=False,
)


class AssociateFirewallPolicyRequestRequestTypeDef(
    _RequiredAssociateFirewallPolicyRequestRequestTypeDef,
    _OptionalAssociateFirewallPolicyRequestRequestTypeDef,
):
    pass


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

SubnetMappingTypeDef = TypedDict(
    "SubnetMappingTypeDef",
    {
        "SubnetId": str,
    },
)

AttachmentTypeDef = TypedDict(
    "AttachmentTypeDef",
    {
        "SubnetId": str,
        "EndpointId": str,
        "Status": AttachmentStatusType,
    },
    total=False,
)

_RequiredEncryptionConfigurationTypeDef = TypedDict(
    "_RequiredEncryptionConfigurationTypeDef",
    {
        "Type": EncryptionTypeType,
    },
)
_OptionalEncryptionConfigurationTypeDef = TypedDict(
    "_OptionalEncryptionConfigurationTypeDef",
    {
        "KeyId": str,
    },
    total=False,
)


class EncryptionConfigurationTypeDef(
    _RequiredEncryptionConfigurationTypeDef, _OptionalEncryptionConfigurationTypeDef
):
    pass


TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

SourceMetadataTypeDef = TypedDict(
    "SourceMetadataTypeDef",
    {
        "SourceArn": str,
        "SourceUpdateToken": str,
    },
    total=False,
)

DeleteFirewallPolicyRequestRequestTypeDef = TypedDict(
    "DeleteFirewallPolicyRequestRequestTypeDef",
    {
        "FirewallPolicyName": str,
        "FirewallPolicyArn": str,
    },
    total=False,
)

DeleteFirewallRequestRequestTypeDef = TypedDict(
    "DeleteFirewallRequestRequestTypeDef",
    {
        "FirewallName": str,
        "FirewallArn": str,
    },
    total=False,
)

DeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "DeleteResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DeleteRuleGroupRequestRequestTypeDef = TypedDict(
    "DeleteRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupName": str,
        "RuleGroupArn": str,
        "Type": RuleGroupTypeType,
    },
    total=False,
)

DescribeFirewallPolicyRequestRequestTypeDef = TypedDict(
    "DescribeFirewallPolicyRequestRequestTypeDef",
    {
        "FirewallPolicyName": str,
        "FirewallPolicyArn": str,
    },
    total=False,
)

DescribeFirewallRequestRequestTypeDef = TypedDict(
    "DescribeFirewallRequestRequestTypeDef",
    {
        "FirewallName": str,
        "FirewallArn": str,
    },
    total=False,
)

DescribeLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeLoggingConfigurationRequestRequestTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
    },
    total=False,
)

DescribeResourcePolicyRequestRequestTypeDef = TypedDict(
    "DescribeResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DescribeRuleGroupMetadataRequestRequestTypeDef = TypedDict(
    "DescribeRuleGroupMetadataRequestRequestTypeDef",
    {
        "RuleGroupName": str,
        "RuleGroupArn": str,
        "Type": RuleGroupTypeType,
    },
    total=False,
)

StatefulRuleOptionsTypeDef = TypedDict(
    "StatefulRuleOptionsTypeDef",
    {
        "RuleOrder": RuleOrderType,
    },
    total=False,
)

DescribeRuleGroupRequestRequestTypeDef = TypedDict(
    "DescribeRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupName": str,
        "RuleGroupArn": str,
        "Type": RuleGroupTypeType,
    },
    total=False,
)

DimensionTypeDef = TypedDict(
    "DimensionTypeDef",
    {
        "Value": str,
    },
)

_RequiredDisassociateSubnetsRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateSubnetsRequestRequestTypeDef",
    {
        "SubnetIds": Sequence[str],
    },
)
_OptionalDisassociateSubnetsRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateSubnetsRequestRequestTypeDef",
    {
        "UpdateToken": str,
        "FirewallArn": str,
        "FirewallName": str,
    },
    total=False,
)


class DisassociateSubnetsRequestRequestTypeDef(
    _RequiredDisassociateSubnetsRequestRequestTypeDef,
    _OptionalDisassociateSubnetsRequestRequestTypeDef,
):
    pass


FirewallMetadataTypeDef = TypedDict(
    "FirewallMetadataTypeDef",
    {
        "FirewallName": str,
        "FirewallArn": str,
    },
    total=False,
)

FirewallPolicyMetadataTypeDef = TypedDict(
    "FirewallPolicyMetadataTypeDef",
    {
        "Name": str,
        "Arn": str,
    },
    total=False,
)

StatefulEngineOptionsTypeDef = TypedDict(
    "StatefulEngineOptionsTypeDef",
    {
        "RuleOrder": RuleOrderType,
    },
    total=False,
)

StatelessRuleGroupReferenceTypeDef = TypedDict(
    "StatelessRuleGroupReferenceTypeDef",
    {
        "ResourceArn": str,
        "Priority": int,
    },
)

HeaderTypeDef = TypedDict(
    "HeaderTypeDef",
    {
        "Protocol": StatefulRuleProtocolType,
        "Source": str,
        "SourcePort": str,
        "Direction": StatefulRuleDirectionType,
        "Destination": str,
        "DestinationPort": str,
    },
)

IPSetTypeDef = TypedDict(
    "IPSetTypeDef",
    {
        "Definition": Sequence[str],
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

ListFirewallPoliciesRequestRequestTypeDef = TypedDict(
    "ListFirewallPoliciesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListFirewallsRequestRequestTypeDef = TypedDict(
    "ListFirewallsRequestRequestTypeDef",
    {
        "NextToken": str,
        "VpcIds": Sequence[str],
        "MaxResults": int,
    },
    total=False,
)

ListRuleGroupsRequestRequestTypeDef = TypedDict(
    "ListRuleGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Scope": ResourceManagedStatusType,
        "ManagedType": ResourceManagedTypeType,
        "Type": RuleGroupTypeType,
    },
    total=False,
)

RuleGroupMetadataTypeDef = TypedDict(
    "RuleGroupMetadataTypeDef",
    {
        "Name": str,
        "Arn": str,
    },
    total=False,
)

_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass


LogDestinationConfigTypeDef = TypedDict(
    "LogDestinationConfigTypeDef",
    {
        "LogType": LogTypeType,
        "LogDestinationType": LogDestinationTypeType,
        "LogDestination": Dict[str, str],
    },
)

PortRangeTypeDef = TypedDict(
    "PortRangeTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
    },
)

_RequiredTCPFlagFieldTypeDef = TypedDict(
    "_RequiredTCPFlagFieldTypeDef",
    {
        "Flags": Sequence[TCPFlagType],
    },
)
_OptionalTCPFlagFieldTypeDef = TypedDict(
    "_OptionalTCPFlagFieldTypeDef",
    {
        "Masks": Sequence[TCPFlagType],
    },
    total=False,
)


class TCPFlagFieldTypeDef(_RequiredTCPFlagFieldTypeDef, _OptionalTCPFlagFieldTypeDef):
    pass


PerObjectStatusTypeDef = TypedDict(
    "PerObjectStatusTypeDef",
    {
        "SyncStatus": PerObjectSyncStatusType,
        "UpdateToken": str,
    },
    total=False,
)

PortSetTypeDef = TypedDict(
    "PortSetTypeDef",
    {
        "Definition": Sequence[str],
    },
    total=False,
)

PutResourcePolicyRequestRequestTypeDef = TypedDict(
    "PutResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Policy": str,
    },
)

_RequiredRuleOptionTypeDef = TypedDict(
    "_RequiredRuleOptionTypeDef",
    {
        "Keyword": str,
    },
)
_OptionalRuleOptionTypeDef = TypedDict(
    "_OptionalRuleOptionTypeDef",
    {
        "Settings": Sequence[str],
    },
    total=False,
)


class RuleOptionTypeDef(_RequiredRuleOptionTypeDef, _OptionalRuleOptionTypeDef):
    pass


RulesSourceListTypeDef = TypedDict(
    "RulesSourceListTypeDef",
    {
        "Targets": Sequence[str],
        "TargetTypes": Sequence[TargetTypeType],
        "GeneratedRulesType": GeneratedRulesTypeType,
    },
)

StatefulRuleGroupOverrideTypeDef = TypedDict(
    "StatefulRuleGroupOverrideTypeDef",
    {
        "Action": Literal["DROP_TO_ALERT"],
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateFirewallDeleteProtectionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFirewallDeleteProtectionRequestRequestTypeDef",
    {
        "DeleteProtection": bool,
    },
)
_OptionalUpdateFirewallDeleteProtectionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFirewallDeleteProtectionRequestRequestTypeDef",
    {
        "UpdateToken": str,
        "FirewallArn": str,
        "FirewallName": str,
    },
    total=False,
)


class UpdateFirewallDeleteProtectionRequestRequestTypeDef(
    _RequiredUpdateFirewallDeleteProtectionRequestRequestTypeDef,
    _OptionalUpdateFirewallDeleteProtectionRequestRequestTypeDef,
):
    pass


UpdateFirewallDescriptionRequestRequestTypeDef = TypedDict(
    "UpdateFirewallDescriptionRequestRequestTypeDef",
    {
        "UpdateToken": str,
        "FirewallArn": str,
        "FirewallName": str,
        "Description": str,
    },
    total=False,
)

_RequiredUpdateFirewallPolicyChangeProtectionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFirewallPolicyChangeProtectionRequestRequestTypeDef",
    {
        "FirewallPolicyChangeProtection": bool,
    },
)
_OptionalUpdateFirewallPolicyChangeProtectionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFirewallPolicyChangeProtectionRequestRequestTypeDef",
    {
        "UpdateToken": str,
        "FirewallArn": str,
        "FirewallName": str,
    },
    total=False,
)


class UpdateFirewallPolicyChangeProtectionRequestRequestTypeDef(
    _RequiredUpdateFirewallPolicyChangeProtectionRequestRequestTypeDef,
    _OptionalUpdateFirewallPolicyChangeProtectionRequestRequestTypeDef,
):
    pass


_RequiredUpdateSubnetChangeProtectionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSubnetChangeProtectionRequestRequestTypeDef",
    {
        "SubnetChangeProtection": bool,
    },
)
_OptionalUpdateSubnetChangeProtectionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSubnetChangeProtectionRequestRequestTypeDef",
    {
        "UpdateToken": str,
        "FirewallArn": str,
        "FirewallName": str,
    },
    total=False,
)


class UpdateSubnetChangeProtectionRequestRequestTypeDef(
    _RequiredUpdateSubnetChangeProtectionRequestRequestTypeDef,
    _OptionalUpdateSubnetChangeProtectionRequestRequestTypeDef,
):
    pass


AssociateFirewallPolicyResponseTypeDef = TypedDict(
    "AssociateFirewallPolicyResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "FirewallPolicyArn": str,
        "UpdateToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeResourcePolicyResponseTypeDef = TypedDict(
    "DescribeResourcePolicyResponseTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallDeleteProtectionResponseTypeDef = TypedDict(
    "UpdateFirewallDeleteProtectionResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "DeleteProtection": bool,
        "UpdateToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallDescriptionResponseTypeDef = TypedDict(
    "UpdateFirewallDescriptionResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "Description": str,
        "UpdateToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallPolicyChangeProtectionResponseTypeDef = TypedDict(
    "UpdateFirewallPolicyChangeProtectionResponseTypeDef",
    {
        "UpdateToken": str,
        "FirewallArn": str,
        "FirewallName": str,
        "FirewallPolicyChangeProtection": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSubnetChangeProtectionResponseTypeDef = TypedDict(
    "UpdateSubnetChangeProtectionResponseTypeDef",
    {
        "UpdateToken": str,
        "FirewallArn": str,
        "FirewallName": str,
        "SubnetChangeProtection": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAssociateSubnetsRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateSubnetsRequestRequestTypeDef",
    {
        "SubnetMappings": Sequence[SubnetMappingTypeDef],
    },
)
_OptionalAssociateSubnetsRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateSubnetsRequestRequestTypeDef",
    {
        "UpdateToken": str,
        "FirewallArn": str,
        "FirewallName": str,
    },
    total=False,
)


class AssociateSubnetsRequestRequestTypeDef(
    _RequiredAssociateSubnetsRequestRequestTypeDef, _OptionalAssociateSubnetsRequestRequestTypeDef
):
    pass


AssociateSubnetsResponseTypeDef = TypedDict(
    "AssociateSubnetsResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "SubnetMappings": List[SubnetMappingTypeDef],
        "UpdateToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateSubnetsResponseTypeDef = TypedDict(
    "DisassociateSubnetsResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "SubnetMappings": List[SubnetMappingTypeDef],
        "UpdateToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallEncryptionConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateFirewallEncryptionConfigurationRequestRequestTypeDef",
    {
        "UpdateToken": str,
        "FirewallArn": str,
        "FirewallName": str,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
    },
    total=False,
)

UpdateFirewallEncryptionConfigurationResponseTypeDef = TypedDict(
    "UpdateFirewallEncryptionConfigurationResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "UpdateToken": str,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateFirewallRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFirewallRequestRequestTypeDef",
    {
        "FirewallName": str,
        "FirewallPolicyArn": str,
        "VpcId": str,
        "SubnetMappings": Sequence[SubnetMappingTypeDef],
    },
)
_OptionalCreateFirewallRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFirewallRequestRequestTypeDef",
    {
        "DeleteProtection": bool,
        "SubnetChangeProtection": bool,
        "FirewallPolicyChangeProtection": bool,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
    },
    total=False,
)


class CreateFirewallRequestRequestTypeDef(
    _RequiredCreateFirewallRequestRequestTypeDef, _OptionalCreateFirewallRequestRequestTypeDef
):
    pass


_RequiredFirewallPolicyResponseTypeDef = TypedDict(
    "_RequiredFirewallPolicyResponseTypeDef",
    {
        "FirewallPolicyName": str,
        "FirewallPolicyArn": str,
        "FirewallPolicyId": str,
    },
)
_OptionalFirewallPolicyResponseTypeDef = TypedDict(
    "_OptionalFirewallPolicyResponseTypeDef",
    {
        "Description": str,
        "FirewallPolicyStatus": ResourceStatusType,
        "Tags": List[TagTypeDef],
        "ConsumedStatelessRuleCapacity": int,
        "ConsumedStatefulRuleCapacity": int,
        "NumberOfAssociations": int,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "LastModifiedTime": datetime,
    },
    total=False,
)


class FirewallPolicyResponseTypeDef(
    _RequiredFirewallPolicyResponseTypeDef, _OptionalFirewallPolicyResponseTypeDef
):
    pass


_RequiredFirewallTypeDef = TypedDict(
    "_RequiredFirewallTypeDef",
    {
        "FirewallPolicyArn": str,
        "VpcId": str,
        "SubnetMappings": List[SubnetMappingTypeDef],
        "FirewallId": str,
    },
)
_OptionalFirewallTypeDef = TypedDict(
    "_OptionalFirewallTypeDef",
    {
        "FirewallName": str,
        "FirewallArn": str,
        "DeleteProtection": bool,
        "SubnetChangeProtection": bool,
        "FirewallPolicyChangeProtection": bool,
        "Description": str,
        "Tags": List[TagTypeDef],
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
    },
    total=False,
)


class FirewallTypeDef(_RequiredFirewallTypeDef, _OptionalFirewallTypeDef):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "NextToken": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredRuleGroupResponseTypeDef = TypedDict(
    "_RequiredRuleGroupResponseTypeDef",
    {
        "RuleGroupArn": str,
        "RuleGroupName": str,
        "RuleGroupId": str,
    },
)
_OptionalRuleGroupResponseTypeDef = TypedDict(
    "_OptionalRuleGroupResponseTypeDef",
    {
        "Description": str,
        "Type": RuleGroupTypeType,
        "Capacity": int,
        "RuleGroupStatus": ResourceStatusType,
        "Tags": List[TagTypeDef],
        "ConsumedCapacity": int,
        "NumberOfAssociations": int,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "SourceMetadata": SourceMetadataTypeDef,
        "SnsTopic": str,
        "LastModifiedTime": datetime,
    },
    total=False,
)


class RuleGroupResponseTypeDef(
    _RequiredRuleGroupResponseTypeDef, _OptionalRuleGroupResponseTypeDef
):
    pass


DescribeRuleGroupMetadataResponseTypeDef = TypedDict(
    "DescribeRuleGroupMetadataResponseTypeDef",
    {
        "RuleGroupArn": str,
        "RuleGroupName": str,
        "Description": str,
        "Type": RuleGroupTypeType,
        "Capacity": int,
        "StatefulRuleOptions": StatefulRuleOptionsTypeDef,
        "LastModifiedTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PublishMetricActionTypeDef = TypedDict(
    "PublishMetricActionTypeDef",
    {
        "Dimensions": Sequence[DimensionTypeDef],
    },
)

ListFirewallsResponseTypeDef = TypedDict(
    "ListFirewallsResponseTypeDef",
    {
        "NextToken": str,
        "Firewalls": List[FirewallMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFirewallPoliciesResponseTypeDef = TypedDict(
    "ListFirewallPoliciesResponseTypeDef",
    {
        "NextToken": str,
        "FirewallPolicies": List[FirewallPolicyMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFirewallPoliciesRequestListFirewallPoliciesPaginateTypeDef = TypedDict(
    "ListFirewallPoliciesRequestListFirewallPoliciesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListFirewallsRequestListFirewallsPaginateTypeDef = TypedDict(
    "ListFirewallsRequestListFirewallsPaginateTypeDef",
    {
        "VpcIds": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRuleGroupsRequestListRuleGroupsPaginateTypeDef = TypedDict(
    "ListRuleGroupsRequestListRuleGroupsPaginateTypeDef",
    {
        "Scope": ResourceManagedStatusType,
        "ManagedType": ResourceManagedTypeType,
        "Type": RuleGroupTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
):
    pass


ListRuleGroupsResponseTypeDef = TypedDict(
    "ListRuleGroupsResponseTypeDef",
    {
        "NextToken": str,
        "RuleGroups": List[RuleGroupMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LoggingConfigurationTypeDef = TypedDict(
    "LoggingConfigurationTypeDef",
    {
        "LogDestinationConfigs": List[LogDestinationConfigTypeDef],
    },
)

MatchAttributesTypeDef = TypedDict(
    "MatchAttributesTypeDef",
    {
        "Sources": Sequence[AddressTypeDef],
        "Destinations": Sequence[AddressTypeDef],
        "SourcePorts": Sequence[PortRangeTypeDef],
        "DestinationPorts": Sequence[PortRangeTypeDef],
        "Protocols": Sequence[int],
        "TCPFlags": Sequence[TCPFlagFieldTypeDef],
    },
    total=False,
)

SyncStateTypeDef = TypedDict(
    "SyncStateTypeDef",
    {
        "Attachment": AttachmentTypeDef,
        "Config": Dict[str, PerObjectStatusTypeDef],
    },
    total=False,
)

RuleVariablesTypeDef = TypedDict(
    "RuleVariablesTypeDef",
    {
        "IPSets": Mapping[str, IPSetTypeDef],
        "PortSets": Mapping[str, PortSetTypeDef],
    },
    total=False,
)

StatefulRuleTypeDef = TypedDict(
    "StatefulRuleTypeDef",
    {
        "Action": StatefulActionType,
        "Header": HeaderTypeDef,
        "RuleOptions": Sequence[RuleOptionTypeDef],
    },
)

_RequiredStatefulRuleGroupReferenceTypeDef = TypedDict(
    "_RequiredStatefulRuleGroupReferenceTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalStatefulRuleGroupReferenceTypeDef = TypedDict(
    "_OptionalStatefulRuleGroupReferenceTypeDef",
    {
        "Priority": int,
        "Override": StatefulRuleGroupOverrideTypeDef,
    },
    total=False,
)


class StatefulRuleGroupReferenceTypeDef(
    _RequiredStatefulRuleGroupReferenceTypeDef, _OptionalStatefulRuleGroupReferenceTypeDef
):
    pass


CreateFirewallPolicyResponseTypeDef = TypedDict(
    "CreateFirewallPolicyResponseTypeDef",
    {
        "UpdateToken": str,
        "FirewallPolicyResponse": FirewallPolicyResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFirewallPolicyResponseTypeDef = TypedDict(
    "DeleteFirewallPolicyResponseTypeDef",
    {
        "FirewallPolicyResponse": FirewallPolicyResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallPolicyResponseTypeDef = TypedDict(
    "UpdateFirewallPolicyResponseTypeDef",
    {
        "UpdateToken": str,
        "FirewallPolicyResponse": FirewallPolicyResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRuleGroupResponseTypeDef = TypedDict(
    "CreateRuleGroupResponseTypeDef",
    {
        "UpdateToken": str,
        "RuleGroupResponse": RuleGroupResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRuleGroupResponseTypeDef = TypedDict(
    "DeleteRuleGroupResponseTypeDef",
    {
        "RuleGroupResponse": RuleGroupResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRuleGroupResponseTypeDef = TypedDict(
    "UpdateRuleGroupResponseTypeDef",
    {
        "UpdateToken": str,
        "RuleGroupResponse": RuleGroupResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ActionDefinitionTypeDef = TypedDict(
    "ActionDefinitionTypeDef",
    {
        "PublishMetricAction": PublishMetricActionTypeDef,
    },
    total=False,
)

DescribeLoggingConfigurationResponseTypeDef = TypedDict(
    "DescribeLoggingConfigurationResponseTypeDef",
    {
        "FirewallArn": str,
        "LoggingConfiguration": LoggingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateLoggingConfigurationRequestRequestTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "LoggingConfiguration": LoggingConfigurationTypeDef,
    },
    total=False,
)

UpdateLoggingConfigurationResponseTypeDef = TypedDict(
    "UpdateLoggingConfigurationResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "LoggingConfiguration": LoggingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RuleDefinitionTypeDef = TypedDict(
    "RuleDefinitionTypeDef",
    {
        "MatchAttributes": MatchAttributesTypeDef,
        "Actions": Sequence[str],
    },
)

_RequiredFirewallStatusTypeDef = TypedDict(
    "_RequiredFirewallStatusTypeDef",
    {
        "Status": FirewallStatusValueType,
        "ConfigurationSyncStateSummary": ConfigurationSyncStateType,
    },
)
_OptionalFirewallStatusTypeDef = TypedDict(
    "_OptionalFirewallStatusTypeDef",
    {
        "SyncStates": Dict[str, SyncStateTypeDef],
    },
    total=False,
)


class FirewallStatusTypeDef(_RequiredFirewallStatusTypeDef, _OptionalFirewallStatusTypeDef):
    pass


CustomActionTypeDef = TypedDict(
    "CustomActionTypeDef",
    {
        "ActionName": str,
        "ActionDefinition": ActionDefinitionTypeDef,
    },
)

StatelessRuleTypeDef = TypedDict(
    "StatelessRuleTypeDef",
    {
        "RuleDefinition": RuleDefinitionTypeDef,
        "Priority": int,
    },
)

CreateFirewallResponseTypeDef = TypedDict(
    "CreateFirewallResponseTypeDef",
    {
        "Firewall": FirewallTypeDef,
        "FirewallStatus": FirewallStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFirewallResponseTypeDef = TypedDict(
    "DeleteFirewallResponseTypeDef",
    {
        "Firewall": FirewallTypeDef,
        "FirewallStatus": FirewallStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFirewallResponseTypeDef = TypedDict(
    "DescribeFirewallResponseTypeDef",
    {
        "UpdateToken": str,
        "Firewall": FirewallTypeDef,
        "FirewallStatus": FirewallStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredFirewallPolicyTypeDef = TypedDict(
    "_RequiredFirewallPolicyTypeDef",
    {
        "StatelessDefaultActions": Sequence[str],
        "StatelessFragmentDefaultActions": Sequence[str],
    },
)
_OptionalFirewallPolicyTypeDef = TypedDict(
    "_OptionalFirewallPolicyTypeDef",
    {
        "StatelessRuleGroupReferences": Sequence[StatelessRuleGroupReferenceTypeDef],
        "StatelessCustomActions": Sequence[CustomActionTypeDef],
        "StatefulRuleGroupReferences": Sequence[StatefulRuleGroupReferenceTypeDef],
        "StatefulDefaultActions": Sequence[str],
        "StatefulEngineOptions": StatefulEngineOptionsTypeDef,
    },
    total=False,
)


class FirewallPolicyTypeDef(_RequiredFirewallPolicyTypeDef, _OptionalFirewallPolicyTypeDef):
    pass


_RequiredStatelessRulesAndCustomActionsTypeDef = TypedDict(
    "_RequiredStatelessRulesAndCustomActionsTypeDef",
    {
        "StatelessRules": Sequence[StatelessRuleTypeDef],
    },
)
_OptionalStatelessRulesAndCustomActionsTypeDef = TypedDict(
    "_OptionalStatelessRulesAndCustomActionsTypeDef",
    {
        "CustomActions": Sequence[CustomActionTypeDef],
    },
    total=False,
)


class StatelessRulesAndCustomActionsTypeDef(
    _RequiredStatelessRulesAndCustomActionsTypeDef, _OptionalStatelessRulesAndCustomActionsTypeDef
):
    pass


_RequiredCreateFirewallPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFirewallPolicyRequestRequestTypeDef",
    {
        "FirewallPolicyName": str,
        "FirewallPolicy": FirewallPolicyTypeDef,
    },
)
_OptionalCreateFirewallPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFirewallPolicyRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "DryRun": bool,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
    },
    total=False,
)


class CreateFirewallPolicyRequestRequestTypeDef(
    _RequiredCreateFirewallPolicyRequestRequestTypeDef,
    _OptionalCreateFirewallPolicyRequestRequestTypeDef,
):
    pass


DescribeFirewallPolicyResponseTypeDef = TypedDict(
    "DescribeFirewallPolicyResponseTypeDef",
    {
        "UpdateToken": str,
        "FirewallPolicyResponse": FirewallPolicyResponseTypeDef,
        "FirewallPolicy": FirewallPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateFirewallPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFirewallPolicyRequestRequestTypeDef",
    {
        "UpdateToken": str,
        "FirewallPolicy": FirewallPolicyTypeDef,
    },
)
_OptionalUpdateFirewallPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFirewallPolicyRequestRequestTypeDef",
    {
        "FirewallPolicyArn": str,
        "FirewallPolicyName": str,
        "Description": str,
        "DryRun": bool,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
    },
    total=False,
)


class UpdateFirewallPolicyRequestRequestTypeDef(
    _RequiredUpdateFirewallPolicyRequestRequestTypeDef,
    _OptionalUpdateFirewallPolicyRequestRequestTypeDef,
):
    pass


RulesSourceTypeDef = TypedDict(
    "RulesSourceTypeDef",
    {
        "RulesString": str,
        "RulesSourceList": RulesSourceListTypeDef,
        "StatefulRules": Sequence[StatefulRuleTypeDef],
        "StatelessRulesAndCustomActions": StatelessRulesAndCustomActionsTypeDef,
    },
    total=False,
)

_RequiredRuleGroupTypeDef = TypedDict(
    "_RequiredRuleGroupTypeDef",
    {
        "RulesSource": RulesSourceTypeDef,
    },
)
_OptionalRuleGroupTypeDef = TypedDict(
    "_OptionalRuleGroupTypeDef",
    {
        "RuleVariables": RuleVariablesTypeDef,
        "StatefulRuleOptions": StatefulRuleOptionsTypeDef,
    },
    total=False,
)


class RuleGroupTypeDef(_RequiredRuleGroupTypeDef, _OptionalRuleGroupTypeDef):
    pass


_RequiredCreateRuleGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupName": str,
        "Type": RuleGroupTypeType,
        "Capacity": int,
    },
)
_OptionalCreateRuleGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRuleGroupRequestRequestTypeDef",
    {
        "RuleGroup": RuleGroupTypeDef,
        "Rules": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "DryRun": bool,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "SourceMetadata": SourceMetadataTypeDef,
    },
    total=False,
)


class CreateRuleGroupRequestRequestTypeDef(
    _RequiredCreateRuleGroupRequestRequestTypeDef, _OptionalCreateRuleGroupRequestRequestTypeDef
):
    pass


DescribeRuleGroupResponseTypeDef = TypedDict(
    "DescribeRuleGroupResponseTypeDef",
    {
        "UpdateToken": str,
        "RuleGroup": RuleGroupTypeDef,
        "RuleGroupResponse": RuleGroupResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateRuleGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRuleGroupRequestRequestTypeDef",
    {
        "UpdateToken": str,
    },
)
_OptionalUpdateRuleGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupArn": str,
        "RuleGroupName": str,
        "RuleGroup": RuleGroupTypeDef,
        "Rules": str,
        "Type": RuleGroupTypeType,
        "Description": str,
        "DryRun": bool,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "SourceMetadata": SourceMetadataTypeDef,
    },
    total=False,
)


class UpdateRuleGroupRequestRequestTypeDef(
    _RequiredUpdateRuleGroupRequestRequestTypeDef, _OptionalUpdateRuleGroupRequestRequestTypeDef
):
    pass
