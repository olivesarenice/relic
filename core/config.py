import os

from dotenv import load_dotenv

load_dotenv()


INGRESS_CREDENTIALS = {os.getenv("CLIENT_ID"): os.getenv("CLIENT_API_KEY")}
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

print("Configuration loaded:")
print(f"INGRESS_CREDENTIALS: {INGRESS_CREDENTIALS}")
print(f"REDIS_HOST: {REDIS_HOST}")
print(f"REDIS_PORT: {REDIS_PORT}")
