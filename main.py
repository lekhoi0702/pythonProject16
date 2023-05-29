import socket
import struct
import tkinter as tk

def receive_data(group, port, message_text):
    # Tạo socket và thiết lập các giá trị cần thiết
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', int(port)))
    mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Nhận dữ liệu từ multicast group
    while True:
        data, addr = sock.recvfrom(1024)
        message_text.config(state=tk.NORMAL)
        message_text.insert(tk.END, f"Nhận từ {addr[0]}: {data.decode()}\n")
        message_text.config(state=tk.DISABLED)

    sock.close()

def start_server():
    group = group_entry.get()
    port = port_entry.get()
    receive_data(group, port, message_text)

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

start_button = tk.Button(root, text="Bắt đầu nhận", command=start_server)
start_button.pack()

message_label = tk.Label(root, text="Dữ liệu nhận được:")
message_label.pack()
message_text = tk.Text(root)
message_text.pack()
message_text.config(state=tk.DISABLED)

root.mainloop()
