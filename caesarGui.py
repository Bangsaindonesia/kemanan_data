import tkinter as tk
from tkinter import ttk

class CaesarCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Program Enkripsi & Dekripsi - Caesar Cipher")
        self.root.geometry("600x500")

        self.shift_value = tk.IntVar(value=3)  # otomatis 3 (default)

        self.tab_control = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab1, text='Enkripsi')
        self.tab_control.add(self.tab2, text='Dekripsi')
        self.tab_control.pack(expand=1, fill="both")
        
        self.setup_enkripsi_tab()
        self.setup_dekripsi_tab()

    def create_gradient_background(self, canvas, color1, color2):
        """Creates a vertical gradient background on the canvas."""
        steps = 100
        for i in range(steps):
            r1, g1, b1 = self.hex_to_rgb(color1)
            r2, g2, b2 = self.hex_to_rgb(color2)
            r = r1 + (r2 - r1) * i // steps
            g = g1 + (g2 - g1) * i // steps
            b = b1 + (b2 - b1) * i // steps
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_rectangle(0, i * (500 // steps), 600, (i + 1) * (500 // steps), outline="", fill=color)

    def hex_to_rgb(self, hex_color):
        """Converts a hex color to an RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def create_textbox_with_border(self, canvas, x1, y1, x2, y2, text_var=None, **kwargs):
        """Create a textbox with rounded borders"""
        textbox = tk.Text(canvas, height=5, width=55, bg="#222831", fg="#eeeeee", wrap="word", borderwidth=0, relief="flat")
        textbox.place(x=x1 + 10, y=y1 + 10, width=x2 - x1 - 20, height=y2 - y1 - 20)
        return textbox

    def setup_enkripsi_tab(self):
        canvas = tk.Canvas(self.tab1, highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_gradient_background(canvas, "#3a6186", "#89253e")

        tk.Label(canvas, text="Jumlah Pergeseran:", bg="#3a6186", fg="#ffffff", font=("Arial", 10, "bold")).place(x=40, y=40)
        shift_spinbox = ttk.Spinbox(canvas, from_=1, to=25, width=5, textvariable=self.shift_value)
        shift_spinbox.place(x=160, y=40)

        tk.Label(canvas, text="Masukkan Plainteks:", bg="#3a6186", fg="#ffffff", font=("Arial", 10, "bold")).place(x=40, y=130)
        self.plaintext_input = self.create_textbox_with_border(canvas, 40, 150, 540, 220)

        tk.Button(canvas, text="Enkripsi", command=self.encrypt, bg="#555a64", fg="#ffffff", font=("Arial", 10, "bold"), relief="flat").place(x=260, y=250)

        tk.Label(canvas, text="Hasil Enkripsi (Cipherteks):", bg="#3a6186", fg="#ffffff", font=("Arial", 10, "bold")).place(x=40, y=310)
        self.cipher_output = self.create_textbox_with_border(canvas, 40, 330, 540, 400)

    def setup_dekripsi_tab(self):
        canvas = tk.Canvas(self.tab2, highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_gradient_background(canvas, "#3a6186", "#89253e")

        tk.Label(canvas, text="Jumlah Pergeseran:", bg="#3a6186", fg="#ffffff", font=("Arial", 10, "bold")).place(x=40, y=40)
        shift_spinbox = ttk.Spinbox(canvas, from_=1, to=25, width=5, textvariable=self.shift_value)
        shift_spinbox.place(x=160, y=40)

        tk.Label(canvas, text="Masukkan Cipherteks:", bg="#3a6186", fg="#ffffff", font=("Arial", 10, "bold")).place(x=40, y=130)
        self.cipher_input = self.create_textbox_with_border(canvas, 40, 150, 540, 220)

        tk.Button(canvas, text="Dekripsi", command=self.decrypt, bg="#555a64", fg="#ffffff", font=("Arial", 10, "bold"), relief="flat").place(x=260, y=250)

        tk.Label(canvas, text="Hasil Dekripsi (Plainteks):", bg="#3a6186", fg="#ffffff", font=("Arial", 10, "bold")).place(x=40, y=310)
        self.plain_output = self.create_textbox_with_border(canvas, 40, 330, 540, 400)

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
