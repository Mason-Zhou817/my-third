from openweather_client import OpenWeatherClient

client = OpenWeatherClient(units="metric", lang="zh_cn", cache_ttl_seconds=600)
# 查询上海的实时天气数据
weather = client.current_by_city("Shanghai,CN")
print(weather.temperature)
print(weather.description)
print(weather.to_text())
