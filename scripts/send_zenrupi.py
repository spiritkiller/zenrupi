import os
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset


# Çevresel değişkenleri elle tanımla
ISSUER_SECRET_KEY="SCZVV4BZXR3CKYC66DG2FJ5IM3QNAKEXZQHKKOGCHS5LPSOXKZXESMLH"
ISSUER_PUBLIC_KEY="GC4HDV2H3PRIAPE32R3QU5PXAMAJ6FB5VKZXDR6ZZQPTXNMMQXEDEX3V"
DISTRIBUTION_SECRET_KEY="SAPDRIYXLMLN6XFIHI55ZJPQSO3GF43S64AXRJ6PIGAWZLUTUV32UM2P"
DISTRIBUTION_PUBLIC_KEY="GAL7BEI2I5TO3GJBDADFEA356QP46YHBDJM7GQAYVFAY4FT2SM5XULFF"

# Stellar Ağına Bağlan
server = Server(horizon_url="https://horizon-testnet.stellar.org")
distribution_keypair = Keypair.from_secret(DISTRIBUTION_SECRET_KEY)
distribution_account = server.load_account(DISTRIBUTION_PUBLIC_KEY)

# ZenRupi (ZP) Varlığını Tanımla
asset_code = "ZP"
asset = Asset(asset_code, ISSUER_PUBLIC_KEY)

# İşlem Oluştur
transaction = (
    TransactionBuilder(
        source_account=distribution_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100
    )
    .append_payment_op(destination=DISTRIBUTION_PUBLIC_KEY, amount="50", asset=asset)
    .set_timeout(30)
    .build()
)

# İşlemi İmzala ve Gönder
transaction.sign(distribution_keypair)
response = server.submit_transaction(transaction)

print(f"✅ ZenRupi Gönderildi! İşlem Hash: {response['hash']}")
