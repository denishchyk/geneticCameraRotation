import requests

import Private_setting
from code.data_storageSQLlite import create_tables

create_tables()

guid_url = f"http://{Private_setting.ip}/objects/?password={Private_setting.password}"
response = requests.get(guid_url, verify=False)

