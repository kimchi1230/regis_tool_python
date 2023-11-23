import requests


session = requests.Session()
url_step1 = "https://dev.lampart.com.vn/_cgi/ivr_process/cancellation_reception"
headers ={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}
data = {
  "customer_id": "2591972",
  "tel": "0994984984",
  "call_id": "090123456789",
  "callback_tel": "0994984984",
}

x=session.post(url=url_step1,data=data,headers=headers,verify=False)