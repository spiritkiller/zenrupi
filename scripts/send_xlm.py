import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# Sunucuya bağlan
server = Server("https://horizon-testnet.stellar.org")

# Çevresel değişkenlerden gizli bilgileri al
issuer_secret = os.getenv("SECRET_KEY")  # Tokeni basan hesap
distribution_public = os.getenv("DESTINATION_ADDRESS")  # Tokeni alacak hesap

# Issuer ve Distribution hesaplarını yükle
issuer_keypair = Keypair.from_secret(issuer_secret)
issuer_account = server.load_account(issuer_keypair.public_key)

# ZenRupi (ZP) Tokenini Tanımla
zenrupi_asset = Asset("ZP", issuer_keypair.public_key)

# Tokeni Dağıtıcı Hesaba Gönder
transaction = (
    TransactionBuilder(
        source_account=issuer_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_change_trust_op(asset=zenrupi_asset, source=distribution_public)
    .append_payment_op(destination=distribution_public, amount="1000000", asset=zenrupi_asset)
    .set_timeout(300)
    .build()
)

# İşlemi imzala ve gönder
transaction.sign(issuer_keypair)
response = server.submit_transaction(transaction)

print(f"✅ ZenRupi Tokeni Oluşturuldu! Transaction Hash: {response['hash']}")
