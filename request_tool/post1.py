import requests
from bs4 import BeautifulSoup
from datetime import datetime
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
import threading
import tkinter.messagebox as messagebox
import special_request
import time
import get_input
import sys
import asyncio
import json


def regis():
    try:
        is_running[0] = True
        button.config(state="disabled")
        start = time.time()
        env = combobox_var.get().lower()
        switcher = {
            'local':'https://dev.beer.com.vn',
            'dev':'https://dev1.drbe.jp',
            'debug1':'https://debug1.drbe.jp',
            'beer1':'https://beer1-lampart.com.vn',
            'sql_agree':'agree',
        }
        url_root = switcher.get(env,'invalid')
            
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
        # server = input['server']   
#---------------------------------------------------------------------------------------
#---------------------------------INPUT DATA--------------------------------------------
    


#---------------------------------------------------------------------------------------
#---------------------------------SYSTEM DATA-------------------------------------------
        tmp =[]
        session = requests.Session()
        csrf_key = 'chideptrai'
        headers ={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}
        url_final = url_root+'/register/success/code/registration'
        url_step1 = url_root+'/register/server/entrymailaddress'
        url_step3 = url_root+'/register/server/code/registration'
        url_agree = url_root+'/register/contract/code/registration'
        # url_sub_final = url_root+'/register/confirm/code/registration'
#---------------------------------------------------------------------------------------
#---------------------------------SYSTEM DATA-------------------------------------------


#-----------------------------------------------------------------------------------------
#---------------------------------SEND REQUEST 1------------------------------------------
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
        x=session.post(url_step1,data=data_step1,cookies=cookie_step1,headers=headers,verify=False)
        progress_bar["value"] = 20
        progress_bar.update()

        soup = BeautifulSoup(x.text,features="lxml")
        mail_token_input = soup.find_all('input', {'name': 'token'})
        if mail_token_input:
            mail_token_values = [input_tag['value'] for input_tag in mail_token_input]
            tmp.append(mail_token_values[0])
#-----------------------------------------------------------------------------------------
#---------------------------------SEND REQUEST 1------------------------------------------     

#-----------------------------------------------------------------------------------------
#---------------------------------SEND REQUEST 2------------------------------------------  
        data_step3 = {
            'token': tmp[0]
        }

        # get variable server
        n = session.post(url_step3,data=data_step3,verify=False)
        progress_bar["value"] = 40
        progress_bar.update()

        soup_server = BeautifulSoup(n.text,features="lxml")
        server_inputs = soup_server.find_all('input', {'name': 'server'})
        if not server_inputs: raise Exception('server_inputs input not found')
        if server_inputs:
            server_values = [input_tag['value'] for input_tag in server_inputs]
            ser_server = check_exits_value(server_values,0,'ser_server')
        # print(ser_server)

        # get variable campaign
        enterprise_inputs = soup_server.find_all('input', {'name': 'enterprise_campaign'})
        if not enterprise_inputs: raise Exception('enterprise_inputs input not found')
        if enterprise_inputs:
            enterprise_values = [input_tag['value'] for input_tag in enterprise_inputs]
            ser_enterprise_campaign = check_exits_value(enterprise_values,0,'ser_enterprise_campaign')
        # print(ser_enterprise_campaign)

        option_service_input = soup_server.find_all('input', {'name': 'option_service'})
        if not option_service_input: raise Exception('option_service_input input not found')
        if option_service_input:
            option_service_values = [input_tag['value'] for input_tag in option_service_input]
            ser_option_service = check_exits_value(option_service_values,0,'ser_option_service')

        partner_id_input = soup_server.find_all('input', {'name': 'aquisition_partner_id_check'})
        if not partner_id_input: raise Exception('partner_id_input input not found')
        if partner_id_input:
            partner_id_values = [input_tag['value'] for input_tag in partner_id_input]
            ser_partner_id = check_exits_value(partner_id_values,0,'ser_partner_id')

        campaign_page_code = soup_server.find_all('input', {'name': 'campaign_page_code'})
        if not campaign_page_code: raise Exception('campaign_page_code input not found')
        if campaign_page_code:
            campaign_page_code_values = [input_tag['value'] for input_tag in campaign_page_code]
            ser_campaign_page_code = check_exits_value(campaign_page_code_values,0,'campaign_page_code')

