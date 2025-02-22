from stellar_sdk import Server

server = Server("https://horizon-testnet.stellar.org")

accounts = [
    ("ISSUER", "ISSUER_SECRET_KEY"),
    ("DISTRIBUTION", "DISTRIBUTION_SECRET_KEY")
]

for name, env_var in accounts:
    public_key = os.getenv(env_var)
    if not public_key:
        print(f"❌ {name} hesabı bulunamadı! Çevresel değişkeni eksik: {env_var}")
        exit(1)
    
    try:
        account = server.load_account(public_key)
        print(f"✅ {name} hesabı bulundu: {public_key}")
    except:
        print(f"⚠️ {name} hesabı Stellar Testnet'te bulunamadı!")
        exit(1)
