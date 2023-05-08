#----------Library----------

from flask import Flask, jsonify, render_template, request, render_template_string
import keras
import requests
import json
from sklearn.preprocessing import MinMaxScaler
from difflib import SequenceMatcher
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import pandas as pd

#----------Data----------
file_data = '../data/final_data_street_price_update.csv'
file_info = '../data/final_data_street_price_update_info.csv'
data = pd.read_csv(file_data)

#----------Normalize----------

# data["price"] = np.log(data["price"])
# 1 billion
one_billion = 1000000000
data["price"] = data["price"]/one_billion
X = data.drop("price", axis=1)
y = data["price"]
scaler = MinMaxScaler()
feature_minmax_transform_data = scaler.fit_transform(X)
X = pd.DataFrame(columns=X.columns, data=feature_minmax_transform_data)

#----------Functions----------

#Hàm tạo dictionary với key là tên đường và value số thứ tự của tên đường trong mảng tên đường đã được sắp xếp
def create_street_name_list():
    data_info = pd.read_csv(file_info)

    streets_info = data_info['street'].values
    streets_info = list(set(streets_info))
    streets_info.sort()
    street_info_list = dict()
    for i in range(len(streets_info)):
        street_info_list.update({streets_info[i]: i})
    return street_info_list

#Hàm tạo dictionary với key là số thứ tự của id đường trong mảng id đường đã được sắp xếp và value là id đường
def create_street_id_list():
    data = pd.read_csv(file_data)
    streets = data['street'].values
    streets = list(set(streets))
    streets.sort()
    street_list = dict()
    for i in range(len(streets)):
        street_list.update({i: streets[i]})
    return street_list
  
#Hàm lấy id đường từ tên đường đã nhập
def get_street_id(street_name):
    street_name = street_name.lower().strip()
    street_info_list = create_street_name_list()
    street_list = create_street_id_list()
    idx = street_info_list[street_name]
    return street_list[idx]
    
#Hàm lấy tên đường giống nhất với tên đường người dùng nhập
def get_best_street_name(street_name):
    data_info = pd.read_csv(file_info)
    streets = data_info['street'].values
    streets = list(set(streets))
    streets.sort()
    street_list = dict()
    for i in range(len(streets)):
        sim = SequenceMatcher(None, street_name.lower(), streets[i].lower()).ratio()
        street_list.update({streets[i]: sim})
    street_name = max(street_list, key=street_list.get)
    return street_name
       
#Hàm gán id tốt nhất cho tên đường người dùng nhập
def get_best_street_id(street_name):
    street_name = get_best_street_name(street_name)
    return get_street_id(street_name)
    
#Hàm tạo dictionary với key là tên quận huyện và value là id
def create_area_list():
    districts = ["quận " + str(i+1) for i in range(12)]
    districts.extend(["quận bình tân","quận bình thạnh","quận gò vấp","quận phú nhuận","quận tân bình","quận tân phú","huyện bình chánh","huyện cần giờ","huyện củ chi","huyện hóc môn","huyện nhà bè"])

    temp_area = 96
    area_list = dict()

    for i in range(len(districts)):
        area_list.update({districts[i]: temp_area+i})
    return area_list
        
#Hàm lấy id quận, huyện
def get_area_id(district):
    district = district.lower().strip()
    area_list = create_area_list()
    area_id = area_list[district]
    return area_id

#Hàm tạo dictionary chứa danh sách tên phường của quận, key là tên phường và value là id phường
def create_wards_name_list(district):
    columns = ['area','ward']
    data = pd.read_csv(file_data)
    area_id = get_area_id(district)
    data_area_ward = data[columns].values
    wards_list = []
    for i in range(len(data_area_ward)):
        if data_area_ward[i][0] == area_id:
            temp = data_area_ward[i][1]
            if temp not in wards_list:
                wards_list.append(temp)
    wards_name_list = dict()
    for ward in wards_list:
        api = "https://gateway.chotot.com/v1/public/ad-listing?region_v2=13000&area_v2=" + str(13000+area_id) + "&cg=1020&o=20&page=2&ward="+ str(ward) + "&st=s,k&limit=20&w=1&key_param_included=true"
        API_request = requests.get(api)
        if API_request.status_code == 404:
            break
        data_text = API_request.text
        parse_json = json.loads(data_text)
        for info in parse_json['ads']:
            if info['ward_name'].lower() not in wards_name_list:
                wards_name_list.update({info['ward_name'].lower(): ward})
                break
    return wards_name_list

#Hàm khởi tạo các giá trị cần dự đoán dựa vào thông tin người dùng nhập
def get_predictive_items(size, width, length, room, toilet, floor, house_type, street_name, district, ward_name):
    wards_name_list = create_wards_name_list(district)
    ward_id = wards_name_list[ward_name.lower()]
    street_id = get_best_street_id(street_name)
    area_id = get_area_id(district)
    predictive_item = [[size, width, length, int(room), area_id, ward_id, int(toilet), int(floor), house_type, street_id]]
    predictive_item = np.array(predictive_item)
    feature_minmax_transform_data = scaler.transform(predictive_item)
    return feature_minmax_transform_data

#----------Deploy model on the Web by Flask----------
app = Flask(__name__)

one_billion = 1000000000
model_name = "model_CNN.h5"

#Hàm lấy danh sách tên quận, huyện tại TPHCM
@app.route("/")
def index():
    return render_template("index.html")

#Hàm lấy danh sách tên quận, huyện tại TPHCM
@app.route('/wards_name', methods = ['POST'])
def wards_name():
    data = request.form.to_dict(flat=True)
    data['district'] = data.get('district')
    data['wards'] = list(create_wards_name_list(data.get('district')).keys())
    return render_template('index.html', data = data)

#Hàm dự đoán giá nhà dựa vào thông tin người dùng đã nhập
@app.route('/predict', methods = ['POST'])
def predict():
    info_predict_list = request.form.to_dict(flat=True)
    size = float(info_predict_list.get('size'))
    width = float(info_predict_list.get('width'))
    length = float(info_predict_list.get('length'))
    room = int(info_predict_list.get('room'))
    toilet = int(info_predict_list.get('toilet'))
    floor = int(info_predict_list.get('floor'))
    house_type = int(info_predict_list.get('house_type'))
    item = get_predictive_items(size, width, length, room, toilet, floor, house_type, info_predict_list.get('street_name'), info_predict_list.get('district'),info_predict_list.get('ward_name'))
    X_predict_CNN = item.reshape(item.shape[0], item.shape[1], 1)
    predict = model.predict(X_predict_CNN)
    info_predict_list['prediction'] = predict[0][0]
    return render_template('index.html', info_predict_list = info_predict_list)

if __name__ == "__main__":
    model = keras.models.load_model(model_name)
    app.run(debug=True)