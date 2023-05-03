import requests
import json
import pandas as pd

from numpy import NaN
def Crawl_Data(page_start, page_end):
  subject = []
  price = []
  size = []
  width = []
  length = []
  room = []
  area = []
  ward = []
  toilet = []
  living_size = []
  floor = []
  house_type = []
  street = []
  direction = []
  zero_deposit = []
  escrow_can_deposit = []
  protection_entitlement = []
  property_legal_document = []
  furnishing_sell = []
  for page in range(page_start, page_end+1):
    o = 20 * (page-1)
    api = "https://gateway.chotot.com/v1/public/ad-listing?region_v2=13000&cg=1020&o=" + str(o) + "&page=" + str(page) + "&st=s,k&limit=20&w=1&key_param_included=true"
    API_request = requests.get(api)
    if API_request.status_code == 404:
      break
    data = API_request.text
    parse_json = json.loads(data)
    for data in parse_json['ads']:
      if data['date'] == "7 tháng trước":
        return True
      subject.append(data['subject']) if 'subject' in data else subject.append(NaN)
      price.append(data['price']) if 'price' in data else price.append(0)
      size.append(data['size']) if 'size' in data else size.append(NaN)
      width.append(data['width']) if 'width' in data else width.append(NaN)
      length.append(data['length']) if 'length' in data else length.append(NaN)
      room.append(data['rooms']) if 'rooms' in data else room.append(NaN)
      area.append(data['area']) if 'area' in data else area.append(NaN)
      ward.append(data['ward']) if 'ward' in data else ward.append(NaN)
      toilet.append(data['toilets']) if 'toilets' in data else toilet.append(NaN)
      living_size.append(data['living_size']) if 'living_size' in data else living_size.append(NaN)
      floor.append(data['floors']) if 'floors' in data else floor.append(NaN)
      house_type.append(data['house_type']) if 'house_type' in data else house_type.append(NaN)
      street.append(data['street_name']) if 'street_name' in data else street.append(NaN)
      direction.append(data['direction']) if 'direction' in data else direction.append(NaN)
      escrow_can_deposit.append(data['escrow_can_deposit']) if 'escrow_can_deposit' in data else escrow_can_deposit.append(NaN)
      property_legal_document.append(data['property_legal_document']) if 'property_legal_document' in data else property_legal_document.append(NaN)
      protection_entitlement.append(data['protection_entitlement']) if 'protection_entitlement' in data else protection_entitlement.append(NaN)
      zero_deposit.append(data['zero_deposit']) if 'zero_deposit' in data else zero_deposit.append(NaN)
      furnishing_sell.append(data['furnishing_sell']) if 'furnishing_sell' in data else furnishing_sell.append(NaN)
    df = pd.DataFrame({'subject': subject,
                       'size': size,
                       'width': width,
                       'length': length,
                       'room': room,
                       'area': area,
                       'ward': ward,
                       'toilet': toilet,
                       'living size': living_size,
                       'floor': floor,
                       'house type': house_type,
                       'zero deposit': zero_deposit,
                       'direction': direction,
                       'street': street,
                       'escrow can deposit': escrow_can_deposit,
                       'property legal document': property_legal_document,
                       'protection entitlement': protection_entitlement,
                       'furnishing sell': furnishing_sell,
                       'price': price})
    df.to_csv('chotot.csv', encoding="utf-8-sig")
  return True

dataset = Crawl_Data(1,4770)

print(dataset)