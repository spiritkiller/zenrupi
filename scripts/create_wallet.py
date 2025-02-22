from stellar_sdk import Keypair

issuer = Keypair.random()

print(f"Issuer Public Key: {issuer.public_key}")
print(f"Issuer Secret Key: {issuer.secret}")
