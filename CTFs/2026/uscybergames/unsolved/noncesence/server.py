import os
import socketserver
from Crypto.Cipher import AES

KEY = os.urandom(16)
NONCE = os.urandom(8)
FLAG = os.environ.get("FLAG", "SVIBGR{fake_flag_for_local_testing}").encode()
PORT = int(os.environ.get("PORT", 1337))

def encrypt(data: bytes) -> bytes:
    cipher = AES.new(KEY, AES.MODE_CTR, nonce=NONCE)
    return cipher.encrypt(data)

class ChallengeHandler(socketserver.StreamRequestHandler):
    timeout = 30  # seconds
    def handle(self):
        try:
            enc_flag = encrypt(FLAG)
            self.wfile.write(b"Encrypted flag: " + enc_flag.hex().encode() + b"\n")
            self.wfile.write(b"Enter plaintext (hex): ")
            self.wfile.flush()
            raw = self.rfile.readline(513).strip().decode()
            data = bytes.fromhex(raw)[:256]
            enc_data = encrypt(data)
            self.wfile.write(b"Ciphertext: " + enc_data.hex().encode() + b"\n")
        except Exception:
            pass

class ChallengeServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    with ChallengeServer(("0.0.0.0", PORT), ChallengeHandler) as server:
        print(f"Listening on port {PORT}")
        server.serve_forever()
