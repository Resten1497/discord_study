import json
import telegram
import requests
import xmltodict


def bus_response(data):
    id = data
    url = 'http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?serviceKey=API_KEY&arsId={}'.format(id)
    # API_KEY 에 발급받은 api key 입력  
    data = requests.get(url)

    dict_type = xmltodict.parse(data.text)
    json_type = json.dumps(dict_type)
    res = json.loads(json_type)

    return res

# def telegram_sendMessage():
#
#


if __name__ == '__main__':
    print(bus_response("03567")['ServiceResult']['msgBody']['itemList']['arrmsg1'])