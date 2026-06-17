import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import hashlib, json, time, base64, os
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad


class CryptoEngine:
    @staticmethod
    def aes_encrypt(text, key):
        key = key.encode().ljust(32, b'\0')[:32]
        cipher = AES.new(key, AES.MODE_CBC)
        encrypted = cipher.encrypt(pad(text.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + encrypted).decode()

    @staticmethod
    def aes_decrypt(encrypted_text, key):
        try:
            key = key.encode().ljust(32, b'\0')[:32]
            data = base64.b64decode(encrypted_text)
            iv = data[:16]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(data[16:]), AES.block_size)
            return decrypted.decode()
        except Exception:
            return None

    @staticmethod
    def des_encrypt(text, key):
        key = key.encode().ljust(8, b'\0')[:8]
        cipher = DES.new(key, DES.MODE_ECB)
        encrypted = cipher.encrypt(pad(text.encode(), DES.block_size))
        return base64.b64encode(encrypted).decode()

    @staticmethod
    def des_decrypt(encrypted_text, key):
        try:
            key = key.encode().ljust(8, b'\0')[:8]
            cipher = DES.new(key, DES.MODE_ECB)
            decrypted = unpad(cipher.decrypt(base64.b64decode(encrypted_text)), DES.block_size)
            return decrypted.decode()
        except Exception:
            return None

    @staticmethod
    def vigenere_encrypt(text, key):
        result = ""
        key = key.upper()
        key_index = 0
        for c in text:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                shift = ord(key[key_index % len(key)]) - ord('A')
                result += chr((ord(c) - base + shift) % 26 + base)
                key_index += 1
            else:
                result += c
        return result

    @staticmethod
    def vigenere_decrypt(text, key):
        result = ""
        key = key.upper()
        key_index = 0
        for c in text:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                shift = ord(key[key_index % len(key)]) - ord('A')
                result += chr((ord(c) - base - shift) % 26 + base)
                key_index += 1
            else:
                result += c
        return result

    @staticmethod
    def caesar_encrypt(text, shift):
        result = ""
        shift = int(shift)
        for c in text:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                result += chr((ord(c) - base + shift) % 26 + base)
            else:
                result += c
        return result

    @staticmethod
    def caesar_decrypt(text, shift):
        return CryptoEngine.caesar_encrypt(text, -int(shift))


class SteganoEngine:
    @staticmethod
    def text_to_bits(text):
        return ''.join(format(ord(c), '08b') for c in text)

    @staticmethod
    def bits_to_text(bits):
        chars = [bits[i:i + 8] for i in range(0, len(bits), 8)]
        return ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)

    @staticmethod
    def encode_lsb(image_path, message, output_path):
        try:
            img = Image.open(image_path).convert("RGB")
            width, height = img.size

            message += "####END####"
            binary_msg = SteganoEngine.text_to_bits(message)

            max_capacity = width * height * 3
            if len(binary_msg) > max_capacity:
                return False, f"Message too large! Max: {max_capacity // 8} bytes, Required: {len(binary_msg) // 8} bytes"

            pixels = list(img.getdata())
            new_pixels = []
            data_idx = 0

            for pixel in pixels:
                r, g, b = pixel[:3]

                if data_idx < len(binary_msg):
                    r = (r & 0xFE) | int(binary_msg[data_idx])
                    data_idx += 1
                if data_idx < len(binary_msg):
                    g = (g & 0xFE) | int(binary_msg[data_idx])
                    data_idx += 1
                if data_idx < len(binary_msg):
                    b = (b & 0xFE) | int(binary_msg[data_idx])
                    data_idx += 1

                new_pixels.append((r, g, b))

            encoded_img = Image.new("RGB", (width, height))
            encoded_img.putdata(new_pixels)
            encoded_img.save(output_path, "PNG")

            return True, f"Success! Saved to: {output_path}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    @staticmethod
    def decode_lsb(image_path):
        try:
            img = Image.open(image_path).convert("RGB")
            pixels = list(img.getdata())

            binary = ""
            for pixel in pixels:
                r, g, b = pixel[:3]
                binary += str(r & 1)
                binary += str(g & 1)
                binary += str(b & 1)

            message = SteganoEngine.bits_to_text(binary)

            if "####END####" in message:
                message = message.split("####END####")[0]
                return True, message
            return False, "No hidden message found or message is corrupted!"
        except Exception as e:
            return False, f"Error: {str(e)}"


