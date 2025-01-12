from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

UPBIT_REST_API_BASE = os.getenv("UPBIT_REST_API_BASE")