#-----------------------------------------------------------------------------------------
#---------------------------------SEND REQUEST 2------------------------------------------  


#-----------------------------------------------------------------------------------------
#---------------------------------SEND REQUEST 3------------------------------------------  
            
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
        request_agree = session.post(url_agree,data=data_agree,verify=False)
        progress_bar["value"] = 60
        progress_bar.update()

        soup_agree = BeautifulSoup(request_agree.text,features="lxml")
        agree_inputs = soup_agree.find_all('input', {'name': 'agree'})
        if not agree_inputs: raise Exception('agree input not found')
        if agree_inputs:
            agree_values = [input_tag['value'] for input_tag in agree_inputs]
            con_agree = check_exits_value(agree_values,0,'con_agree')
        # print(con_agree)

        shop = soup_agree.find_all('input', {'name': 'gmo_authorization_shop_id'})
        if not shop: raise Exception('agree input not found')
        if shop:
            shop_values = [input_tag['value'] for input_tag in shop]
            tshop = check_exits_value(shop_values,0,'tshop')
#-----------------------------------------------------------------------------------------
#---------------------------------SEND REQUEST 3------------------------------------------  

        # data_sub_final = {
        #     "token_mail_confirm": tmp[0],
        #     "ser_server": ser_server,
        #     "ser_server_rental": server_rental,
        #     "ser_plan_type": plan_type,
        #     "ser_water": water,
        #     "ser_holder_color": holder_color,
        #     "ser_customer_type": customer_type,
        #     "ser_category_settlement_type": settlement_type,
        #     "ser_enterprise_campaign": ser_enterprise_campaign,
        #     "ser_option_service": ser_option_service,
        #     "ser_server_id": ser_server,
        #     "ser_product_id": water,
        #     "hidden_partner_id": ser_partner_id,
        #     "campaign_page_settlement": 'sett_type_gmo',
        #     "campaign_page_code": "registration",
        #     "c_old_agreements": "",
        #     "form_action": "contract",
        #     "c_last_name": last_name,
        #     "c_first_name": first_name,
        #     "c_last_name_kana": last_name_kana,
        #     "c_first_name_kana": first_name_kana,
        #     "c_sex_cd": sex_cd,
        #     "c_birth_date_year": birth_date_year,
        #     "c_birth_date_month": birth_date_month,
        #     "c_birth_date_day": birth_date_day,
        #     "c_zipcode": zipcode,
        #     "c_prefecture_id_text": prefecture_id_text,
        #     "c_prefecture": prefecture,
        #     "c_address_1": address_1,
        #     "c_address_2": address_2,
        #     "c_phone_no": phone_no,
        #     "login_id": email,
        #     "optin_type_premium": "1",
        #     "mypage_password": password_p,
        #     "c_mypage_password_confirm": password_p,
        #     "d_delivery_address": "contract",
        #     "d_last_name": "",
        #     "d_first_name": "",
        #     "d_last_name_kana": "",
        #     "d_first_name_kana": "",
        #     "d_zipcode": "",
        #     "d_prefecture_id_text": "",
        #     "d_prefecture": "",
        #     "d_address_1": "",
        #     "d_address_2": "",
        #     "d_phone_no": "",
        #     "gmo_authorization_shop_id": tshop,
        #     "payment_card_no_1": payment_card_no_1,
        #     "payment_card_no_2": payment_card_no_2,
        #     "payment_card_no_3": payment_card_no_3,
        #     "payment_card_no_4": payment_card_no_4,
        #     "payment_expiry_year": payment_expiry_year,
        #     "payment_expiry_month": payment_expiry_month,
        #     "payment_card_name": payment_card_name,
        #     "payment_card_cvc": payment_card_cvc,
        #     "agree": con_agree,
        #     "campaign_code": "",
        #     "is_disable_brower": is_disable_brower
        # }
        #selenium
        # html_rs = special_request.perform_post_request_with_button_click(url_sub_final, data_sub_final)
        
        #pyppeteer
        # html_rs = asynco.run_until_complete(special_request.perform_post_request_with_button_click1(url_sub_final, data_sub_final))
        token = asyncio.run(special_request.get_gmo_token(env,tshop))
        if token['status'] == '551':
            raise Exception("FINAL REQUEST FAIL")
        data_final = {
            'token_mail_confirm': tmp[0], 
            'ser_server': ser_server,
            'ser_server_rental':server_rental,
            'ser_server_type':'4',
            'ser_plan_type':plan_type,
            'ser_water':water,
            'ser_server_size':'3',
            'ser_server_color':'3',
            'ser_holder_color':holder_color,
            'ser_customer_type':customer_type,
            'ser_category_settlement_type':settlement_type,
            'ser_enterprise_campaign':ser_enterprise_campaign, #dev 111 | local 67 | debug 143
            'ser_option_service':ser_option_service,
            'ser_server_id': ser_server,
            'ser_product_id':water,
            'con_campaign_code':'',
            'con_agree':con_agree, #2552 local||1971 debug1 || 2590 beer1 || 2678 dev1
            'con_c_first_name':first_name,
            'con_c_last_name':last_name,
            'con_c_first_name_kana':first_name_kana,
            'con_c_last_name_kana':last_name_kana,
            'con_c_sex_cd':sex_cd,
            'con_optin_type_premium':'1',
            'con_c_phone_no':phone_no,
            'con_mypage_login_id':email,
            'con_mypage_password':password_p,
            'con_c_mypage_password_confirm':password_p,
            'con_d_delivery_address':'contract',
            'con_c_zipcode':zipcode,
            'con_c_prefecture_id':prefecture,
            'con_c_prefecture_id_text':prefecture_id_text,
            'con_c_address_1':address_1,
            'con_c_address_2':'',
            'con_payment_card_no_1':payment_card_no_1,
            'con_payment_card_no_2':payment_card_no_2,
            'con_payment_card_no_3':payment_card_no_3,
            'con_payment_card_no_4':payment_card_no_4,
            'con_card_name':payment_card_name,
            'con_card_cvc':payment_card_cvc,
            'con_gmo_authorization_shop_id': tshop,
            'con_campaign_page_settlement':'sett_type_gmo',
            'con_c_birth_date': birth_date_year+'-'+birth_date_month+'-'+birth_date_day,
            'con_payment_card_expiration':payment_expiry_year+'-'+payment_expiry_month,
            'con_chosen_question_class_1':'',
            'con_optin_premium':'empty',
            'con_payment_card_no':payment_card_no_1+payment_card_no_2+payment_card_no_3+payment_card_no_4,
            'con_c_old_agreements':'',
            'form_action':'confirm',
            'result_code_gmo_token':token['status'],
            'gmo_token':token['token'],
        }
        html_rs = session.post(url_final,data=data_final,headers=headers ,verify=False)
        html_rs = special_request.format_html(html_rs.text)
        print(str(html_rs))
        text_success = html_rs.find('input', {'name': 'success_data[contract_id]'})
        text_success2 = html_rs.find('div', {'class': 'thank_you_text'})
        text_success3 = html_rs.find('div', {'class': 'success_text'})
        end = time.time()
        excution_time = end-start
        if(text_success or text_success2 or text_success3):
            print(email)
            print(password_p)
            # set label_password text
            end = time.time()
            update_text(email,env,excution_time=end-start)
            # set label_password text   
            update_text(password_p,time=True)
            progress_bar["value"] = 100
            progress_bar.update()
            get_input.generate_history_file({'email':email,'password':password_p,'excution_time':round(excution_time,2),'date':datetime.now().strftime("%H:%M %Y/%m/%d")})
        else:
            raise Exception("FINAL REQUEST PROCESS FAIL")
    except Exception as e:
        # update_text("ALO lỗi rồi đại vương ơi !")
        print(e)
        update_text(e,env,excution_time=excution_time)
    session.close()
    print(excution_time)
    button.config(state="normal")
    is_running[0] = False   

