from dotenv import load_dotenv
import os

load_dotenv()

cred = {
    "dbhost" : os.getenv("db_host"),
    "dbuser" : os.getenv("db_user"),
    "dbpassword" : os.getenv("db_password"),
    "dbname" : os.getenv("db_name"),
    "dbTableName" : os.getenv("db_table_name"),
    "dbTableSchema" : os.getenv("db_profile_schema"),
    "secret_key" : os.getenv("SECRET_KEY"),
    "senderEmail" : os.getenv("SENDER_EMAIL"),
    "senderPassword" : os.getenv("SENDER_EMAIL_PASSWORD")
}