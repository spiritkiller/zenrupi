import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# 🔥 Çevresel değişkenleri yükle
issuer_secret = os.getenv("ISSUER_SECRET_KEY")
issuer_public = os.getenv("ISSUER_PUBLIC_KEY")
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
distribution_public = os.getenv("DISTRIBUTION_PUBLIC_KEY")

# 🛠️ ENV Değişkenleri gerçekten var mı kontrol et
if not issuer_public:
    raise ValueError("❌ HATA: ISSUER_PUBLIC_KEY ENV değişkeni alınamıyor. GitHub Secrets ayarlarını kontrol et!")

# Stellar ağına bağlan
server = Server(horizon_url="https://horizon-testnet.stellar.org")
distribution_keypair = Keypair.from_secret(distribution_secret)
distribution_account = server.load_account(distribution_public)

# ZenRupi (ZP) varlığını tanımla
asset_code = "ZP"
asset = Asset(asset_code, issuer_public)

# İşlem oluştur
transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_payment_op(destination=distribution_public, amount="50", asset=asset
