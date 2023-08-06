"""
Type annotations for cloudsearch service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudsearch/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudsearch.type_defs import OptionStatusTypeDef

    data: OptionStatusTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AlgorithmicStemmingType,
    AnalysisSchemeLanguageType,
    IndexFieldTypeType,
    OptionStateType,
    PartitionInstanceTypeType,
    SuggesterFuzzyMatchingType,
    TLSSecurityPolicyType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "OptionStatusTypeDef",
    "AnalysisOptionsTypeDef",
    "BuildSuggestersRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateDomainRequestRequestTypeDef",
    "DateArrayOptionsTypeDef",
    "DateOptionsTypeDef",
    "ExpressionTypeDef",
    "DeleteAnalysisSchemeRequestRequestTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DeleteExpressionRequestRequestTypeDef",
    "DeleteIndexFieldRequestRequestTypeDef",
    "DeleteSuggesterRequestRequestTypeDef",
    "DescribeAnalysisSchemesRequestRequestTypeDef",
    "DescribeAvailabilityOptionsRequestRequestTypeDef",
    "DescribeDomainEndpointOptionsRequestRequestTypeDef",
    "DescribeDomainsRequestRequestTypeDef",
    "DescribeExpressionsRequestRequestTypeDef",
    "DescribeIndexFieldsRequestRequestTypeDef",
    "DescribeScalingParametersRequestRequestTypeDef",
    "DescribeServiceAccessPoliciesRequestRequestTypeDef",
    "DescribeSuggestersRequestRequestTypeDef",
    "DocumentSuggesterOptionsTypeDef",
    "DomainEndpointOptionsTypeDef",
    "LimitsTypeDef",
    "ServiceEndpointTypeDef",
    "DoubleArrayOptionsTypeDef",
    "DoubleOptionsTypeDef",
    "IndexDocumentsRequestRequestTypeDef",
    "IntArrayOptionsTypeDef",
    "IntOptionsTypeDef",
    "LatLonOptionsTypeDef",
    "LiteralArrayOptionsTypeDef",
    "LiteralOptionsTypeDef",
    "TextArrayOptionsTypeDef",
    "TextOptionsTypeDef",
    "ScalingParametersTypeDef",
    "UpdateAvailabilityOptionsRequestRequestTypeDef",
    "UpdateServiceAccessPoliciesRequestRequestTypeDef",
    "AccessPoliciesStatusTypeDef",
    "AvailabilityOptionsStatusTypeDef",
    "AnalysisSchemeTypeDef",
    "BuildSuggestersResponseTypeDef",
    "IndexDocumentsResponseTypeDef",
    "ListDomainNamesResponseTypeDef",
    "DefineExpressionRequestRequestTypeDef",
    "ExpressionStatusTypeDef",
    "SuggesterTypeDef",
    "DomainEndpointOptionsStatusTypeDef",
    "UpdateDomainEndpointOptionsRequestRequestTypeDef",
    "DomainStatusTypeDef",
    "IndexFieldTypeDef",
    "ScalingParametersStatusTypeDef",
    "UpdateScalingParametersRequestRequestTypeDef",
    "DescribeServiceAccessPoliciesResponseTypeDef",
    "UpdateServiceAccessPoliciesResponseTypeDef",
    "DescribeAvailabilityOptionsResponseTypeDef",
    "UpdateAvailabilityOptionsResponseTypeDef",
    "AnalysisSchemeStatusTypeDef",
    "DefineAnalysisSchemeRequestRequestTypeDef",
    "DefineExpressionResponseTypeDef",
    "DeleteExpressionResponseTypeDef",
    "DescribeExpressionsResponseTypeDef",
    "DefineSuggesterRequestRequestTypeDef",
    "SuggesterStatusTypeDef",
    "DescribeDomainEndpointOptionsResponseTypeDef",
    "UpdateDomainEndpointOptionsResponseTypeDef",
    "CreateDomainResponseTypeDef",
    "DeleteDomainResponseTypeDef",
    "DescribeDomainsResponseTypeDef",
    "DefineIndexFieldRequestRequestTypeDef",
    "IndexFieldStatusTypeDef",
    "DescribeScalingParametersResponseTypeDef",
    "UpdateScalingParametersResponseTypeDef",
    "DefineAnalysisSchemeResponseTypeDef",
    "DeleteAnalysisSchemeResponseTypeDef",
    "DescribeAnalysisSchemesResponseTypeDef",
    "DefineSuggesterResponseTypeDef",
    "DeleteSuggesterResponseTypeDef",
    "DescribeSuggestersResponseTypeDef",
    "DefineIndexFieldResponseTypeDef",
    "DeleteIndexFieldResponseTypeDef",
    "DescribeIndexFieldsResponseTypeDef",
)

_RequiredOptionStatusTypeDef = TypedDict(
    "_RequiredOptionStatusTypeDef",
    {
        "CreationDate": datetime,
        "UpdateDate": datetime,
        "State": OptionStateType,
    },
)
_OptionalOptionStatusTypeDef = TypedDict(
    "_OptionalOptionStatusTypeDef",
    {
        "UpdateVersion": int,
        "PendingDeletion": bool,
    },
    total=False,
)

class OptionStatusTypeDef(_RequiredOptionStatusTypeDef, _OptionalOptionStatusTypeDef):
    pass

AnalysisOptionsTypeDef = TypedDict(
    "AnalysisOptionsTypeDef",
    {
        "Synonyms": str,
        "Stopwords": str,
        "StemmingDictionary": str,
        "JapaneseTokenizationDictionary": str,
        "AlgorithmicStemming": AlgorithmicStemmingType,
    },
    total=False,
)

BuildSuggestersRequestRequestTypeDef = TypedDict(
    "BuildSuggestersRequestRequestTypeDef",
    {
        "DomainName": str,
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

CreateDomainRequestRequestTypeDef = TypedDict(
    "CreateDomainRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

DateArrayOptionsTypeDef = TypedDict(
    "DateArrayOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceFields": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
    },
    total=False,
)

DateOptionsTypeDef = TypedDict(
    "DateOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceField": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
        "SortEnabled": bool,
    },
    total=False,
)

ExpressionTypeDef = TypedDict(
    "ExpressionTypeDef",
    {
        "ExpressionName": str,
        "ExpressionValue": str,
    },
)

DeleteAnalysisSchemeRequestRequestTypeDef = TypedDict(
    "DeleteAnalysisSchemeRequestRequestTypeDef",
    {
        "DomainName": str,
        "AnalysisSchemeName": str,
    },
)

DeleteDomainRequestRequestTypeDef = TypedDict(
    "DeleteDomainRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

DeleteExpressionRequestRequestTypeDef = TypedDict(
    "DeleteExpressionRequestRequestTypeDef",
    {
        "DomainName": str,
        "ExpressionName": str,
    },
)

DeleteIndexFieldRequestRequestTypeDef = TypedDict(
    "DeleteIndexFieldRequestRequestTypeDef",
    {
        "DomainName": str,
        "IndexFieldName": str,
    },
)

DeleteSuggesterRequestRequestTypeDef = TypedDict(
    "DeleteSuggesterRequestRequestTypeDef",
    {
        "DomainName": str,
        "SuggesterName": str,
    },
)

_RequiredDescribeAnalysisSchemesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAnalysisSchemesRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalDescribeAnalysisSchemesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAnalysisSchemesRequestRequestTypeDef",
    {
        "AnalysisSchemeNames": Sequence[str],
        "Deployed": bool,
    },
    total=False,
)

class DescribeAnalysisSchemesRequestRequestTypeDef(
    _RequiredDescribeAnalysisSchemesRequestRequestTypeDef,
    _OptionalDescribeAnalysisSchemesRequestRequestTypeDef,
):
    pass

_RequiredDescribeAvailabilityOptionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAvailabilityOptionsRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalDescribeAvailabilityOptionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAvailabilityOptionsRequestRequestTypeDef",
    {
        "Deployed": bool,
    },
    total=False,
)

class DescribeAvailabilityOptionsRequestRequestTypeDef(
    _RequiredDescribeAvailabilityOptionsRequestRequestTypeDef,
    _OptionalDescribeAvailabilityOptionsRequestRequestTypeDef,
):
    pass

_RequiredDescribeDomainEndpointOptionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDomainEndpointOptionsRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalDescribeDomainEndpointOptionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDomainEndpointOptionsRequestRequestTypeDef",
    {
        "Deployed": bool,
    },
    total=False,
)

class DescribeDomainEndpointOptionsRequestRequestTypeDef(
    _RequiredDescribeDomainEndpointOptionsRequestRequestTypeDef,
    _OptionalDescribeDomainEndpointOptionsRequestRequestTypeDef,
):
    pass

DescribeDomainsRequestRequestTypeDef = TypedDict(
    "DescribeDomainsRequestRequestTypeDef",
    {
        "DomainNames": Sequence[str],
    },
    total=False,
)

_RequiredDescribeExpressionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeExpressionsRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalDescribeExpressionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeExpressionsRequestRequestTypeDef",
    {
        "ExpressionNames": Sequence[str],
        "Deployed": bool,
    },
    total=False,
)

class DescribeExpressionsRequestRequestTypeDef(
    _RequiredDescribeExpressionsRequestRequestTypeDef,
    _OptionalDescribeExpressionsRequestRequestTypeDef,
):
    pass

_RequiredDescribeIndexFieldsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeIndexFieldsRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalDescribeIndexFieldsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeIndexFieldsRequestRequestTypeDef",
    {
        "FieldNames": Sequence[str],
        "Deployed": bool,
    },
    total=False,
)

class DescribeIndexFieldsRequestRequestTypeDef(
    _RequiredDescribeIndexFieldsRequestRequestTypeDef,
    _OptionalDescribeIndexFieldsRequestRequestTypeDef,
):
    pass

DescribeScalingParametersRequestRequestTypeDef = TypedDict(
    "DescribeScalingParametersRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

_RequiredDescribeServiceAccessPoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeServiceAccessPoliciesRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalDescribeServiceAccessPoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeServiceAccessPoliciesRequestRequestTypeDef",
    {
        "Deployed": bool,
    },
    total=False,
)

class DescribeServiceAccessPoliciesRequestRequestTypeDef(
    _RequiredDescribeServiceAccessPoliciesRequestRequestTypeDef,
    _OptionalDescribeServiceAccessPoliciesRequestRequestTypeDef,
):
    pass

_RequiredDescribeSuggestersRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeSuggestersRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalDescribeSuggestersRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeSuggestersRequestRequestTypeDef",
    {
        "SuggesterNames": Sequence[str],
        "Deployed": bool,
    },
    total=False,
)

class DescribeSuggestersRequestRequestTypeDef(
    _RequiredDescribeSuggestersRequestRequestTypeDef,
    _OptionalDescribeSuggestersRequestRequestTypeDef,
):
    pass

_RequiredDocumentSuggesterOptionsTypeDef = TypedDict(
    "_RequiredDocumentSuggesterOptionsTypeDef",
    {
        "SourceField": str,
    },
)
_OptionalDocumentSuggesterOptionsTypeDef = TypedDict(
    "_OptionalDocumentSuggesterOptionsTypeDef",
    {
        "FuzzyMatching": SuggesterFuzzyMatchingType,
        "SortExpression": str,
    },
    total=False,
)

class DocumentSuggesterOptionsTypeDef(
    _RequiredDocumentSuggesterOptionsTypeDef, _OptionalDocumentSuggesterOptionsTypeDef
):
    pass

DomainEndpointOptionsTypeDef = TypedDict(
    "DomainEndpointOptionsTypeDef",
    {
        "EnforceHTTPS": bool,
        "TLSSecurityPolicy": TLSSecurityPolicyType,
    },
    total=False,
)

LimitsTypeDef = TypedDict(
    "LimitsTypeDef",
    {
        "MaximumReplicationCount": int,
        "MaximumPartitionCount": int,
    },
)

ServiceEndpointTypeDef = TypedDict(
    "ServiceEndpointTypeDef",
    {
        "Endpoint": str,
    },
    total=False,
)

DoubleArrayOptionsTypeDef = TypedDict(
    "DoubleArrayOptionsTypeDef",
    {
        "DefaultValue": float,
        "SourceFields": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
    },
    total=False,
)

DoubleOptionsTypeDef = TypedDict(
    "DoubleOptionsTypeDef",
    {
        "DefaultValue": float,
        "SourceField": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
        "SortEnabled": bool,
    },
    total=False,
)

IndexDocumentsRequestRequestTypeDef = TypedDict(
    "IndexDocumentsRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

IntArrayOptionsTypeDef = TypedDict(
    "IntArrayOptionsTypeDef",
    {
        "DefaultValue": int,
        "SourceFields": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
    },
    total=False,
)

IntOptionsTypeDef = TypedDict(
    "IntOptionsTypeDef",
    {
        "DefaultValue": int,
        "SourceField": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
        "SortEnabled": bool,
    },
    total=False,
)

LatLonOptionsTypeDef = TypedDict(
    "LatLonOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceField": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
        "SortEnabled": bool,
    },
    total=False,
)

LiteralArrayOptionsTypeDef = TypedDict(
    "LiteralArrayOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceFields": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
    },
    total=False,
)

LiteralOptionsTypeDef = TypedDict(
    "LiteralOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceField": str,
        "FacetEnabled": bool,
        "SearchEnabled": bool,
        "ReturnEnabled": bool,
        "SortEnabled": bool,
    },
    total=False,
)

TextArrayOptionsTypeDef = TypedDict(
    "TextArrayOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceFields": str,
        "ReturnEnabled": bool,
        "HighlightEnabled": bool,
        "AnalysisScheme": str,
    },
    total=False,
)

TextOptionsTypeDef = TypedDict(
    "TextOptionsTypeDef",
    {
        "DefaultValue": str,
        "SourceField": str,
        "ReturnEnabled": bool,
        "SortEnabled": bool,
        "HighlightEnabled": bool,
        "AnalysisScheme": str,
    },
    total=False,
)

ScalingParametersTypeDef = TypedDict(
    "ScalingParametersTypeDef",
    {
        "DesiredInstanceType": PartitionInstanceTypeType,
        "DesiredReplicationCount": int,
        "DesiredPartitionCount": int,
    },
    total=False,
)

UpdateAvailabilityOptionsRequestRequestTypeDef = TypedDict(
    "UpdateAvailabilityOptionsRequestRequestTypeDef",
    {
        "DomainName": str,
        "MultiAZ": bool,
    },
)

UpdateServiceAccessPoliciesRequestRequestTypeDef = TypedDict(
    "UpdateServiceAccessPoliciesRequestRequestTypeDef",
    {
        "DomainName": str,
        "AccessPolicies": str,
    },
)

AccessPoliciesStatusTypeDef = TypedDict(
    "AccessPoliciesStatusTypeDef",
    {
        "Options": str,
        "Status": OptionStatusTypeDef,
    },
)

AvailabilityOptionsStatusTypeDef = TypedDict(
    "AvailabilityOptionsStatusTypeDef",
    {
        "Options": bool,
        "Status": OptionStatusTypeDef,
    },
)

_RequiredAnalysisSchemeTypeDef = TypedDict(
    "_RequiredAnalysisSchemeTypeDef",
    {
        "AnalysisSchemeName": str,
        "AnalysisSchemeLanguage": AnalysisSchemeLanguageType,
    },
)
_OptionalAnalysisSchemeTypeDef = TypedDict(
    "_OptionalAnalysisSchemeTypeDef",
    {
        "AnalysisOptions": AnalysisOptionsTypeDef,
    },
    total=False,
)

class AnalysisSchemeTypeDef(_RequiredAnalysisSchemeTypeDef, _OptionalAnalysisSchemeTypeDef):
    pass

BuildSuggestersResponseTypeDef = TypedDict(
    "BuildSuggestersResponseTypeDef",
    {
        "FieldNames": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IndexDocumentsResponseTypeDef = TypedDict(
    "IndexDocumentsResponseTypeDef",
    {
        "FieldNames": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDomainNamesResponseTypeDef = TypedDict(
    "ListDomainNamesResponseTypeDef",
    {
        "DomainNames": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DefineExpressionRequestRequestTypeDef = TypedDict(
    "DefineExpressionRequestRequestTypeDef",
    {
        "DomainName": str,
        "Expression": ExpressionTypeDef,
    },
)

ExpressionStatusTypeDef = TypedDict(
    "ExpressionStatusTypeDef",
    {
        "Options": ExpressionTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

SuggesterTypeDef = TypedDict(
    "SuggesterTypeDef",
    {
        "SuggesterName": str,
        "DocumentSuggesterOptions": DocumentSuggesterOptionsTypeDef,
    },
)

DomainEndpointOptionsStatusTypeDef = TypedDict(
    "DomainEndpointOptionsStatusTypeDef",
    {
        "Options": DomainEndpointOptionsTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

UpdateDomainEndpointOptionsRequestRequestTypeDef = TypedDict(
    "UpdateDomainEndpointOptionsRequestRequestTypeDef",
    {
        "DomainName": str,
        "DomainEndpointOptions": DomainEndpointOptionsTypeDef,
    },
)

_RequiredDomainStatusTypeDef = TypedDict(
    "_RequiredDomainStatusTypeDef",
    {
        "DomainId": str,
        "DomainName": str,
        "RequiresIndexDocuments": bool,
    },
)
_OptionalDomainStatusTypeDef = TypedDict(
    "_OptionalDomainStatusTypeDef",
    {
        "ARN": str,
        "Created": bool,
        "Deleted": bool,
        "DocService": ServiceEndpointTypeDef,
        "SearchService": ServiceEndpointTypeDef,
        "Processing": bool,
        "SearchInstanceType": str,
        "SearchPartitionCount": int,
        "SearchInstanceCount": int,
        "Limits": LimitsTypeDef,
    },
    total=False,
)

class DomainStatusTypeDef(_RequiredDomainStatusTypeDef, _OptionalDomainStatusTypeDef):
    pass

_RequiredIndexFieldTypeDef = TypedDict(
    "_RequiredIndexFieldTypeDef",
    {
        "IndexFieldName": str,
        "IndexFieldType": IndexFieldTypeType,
    },
)
_OptionalIndexFieldTypeDef = TypedDict(
    "_OptionalIndexFieldTypeDef",
    {
        "IntOptions": IntOptionsTypeDef,
        "DoubleOptions": DoubleOptionsTypeDef,
        "LiteralOptions": LiteralOptionsTypeDef,
        "TextOptions": TextOptionsTypeDef,
        "DateOptions": DateOptionsTypeDef,
        "LatLonOptions": LatLonOptionsTypeDef,
        "IntArrayOptions": IntArrayOptionsTypeDef,
        "DoubleArrayOptions": DoubleArrayOptionsTypeDef,
        "LiteralArrayOptions": LiteralArrayOptionsTypeDef,
        "TextArrayOptions": TextArrayOptionsTypeDef,
        "DateArrayOptions": DateArrayOptionsTypeDef,
    },
    total=False,
)

class IndexFieldTypeDef(_RequiredIndexFieldTypeDef, _OptionalIndexFieldTypeDef):
    pass

ScalingParametersStatusTypeDef = TypedDict(
    "ScalingParametersStatusTypeDef",
    {
        "Options": ScalingParametersTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

UpdateScalingParametersRequestRequestTypeDef = TypedDict(
    "UpdateScalingParametersRequestRequestTypeDef",
    {
        "DomainName": str,
        "ScalingParameters": ScalingParametersTypeDef,
    },
)

DescribeServiceAccessPoliciesResponseTypeDef = TypedDict(
    "DescribeServiceAccessPoliciesResponseTypeDef",
    {
        "AccessPolicies": AccessPoliciesStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateServiceAccessPoliciesResponseTypeDef = TypedDict(
    "UpdateServiceAccessPoliciesResponseTypeDef",
    {
        "AccessPolicies": AccessPoliciesStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAvailabilityOptionsResponseTypeDef = TypedDict(
    "DescribeAvailabilityOptionsResponseTypeDef",
    {
        "AvailabilityOptions": AvailabilityOptionsStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAvailabilityOptionsResponseTypeDef = TypedDict(
    "UpdateAvailabilityOptionsResponseTypeDef",
    {
        "AvailabilityOptions": AvailabilityOptionsStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AnalysisSchemeStatusTypeDef = TypedDict(
    "AnalysisSchemeStatusTypeDef",
    {
        "Options": AnalysisSchemeTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

DefineAnalysisSchemeRequestRequestTypeDef = TypedDict(
    "DefineAnalysisSchemeRequestRequestTypeDef",
    {
        "DomainName": str,
        "AnalysisScheme": AnalysisSchemeTypeDef,
    },
)

DefineExpressionResponseTypeDef = TypedDict(
    "DefineExpressionResponseTypeDef",
    {
        "Expression": ExpressionStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteExpressionResponseTypeDef = TypedDict(
    "DeleteExpressionResponseTypeDef",
    {
        "Expression": ExpressionStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeExpressionsResponseTypeDef = TypedDict(
    "DescribeExpressionsResponseTypeDef",
    {
        "Expressions": List[ExpressionStatusTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DefineSuggesterRequestRequestTypeDef = TypedDict(
    "DefineSuggesterRequestRequestTypeDef",
    {
        "DomainName": str,
        "Suggester": SuggesterTypeDef,
    },
)

SuggesterStatusTypeDef = TypedDict(
    "SuggesterStatusTypeDef",
    {
        "Options": SuggesterTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

DescribeDomainEndpointOptionsResponseTypeDef = TypedDict(
    "DescribeDomainEndpointOptionsResponseTypeDef",
    {
        "DomainEndpointOptions": DomainEndpointOptionsStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDomainEndpointOptionsResponseTypeDef = TypedDict(
    "UpdateDomainEndpointOptionsResponseTypeDef",
    {
        "DomainEndpointOptions": DomainEndpointOptionsStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDomainResponseTypeDef = TypedDict(
    "CreateDomainResponseTypeDef",
    {
        "DomainStatus": DomainStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDomainResponseTypeDef = TypedDict(
    "DeleteDomainResponseTypeDef",
    {
        "DomainStatus": DomainStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDomainsResponseTypeDef = TypedDict(
    "DescribeDomainsResponseTypeDef",
    {
        "DomainStatusList": List[DomainStatusTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DefineIndexFieldRequestRequestTypeDef = TypedDict(
    "DefineIndexFieldRequestRequestTypeDef",
    {
        "DomainName": str,
        "IndexField": IndexFieldTypeDef,
    },
)

IndexFieldStatusTypeDef = TypedDict(
    "IndexFieldStatusTypeDef",
    {
        "Options": IndexFieldTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

DescribeScalingParametersResponseTypeDef = TypedDict(
    "DescribeScalingParametersResponseTypeDef",
    {
        "ScalingParameters": ScalingParametersStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateScalingParametersResponseTypeDef = TypedDict(
    "UpdateScalingParametersResponseTypeDef",
    {
        "ScalingParameters": ScalingParametersStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DefineAnalysisSchemeResponseTypeDef = TypedDict(
    "DefineAnalysisSchemeResponseTypeDef",
    {
        "AnalysisScheme": AnalysisSchemeStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAnalysisSchemeResponseTypeDef = TypedDict(
    "DeleteAnalysisSchemeResponseTypeDef",
    {
        "AnalysisScheme": AnalysisSchemeStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAnalysisSchemesResponseTypeDef = TypedDict(
    "DescribeAnalysisSchemesResponseTypeDef",
    {
        "AnalysisSchemes": List[AnalysisSchemeStatusTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DefineSuggesterResponseTypeDef = TypedDict(
    "DefineSuggesterResponseTypeDef",
    {
        "Suggester": SuggesterStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSuggesterResponseTypeDef = TypedDict(
    "DeleteSuggesterResponseTypeDef",
    {
        "Suggester": SuggesterStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSuggestersResponseTypeDef = TypedDict(
    "DescribeSuggestersResponseTypeDef",
    {
        "Suggesters": List[SuggesterStatusTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DefineIndexFieldResponseTypeDef = TypedDict(
    "DefineIndexFieldResponseTypeDef",
    {
        "IndexField": IndexFieldStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteIndexFieldResponseTypeDef = TypedDict(
    "DeleteIndexFieldResponseTypeDef",
    {
        "IndexField": IndexFieldStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeIndexFieldsResponseTypeDef = TypedDict(
    "DescribeIndexFieldsResponseTypeDef",
    {
        "IndexFields": List[IndexFieldStatusTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
