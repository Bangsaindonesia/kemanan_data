import tkinter as tk
from tkinter import ttk

class CaesarCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Program Enkripsi & Dekripsi - Caesar Cipher")
        self.root.geometry("600x500")
        self.root.configure(bg="#F0F8FF")  # untuk warna (AliceBlue)

        # Nilai pergeseran
        self.shift_value = tk.IntVar(value=3)  # otomatis 3 (default)

        # Membuat tab
        self.tab_control = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab1, text='Enkripsi')
        self.tab_control.add(self.tab2, text='Dekripsi')
        self.tab_control.pack(expand=1, fill="both")
        
        # Tab Enkripsi
        self.setup_enkripsi_tab()
        
        # Tab Dekripsi
        self.setup_dekripsi_tab()
    
    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def setup_enkripsi_tab(self):
        # Untuk sudut kotak melengkung
        canvas = tk.Canvas(self.tab1, bg="#F0F8FF", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Kotak sudut melengkung untuk pengaturan pergeseran
        self.create_rounded_rectangle(canvas, 20, 20, 560, 100, radius=20, fill="#FFDEAD", outline="#FFA07A")
        tk.Label(canvas, text="Jumlah Pergeseran:", bg="#FFDEAD", fg="black", font=("Arial", 10, "bold")).place(x=40, y=40)
        shift_spinbox = ttk.Spinbox(canvas, from_=1, to=25, width=5, textvariable=self.shift_value)
        shift_spinbox.place(x=160, y=40)

        # Kotak sudut melengkung untuk plainteks
        self.create_rounded_rectangle(canvas, 20, 110, 560, 230, radius=20, fill="#FFDEAD", outline="#FFA07A")
        tk.Label(canvas, text="Masukkan Plainteks:", bg="#FFDEAD", fg="black", font=("Arial", 10, "bold")).place(x=40, y=130)
        self.plaintext_input = tk.Text(canvas, height=5, width=55, bg="#FFFACD", fg="#8B0000", wrap="word", borderwidth=1, relief="solid")
        self.plaintext_input.place(x=40, y=150)

        # Tombol enkripsi
        tk.Button(canvas, text="Enkripsi", command=self.encrypt, bg="#FF7F50", fg="black", font=("Arial", 10, "bold"), relief="flat").place(x=260, y=250)

        # Kotak sudut melengkung untuk cipherteks
        self.create_rounded_rectangle(canvas, 20, 290, 560, 410, radius=20, fill="#FFDEAD", outline="#FFA07A")
        tk.Label(canvas, text="Hasil Enkripsi (Cipherteks):", bg="#FFDEAD", fg="black", font=("Arial", 10, "bold")).place(x=40, y=310)
        self.cipher_output = tk.Text(canvas, height=5, width=55, bg="#FFFACD", fg="#8B0000", wrap="word", borderwidth=1, relief="solid")
        self.cipher_output.place(x=40, y=330)

    def setup_dekripsi_tab(self):
        # Canvas untuk kotak sudut melengkung
        canvas = tk.Canvas(self.tab2, bg="#F0F8FF", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Kotak sudut melengkung untuk pengaturan pergeseran
        self.create_rounded_rectangle(canvas, 20, 20, 560, 100, radius=20, fill="#FFDEAD", outline="#FFA07A")
        tk.Label(canvas, text="Jumlah Pergeseran:", bg="#FFDEAD", fg="black", font=("Arial", 10, "bold")).place(x=40, y=40)
        shift_spinbox = ttk.Spinbox(canvas, from_=1, to=25, width=5, textvariable=self.shift_value)
        shift_spinbox.place(x=160, y=40)

        # Kotak sudut melengkung untuk cipherteks
        self.create_rounded_rectangle(canvas, 20, 110, 560, 180, radius=20, fill="#FFDEAD", outline="#FFA07A")
        tk.Label(canvas, text="Masukkan Cipherteks:", bg="#FFDEAD", fg="black", font=("Arial", 10, "bold")).place(x=40, y=130)
        self.cipher_input = tk.Text(canvas, height=2, width=55, bg="#FFFACD", fg="#8B0000", wrap="word", borderwidth=1, relief="solid")
        self.cipher_input.place(x=40, y=150)

        # Tombol dekripsi
        tk.Button(canvas, text="Dekripsi", command=self.decrypt, bg="#FF7F50", fg="black", font=("Arial", 10, "bold"), relief="flat").place(x=260, y=200)

        # Kotak sudut melengkung untuk plainteks hasil dekripsi
        self.create_rounded_rectangle(canvas, 20, 240, 560, 310, radius=20, fill="#FFDEAD", outline="#FFA07A")
        tk.Label(canvas, text="Hasil Dekripsi (Plainteks):", bg="#FFDEAD", fg="black", font=("Arial", 10, "bold")).place(x=40, y=260)
        self.plain_output = tk.Text(canvas, height=2, width=55, bg="#FFFACD", fg="#8B0000", wrap="word", borderwidth=1, relief="solid")
        self.plain_output.place(x=40, y=280)

    def shift_character(self, char, shift, encrypt=True):
        if not char.isalpha():
            return char
            
        ascii_base = 97 if char.islower() else 65
        if not encrypt:
            shift = -shift
        shifted = (ord(char) - ascii_base + shift) % 26
        return chr(shifted + ascii_base)
    
    def process_text(self, text, encrypt=True):
        shift = self.shift_value.get()
        result = ''
        for char in text:
            result += self.shift_character(char, shift, encrypt)
        return result
    
    def encrypt(self):
        plaintext = self.plaintext_input.get("1.0", tk.END).strip()
        ciphertext = self.process_text(plaintext, encrypt=True)
        self.cipher_output.delete("1.0", tk.END)
        self.cipher_output.insert("1.0", ciphertext)
    
    def decrypt(self):
        ciphertext = self.cipher_input.get("1.0", tk.END).strip()
        plaintext = self.process_text(ciphertext, encrypt=False)
        self.plain_output.delete("1.0", tk.END)
        self.plain_output.insert("1.0", plaintext)

if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherApp(root)
    root.mainloop()
