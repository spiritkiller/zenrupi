import requests
from stellar_sdk import Keypair

# Yeni bir cüzdan oluştur
keypair = Keypair.random()
public_key = keypair.public_key

# Friendbot'tan ücretsiz XLM al
response = requests.get(f"https://friendbot.stellar.org/?addr={public_key}")

if response.status_code == 200:
    print(f"Başarıyla {public_key} adresine 10,000 XLM gönderildi!")
else:
    print("XLM yüklenemedi, tekrar deneyin.")
