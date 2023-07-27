from http.cookiejar import Cookie
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
import threading
import tkinter.messagebox as messagebox
from requests_html import HTMLSession 
import special_request
import time
import get_input
import sys

session = HTMLSession(verify=False)
session.browser

tk_object = tk.Tk()
combobox_var = tk.StringVar()
tk_object.title("THE REGISTOR")
# tk_object.geometry("750x350+100+100")
tk_object.resizable(0,0)
custom_font = Font(family="Comic Sans MS", size=15)

window1 = tk.Frame(tk_object)
window1.grid(row=0, column=0, sticky='nsew')

canvas = tk.Canvas(window1, width=750, height=350)
canvas.grid(row=0, column=0, sticky='nsew')

my_scrollbar = tk.Scrollbar(window1, orient='vertical', command=canvas.yview)
my_scrollbar.grid(row=0, column=1, sticky='nsew')

canvas.configure(yscrollcommand=my_scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

window2 = tk.Frame(canvas)
window2.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
canvas.create_window((0,0), window=window2, anchor='nw')
window1.columnconfigure(0, weight=1)
window1.rowconfigure(0, weight=1)

result_get_file = get_input.generate_default_config_file(is_check_exist_default=True)
if not result_get_file:
    messagebox.showinfo("Error", "Can not create config file")
    sys.exit()


def regis():
    try:
        while(True):
            env = combobox_var.get()
            env = env.lower()
            if env == "":
                return
            if env == "cls":
                os.system('cls' if os.name == 'nt' else 'clear')
                return       
            # switcher1 = {
            #     'local':'111',
            #     'dev':'321',
            #     'debug1':'143',
            #     'beer1':'67',
            # }
            # switcher2 = {
            #     'local':'2678',
            #     'dev':'2804',
            #     'debug1':'1971',
            #     'beer1':'2590'
            # }
            switcher = {
                'local':'https://dev.beer.com.vn',
                'dev':'https://dev1.drbe.jp',
                'debug1':'https://debug1.drbe.jp',
                'beer1':'https://beer1-lampart.com.vn',
                'sql_agree':'agree',
            }
            # switcher3 = {
            #     'local':'2',
            #     'dev':'115',
            #     'debug1':'113',
            #     'beer1':'2',
            # }
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


#---------------------------------------------------------------------------------------
#---------------------------------INPUT DATA--------------------------------------------
        input = get_input.get_config()
        first_name = input['first_name'] #first_name': 'tool',
        last_name = input['last_name'] #last_name': 'provjp',
        first_name_kana = input['first_name_kana'] #first_name_kana': 'フリガナ',
        last_name_kana = input['last_name_kana'] #last_name_kana': 'フリガナ',
        email = input['email']+ datetime.now().strftime('%y%m%d%H%M%S')+ '@lampart-vn.com' #email': 'toolprovjpno1vodichvutru',
        password_p = input['password'] #pass' : 'lampart123',
        zipcode = input['zipcode'] #zipcode': '1500000',
        server_rental = input['server_rental'] #server_rental': '2',
        water = input['water'] #water': '211',
        holder_color = input['holder_color'] #holder_color': '3',
        customer_type = input['customer_type'] #customer_type': '1',
        settlement_type = input['settlement_type'] #settlement_type': 'credit_card_gmo',
        plan_type = input['plan_type'] #plan_type": "1",
        payment_card_no_1 = input['payment_card_no_1'] #payment_card_no_1": "3540",
        payment_card_no_2 = input['payment_card_no_2'] #payment_card_no_2": "1111",
        payment_card_no_3 = input['payment_card_no_3'] #payment_card_no_3": "1111",
        payment_card_no_4 = input['payment_card_no_4'] #payment_card_no_4": "1111",
        payment_expiry_year = input['payment_expiry_year'] #payment_expiry_year": "2026",
        payment_expiry_month = input['payment_expiry_month'] #payment_expiry_month": "01",
        payment_card_name = input['payment_card_name'] #payment_card_name": "chi",
        payment_card_cvc = input['payment_card_cvc'] #payment_card_cvc": "2410",
        prefecture = input['prefecture'] #prefecture': '13',
        prefecture_id_text = input['prefecture_id_text'] #prefecture_id_text': '東京都',
        address_1 = input['address_1'] #address_1': '渋谷区以下に掲載がない場合454',
        address_2 = input['address_2'] #address_2': '',
        sex_cd = input['sex_cd'] #sex_cd': '2',
        birth_date_year = input['birth_date_year']  #birth_date_year = 1993
        birth_date_month = input['birth_date_month'] #birth_date_month = 10
        birth_date_day = input['birth_date_day'] #birth_date_day = 24
        phone_no = input['phone_no'] #phone_no': '0994984984',
        # payment_card = payment_card_no_1 + payment_card_no_2 + payment_card_no_3 + payment_card_no_4
        is_disable_brower = input['is_disable_brower'] #is_disable_brower': '0',


#---------------------------------------------------------------------------------------
#---------------------------------SYSTEM DATA-------------------------------------------
        tmp =[]
        csrf_key = 'chideptrai'
        headers ={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}
        # url_final = url_root+'/register/success/code/registration'
        url_step1 = url_root+'/register/server/entrymailaddress'
        # url_step2 = 'https://pt01.mul-pay.jp/ext/api/getToken?key=nVmYmre0TWuwsXF9IX3VFuCRMf%2F%2FSPXLipsFpT1NnTfzRYP7M7bqAk4LV0HvqzH%2BqrtBRlCZbQXprTO9gUuQXHETLB9ZASlDTMAnVtgiorhUdnM75dk69Jg9al4LvwdXAEgVQQa%2Ffnc2t0EjNaskHvOuLQM8frtoeu77AbhOkuHnGaFnLtjbimUfIgIv1e%2BtQXn6uxYu2RHAhniTlXqDnBxPDrNE2xXneNQZdBwmlHPhW%2FIvUwoyfe9ijBSC6XO%2Be6Ca6j10eORigBvmIVr4LXYWATX%2FV6Bi6Jxqf2saiYsSVhQNDN0V1CH6S%2FgYo2gmRzMR7iL290djASkm9dXGNw%3D%3D&callback=gmo_token_add&publicKey=tshop00058724&encrypted=NM9vLhqVOoV4gcsHCpuWfBJNjRnM2QL9GLiKwH%2FBhm8FUME%2FdNPuiqrWKVNijDA7&seal=05f2e38bc68df7c68619e0b31b6c8f1e4dfc8f7a&version=5'
        url_step3 = url_root+'/register/server/code/registration'
        url_agree = url_root+'/register/contract/code/registration'
        url_sub_final = url_root+'/register/confirm/code/registration'

        cookie_step1 = {
            'csrf_cookie_name':csrf_key
        }


        data_step1 = {
            'c_zipcode':zipcode,
            'uniqid':'dadadada47',
            'form_action':'entrymailaddress',
            'txt_confirm_zipcode':zipcode,
            'txt_check_address':'',
            'email': email,
            'confirm_email': email,
            'year_old':'1',
            'agreement':'1',
            'csrf_test_name':csrf_key
        }
        x=requests.post(url_step1,data=data_step1,cookies=cookie_step1,headers=headers,verify=False)
        progress_bar["value"] = 20
        progress_bar.update()

        soup = BeautifulSoup(x.text,features="lxml")
        mail_token_input = soup.find_all('input', {'name': 'token'})
        if mail_token_input:
            mail_token_values = [input_tag['value'] for input_tag in mail_token_input]
            tmp.append(mail_token_values[0])
      
        data_step3 = {
            'token': tmp[0]
        }

        # get variable server
        n = requests.post(url_step3,data=data_step3,verify=False)
        progress_bar["value"] = 40
        progress_bar.update()

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

        option_service_input = soup_server.find_all('input', {'name': 'option_service'})
        if option_service_input:
            option_service_values = [input_tag['value'] for input_tag in option_service_input]
            ser_option_service = option_service_values[0]

        partner_id_input = soup_server.find_all('input', {'name': 'aquisition_partner_id_check'})
        if partner_id_input:
            partner_id_values = [input_tag['value'] for input_tag in partner_id_input]
            ser_partner_id = partner_id_values[0]

        campaign_page_code = soup_server.find_all('input', {'name': 'campaign_page_code'})
        if campaign_page_code:
            campaign_page_code_values = [input_tag['value'] for input_tag in campaign_page_code]
            ser_campaign_page_code = campaign_page_code_values[0]
            
        data_agree = {
            'token_mail_confirm': tmp[0], 
            'ser_server': ser_server,
            'ser_server_rental':server_rental,
            'ser_plan_type':plan_type,
            'ser_water':water,
            'ser_holder_color':holder_color,
            'ser_customer_type':customer_type,
            'ser_category_settlement_type':settlement_type,
            'ser_enterprise_campaign':ser_enterprise_campaign, #dev 111 | local 67 | debug 143
            'ser_server_id': ser_server,
            'ser_product_id':water,
            'campaign_page_code': ser_campaign_page_code,
            'aquisition_partner_id_check': ser_partner_id,
            'files':'',
            'form_action':'server',
            'water':water,
            'plan_type':plan_type,
            'holder_color':holder_color,
            'enterprise_campaign':ser_enterprise_campaign,
            'server':ser_server,
            'server_rental':server_rental,
            'server_plan_free':'',
            'server_plan':'',
            'customer_type':customer_type,
            'category_settlement_type':settlement_type,
        }
        # send request to get variable agree
        request_agree = requests.post(url_agree,data=data_agree,verify=False)
        progress_bar["value"] = 60
        progress_bar.update()

        soup_agree = BeautifulSoup(request_agree.text,features="lxml")
        agree_inputs = soup_agree.find_all('input', {'name': 'agree'})
        # print(request_agree.text)
        # print(agree_inputs)
        if agree_inputs:
            agree_values = [input_tag['value'] for input_tag in agree_inputs]
            con_agree = agree_values[0]
        # print(con_agree)

        shop = soup_agree.find_all('input', {'name': 'gmo_authorization_shop_id'})
        if shop:
            shop_values = [input_tag['value'] for input_tag in shop]
            tshop = shop_values[0]

        data_sub_final = {
            "token_mail_confirm": tmp[0],
            "ser_server": ser_server,
            "ser_server_rental": server_rental,
            "ser_plan_type": plan_type,
            "ser_water": water,
            "ser_holder_color": holder_color,
            "ser_customer_type": customer_type,
            "ser_category_settlement_type": settlement_type,
            "ser_enterprise_campaign": ser_enterprise_campaign,
            "ser_option_service": ser_option_service,
            "ser_server_id": ser_server,
            "ser_product_id": water,
            # "con_campaign_code": "",
            # "con_agree": "2678",
            # "con_c_first_name": "test",
            # "con_c_last_name": "chi",
            # "con_c_first_name_kana": "フリガナ",
            # "con_c_last_name_kana": "フリガナ",
            # "con_c_sex_cd": "3",
            # "con_optin_type_premium": "1",
            # "con_c_phone_no": "0994984984",
            # "con_mypage_login_id": email,
            # "con_mypage_password": password_p,
            # "con_c_mypage_password_confirm": password_p,
            # "con_d_delivery_address": "contract",
            # "con_c_zipcode": "1500000",
            # "con_c_prefecture_id": "13",
            # "con_c_prefecture_id_text": "東京都",
            # "con_c_address_1": "渋谷区6",
            # "con_c_address_2": "",
            # "con_payment_card_no_1": "3540",
            # "con_payment_card_no_2": "1111",
            # "con_payment_card_no_3": "1111",
            # "con_payment_card_no_4": "1111",
            # "con_card_name": "dsadad",
            # "con_card_cvc": "2410",
            # "con_gmo_authorization_shop_id": tshop,
            # "con_campaign_page_settlement": "sett_type_gmo",
            # "con_c_birth_date": "1993-1-1",
            # "con_payment_card_expiration": "2024-01",
            # "con_chosen_question_class_1": "",
            # "con_optin_premium": "empty",
            # "con_payment_card_no": "3540111111111111",
            # "con_c_old_agreements": "",
            "hidden_partner_id": ser_partner_id,
            "campaign_page_settlement": 'sett_type_gmo',
            "campaign_page_code": "registration",
            "c_old_agreements": "",
            "form_action": "contract",
            "c_last_name": last_name,
            "c_first_name": first_name,
            "c_last_name_kana": last_name_kana,
            "c_first_name_kana": first_name_kana,
            "c_sex_cd": sex_cd,
            "c_birth_date_year": birth_date_year,
            "c_birth_date_month": birth_date_month,
            "c_birth_date_day": birth_date_day,
            "c_zipcode": zipcode,
            "c_prefecture_id_text": prefecture_id_text,
            "c_prefecture": prefecture,
            "c_address_1": address_1,
            "c_address_2": address_2,
            "c_phone_no": phone_no,
            "login_id": email,
            "optin_type_premium": "1",
            "mypage_password": password_p,
            "c_mypage_password_confirm": password_p,
            "d_delivery_address": "contract",
            "d_last_name": "",
            "d_first_name": "",
            "d_last_name_kana": "",
            "d_first_name_kana": "",
            "d_zipcode": "",
            "d_prefecture_id_text": "",
            "d_prefecture": "",
            "d_address_1": "",
            "d_address_2": "",
            "d_phone_no": "",
            "gmo_authorization_shop_id": tshop,
            "payment_card_no_1": payment_card_no_1,
            "payment_card_no_2": payment_card_no_2,
            "payment_card_no_3": payment_card_no_3,
            "payment_card_no_4": payment_card_no_4,
            "payment_expiry_year": payment_expiry_year,
            "payment_expiry_month": payment_expiry_month,
            "payment_card_name": payment_card_name,
            "payment_card_cvc": payment_card_cvc,
            "agree": con_agree,
            "campaign_code": "",
            "is_disable_brower": is_disable_brower
        }
        html_rs = special_request.perform_post_request_with_button_click(url_sub_final, data_sub_final)

        if not html_rs:
            raise Exception("FAIL IN FINAL REQUEST")
        
        # data_final = {
        #     'token_mail_confirm': tmp[0], 
        #     'ser_server': ser_server,
        #     'ser_server_rental':'2',
        #     'ser_server_type':'4',
        #     'ser_plan_type':'1',
        #     'ser_water':'211',
        #     'ser_server_size':'3',
        #     'ser_server_color':'3',
        #     'ser_holder_color':'3',
        #     'ser_customer_type':'1',
        #     'ser_category_settlement_type':'credit_card_gmo',
        #     'ser_enterprise_campaign':ser_enterprise_campaign, #dev 111 | local 67 | debug 143
        #     'ser_option_service':'290',
        #     'ser_server_id': ser_server,
        #     'ser_product_id':'211',
        #     'con_campaign_code':'',
        #     'con_agree':con_agree, #2552 local||1971 debug1 || 2590 beer1 || 2678 dev1
        #     'con_c_first_name':'provjp',
        #     'con_c_last_name':'tool',
        #     'con_c_first_name_kana':'フリガナ',
        #     'con_c_last_name_kana':'フリガナ',
        #     'con_c_sex_cd':'2',
        #     'con_optin_type_premium':'1',
        #     'con_c_phone_no':'0123456789',
        #     'con_mypage_login_id':email,
        #     'con_mypage_password':password_p,
        #     'con_c_mypage_password_confirm':password_p,
        #     'con_d_delivery_address':'contract',
        #     'con_c_zipcode':'1500000',
        #     'con_c_prefecture_id':'13',
        #     'con_c_prefecture_id_text':'東京都',
        #     'con_c_address_1':'渋谷区以下に掲載がない場合454',
        #     'con_c_address_2':'',
        #     'con_payment_card_no_1':'3540',
        #     'con_payment_card_no_2':'1111',
        #     'con_payment_card_no_3':'1111',
        #     'con_payment_card_no_4':'1111',
        #     'con_card_name':'dsadad',
        #     'con_card_cvc':'2410',
        #     'con_gmo_authorization_shop_id': tshop,
        #     'con_campaign_page_settlement':'sett_type_gmo',
        #     'con_c_birth_date':'2000-10-24',
        #     'con_payment_card_expiration':'2026-04',
        #     'con_chosen_question_class_1':'',
        #     'con_optin_premium':'empty',
        #     'con_payment_card_no':'3540111111111111',
        #     'con_c_old_agreements':'',
        #     'form_action':'confirm',
        #     'result_code_gmo_token':'000',
        #     # 'gmo_token': abc['tokenObject']['token'][0]  
        # }
        # z = session.post(url_final,data=data_final,headers=headers ,verify=False)
        


        print(str(html_rs))
        text_success = html_rs.find('input', {'name': 'success_data[contract_id]'})
        text_success2 = html_rs.find('div', {'class': 'thank_you_text'})
        if(text_success or text_success2):
            print(email)
            print(password_p)
            # set label_password text
            update_text(email)
            # set label_password text   
            update_text(password_p)
            progress_bar["value"] = 100
            progress_bar.update()
        else:
            raise Exception("FAIL IN FINAL REQUEST PROCESSING FAIL")
    except Exception as e:
        # update_text("ALO lỗi rồi đại vương ơi !")
        print(e)
    button.config(state="normal")



def update_text(content):
    text_widget = tk.Text(window2, height=1, font=custom_font, width=20)
    text_widget.configure(state='normal')  # Make the Text widget editable
    text_widget.delete('1.0', 'end')  # Delete the current content
    text_widget.insert('1.0', content)  # Insert the new value
    text_widget.configure(state='disabled')  # Make the Text widget uneditable again
    row = window2.grid_size()[1] + 1
    text_widget.grid(row=row, column=0, columnspan=3, sticky="ew", padx=10)
    text_widget.bind("<Button-1>", lambda event: copy_to_clipboard(text_widget))

def on_button_click():
    if not is_running[0]:
        button.config(state="disabled")
        is_running[0] = True
        progress_bar.start()
        thread = threading.Thread(target=regis).start()
        # thread.join()
        is_running[0] = False
        progress_bar.stop()

def copy_to_clipboard(text_widget):
    text = text_widget.get("1.0", "end-1c")
    window2.clipboard_clear()
    window2.clipboard_append(text)
    

#label
label = tk.Label(window2, text="Environment (local/dev/debug1/beer1)",font=custom_font)
label_ps = tk.Label(window2, text="P/s: click chuột vào mk tk sẽ tự động copy !",font=custom_font)
#dropdown
values = ['local', 'dev', 'debug1','beer1']
combobox = ttk.Combobox(window2, values=values, width=12, state="readonly", textvariable=combobox_var)
# combobox.configure(font=custom_font)

#button
button = tk.Button(window2, text="Submit", width=6, height=1, font=custom_font)
button.config(command=on_button_click)

progress_bar = ttk.Progressbar(window2, orient="horizontal", mode="determinate", length=700)

#grid
label.grid(row=0, column=0, padx=10, pady=10)
combobox.grid(row=0, column=1, padx=10, pady=10)
button.grid(row=0, column=2, padx=10, pady=10)
progress_bar.grid(row=2, column=0, padx=10, columnspan=3,sticky="ew")
label_ps.grid(row=1, column=0, columnspan=3,sticky="ew")
combobox.bind("<<ComboboxSelected>>", lambda e: combobox.configure(font=custom_font))
combobox.set('local')

is_running = [False]
tk_object.mainloop()