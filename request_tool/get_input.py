import os
import json

input = {}
input_default = {
    'first_name': 'tool',
    'last_name': 'provjp',
    'first_name_kana': 'フリガナ',
    'last_name_kana': 'フリガナ',
    'email': 'toolprovjpno1vodichvutru',
    'password' : 'lampart123',
    'birth_date_year': '1993',
    'birth_date_month': '10',
    'birth_date_day': '24',
    'sex_cd': '2',
    'phone_no': '0994984984',
    'address_2': '',
    'is_disable_brower': '1',
#---------------DO NOT CHANGE BELOW INPUT-----------------
    'server_rental': '1',
    'water': '211',
    'holder_color': '3',
    'customer_type': '1',
    'settlement_type': 'credit_card_gmo',
    "plan_type": "1",
#---------------DO NOT CHANGE BELOW INPUT-----------------
#---------------YOU CAN CHANGE IF YOU SURE DATA IS VALID IN SERVER----------------
    "payment_card_no_1": "3540",
    "payment_card_no_2": "1111",
    "payment_card_no_3": "1111",
    "payment_card_no_4": "1111",
    "payment_expiry_year": "2026",
    "payment_expiry_month": "01",
    "payment_card_name": "chi",
    "payment_card_cvc": "2410",
    'zipcode': '1500000',
    'prefecture': '13',
    'prefecture_id_text': '東京都',
    'address_1': '渋谷区以下に掲載がない場合454',
#---------------YOU CAN CHANGE IF YOU SURE DATA IS VALID IN SERVER----------------
    'company_name': 'lampart',
    'company_name_kana': 'フリガナ',
    'charge_name': 'chi',
    'charge_name_kana': 'フリガナ',
    'chose_number_person':'2',
    'env': {
        'local':'https://dev.beer.com.vn',
        'dev':'https://dev1.drbe.jp',
        'debug1':'https://debug1.drbe.jp',
        'beer1':'https://beer1-lampart.com.vn',
        'beer':'https://beer-lampart.com.vn',
    }
}

file_path = os.path.join(os.path.expanduser("~"), "Documents","regis_tool","config_input.json")

#read file config
def get_config():
    with open(file_path, 'r', encoding='utf-8') as file:
        input = json.load(file)
    return input

#write file config
def set_config(content,mode = 'w',is_default = False):
    try:
        data_change = content
        if not is_default:
            data_change = get_content_write_file(content)
            if not data_change:
                return True
        with open(file_path, mode, encoding='utf-8') as file:
            json.dump(data_change, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(e)
        return False

# check diff content and get diff content if valid 
def get_content_write_file(content):
    input = get_config()
    is_change = False
    for key, value in content.items():
        if not value: raise Exception('input blank')
        if input[key] != value:
            input[key] = value
            is_change = True
    if is_change:
        return input
    return False

# generate default config file
def generate_default_config_file(is_check_exist_default = False, is_delete_previous = False):
    if is_check_exist_default and os.path.exists(file_path):
        return True
    if is_delete_previous and os.path.exists(file_path):
        os.remove(file_path)
    folder_name = os.path.join(os.path.expanduser("~"), "Documents","regis_tool")
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    result_txt_file = set_config(input_default,'a+',True)
    result_html_file = generate_html_file('')
    return result_txt_file or result_html_file
    
def generate_html_file(content):
    try:
        html_path = os.path.join(os.path.expanduser("~"), "Documents","regis_tool","post1.html")
        if os.path.exists(html_path):
            return True
        content = """
            <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
            <div id="url"></div>
            <div id="resultCode"></div>
            <div id="token"></div>
            <div id="token_search"></div>
            <div id="token_3ds2"></div>
            <script>
                const urlParams = new URLSearchParams(window.location.search);
                let env = urlParams.get('env');
                url = env + '/public/common/js/multipayment_gmo_token_test.js';
                document.getElementById("url").innerHTML = url;
                var newScript = document.createElement('script');
                newScript.src = url;
                document.head.appendChild(newScript);

                // const cardno = urlParams.get('cardno');
                // const expire = urlParams.get('expire');
                // const cvc = urlParams.get('cvc');
                // const name = urlParams.get('name');
                // const tshop = urlParams.get('tshop');
                // const cardno = "3540111111111111";
                // const expire = "2605";
                // const cvc = "1234";
                // const name = "TEST";
                // const tshop = "tshop00060960";

                // Multipayment.init(tshop);
                // Multipayment.getToken({
                //         cardno       : cardno,
                //         expire       : expire,
                //         securitycode : cvc,
                //         holdername   : name,
                //         tokennumber  : 1
                // }, function(response){
                //     console.log(response.resultCode);
                //     console.log(response.tokenObject.token[0]);
                //     document.getElementById("resultCode").innerHTML = response.resultCode;
                //     document.getElementById("token").innerHTML = response.tokenObject.token[0];
                // });
            </script>
            </body>
            </html>
        """
        with open(html_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        print(e)
        return False

def generate_history_file(data):
    try:
        time = data['date'][:5]
        date = data['date'][6:]
        history_data = {
            'email': data['email'],
            'password': data['password'],
            'contract_id':data['contract_id'],
            'excution_time': data['excution_time'],
            'time': time,
            'env': data['env'],
        }
        history_data_file = {}
        history_path = os.path.join(os.path.expanduser("~"), "Documents","regis_tool","history.json")
        if os.path.exists(history_path):
            with open(history_path, 'r', encoding='utf-8') as file:
                if file:
                    history_data_file = json.load(file)

        if history_data_file.get(date):
            history_data_file[date].append(history_data)
        else:
            history_data_file[date] = [history_data]
        
        with open(history_path, 'w', encoding='utf-8') as file:
            json.dump(history_data_file, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(e)
        return False

def get_history_file():
    history_path = os.path.join(os.path.expanduser("~"), "Documents","regis_tool","history.json")
    if os.path.exists(history_path):
        with open(history_path, 'r', encoding='utf-8') as file:
            if file:
                history_data_file = json.load(file)
                return history_data_file
    return {}
# def main():
#     generate_history_file('')


# if __name__ == '__main__':
#     main()