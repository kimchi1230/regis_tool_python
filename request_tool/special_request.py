# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from subprocess import CREATE_NO_WINDOW
from bs4 import BeautifulSoup
from pyppeteer import launch
import get_input
import asyncio
import time
from datetime import datetime
import os
import sys
from urllib.parse import unquote
import requests
import aiohttp
import random
import json

def format_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    element_debug= soup.find(id="codeigniter_profiler")
    element_head = soup.find("head")
    if element_debug:
        element_debug.extract()
    if element_head:
        element_head.extract()
    return soup

# def perform_post_request_with_button_click(url, post_data):
    # try:
    #     # Khởi tạo trình duyệt Chrome và mở URL
    #     chrome_options = Options()
    #     chrome_options.add_argument('--ignore-certificate-errors')
    #     chrome_options.add_argument('--ignore-ssl-errors')
    #     chrome_options.add_argument('--allow-running-insecure-content')
    #     chrome_options.add_argument('--disable-web-security')
    #     service = Service()
    #     if post_data.get('is_disable_brower') == '1':
    #         chrome_options.add_argument('--headless')
    #         service.creation_flags = CREATE_NO_WINDOW
    #     # caps = chrome_options.to_capabilities()
    #     # caps["acceptInsecureCerts"] = True
    #     # user_data_dir = '--user-data-dir=./chrome-profile'
    #     # chrome_options.add_argument(user_data_dir)
    #     driver = webdriver.Chrome(service=service,options=chrome_options)
    #     wait = WebDriverWait(driver, 10)
    #     driver.get("https://www.google.com")
    #     url_sub = url
    #     driver.execute_script("return document.readyState")
    #     post_data_str = ', '.join([f'''"{key}": "{value}"''' for key, value in post_data.items()])
    #     post_data_str = '{' + post_data_str + '}'
    #     script = f"""
    #         var form = document.createElement("form");
    #         form.method = "post";
    #         form.action = "{url_sub}";
    #         var postData = {post_data_str};
    #         for (var key in postData) {{
    #             var input = document.createElement("input");
    #             input.type = "hidden";
    #             input.name = key;
    #             input.value = postData[key];
    #             form.appendChild(input);
    #         }}

    #         document.body.appendChild(form);
    #         form.submit();
    #     """
    #     driver.execute_script(script)
    #     driver.execute_script("return document.readyState")

    #     # đợi cho trình duyệt load xong để xác định được button có classname = submit_button
    #     submit_button = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn_get_gmo_token")))
    #     #nhấn button
    #     submit_button[0].click()
    #     wait.until(EC.presence_of_element_located((By.CLASS_NAME, "redirect-url")))
    #     time.sleep(1)
    #     html = driver.page_source
    #     # Đóng trình duyệt sau khi hoàn thành
    #     return format_html(html)
    # except Exception as e:
    #     print("Đã xảy ra lỗi:", e)
    # driver.quit()    


# async def perform_post_request_with_button_click1(url,content):
#     try:
#         html_file_path = os.path.join(os.path.dirname(__file__), 'test.html')
#         headless = False
#         if content.get('is_disable_brower') == '1':
#             headless = True
#         brower = await launch(headless=headless,handleSIGINT=False,handleSIGTERM=False,handleSIGHUP=False,ignoreHTTPSErrors=True)
#         page = await brower.newPage()
#         await page.goto("https://www.google.com")
#         post_data_str = ', '.join([f'''"{key}": "{value}"''' for key, value in content.items()])
#         post_data_str = '{' + post_data_str + '}'
#         script = f"""
#                 var form = document.createElement("form");
#                 form.method = "post";
#                 form.action = "{url}";
#                 var postData = {post_data_str};
#                 for (var key in postData) {{
#                     var input = document.createElement("input");
#                     input.type = "hidden";
#                     input.name = key;
#                     input.value = postData[key];
#                     form.appendChild(input);
#                 }}

#                 document.body.appendChild(form);
#                 form.submit();
#             """
#         await page.evaluate(script)
#         await page.waitForSelector('.btn_get_gmo_token')
#         time.sleep(1)
#         await page.click('.btn_get_gmo_token')
#         await page.waitForSelector('.redirect-url')
#         html = await page.content()
#         await brower.close()
#         return format_html(html)
#     except Exception as e:
#         await brower.close()
#         return False

