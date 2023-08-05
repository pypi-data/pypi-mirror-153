class Rule:

    def __init__(self, id, name, description, createdAt, updatedAt, backingAssets, thresholdLevel, archivalReason=None,
                 archived=False, enabled=False, schedule=None, notificationChannels=None, **kwargs):
        self.id = id
        self.name = name
        self.description = description
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.backingAssets = backingAssets
        self.thresholdLevel = thresholdLevel
        self.archivalReason = archivalReason
        self.archived = archived
        self.enabled = enabled
        self.schedule = schedule
        self.notificationChannels = notificationChannels

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"Rule({self.__dict__})"


class RuleCancelResponse:

    def __init__(self, message, status, **kwargs):
        self.status = status
        self.message = message

    def __repr__(self):
        return f"Response({self.__dict__})"


class RuleExecution:

    def __init__(self, ruleId, ruleName, thresholdLevel, startedAt, resultStatus, executionStatus, executionMode
                 , ruleType=None, id=None, lastMarker=None, executionError=None, rightLastMarker=None,
                 leftLastMarker=None, finishedAt=None, **kwargs):
        self.ruleId = ruleId
        self.ruleName = ruleName
        self.thresholdLevel = thresholdLevel
        self.startedAt = startedAt
        self.resultStatus = resultStatus
        self.executionStatus = executionStatus
        self.executionMode = executionMode
        self.ruleType = ruleType
        self.executionError = executionError
        self.rightLastMarker = rightLastMarker
        self.lastMarker = lastMarker
        self.leftLastMarker = leftLastMarker
        self.id = id
        self.finishedAt = finishedAt

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"RuleExecution({self.__dict__})"


class RuleExecutionResult:

    def __init__(self, status, ruleExecutionType, qualityScore, description, failedRows, failureCount, rows, successCount,  **kwargs):
        self.status = status
        self.ruleExecutionType = ruleExecutionType
        self.description = description
        self.failedRows = failedRows
        self.failureCount = failureCount
        self.qualityScore = qualityScore
        self.rows = rows
        self.successCount = successCount

class ExecutionResult:

    def __init__(self, execution, items, meta = None, result= None, **kwargs):
        if isinstance(execution, dict):
            self.execution = RuleExecution(**execution)
        else:
            self.execution = execution
        if isinstance(result, dict):
            self.result = RuleExecutionResult(**result)
        else:
            self.result = result
        self.items = items
        self.meta = meta

    def __repr__(self):
        return f"ExecutionResult({self.__dict__})"