#---------UPDATE RESULT TEXT-----------------
def update_text(content,env='',time = False,excution_time = 0):
    text_widget = tk.Text(window3, height=1, font=custom_font, width=60)
    text_widget.configure(state='normal')  # Make the Text widget editable
    text_widget.insert('1.0', content)  # Insert the new value
    text_widget.configure(state='disabled')  # Make the Text widget uneditable again
    # text_widget.configure(width=len(time))
    row = window3.grid_size()[1] + 1
    text_widget.grid(row=row, column=0, sticky="ew",padx=(10,0))
    text_widget.bind("<Button-1>", lambda event: copy_to_clipboard(text_widget))
    
    if env:
        string_var = env+'|Excution: '+str(round(excution_time, 2))+'s'
        text_widget_env = tk.Entry(window3, font=custom_font)
        text_widget_env.configure(state='normal')  # Make the Text widget editable
        text_widget_env.insert(0,string_var)  # Insert the new value
        text_widget_env.configure(state='disabled')  # Make the Text widget uneditable again
        text_widget_env.config(width=len(string_var))
        text_widget_env.grid(row=row, column=1, sticky="ew")

    if time:
        time = datetime.now().strftime("%H:%M %Y/%m/%d")
        text_widget_time = tk.Entry(window3, font=custom_font)
        text_widget_time.configure(state='normal')  # Make the Text widget editable
        text_widget_time.insert(0,time)  # Insert the new value
        text_widget_time.configure(state='disabled')  # Make the Text widget uneditable again
        text_widget_time.config(width=len(time))
        text_widget_time.grid(row=row, column=1, sticky="ew")

