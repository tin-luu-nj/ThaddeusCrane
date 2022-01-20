import yaml

with open('notification/notDelivered.yml', 'r') as stream:
  env = yaml.load(stream, Loader=yaml.CLoader)

import hashlib
for i in env['server']['message']:
  print(i['md5sum'])
  print(hashlib.md5(str(i['content']).encode('utf-8')).hexdigest())

