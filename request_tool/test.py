import win32crypt

def decrypt_dpapi(encrypted_data_blob):
    try:
        decrypted_data = win32crypt.CryptUnprotectData(encrypted_data_blob, None, None, None, 0)[1]
        return decrypted_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Hex string từ hình ảnh (loại bỏ khoảng trắng và xuống dòng)
    encrypted_blob_hex = (
        "763130eeb446dfd19637f4799c42db5f"
"986d347ecb3a0ad8a877d3b5cf2bd04d"
"e4bf9f3598e504d08b"
    )
    
    # Chuyển đổi hex string sang bytes
    encrypted_blob_bytes = bytes.fromhex(encrypted_blob_hex)
    # encrypted_blob_bytes =  encrypted_blob_bytes.decode('utf-8', errors='ignore')
    print("Encrypted data:", encrypted_blob_bytes)
    
    # Giải mã dữ liệu
    decrypted_data = decrypted_data = win32crypt.CryptUnprotectData(encrypted_blob_bytes, None, None, None, 0)[1]
    
    if decrypted_data:
        print("Decrypted data:", decrypted_data.decode('utf-8', errors='ignore'))
    else:
        print("Decryption failed.")
