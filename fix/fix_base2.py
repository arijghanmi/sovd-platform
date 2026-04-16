import os, re
apis_dir = '/home/pi/pfe1/sovd-server-fastapi-new/src/openapi_server/apis'
for filename in os.listdir(apis_dir):
    if not filename.endswith('.py'): continue
    filepath = os.path.join(apis_dir, filename)
    content = open(filepath).read()
    original = content
    content = re.sub(r'([a-zA-Z0-9]+)-([a-zA-Z0-9_]+)(\s*:)', lambda m: m.group(1)+'_'+m.group(2)+m.group(3), content)
    if content != original:
        open(filepath,'w').write(content)
        print('Fixed: '+filename)
