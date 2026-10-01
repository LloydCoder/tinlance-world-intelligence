"""Deterministic temporal filtering and point-distance query helpers."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_M=6_371_008.8

@dataclass(frozen=True, slots=True)
class TemporalRecord:
    record_id: str
    valid_from: datetime
    valid_to: datetime | None
    known_at: datetime

@dataclass(frozen=True, slots=True)
class PointRecord(TemporalRecord):
    latitude: float
    longitude: float

def valid_at(record: TemporalRecord, when: datetime) -> bool:
    return record.valid_from <= when and (record.valid_to is None or when < record.valid_to)

def known_at_or_before(record: TemporalRecord, cutoff: datetime) -> bool:
    return record.known_at <= cutoff

def haversine_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    if not -90 <= lat1 <= 90 or not -90 <= lat2 <= 90:
        raise ValueError("latitude must be -90..90")
    if not -180 <= lon1 <= 180 or not -180 <= lon2 <= 180:
        raise ValueError("longitude must be -180..180")
    dlat=radians(lat2-lat1); dlon=radians(lon2-lon1)
    a=sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return EARTH_RADIUS_M*2*asin(sqrt(a))

def query_points(records: list[PointRecord], *, latitude: float, longitude: float, radius_meters: float,
                 world_at: datetime | None=None, known_at_cutoff: datetime | None=None) -> tuple[PointRecord, ...]:
    if radius_meters < 0:
        raise ValueError("radius_meters must be non-negative")
    result=[]
    for record in records:
        if world_at is not None and not valid_at(record, world_at):
            continue
        if known_at_cutoff is not None and not known_at_or_before(record, known_at_cutoff):
            continue
        if haversine_meters(latitude,longitude,record.latitude,record.longitude) <= radius_meters:
            result.append(record)
    return tuple(result)
