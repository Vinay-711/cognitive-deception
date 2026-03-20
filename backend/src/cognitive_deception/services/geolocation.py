from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GeoInfo:
    city: str
    country: str
    region: str


def geolocate(ip_address: str) -> GeoInfo:
    """Deterministic offline geolocation for demos.

    This avoids external API calls while providing stable geographic labels.
    """
    try:
        last = int(ip_address.split(".")[-1])
    except Exception:
        last = 0

    if last % 5 == 0:
        return GeoInfo(city="Singapore", country="SG", region="APAC")
    if last % 5 == 1:
        return GeoInfo(city="Frankfurt", country="DE", region="EU")
    if last % 5 == 2:
        return GeoInfo(city="Virginia", country="US", region="NA")
    if last % 5 == 3:
        return GeoInfo(city="Sao Paulo", country="BR", region="LATAM")
    return GeoInfo(city="Johannesburg", country="ZA", region="AFRICA")
