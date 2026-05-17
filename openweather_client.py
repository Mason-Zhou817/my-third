from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

# 封装OpenWeather天气API客户端，用于查询实时天气数据
class OpenWeatherError(RuntimeError):
    """Raised when OpenWeather API cannot return valid weather data."""


@dataclass(frozen=True)
class CurrentWeather:
    city: str
    country: str
    description: str
    temperature: float | int | None
    feels_like: float | int | None
    humidity: int | None
    pressure: int | None
    wind_speed: float | int | None
    wind_degree: int | None
    cloudiness: int | None
    visibility: int | None
    rain_1h: float | int | None
    snow_1h: float | int | None
    updated_at: str
    sunrise: str
    sunset: str
    raw: dict[str, Any]

    def to_text(self, units: str = "metric") -> str:
        temp_unit, wind_unit = unit_labels(units)
        precipitation = []
        if self.rain_1h is not None:
            precipitation.append(f"近1小时降雨: {self.rain_1h} mm")
        if self.snow_1h is not None:
            precipitation.append(f"近1小时降雪: {self.snow_1h} mm")
        precipitation_text = "\n".join(precipitation) or "降水: 无近1小时降水字段"

        return "\n".join(
            [
                f"城市: {self.city}, {self.country}",
                f"天气: {self.description}",
                f"温度: {self.temperature} deg {temp_unit}",
                f"体感温度: {self.feels_like} deg {temp_unit}",
                f"湿度: {self.humidity}%",
                f"气压: {self.pressure} hPa",
                f"风速: {self.wind_speed} {wind_unit}",
                f"风向: {self.wind_degree} deg",
                f"云量: {self.cloudiness}%",
                f"能见度: {self.visibility} m",
                precipitation_text,
                f"数据更新时间: {self.updated_at}",
                f"日出: {self.sunrise}",
                f"日落: {self.sunset}",
            ]
        )


class OpenWeatherClient:
    """Small reusable client for OpenWeather Current Weather API."""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(
        self,
        api_key: str | None = None,
        *,
        units: str = "metric",
        lang: str = "zh_cn",
        timeout: int = 15,
        base_url: str = BASE_URL,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise OpenWeatherError(
                "Missing API key. Set OPENWEATHER_API_KEY or pass api_key=..."
            )

        if units not in {"metric", "imperial", "standard"}:
            raise ValueError("units must be one of: metric, imperial, standard")

        self.units = units
        self.lang = lang
        self.timeout = timeout
        self.base_url = base_url

    def current_by_city(self, city: str) -> CurrentWeather:
        if not city.strip():
            raise ValueError("city cannot be empty")
        data = self._request({"q": city})
        return self.parse_current_weather(data)

    def current_by_coordinates(self, lat: float, lon: float) -> CurrentWeather:
        data = self._request({"lat": lat, "lon": lon})
        return self.parse_current_weather(data)

    def current_raw_by_city(self, city: str) -> dict[str, Any]:
        if not city.strip():
            raise ValueError("city cannot be empty")
        return self._request({"q": city})

    def current_raw_by_coordinates(self, lat: float, lon: float) -> dict[str, Any]:
        return self._request({"lat": lat, "lon": lon})

    def parse_current_weather(self, data: dict[str, Any]) -> CurrentWeather:
        timezone_offset = int(data.get("timezone", 0))
        weather = (data.get("weather") or [{}])[0]
        main = data.get("main", {})
        wind = data.get("wind", {})
        clouds = data.get("clouds", {})
        sys_data = data.get("sys", {})

        return CurrentWeather(
            city=data.get("name", "N/A"),
            country=sys_data.get("country", "N/A"),
            description=weather.get("description", "N/A"),
            temperature=main.get("temp"),
            feels_like=main.get("feels_like"),
            humidity=main.get("humidity"),
            pressure=main.get("pressure"),
            wind_speed=wind.get("speed"),
            wind_degree=wind.get("deg"),
            cloudiness=clouds.get("all"),
            visibility=data.get("visibility"),
            rain_1h=data.get("rain", {}).get("1h"),
            snow_1h=data.get("snow", {}).get("1h"),
            updated_at=city_time(data.get("dt"), timezone_offset),
            sunrise=city_time(sys_data.get("sunrise"), timezone_offset),
            sunset=city_time(sys_data.get("sunset"), timezone_offset),
            raw=data,
        )

    def _request(self, params: dict[str, str | float]) -> dict[str, Any]:
        query_params: dict[str, str | float] = {
            "appid": self.api_key,
            "units": self.units,
            "lang": self.lang,
            **params,
        }
        url = f"{self.base_url}?{urllib.parse.urlencode(query_params)}"
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "python-openweather-client/1.0"},
            method="GET",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                payload = response.read().decode(charset)
        except urllib.error.HTTPError as exc:
            raise OpenWeatherError(self._http_error_message(exc)) from exc
        except urllib.error.URLError as exc:
            raise OpenWeatherError(f"Network request failed: {exc.reason}") from exc

        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise OpenWeatherError("API returned data that is not valid JSON.") from exc

        if str(data.get("cod")) != "200":
            raise OpenWeatherError(
                f"API returned an error: {data.get('message', data)}"
            )

        return data

    @staticmethod
    def _http_error_message(exc: urllib.error.HTTPError) -> str:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            error_data = json.loads(body)
            message = error_data.get("message", body)
        except json.JSONDecodeError:
            message = body or exc.reason
        return f"API request failed: HTTP {exc.code}, {message}"


def city_time(unix_seconds: int | None, offset_seconds: int) -> str:
    if unix_seconds is None:
        return "N/A"
    tz = timezone(timedelta(seconds=offset_seconds))
    return datetime.fromtimestamp(unix_seconds, tz=tz).strftime("%Y-%m-%d %H:%M:%S")


def unit_labels(units: str) -> tuple[str, str]:
    if units == "imperial":
        return "F", "mph"
    if units == "standard":
        return "K", "m/s"
    return "C", "m/s"
