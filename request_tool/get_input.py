import os

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
    'server_rental': '2',
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
}

file_path = os.path.join(os.path.expanduser("~"), "Documents","config_input.txt")

#read file config
def get_config():
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            key, value = line.split('=')
            key = key.strip()
            line = line.strip()
            input[key] = value
    return input

#write file config
def set_config(content,mode = 'w',is_default = False):
    try:
        data_change = content
        if not is_default:
            data_change = get_content_write_file(content)
            if not data_change:
                return True
        content_file = '\n'.join([f'{key}={value}' for key, value in data_change.items()])+'\n'
        with open(file_path, mode, encoding='utf-8') as file:
            file.write(content_file)
        return True
    except Exception as e:
        print(e)
        return False

# check diff content and get diff content if valid 
def get_content_write_file(content):
    input = get_config()
    is_change = False
    for key, value in content.items():
        if input.get(key) and input[key] != value:
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
    return set_config(input_default,'a+',True)
    



# def main():
#     rs = generate_default_config_file()
#     print(get_config())
#     set_config({
#         'email': 'abcxuz',
#         'pass' : 'asadsadad',
#     })
#     print(rs)
#     print(get_config())


# if __name__ == '__main__':
#     main()