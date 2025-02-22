import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# Stellar Horizon API'ye bağlan
server = Server("https://horizon-testnet.stellar.org")

# GitHub Secrets’ten çevresel değişkenleri al
issuer_secret = os.getenv("ISSUER_SECRET_KEY")
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
distribution_public = os.getenv("DISTRIBUTION_PUBLIC_KEY")

if not issuer_secret or not distribution_secret or not distribution_public:
    raise ValueError("❌ Gerekli çevresel değişkenler bulunamadı!")

# Issuer ve Distribution hesaplarını yükle
issuer_keypair = Keypair.from_secret(issuer_secret)
issuer_account = server.load_account(issuer_keypair.public_key)

distribution_keypair = Keypair.from_secret(distribution_secret)

# ZenRupi (ZP) Tokenini Tanımla
zenrupi_asset = Asset("ZP", issuer_keypair.public_key)

# Tokeni Dağıtıcı Hesaba Gönder
transaction = (
    TransactionBuilder(
        source_account=issuer_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_change_trust_op(asset=zenrupi_asset, limit="10000000")  # Limit belirtiyoruz
    .append_payment_op(destination=distribution_public, amount="1000000", asset=zenrupi_asset)
    .set_timeout(300)
    .build()
)

# İşlemi imzala ve gönder
transaction.sign(issuer_keypair)
response = server.submit_transaction(transaction)

print(f"✅ ZenRupi Tokeni Oluşturuldu! Transaction Hash: {response['hash']}")
