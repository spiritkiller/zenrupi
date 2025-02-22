from stellar_sdk import Keypair

keypair = Keypair.random()
print(f"Public Key: {keypair.public_key}")
print(f"Secret Key: {keypair.secret}")
