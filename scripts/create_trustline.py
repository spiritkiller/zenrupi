import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# ✅ Stellar Horizon API'ye bağlan
server = Server("https://horizon-testnet.stellar.org")

# ✅ Çevresel değişkenlerden hesapları al
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
issuer_public = os.getenv("ISSUER_PUBLIC_KEY")

if not distribution_secret or not issuer_public:
    raise ValueError("❌ Gerekli çevresel değişkenler eksik!")

# ✅ Hesapları yükle
distribution_keypair = Keypair.from_secret(distribution_secret)
distribution_account = server.load_account(distribution_keypair.public_key)

# ✅ ZenRupi (ZP) Tokenini Tanımla
zenrupi_asset = Asset("ZP", issuer_public)

# 🛠️ **Trustline Aç (Distribution Hesabı İçin)**
print("⏳ Trustline açılıyor...")
trust_transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_change_trust_op(asset=zenrupi_asset)  
    .set_timeout(300)
    .build()
)

trust_transaction.sign(distribution_keypair)
trust_response = server.submit_transaction(trust_transaction)
print(f"✅ Trustline başarıyla açıldı! Transaction Hash: {trust_response['hash']}")
