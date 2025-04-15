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
from tkinter.scrolledtext import ScrolledText
from functools import partial


class tkinter_layout:
    tk_object = tk.Tk()

    def __init__(self):
        self.tk_object.title("THE REGISTOR")
        self.tk_object.resizable(0,0)
        # tk_object.geometry("750x350+100+100")
        self.tk_object.resizable(1,1)
        self.tk_object.bind_all("<Button-1>", lambda event: event.widget.focus_set() if isinstance(event.widget, tk.Widget) else None)
        custom_font = Font(family="Comic Sans MS", size=10)

        window1 = tk.Frame(self.tk_object)
        window1.grid(row=0, column=0, sticky='nsew')

        self.canvas = tk.Canvas(window1, width=1000, height=700)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        self.my_scrollbar = tk.Scrollbar(window1, orient='vertical', command=self.canvas.yview)
        self.my_scrollbar.grid(row=0, column=1, sticky='nsew')

        self.canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.tk_object.bind_all("<MouseWheel>", self.mouse_wheel)

        window2 = tk.Frame(self.canvas)
        window3 = tk.Frame(self.canvas)
        window2.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        window3.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        window2_canvas = self.canvas.create_window((0,0), window=window2, anchor='nw')
        window3_canvas = self.canvas.create_window((0,250), window=window3,anchor='nw')
        self.canvas.bind('<Configure>', lambda event: self.canvas.itemconfig(window2_canvas, height=event.height))

        result_get_file = get_input.generate_default_config_file(is_check_exist_default=True)
        if not result_get_file:
            messagebox.showinfo("Error", "Can not create config file")
            sys.exit()

        #variable input 
        default = get_input.get_config()
        self.combobox_var = tk.StringVar(value='local')
        self.email_var = tk.StringVar(value=default['email'])
        self.pass_var = tk.StringVar(value=default['password'])
        self.fname_var = tk.StringVar(value=default['first_name'])
        self.lname_var = tk.StringVar(value=default['last_name'])
        self.card_var_1 = tk.StringVar(value=default['payment_card_no_1'])
        self.card_var_2 = tk.StringVar(value=default['payment_card_no_2'])
        self.card_var_3 = tk.StringVar(value=default['payment_card_no_3'])
        self.card_var_4 = tk.StringVar(value=default['payment_card_no_4'])
        self.card_name_var = tk.StringVar(value=default['payment_card_name'])
        self.cvc_var = tk.StringVar(value=default['payment_card_cvc'])
        self.year_card_var = tk.StringVar(value=default['payment_expiry_year'])
        self.month_card_var = tk.StringVar(value=default['payment_expiry_month'])
        self.fname_kana_var = tk.StringVar(value=default['first_name_kana'])
        self.lname_kana_var = tk.StringVar(value=default['last_name_kana'])
        self.mode_var = tk.StringVar(value='fast')
        self.zipcode_var = tk.StringVar(value=default['zipcode'])
        self.prefecture_var = tk.StringVar(value=default['prefecture_id_text'])
        self.prefecture_id_var = tk.StringVar(value=default['prefecture'])
        self.address1_var = tk.StringVar(value=default['address_1'])
        self.customer_type_var = tk.StringVar(value=default['customer_type'])
        self.company_name_var = tk.StringVar(value=default['company_name'])
        self.company_name_kana_var = tk.StringVar(value=default['company_name_kana'])
        self.charge_name_var = tk.StringVar(value=default['charge_name'])
        self.charge_name_kana_var = tk.StringVar(value=default['charge_name_kana'])


        #dropdown
        values = list(default['env'].keys())
        self.combobox = ttk.Combobox(window2, values=values, width=22, state="readonly", textvariable=self.combobox_var)
        self.combobox.configure(font=custom_font)
        current_year = datetime.now().year
        years_list = [str(year) for year in range(current_year, current_year + 11)]
        month_list = [str(f'{month:02d}') for month in range(1, 13)]
        self.date_card_combobox_year = ttk.Combobox(window2, font=custom_font, state="readonly", width=5, values=years_list,textvariable=self.year_card_var)
        self.date_card_combobox_year.configure(font=custom_font)
        self.date_card_combobox_year.set(default['payment_expiry_year'])
        self.date_card_combobox_month = ttk.Combobox(window2, font=custom_font, state="readonly", width=5 , values=month_list ,textvariable=self.month_card_var)
        self.date_card_combobox_month.configure(font=custom_font)
        self.date_card_combobox_month.set(default['payment_expiry_month'])
        self.mode_combobox = ttk.Combobox(window2, font=custom_font, state="readonly", width=5 , values=['fast', 'manual'],textvariable=self.mode_var)


        #button
        self.button = tk.Button(window2, text="Submit",width=0, height=2, font=custom_font,bd=2, highlightthickness=2, highlightbackground="red",command=self.on_button_click)
        self.button_clear_output = tk.Button(window3, text="Clear Output", font=custom_font,bd=2, highlightthickness=2, highlightbackground="red",command=self.clear_output)
        self.button_action = tk.Button(window2, text="Action",height=2,font=custom_font,bd=2, highlightthickness=2, highlightbackground="red", command=self.tao_popup)

        #label
        self.label = tk.Label(window2, text="Environment :",font=custom_font)
        self.label_email = tk.Label(window2, text="Email :",font=custom_font)
        self.label_pass = tk.Label(window2, text="Passwork :",font=custom_font)
        self.label_fname = tk.Label(window2, text="First Name :",font=custom_font)
        self.label_lname = tk.Label(window2, text="Last Name :",font=custom_font)
        self.label_card = tk.Label(window2, text="Card :",font=custom_font)
        self.label_card_name = tk.Label(window2, text="Card Name :",font=custom_font)
        self.label_cvc = tk.Label(window2, text="CVC :",font=custom_font)
        self.label_date = tk.Label(window2, text="Date Expired :",font=custom_font)
        self.label_fname_kana = tk.Label(window2, text="First Name Kana :",font=custom_font)
        self.label_lname_kana = tk.Label(window2, text="Last Name Kana :",font=custom_font)
        self.label_mode = tk.Label(window2, text="Mode :",font=custom_font)
        self.label_zipcode = tk.Label(window2, text="Zipcode :",font=custom_font)
        self.label_prefecture = tk.Label(window2, text="Prefecture :",font=custom_font)
        self.label_prefecture_id = tk.Label(window2, text="Prefecture ID :",font=custom_font)
        self.label_address1 = tk.Label(window2, text="Address 1 :",font=custom_font)
        self.label_action = tk.Label(window2, text="You can buy some product, plan in Action button",font=custom_font)

        #entry
        self.email_entry = ttk.Entry(window2, width=25, font=custom_font, textvariable=self.email_var)
        self.pass_entry = ttk.Entry(window2, font=custom_font, textvariable=self.pass_var)
        self.company_name_or_fname_entry = ttk.Entry(window2, font=custom_font, textvariable=self.fname_var)
        self.charge_name_or_lname_entry = ttk.Entry(window2, font=custom_font, textvariable=self.lname_var)
        self.card_entry_1 = ttk.Entry(window2, width=6, font=custom_font, textvariable=self.card_var_1,state='readonly')
        self.card_entry_2 = ttk.Entry(window2, width=6, font=custom_font, textvariable=self.card_var_2,state='readonly')
        self.card_entry_3 = ttk.Entry(window2, width=6, font=custom_font, textvariable=self.card_var_3,state='readonly')
        self.card_entry_4 = ttk.Entry(window2, width=6, font=custom_font, textvariable=self.card_var_4,state='readonly')
        self.card_name_entry = ttk.Entry(window2, width=1, font=custom_font, textvariable=self.card_name_var)
        self.cvc_entry = ttk.Entry(window2, width=6, font=custom_font, textvariable=self.cvc_var)
        self.company_name_or_fname_kana_entry = ttk.Entry(window2, font=custom_font, textvariable=self.fname_kana_var)
        self.charge_name_or_lname_kana_entry = ttk.Entry(window2, font=custom_font, textvariable=self.lname_kana_var)
        self.zipcode_entry = ttk.Entry(window2, font=custom_font, textvariable=self.zipcode_var)
        self.is_modified = False
        self.zipcode_entry.bind("<Key>", self.on_focusin_zipcode)
        self.zipcode_entry.bind("<FocusOut>", self.on_focusout_zipcode)
        self.prefecture_entry = ttk.Entry(window2, font=custom_font, textvariable=self.prefecture_var)
        self.prefecture_id_entry = ttk.Entry(window2, font=custom_font, textvariable=self.prefecture_id_var,state='readonly')
        self.address1_entry = ttk.Entry(window2, font=custom_font, textvariable=self.address1_var)

        #radio
        self.radio_button_a = ttk.Radiobutton(window2, text="Personal ", variable=self.customer_type_var, value="1", command=self.show_entries)
        self.radio_button_b = ttk.Radiobutton(window2, text="Buiness ", variable=self.customer_type_var, value="2", command=self.show_entries)

        history_data = get_input.get_history_file()
        if history_data:
            all_history_data = list(history_data.keys())
        else:
            all_history_data = []
        self.progress_bar = ttk.Progressbar(window3, orient="horizontal", mode="determinate")
        self.progress_bar.bind("<Configure>", lambda e: self.progress_bar.configure(length=window2.winfo_width()))

        all_history_data.insert(0,'')
        self.combobox_date = ttk.Combobox(window3, width=10, values=all_history_data, font=custom_font, state="readonly")
        self.combobox_date.set(datetime.now().strftime("%Y-%m-%d"))
        self.combobox_date.bind("<<ComboboxSelected>>", lambda e: self.display_scroll_text(history_data,self.combobox_date.get()))

        self.text_widget_output = ScrolledText(window3, wrap=tk.WORD,height=21, font=custom_font, width=37, state='disabled')
        self.text_widget_history = ScrolledText(window3, wrap=tk.WORD,height=21, font=custom_font, state='disabled')
        # Hiển thị dữ liệu trong ScrolledText 
        self.display_scroll_text(history_data=history_data,is_specific_date=datetime.now().strftime("%Y/%m/%d"))


    def regis(self):
        try:
            self.button.config(state="disabled")
            start = time.time()
                
    #---------------------------------------------------------------------------------------
    #---------------------------------INPUT DATA--------------------------------------------
            input = get_input.get_config()
            first_name = input['first_name'] #first_name': 'tool',
            last_name = input['last_name'] #last_name': 'provjp',
            first_name_kana = input['first_name_kana'] #first_name_kana': 'フリガナ',
            last_name_kana = input['last_name_kana'] #last_name_kana': 'フリガナ',
            email = input['email']+'+'+ datetime.now().strftime('%y%m%d%H%M%S')+'@mobtest.mobi' #email': 'toolprovjpno1vodichvutru',
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
            company_name = input['company_name'] #company_name': 'lampart',
            company_name_kana = input['company_name_kana'] #company_name_kana': 'フリガナ',
            charge_name = input['charge_name'] #charge_name': 'chi',
            charge_name_kana = input['charge_name_kana'] #フリガナ': 'チ',
            chose_number_person = input['chose_number_person'] #chose_number_person': '1',
            switcher = input['env']
    #---------------------------------------------------------------------------------------
    #---------------------------------INPUT DATA--------------------------------------------
        


    #---------------------------------------------------------------------------------------
    #---------------------------------SYSTEM DATA-------------------------------------------
            tmp =[]
            session = requests.Session()
            csrf_key = 'chideptrai'
            headers ={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}
            env = self.combobox_var.get().lower()
            url_root = switcher.get(env,'invalid')
            if url_root == 'invalid':
                raise Exception('env config error')
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
            soup = BeautifulSoup(x.text,features="lxml")
            mail_token_input = soup.find_all('input', {'name': 'token'})
            if mail_token_input:
                mail_token_values = [input_tag['value'] for input_tag in mail_token_input]
                tmp.append(mail_token_values[0])
                self.update_output(progressbar_percent=20,progressbar_value='STEP 1/5: GET TOKEN MAIL DONE\n')
    #-----------------------------------------------------------------------------------------
    #---------------------------------SEND REQUEST 1------------------------------------------     

    #-----------------------------------------------------------------------------------------
    #---------------------------------SEND REQUEST 2------------------------------------------  
            data_step3 = {
                'token': tmp[0]
            }

            # get variable server
            n = session.post(url_step3,data=data_step3,verify=False)

            soup_server = BeautifulSoup(n.text,features="lxml")
            server_inputs = soup_server.find_all('input', {'name': 'server'})
            if not server_inputs: raise Exception('server_inputs input not found')
            if server_inputs:
                server_values = [input_tag['value'] for input_tag in server_inputs]
                ser_server = self.check_exits_value(server_values,0,'ser_server')
            # print(ser_server)

            # get variable campaign
            enterprise_inputs = soup_server.find_all('input', {'name': 'enterprise_campaign'})
            if not enterprise_inputs: raise Exception('enterprise_inputs input not found')
            if enterprise_inputs:
                enterprise_values = [input_tag['value'] for input_tag in enterprise_inputs]
                ser_enterprise_campaign = self.check_exits_value(enterprise_values,0,'ser_enterprise_campaign')
            # print(ser_enterprise_campaign)

            option_service_input = soup_server.find_all('input', {'name': 'option_service'})
            if not option_service_input: raise Exception('option_service_input input not found')
            if option_service_input:
                option_service_values = [input_tag['value'] for input_tag in option_service_input]
                ser_option_service = self.check_exits_value(option_service_values,0,'ser_option_service')

            partner_id_input = soup_server.find_all('input', {'name': 'aquisition_partner_id_check'})
            if not partner_id_input: raise Exception('partner_id_input input not found')
            if partner_id_input:
                partner_id_values = [input_tag['value'] for input_tag in partner_id_input]
                ser_partner_id = self.check_exits_value(partner_id_values,0,'ser_partner_id')

            campaign_page_code = soup_server.find_all('input', {'name': 'campaign_page_code'})
            if not campaign_page_code: raise Exception('campaign_page_code input not found')
            if campaign_page_code:
                campaign_page_code_values = [input_tag['value'] for input_tag in campaign_page_code]
                ser_campaign_page_code = self.check_exits_value(campaign_page_code_values,0,'campaign_page_code')
            
            self.update_output(progressbar_percent=40,progressbar_value='STEP 2/5: GET VARIABLE SERVER DONE\n')

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

            soup_agree = BeautifulSoup(request_agree.text,features="lxml")
            agree_inputs = soup_agree.find_all('input', {'name': 'agree'})
            if not agree_inputs: raise Exception('agree input not found')
            if agree_inputs:
                agree_values = [input_tag['value'] for input_tag in agree_inputs]
                con_agree = self.check_exits_value(agree_values,0,'con_agree')
            # print(con_agree)

            shop = soup_agree.find_all('input', {'name': 'gmo_authorization_shop_id'})
            if not shop: raise Exception('agree input not found')
            if shop:
                shop_values = [input_tag['value'] for input_tag in shop]
                tshop = self.check_exits_value(shop_values,0,'tshop')
            self.update_output(progressbar_percent=60,progressbar_value='STEP 3/5: GET VARIABLE AGREE DONE\n') 
    #-----------------------------------------------------------------------------------------
    #---------------------------------SEND REQUEST 3------------------------------------------  

            token = asyncio.run(special_request.get_gmo_token(env,tshop))
            if token['status'] == '551':
                raise Exception("FINAL REQUEST FAIL")
            if not token['token']:
                raise Exception("GET TOKEN FAIL, TOKEN EMPTY")
            self.update_output(progressbar_percent=80,progressbar_value='STEP 4/5: GET GMO TOKEN DONE\n')

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
                'con_choose_number_person':chose_number_person,
                'gmo_token':token['token'],
                'gmo_token_search_card_detail': token['token_search'],
                'gmo_token_3ds2': token['token_3ds2'],
            }
            if customer_type == '2':
                del data_final['con_c_first_name']
                del data_final['con_c_last_name']
                del data_final['con_c_first_name_kana']
                del data_final['con_c_last_name_kana']
                data_company = {
                    'con_c_company_full_name': company_name,
                    'con_c_company_full_name_kana': company_name_kana,
                    'con_c_charge_name': charge_name,
                    'con_c_charge_name_kana': charge_name_kana,
                }
                data_final = {**data_final, **data_company}
            
            html_rs = session.post(url_final,data=data_final,headers=headers ,verify=False)
            html_rs = special_request.format_html(html_rs.text)
            print(str(html_rs))
            text_success = html_rs.find('input', {'name': 'success_data[contract_id]'})
            text_success2 = html_rs.find('div', {'class': 'thank_you_text'})
            text_success3 = html_rs.find('div', {'class': 'success_text'})
            end = time.time()
            excution_time = end-start
            if(text_success or text_success2 or text_success3):
                contract_id = ''
                if text_success: contract_id = text_success['value']
                print(email)
                print(password_p)
                # set label_password text
                end = time.time()
                result_save = {
                    'email':email,
                    'password':password_p,
                    'contract_id':contract_id,
                    'excution_time':round(excution_time,2),
                    'date':datetime.now().strftime("%H:%M %Y/%m/%d"),
                    'env':env
                }
                get_input.generate_history_file(result_save)
                self.text_widget_history.configure(state='normal')
                self.text_widget_history.insert("1.0",''.join((f"{key}: {value}\n" for key,value in result_save.items()))+"==================================================\n")
                self.update_output(progressbar_percent=100,progressbar_value='STEP 5/5: REGISTER CONTRACT DONE\nALL FEATURE SUCCESS\n==========================================\n')
            else:
                raise Exception("FINAL REQUEST PROCESS FAIL")
        except Exception as e:
            print(e)
            self.update_output(progressbar_percent=0,progressbar_value=str(e)+"\n==========================================\n")
        session.close()
        self.button.config(state="normal")
        self.text_widget_history.configure(state='disable')
    
    def show_entries(self):
        customer_type = self.customer_type_var.get()
        paddingy = 3
        paddingx = 8
        if customer_type == '1':
            self.label_lname.config(text='Last Name :')
            self.label_fname.config(text='First Name :')
            self.label_lname_kana.config(text='Last Name Kana:')
            self.label_fname_kana.config(text='First Name Kana :')
            self.charge_name_or_lname_entry.config(textvariable=self.lname_var)
            self.charge_name_or_lname_kana_entry.config(textvariable=self.lname_kana_var)
            self.company_name_or_fname_entry.config(textvariable=self.fname_var)
            self.company_name_or_fname_kana_entry.config(textvariable=self.fname_kana_var)
        if customer_type == '2':
            self.label_lname.config(text='Charge Name :')
            self.label_fname.config(text='Company Name :')
            self.label_lname_kana.config(text='Charge Name Kana :')
            self.label_fname_kana.config(text='Company Name Kana :')
            self.charge_name_or_lname_entry.config(textvariable=self.charge_name_var)
            self.charge_name_or_lname_kana_entry.config(textvariable=self.charge_name_kana_var)
            self.company_name_or_fname_entry.config(textvariable=self.company_name_var)
            self.company_name_or_fname_kana_entry.config(textvariable=self.company_name_kana_var)

        self.label_lname.grid(row=4, column=0, padx=paddingx, pady=paddingy)
        self.charge_name_or_lname_entry.grid(row=4, column=1, sticky="ew")
        self.label_fname.grid(row=5, column=0, padx=paddingx,pady=paddingy)
        self.company_name_or_fname_entry.grid(row=5, column=1, sticky="ew")
        self.label_lname_kana.grid(row=6, column=0, padx=paddingx, pady=paddingy)
        self.charge_name_or_lname_kana_entry.grid(row=6, column=1, sticky="ew")
        self.label_fname_kana.grid(row=7, column=0, padx=paddingx, pady=paddingy)
        self.company_name_or_fname_kana_entry.grid(row=7, column=1, sticky="ew")

    #---------CALL FUNCTION REGIS BY BROWER-----------------
    def do_regis_by_brower(self):
        env = self.combobox_var.get().lower()
        self.button.config(state="disabled")
        widget = {
            'progress_bar':self.progress_bar,
            'text_widget_output':self.text_widget_output,
        }
        result_brower = asyncio.run(special_request.regis_by_browser(env,widget))
        if result_brower:
            result_data = {
                'email':result_brower['email'],
                'password':result_brower['password'],
                'excution_time':round(result_brower['excution_time'],2),
                'date':datetime.now().strftime("%H:%M %Y/%m/%d"),
                'env':env
            }
            self.text_widget_history.insert("1.0",''.join((f"{key}: {value}\n" for key,value in result_data.items()))+"==================================================\n")
            get_input.generate_history_file(result_data)
        self.button.config(state="normal")

    #---------ONCLICK TRIGGER FUNCTION-----------------
    def on_button_click(self):
        input_display = {
            'email': self.email_var.get(),
            'password' : self.pass_var.get(),
            'first_name': self.fname_var.get(),
            'last_name': self.lname_var.get(),
            'first_name_kana': self.fname_kana_var.get(),
            'last_name_kana': self.lname_kana_var.get(),
            'payment_card_no_1': self.card_var_1.get(),
            'payment_card_no_2': self.card_var_2.get(),
            'payment_card_no_3': self.card_var_3.get(),
            'payment_card_no_4': self.card_var_4.get(),
            'payment_expiry_year': self.year_card_var.get(),
            'payment_expiry_month': self.month_card_var.get(),
            'payment_card_name': self.card_name_var.get(),
            'payment_card_cvc': self.cvc_var.get(),
            'zipcode': self.zipcode_var.get(),
            'prefecture': self.prefecture_id_var.get(),
            'prefecture_id_text': self.prefecture_var.get(),
            'address_1': self.address1_var.get(),
            'customer_type': self.customer_type_var.get(),
            'company_name': self.company_name_var.get(),
            'company_name_kana': self.company_name_kana_var.get(),
            'charge_name': self.charge_name_var.get(),
            'charge_name_kana': self.charge_name_kana_var.get(),
        }
        is_write_complete = get_input.set_config(input_display)
        if not is_write_complete:
            messagebox.showerror('Error','Opps something wrong happen, it seem config file is invalid')
            return
        mode = self.mode_var.get()
        if mode == 'manual':
            threading.Thread(target=self.do_regis_by_brower).start()
        elif mode == 'fast':
            threading.Thread(target=self.regis).start()

    #---------CHECK VALUE EXIST-----------------
    def check_exits_value(self,data,key,str):
        if data[key] is None:
            raise Exception("NOT FOUND KEY "+str)
        return data[key]

    #---------GET ZIPCODE INFORMATION-----------------
    def get_zipcode_info(self):
        input = get_input.get_config()
        env = self.combobox_var.get().lower()
        switcher = input['env']
        url_root = switcher.get(env,'invalid')
        if url_root == 'invalid':
            return
        url = url_root +'/register/common/ajax_get_zipcode_information_for_new_lp'
        header = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36",
            "X-Requested-With": "xmlhttprequest",
        }
        data_zipcode = {
            'group':'delivery_new',
            'c_zipcode':self.zipcode_var.get(),
            'water_id':211,
        }
        request_zipcode = requests.post(url,data=data_zipcode,headers=header,verify=False)
        directory_zipcode = json.loads(request_zipcode.text)
        if(directory_zipcode['status'] == 1):
            print(directory_zipcode['data'])
            self.prefecture_var.set(directory_zipcode['data']['pref_name'])
            self.prefecture_id_var.set(directory_zipcode['data']['pref_id'])
            self.address1_var.set(str(directory_zipcode['data']['city_name']) + str(directory_zipcode['data']['town_name']) + '123')

    #---------EVENT FOCUSOUT ZIPCODE-----------------
    def on_focusout_zipcode(self,event):
        if self.is_modified:
            self.is_modified = False
            threading.Thread(target=self.get_zipcode_info).start()

    def on_focusin_zipcode(self,event):
        self.is_modified = True
        
    #---------EVENT MOUSE WHEEL-----------------
    def mouse_wheel(self,event):
        if isinstance(event.widget, tk.Widget)  and not isinstance(event.widget, ScrolledText):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            self.my_scrollbar.set(*self.canvas.yview())


    def display_scroll_text(self,history_data,is_specific_date=False):
            self.text_widget_history.configure(state='normal')
            self.text_widget_history.delete("1.0",tk.END)
            if is_specific_date:
                history_data = history_data.get(is_specific_date)
                if not history_data:
                    self.text_widget_history.insert("end","No data\n")
                    self.text_widget_history.configure(state='disable')
                    return
                for history in history_data[::-1]:
                    self.text_widget_history.insert("end",''.join((f"{key}: {value +' '+is_specific_date if key == 'time' else value}\n" for key,value in history.items()))+"==================================================\n")
                self.text_widget_history.configure(state='disable')
                return
            for date, histories in sorted(history_data.items(), key=lambda item: item[0], reverse=True):
                for history in histories[::-1]:
                    self.text_widget_history.insert("end",''.join((f"{key}: {value +' '+date if key == 'time' else value}\n" for key,value in history.items()))+"==================================================\n")
            self.text_widget_history.configure(state='disable')

    def update_output(self,progressbar_percent,progressbar_value):
        self.progress_bar["value"] = progressbar_percent
        self.progress_bar.update()
        self.text_widget_output.configure(state='normal')
        self.text_widget_output.insert("end",progressbar_value)
        self.text_widget_output.configure(state='disable')

    def clear_output(self):
        self.text_widget_output.configure(state='normal')
        self.text_widget_output.delete("1.0",tk.END)
        self.text_widget_output.configure(state='disable')

    def tao_popup(self):
        custom_font = Font(family="Comic Sans MS", size=10)
        popup = tk.Toplevel(self.tk_object)
        popup.title("Action")
        popup.geometry("400x200")
        popup.resizable(0,0)
        
        # Khóa màn hình chính
        popup.grab_set()
        input = get_input.get_config()
        env = self.combobox_var.get().lower()
        url_root = input['env'].get(env,'invalid')
        if url_root == 'invalid': messagebox.showinfo("Error", "Opps, wrong config file, please check again")

        contracts = get_input.get_history_file()
        # max_date = max(contracts.keys())
        # latest_contract = contracts.get(max_date,[])
        latest_contract = {}
        reversed_contracts = dict(sorted(contracts.items(), key=lambda item: item[0], reverse=True))
        for date,list_contract in reversed_contracts.items():
            list_contract = list_contract[::-1]
            for contract_item in list_contract:
                if contract_item.get('env','') == env:
                    latest_contract = contract_item
                    break
            if latest_contract:
                break        

    
        latest_email = latest_contract.get('email','')
        latest_password = latest_contract.get('password','')
        latest_contract_id = latest_contract.get('contract_id','')

        email_login_var = tk.StringVar(value=latest_email)
        pass_login_var = tk.StringVar(value=latest_password)
        action_var = tk.StringVar(value="Buy 2 ramdom beer")

        email_login = ttk.Entry(popup, width=50, font=custom_font, textvariable=email_login_var)
        pass_login = ttk.Entry(popup,width=50, font=custom_font ,textvariable=pass_login_var)

        action_list = [
            'Buy 2 ramdom beer',
            'Buy Omakase plan',
            'Buy Select plan',
            'Buy Premium plan',
        ]
        action_combobox = ttk.Combobox(popup, values=action_list, width=50, state="readonly", textvariable=action_var)


        label1 = tk.Label(popup, text="The email and password will be automatically filled")
        label2 = tk.Label(popup, text="in according to the contract that you last successfully registered with")


        def excute_process_but():
            params = {
                'email':email_login_var.get(),
                'password':pass_login_var.get(),
                'url_root':url_root,
                'action':action_var.get(),
            }
            threading.Thread(target=special_request.process_buy,args=[params]).start()

        button_buy = tk.Button(popup, text="Submit",width=0, height=2, font=custom_font,bd=2, highlightthickness=2, command=excute_process_but)
        email_login.pack(padx=20, pady=5)
        pass_login.pack(padx=20, pady=5)
        action_combobox.pack(padx=20, pady=5)
        label1.pack(padx=20, pady=2)
        label2.pack(padx=20, pady=2)
        button_buy.pack(padx=20, pady=5)

    def build(self):
        #grid
        paddingy = 3
        paddingx = 8
        self.label.grid(row=0, column=0, padx=5, pady=paddingy)
        self.combobox.grid(row=0, column=1, pady=paddingy)
        self.label_mode.grid(row=0, column=2, pady=paddingy)
        self.mode_combobox.grid(row=0, column=3, pady=paddingy)
        

        self.label_email.grid(row=1, column=0, padx=paddingx, pady=paddingy)
        self.email_entry.grid(row=1, column=1, sticky="ew")
        self.label_pass.grid(row=2, column=0, padx=paddingx, pady=paddingy)
        self.pass_entry.grid(row=2, column=1, sticky="ew")
        self.radio_button_a.grid(row=3, column=0, padx=paddingx, pady=paddingy)
        self.radio_button_b.grid(row=3, column=1, padx=paddingx, pady=paddingy)
        self.show_entries()

        self.label_zipcode.grid(row=1, column=2, padx=paddingx, pady=paddingy)
        self.zipcode_entry.grid(row=1, column=3, sticky="ew")
        self.label_prefecture.grid(row=2, column=2, padx=paddingx, pady=paddingy)
        self.prefecture_entry.grid(row=2, column=3, sticky="ew")
        self.label_prefecture_id.grid(row=3, column=2, padx=paddingx, pady=paddingy)
        self.prefecture_id_entry.grid(row=3, column=3, sticky="ew")
        self.label_address1.grid(row=4, column=2, padx=paddingx, pady=paddingy)
        self.address1_entry.grid(row=4, column=3, sticky="ew")
        self.label_action.grid(row=5, column=2, padx=paddingx, pady=paddingy, columnspan=2)
        # action_combobox.grid(row=5, column=3, sticky="ew")

        self.label_card.grid(row=1, column=5, padx=paddingx, pady=paddingy)
        self.card_entry_1.grid(row=1, column=6, sticky="ew", padx=1)
        self.card_entry_2.grid(row=1, column=7, sticky="ew", padx=1)
        self.card_entry_3.grid(row=1, column=8, sticky="ew", padx=1)
        self.card_entry_4.grid(row=1, column=9, sticky="ew", padx=1)
        self.label_card_name.grid(row=2, column=5, padx=paddingx, pady=paddingy)
        self.card_name_entry.grid(row=2, column=6, sticky="ew",columnspan=4)
        self.label_date.grid(row=3, column=5, padx=paddingx, pady=paddingy)
        self.date_card_combobox_year.grid(row=3, column=6, sticky="ew",padx=1)
        self.date_card_combobox_month.grid(row=3, column=7, sticky="ew",padx=1)
        self.label_cvc.grid(row=4, column=5, padx=paddingx, pady=paddingy)
        self.cvc_entry.grid(row=4, column=6, sticky="ew")
        self.button.grid(row=6, column=2, sticky="ew", rowspan=2, padx=paddingx, pady=paddingy)
        self.button_action.grid(row=6, column=3, sticky="ew", rowspan=2, padx=paddingx, pady=paddingy)

        self.progress_bar.grid(row=0, column=0, sticky="w", padx=paddingx, pady=paddingy,columnspan=3)
        self.text_widget_output.grid(row=2, column=0, sticky="w", padx=paddingx, pady=paddingy)
        self.combobox_date.grid(row=1, column=1, sticky="w", padx=paddingx, pady=paddingy)
        self.button_clear_output.grid(row=1, column=0, sticky="w", padx=paddingx, pady=paddingy)
        self.text_widget_history.grid(row=2, column=1, sticky="w", padx=paddingx, pady=paddingy, columnspan=2)
        self.tk_object.mainloop()


if __name__ == "__main__":
    layout = tkinter_layout()
    layout.build()