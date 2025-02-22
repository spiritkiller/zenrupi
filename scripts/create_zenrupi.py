import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

server = Server("https://horizon-testnet.stellar.org")
issuer_secret = os.getenv("ISSUER_SECRET_KEY")
issuer_keypair = Keypair.from_secret(issuer_secret)

distribution_public = os.getenv("DISTRIBUTION_PUBLIC_KEY")
asset_code = "ZP"
asset = Asset(asset_code, issuer_keypair.public_key)

issuer_account = server.load_account(issuer_keypair.public_key)

transaction = (
    TransactionBuilder(
        source_account=issuer_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_payment_op(distribution_public, "1000000", asset_code, issuer_keypair.public_key)
    .build()
)

transaction.sign(issuer_keypair)
response = server.submit_transaction(transaction)

print("✅ ZenRupi Tokeni oluşturuldu!", response)
