import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# Stellar Horizon Sunucusu
server = Server(horizon_url="https://horizon-testnet.stellar.org")

# Çevresel değişkenlerden anahtarları al
distribution_secret = os.getenv("DISTRIBUTION_SECRET_KEY")
destination_public = os.getenv("DESTINATION_PUBLIC_KEY")  # Kullanıcı adresi

# Hata kontrolü
if not distribution_secret or not destination_public:
    raise ValueError("❌ Çevresel değişkenler eksik! Lütfen DISTRIBUTION_SECRET_KEY ve DESTINATION_PUBLIC_KEY ayarlarını yapın.")

# Hesapları yükle
distribution_keypair = Keypair.from_secret(distribution_secret)
distribution_account = server.load_account(distribution_keypair.public_key)

# ZenRupi Token Tanımı
asset = Asset("ZP", "GDSV3ASUME7EBCLFOME55HOFAVAI34FSSOH25JWJC623FVVOXZVPYNWB")

# İşlem oluşturma
transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_payment_op(destination=destination_public, amount="500", asset=asset)
    .set_timeout(30)
    .build()
)

# İşlemi imzala
transaction.sign(distribution_keypair)

# İşlemi gönder
response = server.submit_transaction(transaction)

# Başarı durumunu yazdır
print(f"✅ İşlem başarılı! Transaction Hash: {response['hash']}")
