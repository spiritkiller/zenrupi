import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# ✅ Stellar Horizon API'ye bağlan
server = Server("https://horizon-testnet.stellar.org")

# ✅ GitHub Secrets’ten çevresel değişkenleri al
issuer_secret = os.getenv("ISSUER_SECRET_KEY")
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
distribution_public = os.getenv("DISTRIBUTION_PUBLIC_KEY")

if not issuer_secret or not distribution_secret or not distribution_public:
    raise ValueError("❌ Gerekli çevresel değişkenler bulunamadı!")

# ✅ Issuer ve Distribution hesaplarını yükle
issuer_keypair = Keypair.from_secret(issuer_secret)
distribution_keypair = Keypair.from_secret(distribution_secret)

issuer_account = server.load_account(issuer_keypair.public_key)
distribution_account = server.load_account(distribution_keypair.public_key)

# ✅ ZenRupi (ZP) Tokenini Tanımla
zenrupi_asset = Asset("ZP", issuer_keypair.public_key)

# 🛠️ **1. Adım: Trustline Aç (Distribution Hesabı İçin)**
print("⏳ Trustline açılıyor...")
trust_transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_change_trust_op(asset=zenrupi_asset, limit="10000000")  # Trustline Limiti Eklendi!
    .set_timeout(300)
    .build()
)

trust_transaction.sign(distribution_keypair)
trust_response = server.submit_transaction(trust_transaction)
print(f"✅ Trustline başarıyla açıldı! Transaction Hash: {trust_response['hash']}")

# 🛠️ **2. Adım: ZenRupi Tokenini Dağıtım Hesabına Gönder**
print("⏳ Token transferi yapılıyor...")
transfer_transaction = (
    TransactionBuilder(
        source_account=issuer_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_payment_op(destination=distribution_public, amount="1000000", asset=zenrupi_asset)
    .set_timeout(300)
    .build()
)

transfer_transaction.sign(issuer_keypair)
transfer_response = server.submit_transaction(transfer_transaction)
print(f"✅ ZenRupi Tokeni başarıyla transfer edildi! Transaction Hash: {transfer_response['hash']}")

print("🚀 **ZenRupi Tokeni Başarıyla Oluşturuldu ve Dağıtıldı!** 🎉")
