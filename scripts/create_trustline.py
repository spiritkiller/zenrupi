from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

server = Server("https://horizon-testnet.stellar.org")

# Çevresel değişkenleri yükle
distribution_secret = "DISTRIBUTION_SECRET_KEY"
issuer_public = "ISSUER_PUBLIC_KEY"
asset_code = "ZENRUPI"  # **4 ile 12 karakter arasında olmalı!**

distribution_keypair = Keypair.from_secret(distribution_secret)
distribution_account = server.load_account(distribution_keypair.public_key)

# Trustline oluştur
print("⏳ Trustline açılıyor...")
asset = Asset(asset_code, issuer_public)
trust_transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_change_trust_op(asset=asset)
    .set_timeout(30)
    .build()
)

trust_transaction.sign(distribution_keypair)
trust_response = server.submit_transaction(trust_transaction)

print(f"✅ Trustline başarıyla açıldı! Transaction Hash: {trust_response['hash']}")
