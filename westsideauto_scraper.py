import requests
import json


def get_vehicle(session, usage_token, rego, state):
    payload = {"query": "query vehicleRegoLookup($rego: String!, $state: String!) {   vehicleRegoLookup(rego: $rego, state: $state) {     result {       make       model       year       variant       transmission       __typename     }     __typename   } } ",
               "operationName": "vehicleRegoLookup", "variables": {"rego": rego, "state": state}}
    r = s.post(
        url='https://services.autoleague.io/api',
        json=payload,
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'x-usage-token': usage_token,
            'referer': 'https://www.westsideauto.com.au/sell-my-car',
        }
    )

    result = json.loads(r.text)
    return result['data']['vehicleRegoLookup']['result']


def get_price(session, usage_token, rego, state, mileage, condition):
    price = None
    vehicle = get_vehicle(session, usage_token, rego, state)

    payload = {"query": "query VehicleEstimate($make: String!, $model: String!, $year: Int!, $variant: String!, $transmission: String!, $mileage: Int!, $condition: String!) {   vehicleEstimate(     make: $make     model: $model     year: $year     variant: $variant     transmission: $transmission     mileage: $mileage     condition: $condition   ) {     min     max     make     model     year     variant     transmission     __typename   } } ",
               "operationName": "VehicleEstimate", "variables": {"make": vehicle['make'], "model": vehicle['model'], "year": vehicle['year'], "variant": vehicle['variant'], "transmission": vehicle['transmission'], "mileage": mileage, "condition": condition}}
    r = s.post(
        url='https://services.autoleague.io/api',
        json=payload,
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'x-usage-token': usage_token,
            'referer': 'https://www.westsideauto.com.au/sell-my-car',
        }
    )

    result = json.loads(r.text)
    price = result['data']['vehicleEstimate']['min']

    return price

def get_usage_token(session):
    usage_token = None

    payload = {"query": "query VehicleQueryStatus {   vehicleQueryStatus {     limit     usageToken     __typename   } } ",
            "operationName": "VehicleQueryStatus", "variables": {}}

    r = session.post(
        url='https://services.autoleague.io/api',
        json=payload,
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'referer': 'https://www.westsideauto.com.au/sell-my-car',
        }
    )
    data = json.loads(r.text)
    usage_token = data['data']['vehicleQueryStatus']['usageToken']

    return usage_token


rego = '662cr9'
state = 'QLD'
mileage = 50000
condition = 'Good'

s = requests.Session()
usage_token = get_usage_token(s)

price = get_price(s, usage_token, rego, state, mileage, condition)
print(price)
