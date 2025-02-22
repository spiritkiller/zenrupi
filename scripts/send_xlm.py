import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

server = Server(horizon_url="https://horizon-testnet.stellar.org")

source_secret = os.getenv("SECRET_KEY")
destination_address = os.getenv("DESTINATION_ADDRESS")

if not source_secret or not destination_address:
    raise ValueError("❌ Gerekli çevresel değişkenler bulunamadı!")

source_keypair = Keypair.from_secret(source_secret)
source_account = server.load_account(source_keypair.public_key)

# 📌 TimeBounds (Zaman Sınırı) ekleyerek hatayı önlüyoruz!
transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
        time_bounds=(server.fetch_base_fee(), server.fetch_base_fee() + 300)  # 5 dakikalık zaman sınırı
    )
    .add_text_memo("ZenRupi transferi")
    .append_payment_op(destination=destination_address, amount="10", asset=Asset.native())  
    .build()
)

transaction.sign(source_keypair)
response = server.submit_transaction(transaction)

print(f"✅ İşlem başarılı! Transaction Hash: {response['hash']}")
