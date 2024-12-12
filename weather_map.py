import requests
from bs4 import BeautifulSoup
import lxml.html

# 目标URL
url = 'http://www.weather.com.cn/radar/'

# 发送HTTP请求获取网页内容
response = requests.get(url)
response.encoding = 'utf-8'  # 根据网页的编码设置

# 使用BeautifulSoup解析网页内容
soup = BeautifulSoup(response.text, 'lxml')

# 如果网页内容是由JavaScript动态生成的，可能需要使用Selenium或其他工具来获取渲染后的页面

# 保存获取的HTML内容到本地文件
with open('weather_map1.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

print('天气地图HTML已保存到weather_map.html')
