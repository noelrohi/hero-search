from dotenv import load_dotenv
import os

load_dotenv()

prefix = os.environ.get("PREFIX")
mongo_uri = os.environ.get("MONGO_URI")
token = os.environ.get("TOKEN")
api = os.environ.get("API")