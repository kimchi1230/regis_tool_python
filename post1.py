from http.cookiejar import Cookie
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import sys
import os
import keyboard

def regis():
    while(True):
        env = input('Enter environment to create contract (local/dev/debug1/beer1/exit to exit/clear console == cls): ')
        env = env.lower()
        if env == "exit":
            sys.exit()
        if env == "cls":
            os.system('cls' if os.name == 'nt' else 'clear')
            return       
        switcher1 = {
            'local':'111',
            'dev':'321',
            'debug1':'143',
            'beer1':'67',
        }
        switcher2 = {
            'local':'2678',
            'dev':'2804',
            'debug1':'1971',
            'beer1':'2590'
        }
        switcher = {
            'local':'https://dev.beer.com.vn',
            'dev':'https://dev1.drbe.jp',
            'debug1':'https://debug1.drbe.jp',
            'beer1':'https://beer1-lampart.com.vn',
            'sql_agree':'agree',
        }
        switcher3 = {
            'local':'2',
            'dev':'115',
            'debug1':'113',
            'beer1':'2',
        }
        url_root = switcher.get(env,'invalid')
        # ser_enterprise_campaign = switcher1.get(env,'invalid')
        # con_agree = switcher2.get(env,'invalid')
        # ser_server = switcher3.get(env,'invalid')
        if(url_root == 'invalid'):
            continue    
        else:
            break

    if env == 'sql_agree':
        sql = "SELECT `agreement`.*, `agreement_adaptation`.`adaptation_date`"
        sql += "FROM `agreement`"
        sql += "LEFT JOIN agreement_adaptation ON agreement_adaptation.id = agreement.agreement_adaptation_id"
        sql += " WHERE `agreement`.`partner_id` = '2750'"
        sql += " AND `agreement_adaptation`.`adaptation_date` <=" + datetime.now().strftime('%Y-%m-%d')
        sql += " AND `agreement`.`disable` =0"
        sql += " ORDER BY `agreement_adaptation`.`adaptation_date` DESC"
        print(sql)
        exit()

    if env == 'local':
        tshop = 'tshop00060960'
    else:
        tshop = 'tshop00034654'

    tmp = tmp1 = ser_server_tmp =[]
    email = 'toolprovjpno1vodichvutru'+ datetime.now().strftime('%y%m%d%H%M%S')+ '@lampart-vn.com'
    password_p = 'lampart123'
    csrf_key = 'chideptrai'
    headers ={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}
    url_final = url_root+'/register/success/code/registration'
    url_step1 = url_root+'/register/server/entrymailaddress'
    url_step2 = 'https://pt01.mul-pay.jp/ext/api/getToken?key=nVmYmre0TWuwsXF9IX3VFuCRMf%2F%2FSPXLipsFpT1NnTfzRYP7M7bqAk4LV0HvqzH%2BqrtBRlCZbQXprTO9gUuQXHETLB9ZASlDTMAnVtgiorhUdnM75dk69Jg9al4LvwdXAEgVQQa%2Ffnc2t0EjNaskHvOuLQM8frtoeu77AbhOkuHnGaFnLtjbimUfIgIv1e%2BtQXn6uxYu2RHAhniTlXqDnBxPDrNE2xXneNQZdBwmlHPhW%2FIvUwoyfe9ijBSC6XO%2Be6Ca6j10eORigBvmIVr4LXYWATX%2FV6Bi6Jxqf2saiYsSVhQNDN0V1CH6S%2FgYo2gmRzMR7iL290djASkm9dXGNw%3D%3D&callback=gmo_token_add&publicKey=tshop00058724&encrypted=NM9vLhqVOoV4gcsHCpuWfBJNjRnM2QL9GLiKwH%2FBhm8FUME%2FdNPuiqrWKVNijDA7&seal=05f2e38bc68df7c68619e0b31b6c8f1e4dfc8f7a&version=5'
    url_step3 = url_root+'/register/server/code/registration'
    url_agree = url_root+'/register/contract/code/registration'

    cookie_step1 = {
        'csrf_cookie_name':csrf_key
    }


    data_step1 = {
        'c_zipcode':'1500000',
        'uniqid':'dadadada47',
        'form_action':'entrymailaddress',
        'txt_confirm_zipcode':'1500000',
        'txt_check_address':'',
        'email': email,
        'confirm_email': email,
        'year_old':'1',
        'agreement':'1',
        'csrf_test_name':csrf_key
    }
    x=requests.post(url_step1,data=data_step1,cookies=cookie_step1,headers=headers,verify=False)
    soup = BeautifulSoup(x.text,features="lxml")
    mail_token_input = soup.find_all('input', {'name': 'token'})
    if mail_token_input:
        mail_token_values = [input_tag['value'] for input_tag in mail_token_input]
        tmp.append(mail_token_values[0])
    if not tmp:
        print("request error 1")
        regis()
        return

    data_step3 = {
        'token': tmp[0]
    }

    # get variable server
    n = requests.post(url_step3,data=data_step3,verify=False)
    soup_server = BeautifulSoup(n.text,features="lxml")
    server_inputs = soup_server.find_all('input', {'name': 'server'})
    # for link in soup_server.find_all('input'):
    #     print(link)

    if server_inputs:
        server_values = [input_tag['value'] for input_tag in server_inputs]
        ser_server = server_values[0]
    # print(ser_server)

    # get variable campaign
    enterprise_inputs = soup_server.find_all('input', {'name': 'enterprise_campaign'})
    if enterprise_inputs:
        enterprise_values = [input_tag['value'] for input_tag in enterprise_inputs]
        ser_enterprise_campaign = enterprise_values[0]
    # print(ser_enterprise_campaign)


    data_agree = {
        'token_mail_confirm': tmp[0], 
        'ser_server': ser_server,
        'ser_server_rental':'2',
        'ser_plan_type':'1',
        'ser_water':'211',
        'ser_holder_color':'3',
        'ser_customer_type':'1',
        'ser_category_settlement_type':'credit_card_gmo',
        'ser_enterprise_campaign':ser_enterprise_campaign, #dev 111 | local 67 | debug 143
        'ser_server_id': ser_server,
        'ser_product_id':'211',
        'campaign_page_code': 'registration',
        'aquisition_partner_id_check': '2750',
        'files':'',
        'form_action':'server',
        'water':'211',
        'plan_type':'1',
        'holder_color':'3',
        'enterprise_campaign':ser_enterprise_campaign,
        'server':ser_server,
        'server_rental':'2',
        'server_plan_free':'',
        'server_plan':'',
        'customer_type':'1',
        'category_settlement_type':'credit_card_gmo',
    }
    # send request to get variable agree
    request_agree = requests.post(url_agree,data=data_agree,verify=False)
    soup_agree = BeautifulSoup(request_agree.text,features="lxml")
    agree_inputs = soup_agree.find_all('input', {'name': 'agree'})
    # print(request_agree.text)
    # print(agree_inputs)
    if agree_inputs:
        agree_values = [input_tag['value'] for input_tag in agree_inputs]
        con_agree = agree_values[0]
    # print(con_agree)


    y = requests.get(url_step2,verify=False)
    tmp2 = y.text.replace('gmo_token_add', '')
    tmp3 = tmp2.replace('(', '')
    tmp4 = tmp3.replace(')', '')
    abc = json.loads(tmp4)

    data_final = {
        'token_mail_confirm': tmp[0], 
        'ser_server': ser_server,
        'ser_server_rental':'2',
        'ser_server_type':'4',
        'ser_plan_type':'1',
        'ser_water':'211',
        'ser_server_size':'3',
        'ser_server_color':'3',
        'ser_holder_color':'3',
        'ser_customer_type':'1',
        'ser_category_settlement_type':'credit_card_gmo',
        'ser_enterprise_campaign':ser_enterprise_campaign, #dev 111 | local 67 | debug 143
        'ser_option_service':'290',
        'ser_server_id': ser_server,
        'ser_product_id':'211',
        'con_campaign_code':'',
        'con_agree':con_agree, #2552 local||1971 debug1 || 2590 beer1 || 2678 dev1
        'con_c_first_name':'provjp',
        'con_c_last_name':'tool',
        'con_c_first_name_kana':'フリガナ',
        'con_c_last_name_kana':'フリガナ',
        'con_c_sex_cd':'2',
        'con_optin_type_premium':'1',
        'con_c_phone_no':'0123456789',
        'con_mypage_login_id':email,
        'con_mypage_password':password_p,
        'con_c_mypage_password_confirm':password_p,
        'con_d_delivery_address':'contract',
        'con_c_zipcode':'1500000',
        'con_c_prefecture_id':'13',
        'con_c_prefecture_id_text':'東京都',
        'con_c_address_1':'渋谷区以下に掲載がない場合454',
        'con_c_address_2':'',
        'con_payment_card_no_1':'3540',
        'con_payment_card_no_2':'1111',
        'con_payment_card_no_3':'1111',
        'con_payment_card_no_4':'1111',
        'con_card_name':'dsadad',
        'con_card_cvc':'2410',
        'con_gmo_authorization_shop_id': tshop,
        'con_campaign_page_settlement':'sett_type_gmo',
        'con_c_birth_date':'2000-10-24',
        'con_payment_card_expiration':'2026-04',
        'con_chosen_question_class_1':'',
        'con_optin_premium':'empty',
        'con_payment_card_no':'3540111111111111',
        'con_c_old_agreements':'',
        'form_action':'confirm',
        'result_code_gmo_token':'000',
        'gmo_token': abc['tokenObject']['token'][0]  
    }
    z = requests.post(url_final,data=data_final,headers=headers ,verify=False)
    print(z.text)
    if(z.text.find('success')):
        print(email)
        print(password_p)

while True:
    regis()      
   