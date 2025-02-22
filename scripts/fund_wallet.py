import requests
import os

public_key = os.getenv("DISTRIBUTION_PUBLIC_KEY")

response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")

if response.status_code == 200:
    print(f"✅ Başarıyla {public_key} adresine 10,000 XLM yüklendi!")
else:
    print(f"❌ XLM yükleme başarısız! {response.text}")
