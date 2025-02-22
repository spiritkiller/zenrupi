import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# Debugging için çevresel değişkenleri yazdır
print(f"ISSUER_SECRET_KEY: {os.getenv('ISSUER_SECRET_KEY')}")
print(f"DISTRIBUTION_SECRET_KEY: {os.getenv('DISTRIBUTION_SECRET_KEY')}")
print(f"DISTRIBUTION_PUBLIC_KEY: {os.getenv('DISTRIBUTION_PUBLIC_KEY')}")

from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset


server = Server("https://horizon-testnet.stellar.org")
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
distribution_keypair = Keypair.from_secret(distribution_secret)

issuer_public = os.getenv("ISSUER_PUBLIC_KEY")
asset_code = "ZP"
asset = Asset(asset_code, issuer_public)

distribution_account = server.load_account(distribution_keypair.public_key)

transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_change_trust_op(asset_code, issuer_public)
    .build()
)

transaction.sign(distribution_keypair)
response = server.submit_transaction(transaction)

print("✅ Trustline oluşturuldu!", response)
