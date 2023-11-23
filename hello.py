import pymsgbox

buttons = ['Không','Có']
while True:
    rs = pymsgbox.alert('Chuẩn bị xóa system32, bạn đồng ý không? ', button=buttons)
    if rs == buttons[0]:
        tmp = pymsgbox.alert('Không bạn chạy file EXE này là bạn sai rồi, mất system32 nhé', button=buttons)
        if tmp == buttons[0]:
            pymsgbox.alert('Vẫn không à, vậy chơi game nhé', button=buttons)
            break