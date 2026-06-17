# 🕵️‍♂️ SteganoCrypt: Image Steganography & Encryption Suite

**SteganoCrypt** is a comprehensive desktop application that combines **Image Steganography**, **Cryptography**, and **Blockchain** technology to provide a secure method for hiding and transmitting secret messages. It allows users to encrypt text using industry-standard algorithms and then hide the encrypted payload inside image files using the Least Significant Bit (LSB) technique. Additionally, it features a local **Blockchain Audit Log** to ensure the integrity of all operations performed within the system.

---

## 🚀 Key Features

### 🖼️ Image Steganography (LSB)
* **Least Significant Bit (LSB) Encoding:** Hides binary data within the pixel values of an image without significantly altering its visual appearance.
* **Capacity Management:** Automatically calculates maximum message capacity based on image resolution.
* **Visual Preview:** Real-time preview of the carrier image before and after encoding.
* **Format Support:** Supports PNG, JPG, JPEG, and BMP formats.

### 🔐 Multi-Algorithm Encryption
Before hiding the message, it can be encrypted using one of the following methods:
* **AES-256 (CBC Mode):** Military-grade symmetric encryption for maximum security.
* **DES (ECB Mode):** Classic symmetric encryption standard.
* **Vigenère Cipher:** Polyalphabetic substitution cipher using a keyword.
* **Caesar Cipher:** Simple shift-based substitution cipher.
* **No Encryption:** Option to hide plain text for demonstration purposes.

### ⛓️ Blockchain Audit Log
* **Immutable Ledger:** Every "Hide" and "Extract" operation is recorded as a block in a local blockchain.
* **SHA-256 Hashing:** Each block contains a cryptographic hash of the previous block, ensuring data integrity.
* **Chain Verification:** Built-in tool to verify if the audit log has been tampered with.
* **Genesis Block:** Initializes with a system block to start the chain.

### 🎨 Modern Dark UI
* **Cyberpunk Theme:** Sleek dark interface with neon accents (Cyan/Green/Red).
* **Tabbed Navigation:** Organized into "Hide", "Extract", and "Audit Log" tabs.
* **Responsive Design:** Scalable layout that adapts to window resizing.

---

## 🛠️ Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3** | Core Programming Language |
| **Tkinter** | Graphical User Interface (GUI) Framework |
| **Pillow (PIL)** | Image Processing and Manipulation |
| **PyCryptodome** | Implementation of Cryptographic Algorithms (AES, DES) |
| **Hashlib / JSON** | Blockchain Hashing and Data Serialization |

---

## 📂 Project Architecture

The application is modularized into three core engines:

1.  **`CryptoEngine`**: Handles all encryption and decryption logic. It supports padding (PKCS7) for block ciphers and handles key derivation/formatting.
2.  **`SteganoEngine`**: Manages the bitwise operations required to embed text into image pixels. It appends a delimiter (`####END####`) to mark the end of the hidden message.
3.  **`BlockchainLogger`**: A simplified blockchain implementation that maintains a chain of dictionaries (blocks). Each block stores the timestamp, operation type, data hash, and the hash of the previous block.

---

## ⚙️ Installation & Setup

### Prerequisites
* **Python 3.8 or higher**
* **pip** package manager

### 1. Clone the Repository
```bash
git clone https://github.com/zuhaishtiaq2006-svg/SteganoCrypt.git
cd SteganoCrypt
```

### 2. Install Dependencies
You need to install the required Python libraries:
```bash
pip install pillow pycryptodome
```

### 3. Run the Application
```bash
python steganocrypt.py
```

---

## 🎮 How to Use

### 📥 Hiding a Message
1.  Navigate to the **"Hide Message"** tab.
2.  Click **"Load Image"** to select a cover image (PNG recommended for lossless compression).
3.  Select an **Encryption Algorithm** (e.g., AES-256).
4.  Enter a **Key/Password** (if required by the algorithm) and **Shift** (for Caesar).
5.  Type your **Secret Message** in the text area.
6.  Click **"Hide & Encrypt"**.
7.  Click **"Save Output Image"** to save the stego-image to your disk.

### 📤 Extracting a Message
1.  Navigate to the **"Extract Message"** tab.
2.  Click **"Load Stego Image"** and select the image containing the hidden data.
3.  Select the **same Algorithm** and enter the **same Key/Shift** used during hiding.
4.  Click **"Extract & Decrypt Message"**.
5.  The decrypted text will appear in the output box. You can **Copy** or **Save to File**.

### ⛓️ Verifying Audit Log
1.  Navigate to the **"Audit Log"** tab.
2.  View the history of all operations performed in the current session.
3.  Click **"Verify Chain"** to check the cryptographic integrity of the logs.

---

## 🎯 Future Enhancements

* [ ] **Network Steganography:** Implement TCP/UDP sockets to send stego-images directly between clients.
* [ ] **Distributed Blockchain:** Connect the audit log to a peer-to-peer network for decentralized verification.
* [ ] **Advanced Steganography:** Implement DCT (Discrete Cosine Transform) based steganography for JPEG resistance.
* [ ] **File Hiding:** Extend support to hide files (PDFs, ZIPs) inside images, not just text.
* [ ] **Password Hashing:** Use Argon2 or bcrypt to hash user passwords before using them as encryption keys.

---

## 👨‍💻 Developer
Developed as a cybersecurity educational tool to demonstrate the intersection of **Cryptography** (confidentiality), **Steganography** (secrecy of existence), and **Blockchain** (integrity).

---

## 📜 License
This project is developed for **educational and research purposes**.

---
*Made with ❤️ using Python, Tkinter, and Cryptography.*
