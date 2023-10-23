import requests

import Private_setting
from code.data_storageSQLlite import create_tables, database_entry, read_from_database

create_tables()


guid_url = f"http://{Private_setting.ip}/objects/?password={Private_setting.password}"
response = requests.get(guid_url, verify=False)
cameras = read_from_database()
# update_guides_in_bd(json.loads(response.content))
# for i in json.loads(response.content):
#     name, guid = next(iter(i.items()))
#
#     api_url = f"http://{Private_setting.ip}/screenshot/{guid}?password={Private_setting.password}"
#     response = requests.get(api_url, verify=False)
#     img_data = response.content
#
#
#     image = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
#     yang = genetics.STEP1_initialize_population_from_frame(image)
#     t = Camera(name, guid, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),yang)
#     cameras.append(t)
# # cameras = [Camera("Окно 1", "AIhKLrez", "2023-09-15 19:53:58")]
#
# # add_initial_data(cameras)
#
#
print(cameras[0].old[0])
database_entry(cameras)