import os
from stellar_sdk import Server

server = Server("https://horizon-testnet.stellar.org")

for env_var in ["ISSUER_SECRET_KEY", "DISTRIBUTION_SECRET_KEY", "DISTRIBUTION_PUBLIC_KEY"]:
    public_key = os.getenv(env_var)
    if not server.accounts().account_id(public_key).call():
        print(f"⚠️ {env_var} hesabı Stellar Testnet'te bulunamadı!")
        exit(1)

print("✅ Tüm hesaplar bulundu!")
