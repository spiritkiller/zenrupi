import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

server = Server("https://horizon-testnet.stellar.org")

issuer_secret = os.getenv("ISSUER_SECRET_KEY")
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
distribution_public = os.getenv("DISTRIBUTION_PUBLIC_KEY")

distribution_keypair = Keypair.from_secret(distribution_secret)
distribution_account = server.load_account(distribution_keypair.public_key)

asset = Asset("ZP", Keypair.from_secret(issuer_secret).public_key)

transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_change_trust_op(asset=asset, limit="10000000")
    .build()
)

transaction.sign(distribution_keypair)
server.submit_transaction(transaction)

print("✅ Trustline başarıyla oluşturuldu!")
