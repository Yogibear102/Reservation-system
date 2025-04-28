# client_gui.py
import tkinter as tk
from tkinter import messagebox
import socket

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def refresh_tables():
    try:
        client.sendall(b"SHOW")
        data = client.recv(1024).decode()
        table_status = data.split(",")

        for i in range(len(table_buttons)):
            if i < len(table_status):
                parts = table_status[i].split(":")
                if len(parts) == 2:
                    status = parts[1]
                    table_buttons[i].config(
                        text=f"Table {i+1}\n{status}",
                        state=tk.NORMAL if status == "Free" else tk.DISABLED
                    )
                else:
                    table_buttons[i].config(
                        text=f"Table {i+1}\nError",
                        state=tk.DISABLED
                    )
            else:
                table_buttons[i].config(
                    text=f"Table {i+1}\nN/A",
                    state=tk.DISABLED
                )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to refresh tables.\n{e}")

def book_table(table_num):
    name = name_entry.get().strip()
    time = time_entry.get().strip()
    if not name or not time:
        messagebox.showerror("Input Error", "Please enter both name and time.")
        return

    message = f"BOOK,{table_num},{name},{time}"
    client.sendall(message.encode())
    response = client.recv(1024).decode()
    messagebox.showinfo("Booking Result", response)
    refresh_tables()

# GUI
root = tk.Tk()
root.title("EasyEats Table Booking")
root.geometry("400x400")

tk.Label(root, text="Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Time:").pack()
time_entry = tk.Entry(root)
time_entry.pack()

tk.Label(root, text="Select a table to book:").pack(pady=10)

table_frame = tk.Frame(root)
table_frame.pack()

table_buttons = []

for i in range(5):  # 5 tables
    btn = tk.Button(table_frame, text=f"Table {i+1}", width=12, height=3,
                    command=lambda i=i: book_table(i+1))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    table_buttons.append(btn)

refresh_btn = tk.Button(root, text="Refresh Tables", command=refresh_tables)
refresh_btn.pack(pady=10)

refresh_tables()

root.mainloop()
