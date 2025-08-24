import os

from dotenv import load_dotenv

load_dotenv()


INGRESS_CREDENTIALS = {os.getenv("CLIENT_ID"): os.getenv("CLIENT_API_KEY")}
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

GRAPHITI_LLM_API_KEY = os.getenv("GRAPHITI_LLM_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