#---------CALL FUNCTION REGIS BY BROWER-----------------
def do_regis_by_brower():
    env = combobox_var.get().lower()
    button.config(state="disabled")
    result_brower = asyncio.run(special_request.regis_by_browser(env))
    if result_brower:
        update_text(result_brower['email'],env,excution_time=result_brower['excution_time'])
        update_text(result_brower['password'],time=True)
        get_input.generate_history_file({'email':result_brower['email'],'password':result_brower['password'],'excution_time':round(result_brower['excution_time'],2),'date':datetime.now().strftime("%H:%M %Y/%m/%d")})
    button.config(state="normal")

#---------ONCLICK TRIGGER FUNCTION-----------------
def on_button_click():
    if not is_running[0]:
        input_display = {
            'email': email_var.get(),
            'password' : pass_var.get(),
            'first_name': fname_var.get(),
            'last_name': lname_var.get(),
            'first_name_kana': fname_kana_var.get(),
            'last_name_kana': lname_kana_var.get(),
            'payment_card_no_1': card_var_1.get(),
            'payment_card_no_2': card_var_2.get(),
            'payment_card_no_3': card_var_3.get(),
            'payment_card_no_4': card_var_4.get(),
            'payment_expiry_year': year_card_var.get(),
            'payment_expiry_month': month_card_var.get(),
            'payment_card_name': card_name_var.get(),
            'payment_card_cvc': cvc_var.get(),
            'zipcode': zipcode_var.get(),
            'prefecture': prefecture_id_var.get(),
            'prefecture_id_text': prefecture_var.get(),
            'address_1': address1_var.get(),
        }
        is_write_complete = get_input.set_config(input_display)
        if not is_write_complete:
            messagebox.showerror('Error','Cannot write file config')
            return
        mode = mode_var.get()
        if mode == 'manual':
            threading.Thread(target=do_regis_by_brower).start()
            return
        if mode == 'fast':
            threading.Thread(target=regis).start()
            return

#---------COPY TO CLIPBOARD-----------------
def copy_to_clipboard(text_widget):
    text = text_widget.get("1.0", "end-1c")
    window2.clipboard_clear()
    window2.clipboard_append(text)

#---------CHECK VALUE EXIST-----------------
def check_exits_value(data,key,str):
    if data[key] is None:
        raise Exception("NOT FOUND KEY "+str)
    return data[key]

#---------EVENT MOUSE WHEEL-----------------
def mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    my_scrollbar.set(*canvas.yview())

