#!/usr/bin/env python3
"""
Fetch real-time weather data from OpenWeather Current Weather API.

Register an account at https://openweathermap.org/, create an API key, then set:

PowerShell:
    $env:OPENWEATHER_API_KEY="your_api_key"

Run:
    python weather_realtime.py --city "Shanghai,CN"
    python weather_realtime.py --lat 31.2304 --lon 121.4737
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any


API_URL = "https://api.openweathermap.org/data/2.5/weather"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call OpenWeather API and print real-time weather data."
    )
    location = parser.add_mutually_exclusive_group(required=True)
    location.add_argument(
        "--city",
        help='City query, for example "Shanghai,CN", "Beijing,CN", or "London,GB".',
    )
    location.add_argument(
        "--lat",
        type=float,
        help="Latitude. Must be used together with --lon.",
    )
    parser.add_argument(
        "--lon",
        type=float,
        help="Longitude. Required when --lat is used.",
    )
    parser.add_argument(
        "--units",
        choices=("metric", "imperial", "standard"),
        default="metric",
        help="metric=Celsius, imperial=Fahrenheit, standard=Kelvin.",
    )
    parser.add_argument(
        "--lang",
        default="zh_cn",
        help='Response language code, for example "zh_cn" or "en".',
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print raw JSON response instead of parsed summary.",
    )
    return parser.parse_args()


def build_params(args: argparse.Namespace, api_key: str) -> dict[str, str | float]:
    if args.lat is not None and args.lon is None:
        raise ValueError("--lon is required when --lat is used.")

    params: dict[str, str | float] = {
        "appid": api_key,
        "units": args.units,
        "lang": args.lang,
    }

    if args.city:
        params["q"] = args.city
    else:
        params["lat"] = args.lat
        params["lon"] = args.lon

    return params


def fetch_weather(params: dict[str, str | float]) -> dict[str, Any]:
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "python-openweather-demo/1.0"},
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            payload = response.read().decode(charset)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            error_data = json.loads(body)
            message = error_data.get("message", body)
        except json.JSONDecodeError:
            message = body or exc.reason
        raise RuntimeError(f"API request failed: HTTP {exc.code}, {message}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network request failed: {exc.reason}") from exc

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError("API returned data that is not valid JSON.") from exc

    if str(data.get("cod")) != "200":
        raise RuntimeError(f"API returned an error: {data.get('message', data)}")

    return data


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


def optional_precipitation(data: dict[str, Any]) -> str:
    rain_1h = data.get("rain", {}).get("1h")
    snow_1h = data.get("snow", {}).get("1h")
    parts = []
    if rain_1h is not None:
        parts.append(f"近1小时降雨: {rain_1h} mm")
    if snow_1h is not None:
        parts.append(f"近1小时降雪: {snow_1h} mm")
    return "\n".join(parts) if parts else "降水: 无近1小时降水字段"


def format_summary(data: dict[str, Any], units: str) -> str:
    temp_unit, wind_unit = unit_labels(units)
    timezone_offset = int(data.get("timezone", 0))
    weather = (data.get("weather") or [{}])[0]
    main = data.get("main", {})
    wind = data.get("wind", {})
    clouds = data.get("clouds", {})
    sys_data = data.get("sys", {})

    lines = [
        f"城市: {data.get('name', 'N/A')}, {sys_data.get('country', 'N/A')}",
        f"天气: {weather.get('description', 'N/A')}",
        f"温度: {main.get('temp', 'N/A')} deg {temp_unit}",
        f"体感温度: {main.get('feels_like', 'N/A')} deg {temp_unit}",
        f"湿度: {main.get('humidity', 'N/A')}%",
        f"气压: {main.get('pressure', 'N/A')} hPa",
        f"风速: {wind.get('speed', 'N/A')} {wind_unit}",
        f"风向: {wind.get('deg', 'N/A')} deg",
        f"云量: {clouds.get('all', 'N/A')}%",
        f"能见度: {data.get('visibility', 'N/A')} m",
        optional_precipitation(data),
        f"数据更新时间: {city_time(data.get('dt'), timezone_offset)}",
        f"日出: {city_time(sys_data.get('sunrise'), timezone_offset)}",
        f"日落: {city_time(sys_data.get('sunset'), timezone_offset)}",
    ]
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print(
            "Missing API key. Set OPENWEATHER_API_KEY first, for example:\n"
            'PowerShell: $env:OPENWEATHER_API_KEY="your_api_key"',
            file=sys.stderr,
        )
        return 2

    try:
        params = build_params(args, api_key)
        data = fetch_weather(params)
    except ValueError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_summary(data, args.units))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
