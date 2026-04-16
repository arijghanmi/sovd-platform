import os, re

apis_dir = '/home/pi/pfe1/sovd-server-fastapi-new/src/openapi_server/apis'
for filename in os.listdir(apis_dir):
    if not filename.endswith('.py'):
        continue
    filepath = os.path.join(apis_dir, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    original = content
    content = re.sub(r'(\w+)-(\w+)(\s*:\s*)', lambda m: m.group(1)+'_'+m.group(2)+m.group(3), content)
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Fixed: {filename}')
print('Done!')