def update_output(widget,progressbar_percent,progressbar_text):
    widget['progress_bar']["value"] = progressbar_percent
    widget['progress_bar'].update()
    widget['text_widget_output'].configure(state='normal')
    widget['text_widget_output'].insert("end",progressbar_text)
    widget['text_widget_output'].configure(state='disable')

def save_data_from_browser(request):
    if url_root_module in request.url:
        print("URL:", request.url)
        print("Method:", request.method)
        print("Headers:", request.headers)
        print("PostData:", request.postData)
        post = request.postData
        if post:
            post = unquote(post)
            data_pilt = post.split('&')
            input_value = {}
            for pair in data_pilt:
                key, value = pair.split('=')
                input_value[key] = value



async def regis_by_browser(env,widget=None):
    try:
        if getattr(sys, 'frozen', False): 
            exe_path = sys._MEIPASS  
        else:
            exe_path = os.path.abspath(".") 
        path = os.path.join(exe_path,"local-chromium","588429","chrome-win32","chrome.exe")        
        start = time.time()
        input = get_input.get_config()
        have_widget = bool(widget)
        switcher = input['env']
        url_root = switcher.get(env,'invalid')
        if url_root == 'invalid':
            raise Exception('env config error')
        
        global url_root_module
        url_root_module = url_root + '/register/success/code/registration'
        url = url_root + '/register/server/entrymailaddress'
        email = input['email']+'+'+ datetime.now().strftime('%y%m%d%H%M%S')+ '@mobtest.mobi'
        headless = False
        brower = await launch(executablePath=path,headless=headless,handleSIGINT=False,handleSIGTERM=False,handleSIGHUP=False,ignoreHTTPSErrors=True,defaultViewport=None)
        page = await brower.newPage()
        page.on('request', save_data_from_browser)
        await page.goto(url)
        await page.type('#txt_confirm_zipcode',input['zipcode'])
        await page.waitForSelector('#btn-ajax-zipcode')
        await page.click('#btn-ajax-zipcode')
        await asyncio.sleep(1)
        await page.waitForSelector('#txt_entrymailaddress')
        await asyncio.sleep(2)
        await page.type('#txt_entrymailaddress',email)
        await page.type('#txt_confirm_entrymailaddress',email)
        await page.click('input[name="year_old"]')
        await page.click('input[name="agreement"]')
        await page.click('#email_register_address')
        if have_widget:
            update_output(widget=widget,progressbar_percent=20,progressbar_text='STEP 1/4: DONE\n')
        
        await page.waitForNavigation()
        await page.waitForSelector('#option_service')
        await page.click('#personal_credit_gmo')
        await page.click('#btn_next_step')
        if have_widget:
            update_output(widget=widget,progressbar_percent=40,progressbar_text='STEP 2/4: DONE\n')

        await page.waitForNavigation()
        await page.waitForSelector('#c_last_name')
        await page.type('#c_last_name',input['last_name'])
        await page.type('#c_first_name',input['first_name'])
        await page.type('#c_last_name_kana',input['last_name_kana'])
        await page.type('#c_first_name_kana',input['first_name_kana'])
        await page.click('input[name="c_sex_cd"][value="2"]')
        await page.select('select[name="c_birth_date_year"]',input['birth_date_year'])
        await page.select('select[name="c_birth_date_month"]',input['birth_date_month'])
        await page.select('select[name="c_birth_date_day"]',input['birth_date_day'])
        await page.type('#c_address_1',input['address_1'])
        await page.type('#c_phone_no',input['phone_no'])
        await page.type('#mypage_password',input['password'])
        await page.type('#c_mypage_password_confirm',input['password'])
        await page.type('#payment_card_no_1',input['payment_card_no_1'])
        await page.type('#payment_card_no_2',input['payment_card_no_2'])
        await page.type('#payment_card_no_3',input['payment_card_no_3'])
        await page.type('#payment_card_no_4',input['payment_card_no_4'])
        await page.select('select[name="payment_expiry_year"]',input['payment_expiry_year'])
        await page.select('select[name="payment_expiry_month"]',input['payment_expiry_month'])
        await page.type('#payment_card_name',input['payment_card_name'])
        await page.type('#payment_card_cvc',input['payment_card_cvc'])
        await page.click('input[name="agree"][type="checkbox"]')
        await page.click('.btn_next_step')
        if have_widget:
            update_output(widget=widget,progressbar_percent=60,progressbar_text='STEP 3/4: DONE\n')

        await page.waitForNavigation()
        await page.waitForSelector('.btn_next_step')
        await asyncio.sleep(1)
        await page.click('.btn_next_step')
        await page.waitForSelector(selector='.redirect-url',timeout=0)
        end = time.time()
        await brower.close()
        if have_widget:
            update_output(widget=widget,progressbar_percent=100,progressbar_text='STEP 4/4: DONE\n==========================================\n')
        return {
            'email':email,
            'password':input['password'],
            'excution_time':end-start
        }
    except Exception as e:
        await brower.close()
        print(e)
        return False
        