#---------GET ZIPCODE INFORMATION-----------------
def get_zipcode_info():
    env = combobox_var.get().lower()
    switcher = {
            'local':'https://dev.beer.com.vn',
            'dev':'https://dev1.drbe.jp',
            'debug1':'https://debug1.drbe.jp',
            'beer1':'https://beer1-lampart.com.vn',
            'sql_agree':'agree',
        }
    url_root = switcher.get(env,'invalid')
    url = url_root +'/register/common/ajax_get_zipcode_information_for_new_lp'
    header = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36",
        "X-Requested-With": "xmlhttprequest",
    }
    data_zipcode = {
        'group':'delivery_new',
        'c_zipcode':zipcode_var.get(),
        'water_id':211,
    }
    request_zipcode = requests.post(url,data=data_zipcode,headers=header,verify=False)
    directory_zipcode = json.loads(request_zipcode.text)
    if(directory_zipcode['status'] == 1):
        print(directory_zipcode['data'])
        prefecture_var.set(directory_zipcode['data']['pref_name'])
        prefecture_id_var.set(directory_zipcode['data']['pref_id'])
        address1_var.set(str(directory_zipcode['data']['city_name']) + str(directory_zipcode['data']['town_name']) + '123')

#---------EVENT FOCUSOUT ZIPCODE-----------------
def on_focusout_zipcode(event):
    global entry_modified
    if entry_modified:
        entry_modified = False
        threading.Thread(target=get_zipcode_info).start()

def entry_modified(e):
    global entry_modified
    entry_modified = True

