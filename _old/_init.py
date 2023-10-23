from sqlalchemy import create_engine, Column, Integer, Float, String, UniqueConstraint, Index, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# guid_url = f"http://{Private_setting.ip}/objects/?password={Private_setting.password}"
# response = requests.get(guid_url, verify=False)
#
# for i in json.loads(response.content):
#     name, guid = next(iter(i.items()))
#     t = Private_setting.Camera(name,guid,datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
#     Private_setting.cameras.append(t)

