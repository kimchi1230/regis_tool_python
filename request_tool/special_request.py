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
    

async def regis_by_browser(url):
    try:
        start = time.time()
        input = get_input.get_config()
        env = 'local'
        switcher = {
            'local':'https://dev.beer.com.vn',
            'dev':'https://dev1.drbe.jp',
            'debug1':'https://debug1.drbe.jp',
            'beer1':'https://beer1-lampart.com.vn'
        }
        url_root = switcher.get(env,'invalid')
        url = url_root + '/register/server/entrymailaddress'
        email = input['email']+ datetime.now().strftime('%y%m%d%H%M%S')+ '@lampart-vn.com'
        headless = False
        brower = await launch(headless=headless,handleSIGINT=False,handleSIGTERM=False,handleSIGHUP=False,ignoreHTTPSErrors=True)
        page = await brower.newPage()
        await page.goto(url)
        await page.type('#txt_confirm_zipcode',input['zipcode'])
        await page.waitForSelector('#btn-ajax-zipcode')
        await page.click('#btn-ajax-zipcode')
        await page.waitForSelector('#txt_entrymailaddress')
        await asyncio.sleep(2)
        await page.type('#txt_entrymailaddress',email)
        await page.type('#txt_confirm_entrymailaddress',email)
        await page.click('input[name="year_old"]')
        await page.click('input[name="agreement"]')
        await page.click('#email_register_address')
        

        await page.waitForSelector('#option_service')
        await page.click('#personal_credit_gmo')
        await page.click('#btn_next_step')

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

        await page.waitForSelector('.btn_get_gmo_token')
        await page.click('.btn_get_gmo_token')
        await page.waitForSelector('.redirect-url')
        end = time.time()
        return {
            'email':email,
            'password':input['password'],
            'excution_time':end-start
        }
    except Exception as e:
        return False

async def get_gmo_token(env,tshop):
    input = get_input.get_config()
    switcher = {
        'local':'https://dev.beer.com.vn',
        'dev':'https://dev1.drbe.jp',
        'debug1':'https://debug1.drbe.jp',
        'beer1':'https://beer1-lampart.com.vn'
    }
    url_root = switcher.get(env,'invalid')
    card = input['payment_card_no_1']+input['payment_card_no_2']+input['payment_card_no_3']+input['payment_card_no_4']
    expire = input['payment_expiry_year'][-2:]+input['payment_expiry_month']
    html_file_path = os.path.join(os.path.dirname(__file__), 'test.html')+ '?env='+ url_root
    headless = False
    if input.get('is_disable_brower') == '1':
        headless = True
    brower = await launch(headless=headless,handleSIGINT=False,handleSIGTERM=False,handleSIGHUP=False,ignoreHTTPSErrors=True,args=['--ignore-certificate-errors'])   
    page = await brower.newPage()
    await page.goto(html_file_path)
    script = f""" 
                 Multipayment.init("{tshop}");
                 Multipayment.getToken({{
                        cardno       : "{card}",
                        expire       : "{expire}",
                        securitycode : "{input['payment_card_cvc']}",
                        holdername   : "{input['payment_card_name']}",
                        tokennumber  : 1
                 }}, function(response){{
                    console.log(response.resultCode);
                    console.log(response.tokenObject.token[0]);
                    document.getElementById("resultCode").innerHTML = response.resultCode;
                    document.getElementById("token").innerHTML = response.tokenObject.token[0];
                 }});"""
    await page.evaluate(script)
    await asyncio.sleep(1)
    html = await page.content()
    soup_token = BeautifulSoup(html, 'html.parser')
    token = soup_token.find(id='token').text
    result = soup_token.find(id='resultCode').text
    await brower.close()
    return {
        'status':result,
        'token':token,
    }
   

if __name__ == "__main__":
    asyncio.run(get_gmo_token(''))

    # perform_post_request_with_button_click(url, post_data)