if __name__ == "__main__":
    asynco = asyncio.new_event_loop()
    tk_object = tk.Tk()
    tk_object.title("THE REGISTOR")
    # tk_object.geometry("750x350+100+100")
    tk_object.resizable(0,0)
    tk_object.bind_all("<Button-1>", lambda event: event.widget.focus_set() if isinstance(event.widget, tk.Widget) else None)
    custom_font = Font(family="Comic Sans MS", size=10)

    window1 = tk.Frame(tk_object)
    window1.grid(row=0, column=0, sticky='nsew')

    canvas = tk.Canvas(window1, width=1250, height=350)
    canvas.grid(row=0, column=0, sticky='nsew')

    my_scrollbar = tk.Scrollbar(window1, orient='vertical', command=canvas.yview)
    my_scrollbar.grid(row=0, column=1, sticky='nsew')

    canvas.configure(yscrollcommand=my_scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    window2 = tk.Frame(canvas)
    window3 = tk.Frame(canvas)
    window2.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    window3.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    window2.bind("<MouseWheel>", mouse_wheel)
    window3.bind("<MouseWheel>", mouse_wheel)
    canvas.create_window((0,0), window=window2, anchor='nw')
    canvas.create_window((0,215), window=window3, anchor='nw')
    window1.columnconfigure(0, weight=1)
    window1.rowconfigure(0, weight=1)

    result_get_file = get_input.generate_default_config_file(is_check_exist_default=True)
    if not result_get_file:
        messagebox.showinfo("Error", "Can not create config file")
        sys.exit()

    #variable input 
    combobox_var = tk.StringVar()
    email_var = tk.StringVar()
    pass_var = tk.StringVar()
    fname_var = tk.StringVar()
    lname_var = tk.StringVar()
    card_var_1 = tk.StringVar()
    card_var_2 = tk.StringVar()
    card_var_3 = tk.StringVar()
    card_var_4 = tk.StringVar()
    card_name_var = tk.StringVar()
    cvc_var = tk.StringVar()
    year_card_var = tk.StringVar()
    month_card_var = tk.StringVar()
    fname_kana_var = tk.StringVar()
    lname_kana_var = tk.StringVar()
    mode_var = tk.StringVar()
    zipcode_var = tk.StringVar()
    prefecture_var = tk.StringVar()
    prefecture_id_var = tk.StringVar()
    address1_var = tk.StringVar()

    #set default value
    default = get_input.get_config()
    email_var.set(default['email'])
    pass_var.set(default['password'])
    fname_var.set(default['first_name'])
    lname_var.set(default['last_name'])
    card_var_1.set(default['payment_card_no_1'])
    card_var_2.set(default['payment_card_no_2'])
    card_var_3.set(default['payment_card_no_3'])
    card_var_4.set(default['payment_card_no_4'])
    card_name_var.set(default['payment_card_name'])
    cvc_var.set(default['payment_card_cvc'])
    year_card_var.set(default['payment_expiry_year'])
    month_card_var.set(default['payment_expiry_month'])
    fname_kana_var.set(default['first_name_kana'])
    lname_kana_var.set(default['last_name_kana'])
    zipcode_var.set(default['zipcode'])
    prefecture_var.set(default['prefecture_id_text'])
    prefecture_id_var.set(default['prefecture'])
    address1_var.set(default['address_1'])


    #dropdown
    values = ['local', 'dev', 'debug1','beer1']
    combobox = ttk.Combobox(window2, values=values, width=22, state="readonly", textvariable=combobox_var)
    combobox.configure(font=custom_font)
    combobox.set('local')
    # combobox.bind("<<ComboboxSelected>>", on_focusout_zipcode)
    current_year = datetime.now().year
    years_list = [str(year) for year in range(current_year, current_year + 11)]
    month_list = [str(f'{month:02d}') for month in range(1, 13)]
    date_card_combobox_year = ttk.Combobox(window2, font=custom_font, state="readonly", width=5, values=years_list,textvariable=year_card_var)
    date_card_combobox_year.configure(font=custom_font)
    date_card_combobox_year.set(default['payment_expiry_year'])
    date_card_combobox_month = ttk.Combobox(window2, font=custom_font, state="readonly", width=5 , values=month_list ,textvariable=month_card_var)
    date_card_combobox_month.configure(font=custom_font)
    date_card_combobox_month.set(default['payment_expiry_month'])
    mode_combobox = ttk.Combobox(window2, font=custom_font, state="readonly", width=5 , values=['fast', 'manual'],textvariable=mode_var)
    mode_combobox.set('fast')

    #button
    button = tk.Button(window2, text="Submit",width=0, height=2, font=custom_font,bd=2, highlightthickness=2, highlightbackground="red")
    button.config(command=on_button_click)

    #progress bar
    progress_bar = ttk.Progressbar(window3, orient="horizontal", mode="determinate", length=680)

     #label
    label = tk.Label(window2, text="Environment :",font=custom_font)
    label_ps = tk.Label(window2, text="P/s: single click on field to copy !",font=custom_font)
    label_email = tk.Label(window2, text="Email :",font=custom_font)
    label_pass = tk.Label(window2, text="Passwork :",font=custom_font)
    label_fname = tk.Label(window2, text="First Name :",font=custom_font)
    label_lname = tk.Label(window2, text="Last Name :",font=custom_font)
    label_card = tk.Label(window2, text="Card :",font=custom_font)
    label_card_name = tk.Label(window2, text="Card Name :",font=custom_font)
    label_cvc = tk.Label(window2, text="CVC :",font=custom_font)
    label_date = tk.Label(window2, text="Date Expired :",font=custom_font)
    label_fname_kana = tk.Label(window2, text="First Name Kana :",font=custom_font)
    label_lname_kana = tk.Label(window2, text="Last Name Kana :",font=custom_font)
    label_mode = tk.Label(window2, text="Mode :",font=custom_font)
    label_zipcode = tk.Label(window2, text="Zipcode :",font=custom_font)
    label_prefecture = tk.Label(window2, text="Prefecture :",font=custom_font)
    label_prefecture_id = tk.Label(window2, text="Prefecture ID :",font=custom_font)
    label_address1 = tk.Label(window2, text="Address 1 :",font=custom_font)

    #entry
    email_entry = ttk.Entry(window2, width=25, font=custom_font, textvariable=email_var)
    pass_entry = ttk.Entry(window2, font=custom_font, textvariable=pass_var)
    fname_entry = ttk.Entry(window2, font=custom_font, textvariable=fname_var)
    lname_entry = ttk.Entry(window2, font=custom_font, textvariable=lname_var)
    card_entry_1 = ttk.Entry(window2, width=6, font=custom_font, textvariable=card_var_1)
    card_entry_2 = ttk.Entry(window2, width=6, font=custom_font, textvariable=card_var_2)
    card_entry_3 = ttk.Entry(window2, width=6, font=custom_font, textvariable=card_var_3)
    card_entry_4 = ttk.Entry(window2, width=6, font=custom_font, textvariable=card_var_4)
    card_entry_1.configure(state='readonly')
    card_entry_2.configure(state='readonly')
    card_entry_3.configure(state='readonly')
    card_entry_4.configure(state='readonly')
    card_name_entry = ttk.Entry(window2, width=1, font=custom_font, textvariable=card_name_var)
    cvc_entry = ttk.Entry(window2, width=6, font=custom_font, textvariable=cvc_var)
    fname_kana_entry = ttk.Entry(window2, font=custom_font, textvariable=fname_kana_var)
    lname_kana_entry = ttk.Entry(window2, font=custom_font, textvariable=lname_kana_var)
    zipcode_entry = ttk.Entry(window2, font=custom_font, textvariable=zipcode_var)
    is_modified = False
    zipcode_entry.bind("<Key>", entry_modified)
    zipcode_entry.bind("<FocusOut>", on_focusout_zipcode)
    prefecture_entry = ttk.Entry(window2, font=custom_font, textvariable=prefecture_var)
    prefecture_id_entry = ttk.Entry(window2, font=custom_font, textvariable=prefecture_id_var)
    prefecture_id_entry.configure(state='readonly')
    address1_entry = ttk.Entry(window2, font=custom_font, textvariable=address1_var)

    #grid
    paddingy = 3
    paddingx = 8
    label.grid(row=0, column=0, padx=5, pady=paddingy)
    combobox.grid(row=0, column=1, pady=paddingy)
    label_mode.grid(row=0, column=2, pady=paddingy)
    mode_combobox.grid(row=0, column=3, pady=paddingy)
    

    label_email.grid(row=1, column=0, padx=paddingx, pady=paddingy)
    email_entry.grid(row=1, column=1, sticky="ew")
    label_pass.grid(row=2, column=0, padx=paddingx, pady=paddingy)
    pass_entry.grid(row=2, column=1, sticky="ew")
    label_lname.grid(row=3, column=0, padx=paddingx, pady=paddingy)
    lname_entry.grid(row=3, column=1, sticky="ew")
    label_fname.grid(row=4, column=0, padx=paddingx,pady=paddingy)
    fname_entry.grid(row=4, column=1, sticky="ew")
    label_lname_kana.grid(row=5, column=0, padx=paddingx, pady=paddingy)
    lname_kana_entry.grid(row=5, column=1, sticky="ew")
    label_fname_kana.grid(row=6, column=0, padx=paddingx, pady=paddingy)
    fname_kana_entry.grid(row=6, column=1, sticky="ew")

    label_zipcode.grid(row=1, column=2, padx=paddingx, pady=paddingy)
    zipcode_entry.grid(row=1, column=3, sticky="ew")
    label_prefecture.grid(row=2, column=2, padx=paddingx, pady=paddingy)
    prefecture_entry.grid(row=2, column=3, sticky="ew")
    label_prefecture_id.grid(row=3, column=2, padx=paddingx, pady=paddingy)
    prefecture_id_entry.grid(row=3, column=3, sticky="ew")
    label_address1.grid(row=4, column=2, padx=paddingx, pady=paddingy)
    address1_entry.grid(row=4, column=3, sticky="ew")

    label_card.grid(row=1, column=5, padx=paddingx, pady=paddingy)
    card_entry_1.grid(row=1, column=6, sticky="ew", padx=1)
    card_entry_2.grid(row=1, column=7, sticky="ew", padx=1)
    card_entry_3.grid(row=1, column=8, sticky="ew", padx=1)
    card_entry_4.grid(row=1, column=9, sticky="ew", padx=1)
    label_card_name.grid(row=2, column=5, padx=paddingx, pady=paddingy)
    card_name_entry.grid(row=2, column=6, sticky="ew",columnspan=4)
    label_date.grid(row=3, column=5, padx=paddingx, pady=paddingy)
    date_card_combobox_year.grid(row=3, column=6, sticky="ew",padx=1)
    date_card_combobox_month.grid(row=3, column=7, sticky="ew",padx=1)
    label_cvc.grid(row=4, column=5, padx=paddingx, pady=paddingy)
    cvc_entry.grid(row=4, column=6, sticky="ew")
    button.grid(row=5, column=2, sticky="ew", rowspan=2, padx=paddingx, pady=paddingy)

    #progress bar
    progress_bar.grid(row=0, column=0, sticky="ew", padx=paddingx, pady=paddingy, columnspan=3)
    is_running = [False]
    tk_object.mainloop()