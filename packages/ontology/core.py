"""Minimal universal ontology for the intelligence fabric."""
from enum import StrEnum

class EntityType(StrEnum):
    PERSON="person"; ORGANIZATION="organization"; COMPANY="company"; GOVERNMENT="government"
    COUNTRY="country"; REGION="region"; CITY="city"; FACILITY="facility"
    INFRASTRUCTURE="infrastructure"; ASSET="asset"; NATURAL_FEATURE="natural_feature"
    TECHNOLOGY="technology"; SOFTWARE="software"; DOMAIN="domain"; NETWORK_ASSET="network_asset"

class EventType(StrEnum):
    GENERIC="generic"; CONFLICT="conflict"; DISASTER="disaster"; POLICY_CHANGE="policy_change"
    CORPORATE="corporate"; CYBER_INCIDENT="cyber_incident"; INFRASTRUCTURE="infrastructure"
    WEATHER="weather"; SECURITY_DISCLOSURE="security_disclosure"

class RelationshipType(StrEnum):
    OWNS="owns"; OPERATES="operates"; LOCATED_IN="located_in"; AFFECTS="affects"
    LEADS="leads"; PARTNERS_WITH="partners_with"; RELATED_TO="related_to"

class IntelligenceObjectType(StrEnum):
    SOURCE="source"; ARTIFACT="artifact"; OBSERVATION="observation"; EVIDENCE="evidence"
    ENTITY="entity"; EVENT="event"; RELATIONSHIP="relationship"; CHANGE="change"
    SIGNAL="signal"; INTELLIGENCE="intelligence"
