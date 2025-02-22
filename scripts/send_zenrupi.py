import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset
from dotenv import load_dotenv

# 🔥 .env dosyasını yükle
load_dotenv()

# 🔥 Ortam değişkenlerini al
issuer_secret = os.getenv("ISSUER_SECRET_KEY")
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
distribution_public = os.getenv("DISTRIBUTION_PUBLIC_KEY")

# 🔥 Değerleri kontrol et
print(f"Issuer Secret Key: {issuer_secret[:5]}... (Gizlendi)")
print(f"Distribution Secret Key: {distribution_secret[:5]}... (Gizlendi)")
print(f"Distribution Public Key: {distribution_public}")


# 🔥 GitHub Secrets'ten ortam değişkenlerini al
issuer_secret = os.getenv("ISSUER_SECRET_KEY")
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
distribution_public = os.getenv("DISTRIBUTION_PUBLIC_KEY")

# 🔴 Eğer değişkenler yüklenmediyse hata ver
if not issuer_secret or not distribution_secret or not distribution_public:
    raise ValueError("❌ HATA: GitHub Secrets ayarları eksik! Lütfen kontrol edin.")

# Stellar Ağına Bağlan
server = Server(horizon_url="https://horizon-testnet.stellar.org")
distribution_keypair = Keypair.from_secret(distribution_secret)
distribution_account = server.load_account(distribution_public)

# ZenRupi (ZP) Varlığını Tanımla
asset_code = "ZP"
asset = Asset(asset_code, Keypair.from_secret(issuer_secret).public_key)

# İşlem Oluştur
transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_payment_op(destination=distribution_public, amount="1000000", asset=asset)  # ✅ Hedef adres güncellendi!
    .set_timeout(30)
    .build()
)

# İşlemi İmzala ve Gönder
transaction.sign(distribution_keypair)
response = server.submit_transaction(transaction)

print(f"✅ ZenRupi Gönderildi! İşlem Hash: {response['hash']}")
