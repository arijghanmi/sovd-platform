import os, re

models_dir = '/home/pi/pfe1/sovd-server-fastapi-new/src/openapi_server/models'
for filename in os.listdir(models_dir):
    if not filename.endswith('.py'):
        continue
    filepath = os.path.join(models_dir, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    original = content
    # Fix _schema -> schema_field
    content = content.replace('_schema', 'schema_field')
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Fixed: {filename}')
print('Done!')
