import re, os

id_pattern = re.compile(r'^.\d+$') 

API_ID = os.environ.get("API_ID", "23265307")

API_HASH = os.environ.get("API_HASH", "cc2b82ee80cabeba9a3408a6972d0ab2")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8086094628:AAHTmVS3pgy_n4CiUI8w4lOua80Sji60Enk") 

FORCE_SUB = os.environ.get("FORCE_SUB", "LazyDeveloper") 

DB_NAME = os.environ.get("DB_NAME","Yashkalvar07")     

DB_URL = os.environ.get("DB_URL","mongodb+srv://Yashkalvar07:Yashkalvar07@yashkalvar07.cylum.mongodb.net/?retryWrites=true&w=majority")
 
FLOOD = int(os.environ.get("FLOOD", "10"))

START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/rv8Lds3/ALL-RENAMER-LOGO-YASH-GOYAL.jpg")

ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '5965340120 6126812037').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in os.environ.get('CHANNELS', '-1002325465716 -1002249141765 -1002317508473 -1002473112911 -1002450859981').split()]

# Bot_Username = "@LazyPrincessXBOT"
BOT_USERNAME = os.environ.get("BOT_USERNAME", "@blindforwarderBOT")
MAX_ACTIVE_TASKS = int(os.environ.get("MAX_ACTIVE_TASKS", "5"))
MAX_FORWARD = int(os.environ.get("MAX_FORWARD", "20"))

PORT = os.environ.get('PORT', '8080')

Lazy_session = {}
Lazy_api_id ={}
Lazy_api_hash ={}

String_Session  = "None"

Permanent_4gb = "-100XXX"
