from packages.contracts.ecosystem import Capability
READ_CAPABILITIES=frozenset(Capability)
def is_read_only(capability:Capability)->bool: return capability in READ_CAPABILITIES
