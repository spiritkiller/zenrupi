import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# Stellar Horizon API'ye bağlan
server = Server(horizon_url="https://horizon-testnet.stellar.org")

# Çevresel değişkenlerden gizli bilgileri al
source_secret = os.getenv("SECRET_KEY")
destination_address = os.getenv("DESTINATION_ADDRESS")

if not source_secret or not destination_address:
    raise ValueError("❌ Gerekli çevresel değişkenler bulunamadı!")

# Cüzdan bilgileri
source_keypair = Keypair.from_secret(source_secret)
source_account = server.load_account(source_keypair.public_key)

# 📌 HATA DÜZELTİLDİ: `time_bounds` yerine `.set_timeout(300)` eklendi!
transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .add_text_memo("ZenRupi transferi")
    .append_payment_op(destination=destination_address, amount="100000", asset=Asset.native())  
    .set_timeout(300)  # ⏳ 5 dakikalık zaman sınırı
    .build()
)

# İşlemi imzala ve gönder
transaction.sign(source_keypair)
response = server.submit_transaction(transaction)

print(f"✅ İşlem başarılı! Transaction Hash: {response['hash']}")
