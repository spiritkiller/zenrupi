import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# Çevresel değişkenleri al
issuer_public = os.getenv("ISSUER_PUBLIC_KEY")
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")

distribution_keypair = Keypair.from_secret(distribution_secret)
distribution_public = distribution_keypair.public_key

# Stellar Testnet Horizon sunucusuna bağlan
server = Server("https://horizon-testnet.stellar.org")

distribution_account = server.load_account(distribution_public)
asset = Asset("ZRP", issuer_public)  # ZenRupi Token

# Trustline oluşturma işlemi
print("⏳ Trustline açılıyor...")
trust_transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_change_trust_op(asset=asset)  # Trustline ekleme
    .set_timeout(30)
    .build()
)
trust_transaction.sign(distribution_keypair)
trust_response = server.submit_transaction(trust_transaction)
print("✅ Trustline başarıyla oluşturuldu!")
