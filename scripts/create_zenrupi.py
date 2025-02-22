import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

server = Server("https://horizon-testnet.stellar.org")

issuer_secret = os.getenv("ISSUER_SECRET_KEY")
distribution_public = os.getenv("DISTRIBUTION_PUBLIC_KEY")

issuer_keypair = Keypair.from_secret(issuer_secret)
issuer_account = server.load_account(issuer_keypair.public_key)

asset = Asset("ZP", issuer_keypair.public_key)

transaction = (
    TransactionBuilder(
        source_account=issuer_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_payment_op(destination=distribution_public, amount="1000000", asset=asset)
    .build()
)

transaction.sign(issuer_keypair)
server.submit_transaction(transaction)

print("✅ ZenRupi tokeni başarıyla oluşturuldu ve dağıtıldı!")
