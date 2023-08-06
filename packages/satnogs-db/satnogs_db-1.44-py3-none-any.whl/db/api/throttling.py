"""SatNOGS DB API throttling classes, django rest framework"""
from rest_framework import throttling


class GetTelemetryAnononymousRateThrottle(throttling.AnonRateThrottle):
    """Anonymous GET Throttling"""
    scope = 'get_telemetry_anon'

    def allow_request(self, request, view):
        if request.method == "POST":
            return True
        return super().allow_request(request, view)


class GetTelemetryUserRateThrottle(throttling.UserRateThrottle):
    """User GET Throttling"""
    scope = 'get_telemetry_user'

    def allow_request(self, request, view):
        if request.method == "POST":
            return True
        return super().allow_request(request, view)
