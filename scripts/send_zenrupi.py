import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# 🔥 Çevresel değişkenleri alıyoruz
issuer_secret = os.getenv("ISSUER_SECRET_KEY")
issuer_public = os.getenv("ISSUER_PUBLIC_KEY")  # 🔥 Eğer boşsa hata verdir
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
distribution_public = os.getenv("DISTRIBUTION_PUBLIC_KEY")

if not issuer_public:
    raise ValueError("❌ HATA: ISSUER_PUBLIC_KEY eksik! GitHub Secrets ayarlarını kontrol et.")

# Stellar bağlantısı
server = Server(horizon_url="https://horizon-testnet.stellar.org")
distribution_keypair = Keypair.from_secret(distribution_secret)
distribution_account = server.load_account(distribution_public)

# ZenRupi varlığını oluşturuyoruz
asset_code = "ZP"
asset = Asset(asset_code, issuer_public)  # 🔥 issuer_public burada None olamaz!

# İşlem oluştur
transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_payment_op(destination="GAWDZZ4MHN7S4LFKGT3IOYIJW2TNCATPIHA6DYE5UH7KQH3ZMQOWZCLW", amount="50", asset=asset)
    .set_timeout(30)
    .build()
)

# İmzala ve gönder
transaction.sign(distribution_keypair)
response = server.submit_transaction(transaction)

print(f"✅ ZenRupi Başarıyla Gönderildi! Transaction Hash: {response['hash']}")
