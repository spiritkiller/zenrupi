import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset


# Çevresel değişkenleri elle tanımla
issuer_secret = os.getenv("ISSUER_SECRET_KEY")
issuer_public = os.getenv("ISSUER_PUBLIC_KEY")
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
distribution_public = os.getenv("DISTRIBUTION_PUBLIC_KEY")

# Stellar Ağına Bağlan
server = Server(horizon_url="https://horizon-testnet.stellar.org")
distribution_keypair = Keypair.from_secret(DISTRIBUTION_SECRET_KEY)
distribution_account = server.load_account(DISTRIBUTION_PUBLIC_KEY)

# ZenRupi (ZP) Varlığını Tanımla
asset_code = "ZP"
asset = Asset(asset_code, ISSUER_PUBLIC_KEY)

# İşlem Oluştur
transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_payment_op(destination=DISTRIBUTION_PUBLIC_KEY, amount="50", asset=asset)
    .set_timeout(30)
    .build()
)

# İşlemi İmzala ve Gönder
transaction.sign(distribution_keypair)
response = server.submit_transaction(transaction)

print(f"✅ ZenRupi Gönderildi! İşlem Hash: {response['hash']}")
