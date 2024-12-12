import json
import pandas as pd
import requests
from flask import Flask, render_template_string, render_template, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

location = {
    '济南市': 370100,
    '青岛市': 370200,
    '淄博市': 370300,
    '枣庄市': 370400,
    '东营市': 370500,
    '烟台市': 370600,
    '潍坊市': 370700,
    '济宁市': 370800,
    '泰安市': 370900,
    '威海市': 371000,
    '日照市': 371100,
    '临沂市': 371300,
    '德州市': 371400,
    '聊城市': 371500,
    '滨州市': 371600,
    '菏泽市': 371700
}

ak = "4WqrZlJcrjVJG6IBGeFpScg6Fp7uQf2R"
#4WqrZlJcrjVJG6IBGeFpScg6Fp7uQf2R
#8KwJIv6FvvPC5LpBOOBwQSeqSPDsuP3Q

def get_data_test(loc):
    # district_id 是 地区行政区划码 ak是百度地图申请的ak
    selected_id = location[loc]
    url = f'https://api.map.baidu.com/weather/v1/?district_id={selected_id}&data_type=all&ak={ak}'
    # url = f'https://api.map.baidu.com/weather/v1/?district_id={selected_id}&data_type=all&ak=你的ak'
    response = requests.get(url)
    #print(response.json())
    # 解析JSON字符串
    data = json.loads(response.text)

    forecasts = data['result']['forecasts']
    now_data = data['result']['now']
    # 打印天气预报信息
    #print(now_data)
    # print(forecasts)
    return now_data, forecasts


current_weather_data = {}
def update_weather_data():
    global current_weather_data
    for city in location.keys():
        now_data, forecasts = get_data_test(city)
        current_weather_data[city] = {
            'now_data': now_data,
            'forecasts': forecasts
        }
        #print(f"Weather data updated for {city}.")

#先初始化数据
update_weather_data()

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_weather_data, trigger='interval', minutes=3)
scheduler.start()


@app.route('/newdata', methods=['POST'])
def newdata():
    request_data = request.get_json()
    city_name = request_data.get('city_name')
    if city_name=='jinan':
        city_name='济南市'
    elif city_name=='dezhou':
        city_name='德州市'
    elif city_name == 'liaocheng':
        city_name = '聊城市'
    elif city_name == 'heze':
        city_name = '菏泽市'
    elif city_name == 'jining':
        city_name = '济宁市'
    elif city_name == 'taian':
        city_name = '泰安市'
    elif city_name == 'zaozhuang':
        city_name = '枣庄市'
    elif city_name == 'linyi':
        city_name = '临沂市'
    elif city_name == 'rizhao':
        city_name = '日照市'
    elif city_name == 'zibo':
        city_name = '淄博市'
    elif city_name == 'binzhou':
        city_name = '滨州市'
    elif city_name == 'dongying':
        city_name = '东营市'
    elif city_name == 'weifang':
        city_name = '潍坊市'
    elif city_name == 'qingdao':
        city_name = '青岛市'
    elif city_name == 'yantai':
        city_name = '烟台市'
    elif city_name == 'weihai':
        city_name = '威海市'

    city_data = current_weather_data[city_name]
    now_data = city_data['now_data']
    forecasts = city_data['forecasts']
    data = {
        "city_name": city_name,
        "weather_now": now_data['text'],
        "temptigan_now": now_data['feels_like'],
        "temp_now": now_data['temp'],
        "fengji_now": now_data['wind_class'],
        "shidu_now": now_data['rh'],
        "fangxiang_now": now_data['wind_dir'],
        "time_now": now_data['uptime'],
        "weather_day": [forecast['text_day'] for forecast in forecasts],
        "weather_night": [forecast['text_night'] for forecast in forecasts],
        "temp_min": [forecast['low'] for forecast in forecasts],
        "temp_max": [forecast['high'] for forecast in forecasts],
        "time": [forecast['date'] for forecast in forecasts],
        "week": [forecast['week'] for forecast in forecasts],
        "fangxiang_day": [forecast['wd_day'] for forecast in forecasts],
        "fangxiang_night": [forecast['wd_night'] for forecast in forecasts],
        "fengji_day": [forecast['wc_day'] for forecast in forecasts],
        "fengji_night": [forecast['wc_night'] for forecast in forecasts]
    }
    return jsonify(data)

