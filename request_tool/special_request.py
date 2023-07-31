from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from subprocess import CREATE_NO_WINDOW
import asyncio
from pyppeteer import launch


def format_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    element_debug= soup.find(id="codeigniter_profiler")
    element_head = soup.find("head")
    element_menu = soup.find_all("div",{'class': 'thank_you_text'})
    if element_debug:
        element_debug.extract()
    if element_head:
        element_head.extract()
    return soup

def perform_post_request_with_button_click(url, post_data):
    try:
        # Khởi tạo trình duyệt Chrome và mở URL
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-web-security')
        service = Service()
        if post_data.get('is_disable_brower') == '1':
            chrome_options.add_argument('--headless')
            service.creation_flags = CREATE_NO_WINDOW
        # caps = chrome_options.to_capabilities()
        # caps["acceptInsecureCerts"] = True
        # user_data_dir = '--user-data-dir=./chrome-profile'
        # chrome_options.add_argument(user_data_dir)
        driver = webdriver.Chrome(service=service,options=chrome_options)
        wait = WebDriverWait(driver, 10)
        driver.get("https://www.google.com")
        url_sub = url
        driver.execute_script("return document.readyState")
        post_data_str = ', '.join([f'''"{key}": "{value}"''' for key, value in post_data.items()])
        post_data_str = '{' + post_data_str + '}'
        script = f"""
            var form = document.createElement("form");
            form.method = "post";
            form.action = "{url_sub}";
            var postData = {post_data_str};
            for (var key in postData) {{
                var input = document.createElement("input");
                input.type = "hidden";
                input.name = key;
                input.value = postData[key];
                form.appendChild(input);
            }}

            document.body.appendChild(form);
            form.submit();
        """
        driver.execute_script(script)
        driver.execute_script("return document.readyState")

        # đợi cho trình duyệt load xong để xác định được button có classname = submit_button
        submit_button = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn_get_gmo_token")))
        #nhấn button
        submit_button[0].click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "redirect-url")))
        time.sleep(1)
        html = driver.page_source
        # Đóng trình duyệt sau khi hoàn thành
        return format_html(html)
    except Exception as e:
        print("Đã xảy ra lỗi:", e)
    driver.quit()    


async def perform_post_request_with_button_click1(url,content):
    headless = False
    if content.get('is_disable_brower') == '1':
        headless = True
    brower = await launch(headless=headless,handleSIGINT=False,handleSIGTERM=False,handleSIGHUP=False,ignoreHTTPSErrors=True)
    page = await brower.newPage()
    await page.goto("https://www.google.com")
    post_data_str = ', '.join([f'''"{key}": "{value}"''' for key, value in content.items()])
    post_data_str = '{' + post_data_str + '}'
    script = f"""
            var form = document.createElement("form");
            form.method = "post";
            form.action = "{url}";
            var postData = {post_data_str};
            for (var key in postData) {{
                var input = document.createElement("input");
                input.type = "hidden";
                input.name = key;
                input.value = postData[key];
                form.appendChild(input);
            }}

            document.body.appendChild(form);
            form.submit();
        """
    await page.evaluate(script)
    await page.waitForSelector('.btn_get_gmo_token')
    time.sleep(1)
    await page.click('.btn_get_gmo_token')
    await page.waitForSelector('.redirect-url')
    html = await page.content()
    await brower.close()
    return format_html(html)


# def perform_post_request_with_button_click1(sesion_obj,url,content):
#     # headers = {'Content-Type': 'application/json; charset=utf-8'}
#     # sesion_obj = HTMLSession()
#     r = sesion_obj.post(url, data=content,verify=False)
#     # time.sleep(3)
#     post_data_str = ', '.join([f'''"{key}": "{value}"''' for key, value in content.items()])
#     post_data_str = '{' + post_data_str + '}'
#     script = f"""
#             var form = document.createElement("form");
#             form.method = "post";
#             var postData = {post_data_str};
#             for (var key in postData) {{
#                 var input = document.createElement("input");
#                 input.type = "hidden";
#                 input.name = key;
#                 input.value = postData[key];
#                 form.appendChild(input);
#             }}

#             document.body.appendChild(form);
#     """
#     # script = f"""
#     #     (".btn_get_gmo_token").click();
#     # """
#     r.html.render(keep_page=True,wait=10,script=script)
#     r.html.page.waitForNavigation()
#     # r.html.page.click(".btn_get_gmo_token")
#     time.sleep(3)
#     print(r.html.html)
#     return format_html(r.html.html)


# if __name__ == "__main__":
#     url = "https://dev.beer.com.vn/my_account"  # Thay thế URL bằng địa chỉ trang web có biểu mẫu để điền thông tin và gửi POST
#     post_data = {
#         "key1": "dsadada",
#         "key2": "dasdadadadad",
#         # Thêm các trường và giá trị dữ liệu khác nếu cần thiết
#     }

    # perform_post_request_with_button_click(url, post_data)
