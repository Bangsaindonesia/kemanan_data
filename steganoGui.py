import os
from stegano import lsb
import tkinter as tk
from tkinter import filedialog, messagebox

def get_image_path():
    # Mengubah filter file agar dapat memilih gambar dengan ekstensi .jpg dan .png
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg")])
    if file_path:
        return file_path
    else:
        return None

def hide_message_gui():
    img_path = get_image_path()
    if not img_path:
        messagebox.showerror("Error", "Path gambar tidak valid atau tidak dipilih.")
        return

    message = message_entry.get()
    if not message:
        messagebox.showerror("Error", "Pesan tidak boleh kosong.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if not save_path:
        messagebox.showerror("Error", "Path untuk menyimpan gambar tidak valid atau tidak dipilih.")
        return

    try:
        secret = lsb.hide(img_path, message)
        secret.save(save_path)
        messagebox.showinfo("Success", f"Pesan berhasil disembunyikan dalam gambar.\nGambar disimpan di: {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan gambar: {e}")

def show_message_gui():
    img_path = get_image_path()
    if not img_path:
        messagebox.showerror("Error", "Path gambar tidak valid atau tidak dipilih.")
        return

    try:
        clear_message = lsb.reveal(img_path)
        if clear_message:
            hidden_message_textbox.config(state="normal")
            hidden_message_textbox.delete("1.0", tk.END)
            hidden_message_textbox.insert(tk.END, clear_message)
            hidden_message_textbox.config(state="disabled")
        else:
            messagebox.showinfo("Info", "Tidak ada pesan tersembunyi dalam gambar ini.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menampilkan pesan dari gambar: {e}")

def exit_app():
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Steganography Tool - GUI Version")
root.geometry("450x450")
root.configure(bg="#F5F5F5")

# Widgets
frame = tk.Frame(root, padx=10, pady=10, bg="#F5F5F5")
frame.pack(expand=True)

title_label = tk.Label(frame, text="Steganography Tool", font=("Helvetica", 18, "bold"), bg="#F5F5F5", fg="#4A90E2")
title_label.pack(pady=15)

message_label = tk.Label(frame, text="Pesan Rahasia:", font=("Arial", 12), bg="#F5F5F5", fg="#333333")
message_label.pack()

message_entry = tk.Entry(frame, width=40, bg="#E8F0FE", fg="#000000", relief="solid", borderwidth=1, font=("Arial", 10))
message_entry.pack(pady=10)

hide_button = tk.Button(frame, text="Sembunyikan Pesan", command=hide_message_gui, width=25, bg="#4A90E2", fg="white", font=("Arial", 10, "bold"), relief="raised")
hide_button.pack(pady=10)

reveal_button = tk.Button(frame, text="Tampilkan Pesan", command=show_message_gui, width=25, bg="#4A90E2", fg="white", font=("Arial", 10, "bold"), relief="raised")
reveal_button.pack(pady=10)

# Hidden Message Display
hidden_message_label = tk.Label(frame, text="Pesan Tersembunyi:", font=("Arial", 12), bg="#F5F5F5", fg="#333333")
hidden_message_label.pack(pady=10)

hidden_message_textbox = tk.Text(frame, height=5, width=40, bg="#E8F0FE", fg="#000000", relief="solid", borderwidth=1, font=("Arial", 10))
hidden_message_textbox.pack(pady=10)
hidden_message_textbox.config(state="disabled")  # Set to readonly initially

exit_button = tk.Button(frame, text="Keluar", command=exit_app, width=25, bg="#D0021B", fg="white", font=("Arial", 10, "bold"), relief="raised")
exit_button.pack(pady=20)

# Run the GUI
root.mainloop()
