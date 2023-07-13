SRC ĐƯỢC VIẾT BẰNG PYTHON

# Cài đặt
 1. vào thư mục file build chạy file exe để sử dụng

Các file .py bên ngoài là src code 
+ post.py và post_ver1.py là src tự động gửi request thẳng lên server để tạo tài khoản
Ưu điểm: nhanh + nhàn không phải suy nghĩ nhiều có thể sử dụng nhiều môi trường
Nhược điểm: trong src hard code khá nhiều lâu lâu hệ thống đổi lớn quá lỗi ráng chịu, đổi sương sương thì không sao

+ regis_step_by_step.py là src regis step by step tự động chạy bằng thư viện selenium
Ưu điểm: tự động có thể ngắc ở bất cứ step nào để thao tác thủ công phù hợp cho việc debug tìm lỗi
Nhược điểm: lâu vãi l** lâu hơn cách trên, nhưng có thể treo máy để nó tự tạo