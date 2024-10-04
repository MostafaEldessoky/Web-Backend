import os
from dotenv import load_dotenv , find_dotenv

path = find_dotenv(".env")
 
load_dotenv(path)

psgr_db = os.getenv("psgr_db")
rds_host = os.getenv("rds_host")
rds_port = os.getenv("rds_port")
key = os.getenv("key")
algorithm = os.getenv("algorithm")
