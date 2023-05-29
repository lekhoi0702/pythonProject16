import socket
from tkinter import messagebox
import tkinter as tk

group_test = "224.1.1.1"
port_test = 3000

def check_input(group, port):
    # Kiểm tra xem địa chỉ multicast group có hợp lệ hay không
    try:
        socket.inet_pton(socket.AF_INET, group)
    except socket.error:
        messagebox.showerror("Lỗi", "Địa chỉ multicast group không hợp lệ!")
        return False

    # Kiểm tra xem port có hợp lệ hay không
    try:
        port = int(port)
        if not (1024 <= port <= 65535):
            raise ValueError
    except (ValueError, TypeError):
        messagebox.showerror("Lỗi", "Port không hợp lệ!")
        return False

    return True

def send_data():
    group = group_entry.get()
    port = port_entry.get()
    data = data_entry.get()
    if not check_input(group, port):
        return

    if not data:
        messagebox.showerror("Lỗi", "Vui lòng nhập dữ liệu gửi!")
        return

    # Tạo socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    # Gửi dữ liệu qua multicast
    sock.sendto(data.encode(), (group, int(port)))

    sock.close()

# Tạo giao diện đồ họa
root = tk.Tk()
root.title("Multicast App")

group_label = tk.Label(root, text="Địa chỉ multicast group:")
group_label.pack()
group_entry = tk.Entry(root)
group_entry.pack()

port_label = tk.Label(root, text="Port:")
port_label.pack()
port_entry = tk.Entry(root)
port_entry.pack()

data_label = tk.Label(root, text="Nội dung dữ liệu:")
data_label.pack()
data_entry = tk.Entry(root, font=('Arial', 12), width=40)
data_entry.pack()

send_button = tk.Button(root, text="Gửi", command=send_data)
send_button.pack()

root.mainloop()
