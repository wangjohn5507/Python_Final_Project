import requests
import urllib.request
import pandas as pd
import json
import ssl
import folium
import time

address=input('請輸入您所在的地址')
# Cwidth=int(input('請輸入範圍:i.e.100'))

def get_latitude_longtitude(address):
    # decode url
    address = urllib.parse.quote(address)
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address +"&key=AIzaSyCvd8PK5-AK2wYaTqYvOTUwAbiAK2znIKk"

    while True:
        res = requests.get(url)
        js = json.loads(res.text)

        if js["status"] != "OVER_QUERY_LIMIT":
            time.sleep(1)
            break

    result = js["results"][0]["geometry"]["location"]
    lat = result["lat"]
    lng = result["lng"]

    return lat, lng


# address = "桃園市桃園區縣府路1號"
lat, lng = get_latitude_longtitude(address)


url = 'https://data.tycg.gov.tw/opendata/datalist/datasetMeta/download?id=f4cc0b12-86ac-40f9-8745-885bddc18f79&rid=0daad6e6-0632-44f5-bd25-5e1de1e9146f'
context = ssl._create_unverified_context()
with urllib.request.urlopen(url, context=context) as jsondata:
    data = json.loads(jsondata.read().decode())
# print(data)
x=lat
y=lng
fmap = folium.Map(location=[x, y], zoom_start=17)
data = data['parkingLots']
fmap.add_child(folium.Marker(location=[lat,lng],popup='現在位置',icon=folium.Icon(color='red')))
fmap.add_child(folium.Circle(location=[lat,lng],
                             color='green', # Circle 顏色
                             # radius=Cwidth, # Circle 寬度
                             radius=500, # Circle 寬度
                             # popup='', # 彈出視窗內容
                             fill=True, # 填滿中間區域
                             fill_opacity=0.5 # 設定透明度
                             ))
for d in data:
    print("{}:{}".format(d['parkName'], d['surplusSpace']))
    if(d['surplusSpace']!='0'):
        # if(x-Cwidth/100000<d['wgsY']<x+Cwidth/100000 and y-Cwidth/100000<d['wgsX']<y+Cwidth/100000):
        #     fmap.add_child(folium.Marker(location=[d['wgsY'], d['wgsX']],
        #                                  popup=d['parkName']+d['surplusSpace']))
        if (x - 500/ 100000 < d['wgsY'] < x + 500 / 100000 and y - 500 / 100000 < d[
            'wgsX'] < y + 500 / 100000):
            fmap.add_child(folium.Marker(location=[d['wgsY'], d['wgsX']],
                                        popup=d['parkName'] + d['surplusSpace']))
fmap.save("fmap.html")



