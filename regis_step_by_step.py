import time
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service

service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=service, options=options)


def step1():  # enter zipcode
    driver.find_element(By.ID, 'txt_confirm_zipcode').send_keys('1500000')
    driver.find_element(By.ID, 'btn-ajax-zipcode').click()


def step2(email):  # enter email
    driver.find_element(By.ID, 'txt_entrymailaddress').send_keys(email)
    driver.find_element(By.ID, 'txt_confirm_entrymailaddress').send_keys(email)
    driver.find_element(By.NAME, 'year_old').click()
    driver.find_element(By.NAME, 'agreement').click()
    driver.find_element(By.ID, 'email_register_address').click()


def step3():  # confirm service
    driver.find_element(By.ID, 'option_service').click()
    driver.find_element(By.ID, 'btn_next_step').click()


def step4():  # enter information's account
    driver.find_element(By.ID, 'c_last_name').send_keys('test')
    driver.find_element(By.ID, 'c_first_name').send_keys('test1')
    driver.find_element(By.ID, 'c_last_name_kana').send_keys('フリガナ')
    driver.find_element(By.ID, 'c_first_name_kana').send_keys('フリガナ')
    driver.find_element(By.XPATH, '//input[@name="c_sex_cd"][@value="2"]').click()
    Select(driver.find_element(By.ID, 'c_birth_date_year')).select_by_value('2000')
    Select(driver.find_element(By.ID, 'c_birth_date_month')).select_by_value('10')
    Select(driver.find_element(By.ID, 'c_birth_date_day')).select_by_value('24')
    driver.find_element(By.ID, 'c_address_1').send_keys('渋谷区以下に掲載がない場合454')
    driver.find_element(By.ID, 'c_phone_no').send_keys('0123456789')
    driver.find_element(By.ID, 'mypage_password').send_keys('lampart123')
    driver.find_element(By.ID, 'c_mypage_password_confirm').send_keys('lampart123')
    driver.find_element(By.ID, 'payment_card_no_1').send_keys('3540')
    driver.find_element(By.ID, 'payment_card_no_2').send_keys('1111')
    driver.find_element(By.ID, 'payment_card_no_3').send_keys('1111')
    driver.find_element(By.ID, 'payment_card_no_4').send_keys('1111')
    Select(driver.find_element(By.ID, 'payment_expiry_year')).select_by_value('2026')
    Select(driver.find_element(By.ID, 'payment_expiry_month')).select_by_value('04')
    driver.find_element(By.ID, 'payment_card_name').send_keys('dadasdsaasfa')
    driver.find_element(By.ID, 'payment_card_cvc').send_keys('2410')
    driver.find_element(By.XPATH, '//input[@name="agree"][@type="checkbox"]').click()
    driver.find_element(By.CLASS_NAME, 'btn_next_step').click()


def step5():
    driver.find_element(By.CLASS_NAME, 'btn_next_step').click()


def logout(url):
    driver.find_element(By.CLASS_NAME, 'user_login').click()
    driver.find_element(By.XPATH, '//a[@href="' + url + '/my_account/authenticate/logout"]').click()


def register():
    step1()
    print('FINISHED STEP 1')
    email = 'test' + datetime.now().strftime('%y%m%d%H%M%S') + '@gmail.com'
    time.sleep(2)
    step2(email)
    print('FINISHED STEP 2')
    time.sleep(2)
    step3()
    print('FINISHED STEP 3')
    time.sleep(2)
    step4()
    print('FINISHED STEP 4')
    step5()
    print('FINISHED STEP 5')
    print('DONE')
    print(email)
    time.sleep(3)


def one_quantum():
    while (True):
        env = input('Enter environment to create account (local/dev/debug1/beer1): ')

        switcher = {
            'local': 'https://dev.beer.com.vn',
            'dev': 'https://dev1.drbe.jp',
            'debug1': 'https://debug1.drbe.jp',
            'beer1': 'https://beer1-lampart.com.vn'
        }
        url_root = switcher.get(env, 'invalid')
        if (url_root == 'invalid'):
            continue
        else:
            break

    url = url_root + '/register/server/entrymailaddress'
    driver.get(url)
    driver.execute_script("return document.readyState")
    count = 1
    total = int(input('input total contract to register: '))
    while (count <= total):
        if (count == 1):
            register()
            if(total == 1):
                break
            count = count + 1
        if (count >= 2):
            logout(url_root)
            time.sleep(1)
            windown_before = driver.window_handles[0]
            driver.execute_script('window.open("' + url + '","_blank");')
            print('REGISTER CONTRACT NUMBER ' + str(count))
            time.sleep(1)
            windown_after = driver.window_handles[1]
            driver.close()
            driver.switch_to.window(windown_after)
            register()
            count = count + 1

def main():
    while True:
        one_quantum()


if __name__ == "__main__":
    main()