class BlockchainLogger:
    def __init__(self):
        self.chain = []
        self.create_genesis()

    def create_genesis(self):
        block = {
            "index": 0,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "operation": "System Initialization",
            "data_hash": "0",
            "prev_hash": "0"
        }
        block["hash"] = self.calculate_hash(block)
        self.chain.append(block)

    def calculate_hash(self, block):
        temp = block.copy()
        if "hash" in temp:
            del temp["hash"]
        return hashlib.sha256(json.dumps(temp, sort_keys=True).encode()).hexdigest()

    def add_block(self, operation, data):
        prev_block = self.chain[-1]
        block = {
            "index": len(self.chain),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "operation": operation,
            "data_hash": hashlib.sha256(data.encode()).hexdigest()[:16],
            "prev_hash": prev_block["hash"]
        }
        block["hash"] = self.calculate_hash(block)
        self.chain.append(block)

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current["prev_hash"] != prev["hash"]:
                return False
            if current["hash"] != self.calculate_hash(current):
                return False
        return True


class SteganoCryptGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SteganoCrypt - Image Steganography Suite")
        self.root.configure(bg="#0f0f1e")
        self.root.geometry("1280x820")
        self.root.minsize(1000, 680)

        try:
            self.root.state("zoomed")
        except Exception:
            pass

        self.crypto = CryptoEngine()
        self.stegano = SteganoEngine()
        self.blockchain = BlockchainLogger()
        self.current_image_path = None
        self.extract_image_path = None

        self.setup_ui()

    def setup_ui(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        header = tk.Frame(self.root, bg="#0f0f1e")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 5))
        header.grid_columnconfigure(1, weight=1)

        tk.Label(
            header,
            text="SteganoCrypt",
            font=("Segoe UI", 24, "bold"),
            bg="#0f0f1e",
            fg="#00d4ff"
        ).grid(row=0, column=0, sticky="w")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        self.hide_tab = tk.Frame(self.notebook, bg="#0f0f1e")
        self.extract_tab = tk.Frame(self.notebook, bg="#0f0f1e")
        self.blockchain_tab = tk.Frame(self.notebook, bg="#0f0f1e")

        self.notebook.add(self.hide_tab, text="  Hide Message  ")
        self.notebook.add(self.extract_tab, text="  Extract Message  ")
        self.notebook.add(self.blockchain_tab, text="  Audit Log  ")

        self.build_hide_tab()
        self.build_extract_tab()
        self.build_blockchain_tab()

        self.status_var = tk.StringVar(value="Ready | System Initialized")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg="#1a1a2e",
            fg="#00ff88",
            font=("Consolas", 9),
            anchor="w",
            padx=15,
            pady=5
        )
        status_bar.grid(row=2, column=0, sticky="ew")

    def build_hide_tab(self):
        self.hide_tab.grid_rowconfigure(0, weight=1)
        self.hide_tab.grid_columnconfigure(0, weight=3)
        self.hide_tab.grid_columnconfigure(1, weight=2)

        left_panel = tk.Frame(self.hide_tab, bg="#0f0f1e")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        left_panel.grid_rowconfigure(0, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)

        img_frame = tk.LabelFrame(
            left_panel,
            text="  Image Preview ",
            bg="#1a1a2e",
            fg="#00d4ff",
            font=("Segoe UI", 11, "bold")
        )
        img_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        img_frame.grid_rowconfigure(0, weight=1)
        img_frame.grid_columnconfigure(0, weight=1)

        self.hide_img_label = tk.Label(
            img_frame,
            text="Click 'Load Image' to begin",
            bg="#0f0f1e",
            fg="#666666",
            font=("Segoe UI", 12)
        )
        self.hide_img_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        btn_frame = tk.Frame(left_panel, bg="#0f0f1e")
        btn_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        tk.Button(
            btn_frame,
            text="Load Image",
            bg="#00d4ff",
            fg="#0f0f1e",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.hide_load_image
        ).grid(row=0, column=0, sticky="ew", padx=(0, 5))

        tk.Button(
            btn_frame,
            text="Clear",
            bg="#ff4757",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.hide_clear
        ).grid(row=0, column=1, sticky="ew", padx=(5, 0))

        right_panel = tk.Frame(self.hide_tab, bg="#0f0f1e")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        enc_frame = tk.LabelFrame(
            right_panel,
            text=" Encryption ",
            bg="#1a1a2e",
            fg="#00d4ff",
            font=("Segoe UI", 11, "bold")
        )
        enc_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 8))

        tk.Label(enc_frame, text="Algorithm:", bg="#1a1a2e", fg="#e0e0e0", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=(10, 5))
        self.hide_algo = ttk.Combobox(
            enc_frame,
            values=["None", "AES-256", "DES", "Vigenere", "Caesar"],
            state="readonly",
            font=("Consolas", 10)
        )
        self.hide_algo.current(0)
        self.hide_algo.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(enc_frame, text="Key/Password:", bg="#1a1a2e", fg="#e0e0e0", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=(0, 5))
        self.hide_key = tk.Entry(
            enc_frame,
            font=("Consolas", 10),
            bg="#0f0f1e",
            fg="#e0e0e0",
            insertbackground="#00d4ff"
        )
        self.hide_key.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(enc_frame, text="Shift (for Caesar):", bg="#1a1a2e", fg="#e0e0e0", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=(0, 5))
        self.hide_shift = tk.Entry(
            enc_frame,
            font=("Consolas", 10),
            bg="#0f0f1e",
            fg="#e0e0e0",
            insertbackground="#00d4ff"
        )
        self.hide_shift.insert(0, "3")
        self.hide_shift.pack(fill="x", padx=10, pady=(0, 10))

        msg_frame = tk.LabelFrame(
            right_panel,
            text=" Secret Message ",
            bg="#1a1a2e",
            fg="#00d4ff",
            font=("Segoe UI", 11, "bold")
        )
        msg_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 8))
        msg_frame.grid_rowconfigure(0, weight=1)
        msg_frame.grid_columnconfigure(0, weight=1)

        self.hide_message = scrolledtext.ScrolledText(
            msg_frame,
            wrap="word",
            height=7,
            bg="#0f0f1e",
            fg="#e0e0e0",
            font=("Consolas", 10),
            insertbackground="#00d4ff"
        )
        self.hide_message.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        action_frame = tk.Frame(right_panel, bg="#0f0f1e")
        action_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=(0, 5))
        action_frame.grid_columnconfigure(0, weight=1)

        self.hide_btn = tk.Button(
            action_frame,
            text="Hide & Encrypt",
            bg="#00d4ff",
            fg="#0f0f1e",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            command=self.hide_message_action
        )
        self.hide_btn.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        self.save_btn = tk.Button(
            action_frame,
            text="Save Output Image",
            bg="#2ed573",
            fg="#0f0f1e",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            state="disabled",
            command=self.hide_save_image
        )
        self.save_btn.grid(row=1, column=0, sticky="ew")

        self.hide_output = tk.Label(
            right_panel,
            text="",
            bg="#1a1a2e",
            fg="#00ff88",
            font=("Consolas", 9),
            justify="left",
            anchor="w",
            padx=10,
            pady=8
        )
        self.hide_output.grid(row=3, column=0, sticky="ew", padx=5, pady=(5, 5))

    def build_extract_tab(self):
        self.extract_tab.grid_rowconfigure(0, weight=1)
        self.extract_tab.grid_columnconfigure(0, weight=3)
        self.extract_tab.grid_columnconfigure(1, weight=2)

        left_panel = tk.Frame(self.extract_tab, bg="#0f0f1e")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        left_panel.grid_rowconfigure(0, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)

        img_frame = tk.LabelFrame(
            left_panel,
            text=" Stego Image ",
            bg="#1a1a2e",
            fg="#ff4757",
            font=("Segoe UI", 11, "bold")
        )
        img_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        img_frame.grid_rowconfigure(0, weight=1)
        img_frame.grid_columnconfigure(0, weight=1)

        self.extract_img_label = tk.Label(
            img_frame,
            text="Click 'Load Image' to begin",
            bg="#0f0f1e",
            fg="#666666",
            font=("Segoe UI", 12)
        )
        self.extract_img_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        btn_frame = tk.Frame(left_panel, bg="#0f0f1e")
        btn_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        btn_frame.grid_columnconfigure(0, weight=1)

        tk.Button(
            btn_frame,
            text="Load Stego Image",
            bg="#00d4ff",
            fg="#0f0f1e",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.extract_load_image
        ).grid(row=0, column=0, sticky="ew")

        right_panel = tk.Frame(self.extract_tab, bg="#0f0f1e")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right_panel.grid_rowconfigure(2, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        dec_frame = tk.LabelFrame(
            right_panel,
            text=" Decryption ",
            bg="#1a1a2e",
            fg="#ff4757",
            font=("Segoe UI", 11, "bold")
        )
        dec_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 8))

        tk.Label(dec_frame, text="Algorithm Used:", bg="#1a1a2e", fg="#e0e0e0", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=(10, 5))
        self.extract_algo = ttk.Combobox(
            dec_frame,
            values=["None", "AES-256", "DES", "Vigenere", "Caesar"],
            state="readonly",
            font=("Consolas", 10)
        )
        self.extract_algo.current(0)
        self.extract_algo.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(dec_frame, text="Key/Password:", bg="#1a1a2e", fg="#e0e0e0", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=(0, 5))
        self.extract_key = tk.Entry(
            dec_frame,
            font=("Consolas", 10),
            bg="#0f0f1e",
            fg="#e0e0e0",
            insertbackground="#00d4ff",
            show="*"
        )
        self.extract_key.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(dec_frame, text="Shift (for Caesar):", bg="#1a1a2e", fg="#e0e0e0", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=(0, 5))
        self.extract_shift = tk.Entry(
            dec_frame,
            font=("Consolas", 10),
            bg="#0f0f1e",
            fg="#e0e0e0",
            insertbackground="#00d4ff"
        )
        self.extract_shift.insert(0, "3")
        self.extract_shift.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(
            right_panel,
            text="Extract & Decrypt Message",
            bg="#00d4ff",
            fg="#0f0f1e",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            command=self.extract_message_action
        ).grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        out_frame = tk.LabelFrame(
            right_panel,
            text=" Extracted Message ",
            bg="#1a1a2e",
            fg="#2ed573",
            font=("Segoe UI", 11, "bold")
        )
        out_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=(0, 8))
        out_frame.grid_rowconfigure(0, weight=1)
        out_frame.grid_columnconfigure(0, weight=1)

        self.extract_output = scrolledtext.ScrolledText(
            out_frame,
            wrap="word",
            bg="#0f0f1e",
            fg="#00ff88",
            font=("Consolas", 10),
            state="disabled"
        )
        self.extract_output.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        action_frame = tk.Frame(right_panel, bg="#0f0f1e")
        action_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 5))
        action_frame.grid_columnconfigure(0, weight=1)
        action_frame.grid_columnconfigure(1, weight=1)

        tk.Button(
            action_frame,
            text="Copy",
            bg="#57606f",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.extract_copy
        ).grid(row=0, column=0, sticky="ew", padx=(0, 5))

        tk.Button(
            action_frame,
            text="Save to File",
            bg="#57606f",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.extract_save
        ).grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def build_blockchain_tab(self):
        self.blockchain_tab.grid_rowconfigure(1, weight=1)
        self.blockchain_tab.grid_columnconfigure(0, weight=1)

        header = tk.Frame(self.blockchain_tab, bg="#0f0f1e")
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        header.grid_columnconfigure(0, weight=1)

        tk.Label(
            header,
            text="Blockchain Audit Log",
            font=("Segoe UI", 16, "bold"),
            bg="#0f0f1e",
            fg="#00d4ff"
        ).grid(row=0, column=0, sticky="w")

        btn_frame = tk.Frame(header, bg="#0f0f1e")
        btn_frame.grid(row=0, column=1, sticky="e")

        tk.Button(
            btn_frame,
            text="Refresh",
            bg="#00d4ff",
            fg="#0f0f1e",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.blockchain_refresh
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Verify Chain",
            bg="#2ed573",
            fg="#0f0f1e",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.blockchain_verify
        ).pack(side="left", padx=5)

        self.bc_text = scrolledtext.ScrolledText(
            self.blockchain_tab,
            bg="#0f0f1e",
            fg="#00ff88",
            font=("Consolas", 10),
            state="disabled"
        )
        self.bc_text.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 10))

        self.blockchain_refresh()

    def hide_load_image(self):
        path = filedialog.askopenfilename(
            title="Select Image to Hide Message In",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if path:
            try:
                self.current_image_path = path
                img = Image.open(path)
                img_copy = img.copy()
                img_copy.thumbnail((700, 500))
                self.hide_photo = ImageTk.PhotoImage(img_copy)
                self.hide_img_label.config(image=self.hide_photo, text="")
                self.status_var.set(f"Loaded: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def hide_clear(self):
        self.current_image_path = None
        self.hide_img_label.config(image="", text="Click 'Load Image' to begin")
        self.hide_output.config(text="")
        self.save_btn.config(state="disabled")
        self.status_var.set("Cleared")

    def hide_message_action(self):
        if not self.current_image_path:
            messagebox.showerror("Error", "Please load an image first!")
            return

        message = self.hide_message.get("1.0", "end-1c").strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message!")
            return

        algo = self.hide_algo.get()
        key = self.hide_key.get()
        shift = self.hide_shift.get()

        try:
            encrypted_msg = message

            if algo == "AES-256":
                if not key:
                    messagebox.showerror("Error", "Please enter encryption key!")
                    return
                encrypted_msg = self.crypto.aes_encrypt(message, key)
            elif algo == "DES":
                if not key:
                    messagebox.showerror("Error", "Please enter encryption key!")
                    return
                encrypted_msg = self.crypto.des_encrypt(message, key)
            elif algo == "Vigenere":
                if not key:
                    messagebox.showerror("Error", "Please enter encryption key!")
                    return
                encrypted_msg = self.crypto.vigenere_encrypt(message, key)
            elif algo == "Caesar":
                encrypted_msg = self.crypto.caesar_encrypt(message, shift if shift else 3)

            self.temp_output = "stego_output.png"
            success, msg = self.stegano.encode_lsb(self.current_image_path, encrypted_msg, self.temp_output)

            if success:
                self.hide_output.config(
                    text=f"Success!\nAlgorithm: {algo}\nMessage Length: {len(message)} chars\nOutput: {self.temp_output}",
                    fg="#00ff88"
                )
                self.save_btn.config(state="normal")
                self.status_var.set(f"Message hidden with {algo}")
                self.blockchain.add_block(
                    "HIDE_MESSAGE",
                    f"Algo:{algo}|Len:{len(message)}|File:{os.path.basename(self.current_image_path)}"
                )
                self.blockchain_refresh()
            else:
                messagebox.showerror("Error", msg)

        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")

    def hide_save_image(self):
        if hasattr(self, "temp_output") and os.path.exists(self.temp_output):
            path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                title="Save Stego Image"
            )
            if path:
                try:
                    import shutil
                    shutil.copy(self.temp_output, path)
                    messagebox.showinfo("Success", f"Image saved to:\n{path}")
                    self.status_var.set(f"Saved: {os.path.basename(path)}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save: {str(e)}")

    def extract_load_image(self):
        path = filedialog.askopenfilename(
            title="Select Stego Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if path:
            try:
                self.extract_image_path = path
                img = Image.open(path)
                img_copy = img.copy()
                img_copy.thumbnail((700, 500))
                self.extract_photo = ImageTk.PhotoImage(img_copy)
                self.extract_img_label.config(image=self.extract_photo, text="")
                self.status_var.set(f"Loaded: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {str(e)}")

    def extract_message_action(self):
        if not self.extract_image_path:
            messagebox.showerror("Error", "Please load a stego image first!")
            return

        try:
            success, extracted_msg = self.stegano.decode_lsb(self.extract_image_path)

            if not success:
                messagebox.showerror("Error", extracted_msg)
                return

            algo = self.extract_algo.get()
            key = self.extract_key.get()
            shift = self.extract_shift.get()

            decrypted_msg = extracted_msg

            if algo == "AES-256":
                if not key:
                    messagebox.showerror("Error", "Please enter decryption key!")
                    return
                result = self.crypto.aes_decrypt(extracted_msg, key)
                if result:
                    decrypted_msg = result
                else:
                    messagebox.showwarning("Warning", "Decryption failed! Wrong key?")
                    return
            elif algo == "DES":
                if not key:
                    messagebox.showerror("Error", "Please enter decryption key!")
                    return
                result = self.crypto.des_decrypt(extracted_msg, key)
                if result:
                    decrypted_msg = result
                else:
                    messagebox.showwarning("Warning", "Decryption failed! Wrong key?")
                    return
            elif algo == "Vigenere":
                if not key:
                    messagebox.showerror("Error", "Please enter decryption key!")
                    return
                decrypted_msg = self.crypto.vigenere_decrypt(extracted_msg, key)
            elif algo == "Caesar":
                decrypted_msg = self.crypto.caesar_decrypt(extracted_msg, shift if shift else 3)

            self.extract_output.config(state="normal")
            self.extract_output.delete("1.0", "end")
            self.extract_output.insert("1.0", decrypted_msg)
            self.extract_output.config(state="disabled")

            self.status_var.set(f"Extracted & decrypted with {algo}")
            self.blockchain.add_block("EXTRACT_MESSAGE", f"Algo:{algo}")
            self.blockchain_refresh()

        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")

    def extract_copy(self):
        msg = self.extract_output.get("1.0", "end-1c")
        if msg:
            self.root.clipboard_clear()
            self.root.clipboard_append(msg)
            messagebox.showinfo("Copied", "Message copied to clipboard!")

    def extract_save(self):
        msg = self.extract_output.get("1.0", "end-1c")
        if msg:
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                title="Save Message"
            )
            if path:
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(msg)
                    messagebox.showinfo("Saved", f"Message saved to:\n{path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save: {str(e)}")

    def blockchain_refresh(self):
        self.bc_text.config(state="normal")
        self.bc_text.delete("1.0", "end")

        for block in self.blockchain.chain:
            block_text = f"""
============================================================
BLOCK #{block['index']}
============================================================
Timestamp:  {block['timestamp']}
Operation:  {block['operation']}
Data Hash:  {block['data_hash']}
Prev Hash:  {block['prev_hash'][:32]}
Block Hash: {block['hash'][:32]}
============================================================

"""
            self.bc_text.insert("end", block_text)

        self.bc_text.config(state="disabled")

    def blockchain_verify(self):
        if self.blockchain.verify_chain():
            messagebox.showinfo("Verification", "Blockchain is VALID!\nAll blocks are intact.")
            self.status_var.set("Blockchain verified - VALID")
        else:
            messagebox.showerror("Verification", "Blockchain is CORRUPTED!\nTampering detected!")
            self.status_var.set("Blockchain verification FAILED")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SteganoCryptGUI()
    app.run()
