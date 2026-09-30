from packages.contracts.change import ChangeType
def classify(before,after,source_changed=False,source_available=True)->ChangeType:
 if not source_available: return ChangeType.SOURCE_OUTAGE
 if source_changed and before==after: return ChangeType.SOURCE_CORRECTION
 if before is None and after is not None: return ChangeType.CREATED
 if before is not None and after is None: return ChangeType.REMOVED
 return ChangeType.MODIFIED if before!=after else ChangeType.SOURCE_CORRECTION
def significance(before,after)->float:
 return 0.0 if before==after else 1.0
