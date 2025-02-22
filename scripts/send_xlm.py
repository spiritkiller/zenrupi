import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network

# Stellar Horizon API'ye bağlan
server = Server(horizon_url="https://horizon-testnet.stellar.org")

# Çevresel değişkenlerden gizli bilgileri al
source_secret = os.getenv("SBV2IGXCYKJVFQZD22N56ZZMXBQLOHEJKVKJB4KQIK6P3OE73EFDOSBS")  # GitHub Secrets içine eklediğin özel anahtar
destination_address = os.getenv("GCWAOUJFQSAOUKXJV3SG3TVFPJF5JBZOKMFAE4NUISWDYSYSG56NXL4O")  # Hedef adres

if not source_secret or not destination_address:
    raise ValueError("Gerekli çevresel değişkenler bulunamadı. Lütfen SECRET_KEY ve DESTINATION_ADDRESS ayarlarını yapın.")

# Cüzdan bilgileri
source_keypair = Keypair.from_secret(source_secret)
source_account = server.load_account(source_keypair.public_key)

# İşlem oluştur
transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .add_text_memo("ZenRupi transferi")
    .append_payment_op(destination=destination_address, amount="10", asset_code="XLM")
    .build()
)

# İşlemi imzala ve gönder
transaction.sign(source_keypair)
response = server.submit_transaction(transaction)

print(f"✅ İşlem başarılı! Transaction Hash: {response['hash']}")