async def get_gmo_token(env,tshop):
    if getattr(sys, 'frozen', False): 
        exe_path = sys._MEIPASS  
    else:
        exe_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(exe_path,"local-chromium","588429","chrome-win32","chrome.exe")
    input = get_input.get_config()

    switcher = input['env']
    url_root = switcher.get(env,'invalid')
    if url_root == 'invalid': 
        raise Exception('env config error')
    
    card = input['payment_card_no_1']+input['payment_card_no_2']+input['payment_card_no_3']+input['payment_card_no_4']
    expire = input['payment_expiry_year'][-2:]+input['payment_expiry_month']
    html_file_path = os.path.join(os.path.expanduser("~"), "Documents","regis_tool","post1.html") + '?env='+ url_root
    headless = False
    if input.get('is_disable_brower') == '1':
        headless = True
    brower = await launch(executablePath=path,headless=headless,handleSIGINT=False,handleSIGTERM=False,handleSIGHUP=False,ignoreHTTPSErrors=True,args=['--ignore-certificate-errors'])   
    page = await brower.newPage()
    await page.goto(html_file_path)
    await asyncio.sleep(1)
    script = f""" 
                 Multipayment.init("{tshop}");
                 Multipayment.getToken({{
                        cardno       : "{card}",
                        expire       : "{expire}",
                        securitycode : "{input['payment_card_cvc']}",
                        holdername   : "{input['payment_card_name']}",
                        tokennumber  : 3
                 }}, function(response){{
                    console.log(response.resultCode);
                    console.log(response.tokenObject.token[0]);
                    document.getElementById("resultCode").innerHTML = response.resultCode;
                    document.getElementById("token").innerHTML = response.tokenObject.token[0];
                    document.getElementById("token_search").innerHTML = response.tokenObject.token[1];
                    document.getElementById("token_3ds2").innerHTML = response.tokenObject.token[2];
                 }});"""
    await page.evaluate(script)
    await asyncio.sleep(1)
    html = await page.content()
    soup_token = BeautifulSoup(html, 'html.parser')
    token = soup_token.find(id='token').text
    token_search = soup_token.find(id='token_search').text
    token_3ds2 = soup_token.find(id='token_3ds2').text
    result = soup_token.find(id='resultCode').text
    await brower.close()
    return {
        'status':result,
        'token':token,
        'token_search':token_search,
        'token_3ds2':token_3ds2,
    }


async def fetch_data(url,method='get'):
    async with aiohttp.ClientSession() as session:
        async with session.get(url,verify_ssl=False) as response:
            return await response.text()

