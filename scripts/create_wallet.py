from stellar_sdk import Keypair

# Yeni bir Stellar cüzdanı oluştur
keypair = Keypair.random()

print(f"Public Key: {keypair.public_key}")
print(f"Secret Key: {keypair.secret}")

