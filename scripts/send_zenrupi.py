import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

server = Server("https://horizon-testnet.stellar.org")

distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
recipient_public = "GDESTINAT1ONPUBLICKEYHERE"

distribution_keypair = Keypair.from_secret(distribution_secret)
distribution_account = server.load_account(distribution_keypair.public_key)

asset = Asset("ZP", distribution_keypair.public_key)

transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_payment_op(destination=recipient_public, amount="10", asset=asset)
    .build()
)

transaction.sign(distribution_keypair)
server.submit_transaction(transaction)

print(f"✅ ZenRupi tokeni {recipient_public} adresine başarıyla gönderildi!")
