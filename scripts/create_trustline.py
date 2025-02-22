import os
import sys
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# 🔍 **Ortam değişkenlerini kontrol et**
issuer_secret = os.getenv("ISSUER_SECRET_KEY")
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
distribution_public = os.getenv("DISTRIBUTION_PUBLIC_KEY")

if not issuer_secret or not distribution_secret or not distribution_public:
    print("❌ HATA: Ortam değişkenleri eksik! GitHub Secrets ayarlarını kontrol et!")
    sys.exit(1)

# 🚀 **Horizon Testnet Bağlantısı**
server = Server("https://horizon-testnet.stellar.org")

# 🔑 **Anahtarları Yükle**
issuer_keypair = Keypair.from_secret(issuer_secret)
distribution_keypair = Keypair.from_secret(distribution_secret)

# 🛑 **Dağıtım hesabının aktif olup olmadığını kontrol et**
try:
    distribution_account = server.load_account(distribution_keypair.public_key)
except Exception as e:
    print(f"❌ HATA: Distribution hesabı bulunamadı! Hata: {e}")
    sys.exit(1)

# 🌟 **Yeni bir Trustline oluştur**
asset_code = "ZP"
asset = Asset(asset_code, issuer_keypair.public_key)

try:
    print("⏳ Trustline oluşturuluyor...")

    trust_transaction = (
        TransactionBuilder(
            source_account=distribution_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100
        )
        .append_change_trust_op(asset=asset, limit="10000000")
        .set_timeout(30)
        .build()
    )

    trust_transaction.sign(distribution_keypair)
    trust_response = server.submit_transaction(trust_transaction)

    print(f"✅ Trustline oluşturuldu! İşlem Hash: {trust_response['hash']}")
except Exception as e:
    print(f"❌ Trustline oluşturma başarısız! Hata: {e}")
    sys.exit(1)
