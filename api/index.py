from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='../templates')

# (1) 台中市十大易肇事路口名單
ROAD_DATA = [
    "西屯區：環中路與市政路口",
    "北區：中清路與五權路口",
    "北區：太原路與崇德路口",
    "烏日區：高鐵東路與高鐵五路口",
    "神岡區：中山路與大富路口",
    "北屯區：環中東路與太原路口",
    "太平區：市民大道與環中東路口",
    "神岡區：中山路與大洲路口",
    "西區：台灣大道與五權路口",
    "西屯區：台灣大道與黎明路口"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_info = None
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        # (2) 串接氣象署 API
        # 請記得去 https://opendata.cwa.gov.tw/ 申請金鑰並替換下方字串
        api_key = "YOUR_CWA_API_KEY" 
        url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}&locationName={city}&elementName=Wx,PoP"
        
        try:
            res = requests.get(url).json()
            if res.get('success') == 'true' and res['records']['location']:
                loc = res['records']['location'][0]
                wx = loc['weatherElement'][0]['time'][0]['parameter']['parameterName']
                pop = loc['weatherElement'][1]['time'][0]['parameter']['parameterName']
                weather_info = {"city": city, "wx": wx, "pop": pop}
            else:
                weather_info = {"error": "查無資料，請輸入正確縣市名稱（如：臺中市）"}
        except:
            weather_info = {"error": "系統連線錯誤或 API 金鑰失效"}

    return render_template('index.html', roads=ROAD_DATA, weather=weather_info)
