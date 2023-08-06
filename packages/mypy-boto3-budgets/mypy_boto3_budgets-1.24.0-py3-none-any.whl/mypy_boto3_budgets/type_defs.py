"""
Type annotations for budgets service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_budgets/type_defs/)

Usage::

    ```python
    from mypy_boto3_budgets.type_defs import ActionThresholdTypeDef

    data: ActionThresholdTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ActionStatusType,
    ActionSubTypeType,
    ActionTypeType,
    ApprovalModelType,
    AutoAdjustTypeType,
    BudgetTypeType,
    ComparisonOperatorType,
    EventTypeType,
    ExecutionTypeType,
    NotificationStateType,
    NotificationTypeType,
    SubscriptionTypeType,
    ThresholdTypeType,
    TimeUnitType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ActionThresholdTypeDef",
    "SubscriberTypeDef",
    "HistoricalOptionsTypeDef",
    "NotificationTypeDef",
    "CostTypesTypeDef",
    "SpendTypeDef",
    "TimePeriodTypeDef",
    "ResponseMetadataTypeDef",
    "IamActionDefinitionTypeDef",
    "ScpActionDefinitionTypeDef",
    "SsmActionDefinitionTypeDef",
    "DeleteBudgetActionRequestRequestTypeDef",
    "DeleteBudgetRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeBudgetActionRequestRequestTypeDef",
    "DescribeBudgetActionsForAccountRequestRequestTypeDef",
    "DescribeBudgetActionsForBudgetRequestRequestTypeDef",
    "DescribeBudgetNotificationsForAccountRequestRequestTypeDef",
    "DescribeBudgetRequestRequestTypeDef",
    "DescribeBudgetsRequestRequestTypeDef",
    "DescribeNotificationsForBudgetRequestRequestTypeDef",
    "ExecuteBudgetActionRequestRequestTypeDef",
    "AutoAdjustDataTypeDef",
    "BudgetNotificationsForAccountTypeDef",
    "CreateNotificationRequestRequestTypeDef",
    "CreateSubscriberRequestRequestTypeDef",
    "DeleteNotificationRequestRequestTypeDef",
    "DeleteSubscriberRequestRequestTypeDef",
    "DescribeSubscribersForNotificationRequestRequestTypeDef",
    "NotificationWithSubscribersTypeDef",
    "UpdateNotificationRequestRequestTypeDef",
    "UpdateSubscriberRequestRequestTypeDef",
    "CalculatedSpendTypeDef",
    "BudgetedAndActualAmountsTypeDef",
    "DescribeBudgetActionHistoriesRequestRequestTypeDef",
    "DescribeBudgetPerformanceHistoryRequestRequestTypeDef",
    "CreateBudgetActionResponseTypeDef",
    "DescribeNotificationsForBudgetResponseTypeDef",
    "DescribeSubscribersForNotificationResponseTypeDef",
    "ExecuteBudgetActionResponseTypeDef",
    "DefinitionTypeDef",
    "DescribeBudgetActionHistoriesRequestDescribeBudgetActionHistoriesPaginateTypeDef",
    "DescribeBudgetActionsForAccountRequestDescribeBudgetActionsForAccountPaginateTypeDef",
    "DescribeBudgetActionsForBudgetRequestDescribeBudgetActionsForBudgetPaginateTypeDef",
    "DescribeBudgetNotificationsForAccountRequestDescribeBudgetNotificationsForAccountPaginateTypeDef",
    "DescribeBudgetPerformanceHistoryRequestDescribeBudgetPerformanceHistoryPaginateTypeDef",
    "DescribeBudgetsRequestDescribeBudgetsPaginateTypeDef",
    "DescribeNotificationsForBudgetRequestDescribeNotificationsForBudgetPaginateTypeDef",
    "DescribeSubscribersForNotificationRequestDescribeSubscribersForNotificationPaginateTypeDef",
    "DescribeBudgetNotificationsForAccountResponseTypeDef",
    "BudgetTypeDef",
    "BudgetPerformanceHistoryTypeDef",
    "ActionTypeDef",
    "CreateBudgetActionRequestRequestTypeDef",
    "UpdateBudgetActionRequestRequestTypeDef",
    "CreateBudgetRequestRequestTypeDef",
    "DescribeBudgetResponseTypeDef",
    "DescribeBudgetsResponseTypeDef",
    "UpdateBudgetRequestRequestTypeDef",
    "DescribeBudgetPerformanceHistoryResponseTypeDef",
    "ActionHistoryDetailsTypeDef",
    "DeleteBudgetActionResponseTypeDef",
    "DescribeBudgetActionResponseTypeDef",
    "DescribeBudgetActionsForAccountResponseTypeDef",
    "DescribeBudgetActionsForBudgetResponseTypeDef",
    "UpdateBudgetActionResponseTypeDef",
    "ActionHistoryTypeDef",
    "DescribeBudgetActionHistoriesResponseTypeDef",
)

ActionThresholdTypeDef = TypedDict(
    "ActionThresholdTypeDef",
    {
        "ActionThresholdValue": float,
        "ActionThresholdType": ThresholdTypeType,
    },
)

SubscriberTypeDef = TypedDict(
    "SubscriberTypeDef",
    {
        "SubscriptionType": SubscriptionTypeType,
        "Address": str,
    },
)

_RequiredHistoricalOptionsTypeDef = TypedDict(
    "_RequiredHistoricalOptionsTypeDef",
    {
        "BudgetAdjustmentPeriod": int,
    },
)
_OptionalHistoricalOptionsTypeDef = TypedDict(
    "_OptionalHistoricalOptionsTypeDef",
    {
        "LookBackAvailablePeriods": int,
    },
    total=False,
)


class HistoricalOptionsTypeDef(
    _RequiredHistoricalOptionsTypeDef, _OptionalHistoricalOptionsTypeDef
):
    pass


_RequiredNotificationTypeDef = TypedDict(
    "_RequiredNotificationTypeDef",
    {
        "NotificationType": NotificationTypeType,
        "ComparisonOperator": ComparisonOperatorType,
        "Threshold": float,
    },
)
_OptionalNotificationTypeDef = TypedDict(
    "_OptionalNotificationTypeDef",
    {
        "ThresholdType": ThresholdTypeType,
        "NotificationState": NotificationStateType,
    },
    total=False,
)


class NotificationTypeDef(_RequiredNotificationTypeDef, _OptionalNotificationTypeDef):
    pass


CostTypesTypeDef = TypedDict(
    "CostTypesTypeDef",
    {
        "IncludeTax": bool,
        "IncludeSubscription": bool,
        "UseBlended": bool,
        "IncludeRefund": bool,
        "IncludeCredit": bool,
        "IncludeUpfront": bool,
        "IncludeRecurring": bool,
        "IncludeOtherSubscription": bool,
        "IncludeSupport": bool,
        "IncludeDiscount": bool,
        "UseAmortized": bool,
    },
    total=False,
)

SpendTypeDef = TypedDict(
    "SpendTypeDef",
    {
        "Amount": str,
        "Unit": str,
    },
)

TimePeriodTypeDef = TypedDict(
    "TimePeriodTypeDef",
    {
        "Start": Union[datetime, str],
        "End": Union[datetime, str],
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

_RequiredIamActionDefinitionTypeDef = TypedDict(
    "_RequiredIamActionDefinitionTypeDef",
    {
        "PolicyArn": str,
    },
)
_OptionalIamActionDefinitionTypeDef = TypedDict(
    "_OptionalIamActionDefinitionTypeDef",
    {
        "Roles": Sequence[str],
        "Groups": Sequence[str],
        "Users": Sequence[str],
    },
    total=False,
)


class IamActionDefinitionTypeDef(
    _RequiredIamActionDefinitionTypeDef, _OptionalIamActionDefinitionTypeDef
):
    pass


ScpActionDefinitionTypeDef = TypedDict(
    "ScpActionDefinitionTypeDef",
    {
        "PolicyId": str,
        "TargetIds": Sequence[str],
    },
)

SsmActionDefinitionTypeDef = TypedDict(
    "SsmActionDefinitionTypeDef",
    {
        "ActionSubType": ActionSubTypeType,
        "Region": str,
        "InstanceIds": Sequence[str],
    },
)

DeleteBudgetActionRequestRequestTypeDef = TypedDict(
    "DeleteBudgetActionRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "ActionId": str,
    },
)

DeleteBudgetRequestRequestTypeDef = TypedDict(
    "DeleteBudgetRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
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

DescribeBudgetActionRequestRequestTypeDef = TypedDict(
    "DescribeBudgetActionRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "ActionId": str,
    },
)

_RequiredDescribeBudgetActionsForAccountRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeBudgetActionsForAccountRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalDescribeBudgetActionsForAccountRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeBudgetActionsForAccountRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeBudgetActionsForAccountRequestRequestTypeDef(
    _RequiredDescribeBudgetActionsForAccountRequestRequestTypeDef,
    _OptionalDescribeBudgetActionsForAccountRequestRequestTypeDef,
):
    pass


_RequiredDescribeBudgetActionsForBudgetRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeBudgetActionsForBudgetRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
    },
)
_OptionalDescribeBudgetActionsForBudgetRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeBudgetActionsForBudgetRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeBudgetActionsForBudgetRequestRequestTypeDef(
    _RequiredDescribeBudgetActionsForBudgetRequestRequestTypeDef,
    _OptionalDescribeBudgetActionsForBudgetRequestRequestTypeDef,
):
    pass


_RequiredDescribeBudgetNotificationsForAccountRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeBudgetNotificationsForAccountRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalDescribeBudgetNotificationsForAccountRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeBudgetNotificationsForAccountRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeBudgetNotificationsForAccountRequestRequestTypeDef(
    _RequiredDescribeBudgetNotificationsForAccountRequestRequestTypeDef,
    _OptionalDescribeBudgetNotificationsForAccountRequestRequestTypeDef,
):
    pass


DescribeBudgetRequestRequestTypeDef = TypedDict(
    "DescribeBudgetRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
    },
)

_RequiredDescribeBudgetsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeBudgetsRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalDescribeBudgetsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeBudgetsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeBudgetsRequestRequestTypeDef(
    _RequiredDescribeBudgetsRequestRequestTypeDef, _OptionalDescribeBudgetsRequestRequestTypeDef
):
    pass


_RequiredDescribeNotificationsForBudgetRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeNotificationsForBudgetRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
    },
)
_OptionalDescribeNotificationsForBudgetRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeNotificationsForBudgetRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeNotificationsForBudgetRequestRequestTypeDef(
    _RequiredDescribeNotificationsForBudgetRequestRequestTypeDef,
    _OptionalDescribeNotificationsForBudgetRequestRequestTypeDef,
):
    pass


ExecuteBudgetActionRequestRequestTypeDef = TypedDict(
    "ExecuteBudgetActionRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "ActionId": str,
        "ExecutionType": ExecutionTypeType,
    },
)

_RequiredAutoAdjustDataTypeDef = TypedDict(
    "_RequiredAutoAdjustDataTypeDef",
    {
        "AutoAdjustType": AutoAdjustTypeType,
    },
)
_OptionalAutoAdjustDataTypeDef = TypedDict(
    "_OptionalAutoAdjustDataTypeDef",
    {
        "HistoricalOptions": HistoricalOptionsTypeDef,
        "LastAutoAdjustTime": Union[datetime, str],
    },
    total=False,
)


class AutoAdjustDataTypeDef(_RequiredAutoAdjustDataTypeDef, _OptionalAutoAdjustDataTypeDef):
    pass


BudgetNotificationsForAccountTypeDef = TypedDict(
    "BudgetNotificationsForAccountTypeDef",
    {
        "Notifications": List[NotificationTypeDef],
        "BudgetName": str,
    },
    total=False,
)

CreateNotificationRequestRequestTypeDef = TypedDict(
    "CreateNotificationRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "Notification": NotificationTypeDef,
        "Subscribers": Sequence[SubscriberTypeDef],
    },
)

CreateSubscriberRequestRequestTypeDef = TypedDict(
    "CreateSubscriberRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "Notification": NotificationTypeDef,
        "Subscriber": SubscriberTypeDef,
    },
)

DeleteNotificationRequestRequestTypeDef = TypedDict(
    "DeleteNotificationRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "Notification": NotificationTypeDef,
    },
)

DeleteSubscriberRequestRequestTypeDef = TypedDict(
    "DeleteSubscriberRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "Notification": NotificationTypeDef,
        "Subscriber": SubscriberTypeDef,
    },
)

_RequiredDescribeSubscribersForNotificationRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeSubscribersForNotificationRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "Notification": NotificationTypeDef,
    },
)
_OptionalDescribeSubscribersForNotificationRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeSubscribersForNotificationRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeSubscribersForNotificationRequestRequestTypeDef(
    _RequiredDescribeSubscribersForNotificationRequestRequestTypeDef,
    _OptionalDescribeSubscribersForNotificationRequestRequestTypeDef,
):
    pass


NotificationWithSubscribersTypeDef = TypedDict(
    "NotificationWithSubscribersTypeDef",
    {
        "Notification": NotificationTypeDef,
        "Subscribers": Sequence[SubscriberTypeDef],
    },
)

UpdateNotificationRequestRequestTypeDef = TypedDict(
    "UpdateNotificationRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "OldNotification": NotificationTypeDef,
        "NewNotification": NotificationTypeDef,
    },
)

UpdateSubscriberRequestRequestTypeDef = TypedDict(
    "UpdateSubscriberRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "Notification": NotificationTypeDef,
        "OldSubscriber": SubscriberTypeDef,
        "NewSubscriber": SubscriberTypeDef,
    },
)

_RequiredCalculatedSpendTypeDef = TypedDict(
    "_RequiredCalculatedSpendTypeDef",
    {
        "ActualSpend": SpendTypeDef,
    },
)
_OptionalCalculatedSpendTypeDef = TypedDict(
    "_OptionalCalculatedSpendTypeDef",
    {
        "ForecastedSpend": SpendTypeDef,
    },
    total=False,
)


class CalculatedSpendTypeDef(_RequiredCalculatedSpendTypeDef, _OptionalCalculatedSpendTypeDef):
    pass


BudgetedAndActualAmountsTypeDef = TypedDict(
    "BudgetedAndActualAmountsTypeDef",
    {
        "BudgetedAmount": SpendTypeDef,
        "ActualAmount": SpendTypeDef,
        "TimePeriod": TimePeriodTypeDef,
    },
    total=False,
)

_RequiredDescribeBudgetActionHistoriesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeBudgetActionHistoriesRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "ActionId": str,
    },
)
_OptionalDescribeBudgetActionHistoriesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeBudgetActionHistoriesRequestRequestTypeDef",
    {
        "TimePeriod": TimePeriodTypeDef,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeBudgetActionHistoriesRequestRequestTypeDef(
    _RequiredDescribeBudgetActionHistoriesRequestRequestTypeDef,
    _OptionalDescribeBudgetActionHistoriesRequestRequestTypeDef,
):
    pass


_RequiredDescribeBudgetPerformanceHistoryRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeBudgetPerformanceHistoryRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
    },
)
_OptionalDescribeBudgetPerformanceHistoryRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeBudgetPerformanceHistoryRequestRequestTypeDef",
    {
        "TimePeriod": TimePeriodTypeDef,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeBudgetPerformanceHistoryRequestRequestTypeDef(
    _RequiredDescribeBudgetPerformanceHistoryRequestRequestTypeDef,
    _OptionalDescribeBudgetPerformanceHistoryRequestRequestTypeDef,
):
    pass


CreateBudgetActionResponseTypeDef = TypedDict(
    "CreateBudgetActionResponseTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "ActionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeNotificationsForBudgetResponseTypeDef = TypedDict(
    "DescribeNotificationsForBudgetResponseTypeDef",
    {
        "Notifications": List[NotificationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSubscribersForNotificationResponseTypeDef = TypedDict(
    "DescribeSubscribersForNotificationResponseTypeDef",
    {
        "Subscribers": List[SubscriberTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExecuteBudgetActionResponseTypeDef = TypedDict(
    "ExecuteBudgetActionResponseTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "ActionId": str,
        "ExecutionType": ExecutionTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DefinitionTypeDef = TypedDict(
    "DefinitionTypeDef",
    {
        "IamActionDefinition": IamActionDefinitionTypeDef,
        "ScpActionDefinition": ScpActionDefinitionTypeDef,
        "SsmActionDefinition": SsmActionDefinitionTypeDef,
    },
    total=False,
)

_RequiredDescribeBudgetActionHistoriesRequestDescribeBudgetActionHistoriesPaginateTypeDef = (
    TypedDict(
        "_RequiredDescribeBudgetActionHistoriesRequestDescribeBudgetActionHistoriesPaginateTypeDef",
        {
            "AccountId": str,
            "BudgetName": str,
            "ActionId": str,
        },
    )
)
_OptionalDescribeBudgetActionHistoriesRequestDescribeBudgetActionHistoriesPaginateTypeDef = (
    TypedDict(
        "_OptionalDescribeBudgetActionHistoriesRequestDescribeBudgetActionHistoriesPaginateTypeDef",
        {
            "TimePeriod": TimePeriodTypeDef,
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)


class DescribeBudgetActionHistoriesRequestDescribeBudgetActionHistoriesPaginateTypeDef(
    _RequiredDescribeBudgetActionHistoriesRequestDescribeBudgetActionHistoriesPaginateTypeDef,
    _OptionalDescribeBudgetActionHistoriesRequestDescribeBudgetActionHistoriesPaginateTypeDef,
):
    pass


_RequiredDescribeBudgetActionsForAccountRequestDescribeBudgetActionsForAccountPaginateTypeDef = TypedDict(
    "_RequiredDescribeBudgetActionsForAccountRequestDescribeBudgetActionsForAccountPaginateTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalDescribeBudgetActionsForAccountRequestDescribeBudgetActionsForAccountPaginateTypeDef = TypedDict(
    "_OptionalDescribeBudgetActionsForAccountRequestDescribeBudgetActionsForAccountPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeBudgetActionsForAccountRequestDescribeBudgetActionsForAccountPaginateTypeDef(
    _RequiredDescribeBudgetActionsForAccountRequestDescribeBudgetActionsForAccountPaginateTypeDef,
    _OptionalDescribeBudgetActionsForAccountRequestDescribeBudgetActionsForAccountPaginateTypeDef,
):
    pass


_RequiredDescribeBudgetActionsForBudgetRequestDescribeBudgetActionsForBudgetPaginateTypeDef = TypedDict(
    "_RequiredDescribeBudgetActionsForBudgetRequestDescribeBudgetActionsForBudgetPaginateTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
    },
)
_OptionalDescribeBudgetActionsForBudgetRequestDescribeBudgetActionsForBudgetPaginateTypeDef = TypedDict(
    "_OptionalDescribeBudgetActionsForBudgetRequestDescribeBudgetActionsForBudgetPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeBudgetActionsForBudgetRequestDescribeBudgetActionsForBudgetPaginateTypeDef(
    _RequiredDescribeBudgetActionsForBudgetRequestDescribeBudgetActionsForBudgetPaginateTypeDef,
    _OptionalDescribeBudgetActionsForBudgetRequestDescribeBudgetActionsForBudgetPaginateTypeDef,
):
    pass


_RequiredDescribeBudgetNotificationsForAccountRequestDescribeBudgetNotificationsForAccountPaginateTypeDef = TypedDict(
    "_RequiredDescribeBudgetNotificationsForAccountRequestDescribeBudgetNotificationsForAccountPaginateTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalDescribeBudgetNotificationsForAccountRequestDescribeBudgetNotificationsForAccountPaginateTypeDef = TypedDict(
    "_OptionalDescribeBudgetNotificationsForAccountRequestDescribeBudgetNotificationsForAccountPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeBudgetNotificationsForAccountRequestDescribeBudgetNotificationsForAccountPaginateTypeDef(
    _RequiredDescribeBudgetNotificationsForAccountRequestDescribeBudgetNotificationsForAccountPaginateTypeDef,
    _OptionalDescribeBudgetNotificationsForAccountRequestDescribeBudgetNotificationsForAccountPaginateTypeDef,
):
    pass


_RequiredDescribeBudgetPerformanceHistoryRequestDescribeBudgetPerformanceHistoryPaginateTypeDef = TypedDict(
    "_RequiredDescribeBudgetPerformanceHistoryRequestDescribeBudgetPerformanceHistoryPaginateTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
    },
)
_OptionalDescribeBudgetPerformanceHistoryRequestDescribeBudgetPerformanceHistoryPaginateTypeDef = TypedDict(
    "_OptionalDescribeBudgetPerformanceHistoryRequestDescribeBudgetPerformanceHistoryPaginateTypeDef",
    {
        "TimePeriod": TimePeriodTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeBudgetPerformanceHistoryRequestDescribeBudgetPerformanceHistoryPaginateTypeDef(
    _RequiredDescribeBudgetPerformanceHistoryRequestDescribeBudgetPerformanceHistoryPaginateTypeDef,
    _OptionalDescribeBudgetPerformanceHistoryRequestDescribeBudgetPerformanceHistoryPaginateTypeDef,
):
    pass


_RequiredDescribeBudgetsRequestDescribeBudgetsPaginateTypeDef = TypedDict(
    "_RequiredDescribeBudgetsRequestDescribeBudgetsPaginateTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalDescribeBudgetsRequestDescribeBudgetsPaginateTypeDef = TypedDict(
    "_OptionalDescribeBudgetsRequestDescribeBudgetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeBudgetsRequestDescribeBudgetsPaginateTypeDef(
    _RequiredDescribeBudgetsRequestDescribeBudgetsPaginateTypeDef,
    _OptionalDescribeBudgetsRequestDescribeBudgetsPaginateTypeDef,
):
    pass


_RequiredDescribeNotificationsForBudgetRequestDescribeNotificationsForBudgetPaginateTypeDef = TypedDict(
    "_RequiredDescribeNotificationsForBudgetRequestDescribeNotificationsForBudgetPaginateTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
    },
)
_OptionalDescribeNotificationsForBudgetRequestDescribeNotificationsForBudgetPaginateTypeDef = TypedDict(
    "_OptionalDescribeNotificationsForBudgetRequestDescribeNotificationsForBudgetPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeNotificationsForBudgetRequestDescribeNotificationsForBudgetPaginateTypeDef(
    _RequiredDescribeNotificationsForBudgetRequestDescribeNotificationsForBudgetPaginateTypeDef,
    _OptionalDescribeNotificationsForBudgetRequestDescribeNotificationsForBudgetPaginateTypeDef,
):
    pass


_RequiredDescribeSubscribersForNotificationRequestDescribeSubscribersForNotificationPaginateTypeDef = TypedDict(
    "_RequiredDescribeSubscribersForNotificationRequestDescribeSubscribersForNotificationPaginateTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "Notification": NotificationTypeDef,
    },
)
_OptionalDescribeSubscribersForNotificationRequestDescribeSubscribersForNotificationPaginateTypeDef = TypedDict(
    "_OptionalDescribeSubscribersForNotificationRequestDescribeSubscribersForNotificationPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeSubscribersForNotificationRequestDescribeSubscribersForNotificationPaginateTypeDef(
    _RequiredDescribeSubscribersForNotificationRequestDescribeSubscribersForNotificationPaginateTypeDef,
    _OptionalDescribeSubscribersForNotificationRequestDescribeSubscribersForNotificationPaginateTypeDef,
):
    pass


DescribeBudgetNotificationsForAccountResponseTypeDef = TypedDict(
    "DescribeBudgetNotificationsForAccountResponseTypeDef",
    {
        "BudgetNotificationsForAccount": List[BudgetNotificationsForAccountTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredBudgetTypeDef = TypedDict(
    "_RequiredBudgetTypeDef",
    {
        "BudgetName": str,
        "TimeUnit": TimeUnitType,
        "BudgetType": BudgetTypeType,
    },
)
_OptionalBudgetTypeDef = TypedDict(
    "_OptionalBudgetTypeDef",
    {
        "BudgetLimit": SpendTypeDef,
        "PlannedBudgetLimits": Mapping[str, SpendTypeDef],
        "CostFilters": Mapping[str, Sequence[str]],
        "CostTypes": CostTypesTypeDef,
        "TimePeriod": TimePeriodTypeDef,
        "CalculatedSpend": CalculatedSpendTypeDef,
        "LastUpdatedTime": Union[datetime, str],
        "AutoAdjustData": AutoAdjustDataTypeDef,
    },
    total=False,
)


class BudgetTypeDef(_RequiredBudgetTypeDef, _OptionalBudgetTypeDef):
    pass


BudgetPerformanceHistoryTypeDef = TypedDict(
    "BudgetPerformanceHistoryTypeDef",
    {
        "BudgetName": str,
        "BudgetType": BudgetTypeType,
        "CostFilters": Dict[str, List[str]],
        "CostTypes": CostTypesTypeDef,
        "TimeUnit": TimeUnitType,
        "BudgetedAndActualAmountsList": List[BudgetedAndActualAmountsTypeDef],
    },
    total=False,
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "ActionId": str,
        "BudgetName": str,
        "NotificationType": NotificationTypeType,
        "ActionType": ActionTypeType,
        "ActionThreshold": ActionThresholdTypeDef,
        "Definition": DefinitionTypeDef,
        "ExecutionRoleArn": str,
        "ApprovalModel": ApprovalModelType,
        "Status": ActionStatusType,
        "Subscribers": List[SubscriberTypeDef],
    },
)

CreateBudgetActionRequestRequestTypeDef = TypedDict(
    "CreateBudgetActionRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "NotificationType": NotificationTypeType,
        "ActionType": ActionTypeType,
        "ActionThreshold": ActionThresholdTypeDef,
        "Definition": DefinitionTypeDef,
        "ExecutionRoleArn": str,
        "ApprovalModel": ApprovalModelType,
        "Subscribers": Sequence[SubscriberTypeDef],
    },
)

_RequiredUpdateBudgetActionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBudgetActionRequestRequestTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "ActionId": str,
    },
)
_OptionalUpdateBudgetActionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBudgetActionRequestRequestTypeDef",
    {
        "NotificationType": NotificationTypeType,
        "ActionThreshold": ActionThresholdTypeDef,
        "Definition": DefinitionTypeDef,
        "ExecutionRoleArn": str,
        "ApprovalModel": ApprovalModelType,
        "Subscribers": Sequence[SubscriberTypeDef],
    },
    total=False,
)


class UpdateBudgetActionRequestRequestTypeDef(
    _RequiredUpdateBudgetActionRequestRequestTypeDef,
    _OptionalUpdateBudgetActionRequestRequestTypeDef,
):
    pass


_RequiredCreateBudgetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBudgetRequestRequestTypeDef",
    {
        "AccountId": str,
        "Budget": BudgetTypeDef,
    },
)
_OptionalCreateBudgetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBudgetRequestRequestTypeDef",
    {
        "NotificationsWithSubscribers": Sequence[NotificationWithSubscribersTypeDef],
    },
    total=False,
)


class CreateBudgetRequestRequestTypeDef(
    _RequiredCreateBudgetRequestRequestTypeDef, _OptionalCreateBudgetRequestRequestTypeDef
):
    pass


DescribeBudgetResponseTypeDef = TypedDict(
    "DescribeBudgetResponseTypeDef",
    {
        "Budget": BudgetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBudgetsResponseTypeDef = TypedDict(
    "DescribeBudgetsResponseTypeDef",
    {
        "Budgets": List[BudgetTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBudgetRequestRequestTypeDef = TypedDict(
    "UpdateBudgetRequestRequestTypeDef",
    {
        "AccountId": str,
        "NewBudget": BudgetTypeDef,
    },
)

DescribeBudgetPerformanceHistoryResponseTypeDef = TypedDict(
    "DescribeBudgetPerformanceHistoryResponseTypeDef",
    {
        "BudgetPerformanceHistory": BudgetPerformanceHistoryTypeDef,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ActionHistoryDetailsTypeDef = TypedDict(
    "ActionHistoryDetailsTypeDef",
    {
        "Message": str,
        "Action": ActionTypeDef,
    },
)

DeleteBudgetActionResponseTypeDef = TypedDict(
    "DeleteBudgetActionResponseTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "Action": ActionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBudgetActionResponseTypeDef = TypedDict(
    "DescribeBudgetActionResponseTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "Action": ActionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBudgetActionsForAccountResponseTypeDef = TypedDict(
    "DescribeBudgetActionsForAccountResponseTypeDef",
    {
        "Actions": List[ActionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBudgetActionsForBudgetResponseTypeDef = TypedDict(
    "DescribeBudgetActionsForBudgetResponseTypeDef",
    {
        "Actions": List[ActionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBudgetActionResponseTypeDef = TypedDict(
    "UpdateBudgetActionResponseTypeDef",
    {
        "AccountId": str,
        "BudgetName": str,
        "OldAction": ActionTypeDef,
        "NewAction": ActionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ActionHistoryTypeDef = TypedDict(
    "ActionHistoryTypeDef",
    {
        "Timestamp": datetime,
        "Status": ActionStatusType,
        "EventType": EventTypeType,
        "ActionHistoryDetails": ActionHistoryDetailsTypeDef,
    },
)

DescribeBudgetActionHistoriesResponseTypeDef = TypedDict(
    "DescribeBudgetActionHistoriesResponseTypeDef",
    {
        "ActionHistories": List[ActionHistoryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
