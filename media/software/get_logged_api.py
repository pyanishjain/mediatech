from datetime import datetime
import os 
import requests

def getToken():
    if token_path_exist:
        print('Please take the token from computer')
        auth(token)
    else:
        print("open the window and take the token")
        auth(token)
        # token = 'fce36b318615de6402db59433df9c0f8c2029be0'



def telegram(self,token):
    url = "http://127.0.0.1:8000/telegramAPI/"
    headers = {
      'Authorization': f'Token {token}',
      'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)

    print(response.json()['DemoDate'])

    return response.json()



def auth(token):
    today = datetime.today().date()
    url = "http://127.0.0.1:8000/profile"
    # url = "https://minermo.herokuapp.com/profile"
    headers = {'Authorization': f'Token {token}'}
    response = requests.request("GET", url, headers=headers,stream=True)

    local_ip_address = self.getIpAddress()
    print('local',local_ip_address)

    print(response)
    remote_ip_address =  response.json()['results'][0]['ip_address']

    if remote_ip_address == None:
        self.createIp(token)
        response = requests.request("GET", url, headers=headers, data=payload,stream=True)
        remote_ip_address =  response.json()['results'][0]['ip_address']

    print('remote',remote_ip_address)

    #Application based code

    if (remote_ip_address  == local_ip_address):
        data = self.telegram(token)
        demo_date = datetime.strptime(data['DemoDate'], '%Y-%m-%d').date()
        license_expire_date = data['licenceExpireDate']

        print(type(today) , type(demo_date), type(license_expire_date))
        print("today",today)
        print('demo_date',demo_date)

        if (demo_date == today):
            print("allow")

        if license_expire_date != None:
            license_expire_date = datetime.strptime(license_expire_date, '%Y-%m-%d').date()
            print('license_expire_date',license_expire_date)
            if(license_expire_date >= today):
                print("allow with license")
            else:
                print("Not allowed your License expired")
        else:
            print('Not allowed Please Activate your account by paying')
    else:
        print('Not allowed')
