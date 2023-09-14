

guid_url = f"http://{Private_setting.ip}/objects/?password={Private_setting.password}"
response = requests.get(guid_url, verify=False)

for i in json.loads(response.content):
    name, guid = next(iter(i.items()))
    t = Private_setting.Camera(name,guid,datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
    Private_setting.cameras.append(t)