@app.route('/dezhou')
def dezhou():
    city_data = current_weather_data['德州市']
    now_data = city_data['now_data']
    forecasts = city_data['forecasts']
    return render_template('city.html', city_name='德州',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])

@app.route('/jinan')
def jinan():
    city_data = current_weather_data['济南市']
    now_data = city_data['now_data']
    forecasts = city_data['forecasts']
    return render_template('city.html', city_name='济南',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/liaocheng')
def liaocheng():
    city_data = current_weather_data['聊城市']
    now_data = city_data['now_data']
    forecasts = city_data['forecasts']
    return render_template('city.html', city_name='聊城',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/jining')
def jining():
    city_data = current_weather_data['济宁市']
    now_data = city_data['now_data']
    forecasts = city_data['forecasts']
    return render_template('city.html', city_name='济宁',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/weifang')
def weifang():
    city_data = current_weather_data['潍坊市']
    now_data = city_data['now_data']
    forecasts = city_data['forecasts']
    return render_template('city.html', city_name='潍坊',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/heze')
def heze():
    city_data = current_weather_data['菏泽市']
    now_data = city_data['now_data']
    forecasts = city_data['forecasts']
    return render_template('city.html', city_name='菏泽',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/yantai')
def yantai():
    city_data = current_weather_data['烟台市']
    now_data = city_data['now_data']
    forecasts = city_data['forecasts']
    return render_template('city.html', city_name='烟台',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/weihai')
def weihai():
    city_data = current_weather_data['威海市']
    now_data = city_data['now_data']
    forecasts = city_data['forecasts']
    return render_template('city.html', city_name='威海',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/qingdao')
def qingdao():
    city_data = current_weather_data['青岛市']
    now_data = city_data['now_data']
    forecasts = city_data['forecasts']
    return render_template('city.html', city_name='青岛',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/rizhao')
def rizhao():
    city_data = current_weather_data['日照市']
    now_data = city_data['now_data']
    forecasts = city_data['forecasts']
    return render_template('city.html', city_name='日照',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/dongying')
def dongying():
    now_data, forecasts = get_data_test('东营市')
    return render_template('city.html', city_name='东营',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/zaozhuang')
def zaozhuang():
    now_data, forecasts = get_data_test('枣庄市')
    return render_template('city.html', city_name='枣庄',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/linyi')
def linyi():
    now_data, forecasts = get_data_test('临沂市')
    return render_template('city.html', city_name='临沂',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/zibo')
def zibo():
    now_data, forecasts = get_data_test('淄博市')
    return render_template('city.html', city_name='淄博',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/taian')
def taian():
    now_data, forecasts = get_data_test('泰安市')
    return render_template('city.html', city_name='泰安',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/binzhou')
def binzhou():
    now_data, forecasts = get_data_test('滨州市')
    return render_template('city.html', city_name='滨州',
                           weather_now=now_data['text'],
                           temptigan_now=now_data['feels_like'],
                           temp_now=now_data['temp'],
                           fengji_now=now_data['wind_class'],
                           shidu_now=now_data['rh'],
                           fangxiang_now=now_data['wind_dir'],
                           time_now=now_data['uptime'],

                           weather_day=[forecast['text_day'] for forecast in forecasts],
                           weather_night=[forecast['text_night'] for forecast in forecasts],
                           temp_min=[forecast['low'] for forecast in forecasts],
                           temp_max=[forecast['high'] for forecast in forecasts],
                           time=[forecast['date'] for forecast in forecasts],
                           week=[forecast['week'] for forecast in forecasts],
                           fangxiang_day=[forecast['wd_day'] for forecast in forecasts],
                           fangxiang_night=[forecast['wd_night'] for forecast in forecasts],
                           fengji_day=[forecast['wc_day'] for forecast in forecasts],
                           fengji_night=[forecast['wc_night'] for forecast in forecasts])


@app.route('/')
def home():
    return render_template('weather_map.html')


@app.route('/weather_map')
def weather_map():
    return render_template('weather_map.html')


if __name__ == '__main__':
    app.run(port=8080, debug=True)