def process_buy(params):
    url_beer = params['url_root'] + '/ec/beer'
    url_login = params['url_root'] + '/my_account/authenticate/login'
    url_cart = params['url_root'] + '/ec/cart'
    url_add_cart = params['url_root'] + '/frontend/ajaxAddCart'
    url_confirmation = params['url_root'] + '/ec/cart/confirmation'

    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36",
    }
    session = requests.Session()
    action = params.get('action','')
    try:
        login_data = {
            'login_id': params['email'],
            'password': params['password']
        }
        request_login = session.post(url_login,data=login_data,verify=False,headers=headers)
        soup_login = BeautifulSoup(request_login.text, 'html.parser')
        error_login = soup_login.find(class_='errors_message')
        if error_login:
            raise Exception('ERROR WHEN LOGIN, ERROR MESSAGE:'+error_login.text)
        layout.update_output(progressbar_percent=10,progressbar_value='STEP 1/5: LOGIN SUCCESS\n')

        if action == 'Buy 2 ramdom beer':
            request_beer = session.get(url_beer,verify=False,headers=headers)
            soup_beer = BeautifulSoup(request_beer.content, 'html.parser')
            page_list = soup_beer.find_all('a', {'class': 'page-numbers'})
            page_number = [page.text for page in page_list]
            max_page = 1
            if page_number:
                max_page = max(page_number)
            
            tasks = [asyncio.run(fetch_data(url_beer + '?page=' + str(i))) for i in range(1, int(max_page) + 1)]
            beer_id_list = []
            for task in tasks:
                html_page = BeautifulSoup(task, 'html.parser')
                beer_list = html_page.find_all('a', attrs={'data-product-id': True})
                beer_id_list.extend([tag['data-product-id'] for tag in beer_list if 'out-of-stock' not in tag.get('class', [])])

            if not beer_id_list or len(beer_id_list) < 2:
                raise Exception('Not enough beer')
            
            post_beer = random.sample(beer_id_list, 2)
            layout.update_output(progressbar_percent=30,progressbar_value='STEP 2/5: GET BEER SUCCESSFULLY\n')
            
            for beer in post_beer:
                header_ajax = {
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36",
                    "X-Requested-With": "xmlhttprequest",
                }
                value_step1 = {
                    'product_id': beer,
                    'quantity': 1,
                    'product_category': 1
                }
                request_add_cart = session.post(url_add_cart,data=value_step1,headers=header_ajax,verify=False)
                response_add_cart = json.loads(request_add_cart.text)
                if response_add_cart['status'] == 0:
                    raise Exception('ERROR WHEN ADD TO CART, ERROR MESSAGE: '+response_add_cart['message'])
            layout.update_output(progressbar_percent=50,progressbar_value='STEP 3/5: ADD TO CART SUCCESSFULLY\n')

            value_step1 = {
                f'order_quantity[{post_beer[0]}]':1,
                f'order_quantity[{post_beer[1]}]':1,
            }
            request_cart= session.post(url_cart,data=value_step1,headers=headers,verify=False)
            html_cart = BeautifulSoup(request_cart.text, 'html.parser')
            delivery_date = html_cart.find('input',{'name':'delivery_date'})
            if not delivery_date:
                raise Exception('ERROR WHEN GET DELIVERY DATE')
            delivery_date = delivery_date.get('value')
            layout.update_output(progressbar_percent=70,progressbar_value='STEP 4/5: GET DELIVERY DATE SUCCESSFULLY\n')

            value_confirm = {
                f'product_id[{post_beer[0]}]':1,
                f'product_id[{post_beer[1]}]':1,
                'delivery_date': delivery_date,
                'delivery_time': '1',
                'coupon_id': '0',
                'is_confirm_order': '1',
                'url_before_update_cart':url_confirmation,
            }
            request_confirmation = session.post(url_confirmation,data=value_confirm,headers=headers,verify=False)
            html_confirmation = BeautifulSoup(request_confirmation.text, 'html.parser')
            success_text = html_confirmation.find(class_='cart_success')
            if not success_text:
                raise Exception('ERROR WHEN CONFIRM ORDER')
            layout.update_output(progressbar_percent=100,progressbar_value='STEP 5/5: CONFIRM ORDER SUCCESSFULLY\n==========================================\n')
            result = {
                'status':True,
                'message':'Buy 2 ramdom beer success'
            }
        elif action == 'Buy Omakase plan':
            return
        elif action == 'Buy Select plan':
            return
        elif action == 'Buy Premium plan':
            return
        else:
            return
    except Exception as e:
        result = {
            'status':False,
            'message':str(e)
        }
        layout.update_output(progressbar_percent=0,progressbar_value=str(e)+'\n==========================================\n')
    session.close()
    return result    


if __name__ == "__main__":
    process_buy({'password':'lampart123','email':'toolprovjpno1vodichvutru240110102426@lampart-vn.com', 'action':'Buy 2 ramdom beer','url_root':'https://dev.beer.com.vn'})
