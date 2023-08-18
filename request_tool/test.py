import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Hiển thị dữ liệu")

# Tạo dữ liệu mẫu (có thể thay thế bằng dữ liệu thực)
data = [
    ("1", "John", "Doe"),
    ("2", "Jane", "Smith"),
    ("3", "Alice", "Johnson"),
    ("1", "John", "Doe"),
    ("2", "Jane", "Smith"),
    ("3", "Alice", "Johnson"),
    ("1", "John", "Doe"),
    ("2", "Jane", "Smith"),
    ("3", "Alice", "Johnson"),
    ("1", "John", "Doe"),
    ("2", "Jane", "Smith"),
    ("3", "Alice", "Johnson"),
    ("1", "John", "Doe"),
    ("2", "Jane", "Smith"),
    ("3", "Alice", "Johnson")
]

# Tạo cửa sổ mới để hiển thị dữ liệu dưới dạng table
table_window = tk.Toplevel(root)
table_window.title("Bảng Dữ liệu")

# Tạo header cho bảng
header = ["ID", "First Name", "Last Name"]
tree = ttk.Treeview(table_window, columns=header, show="headings")
for col in header:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill="both", expand=True)

# Thêm dữ liệu vào bảng
for row in data:
    tree.insert("", "end", values=row)

# Tạo cửa sổ mới để hiển thị dữ liệu dưới dạng text để thao tác
text_window = tk.Toplevel(root)
text_window.title("Dữ liệu dạng Text")

# Tạo một ScrolledText để hiển thị và thao tác với dữ liệu
text_widget = ScrolledText(text_window, wrap=tk.WORD)
text_widget.pack(fill="both", expand=True)

# Hiển thị dữ liệu trong ScrolledText
for row in data:
    text_widget.insert("end", "\t".join(row) + "\n")

# Bắt đầu mainloop
root.mainloop()
