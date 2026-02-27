import json
import re
import sys

html_path = '/tmp/volcengine_price.html'
try:
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
except FileNotFoundError:
    print(f"File {html_path} not found")
    sys.exit(1)

# Find the initial state
pattern = r'window\.__INITIAL_STATE__\s*=\s*({.*?});'
match = re.search(pattern, html, re.DOTALL)
if not match:
    print("No __INITIAL_STATE__ found")
    sys.exit(1)

json_str = match.group(1)
try:
    data = json.loads(json_str)
except json.JSONDecodeError as e:
    print("JSON decode error:", e)
    # try to fix common issues
    json_str = json_str.replace('\\', '\\\\')
    try:
        data = json.loads(json_str)
    except:
        sys.exit(1)

# Navigate to the pricing data
# The structure might be nested. Let's explore keys
def explore(obj, path='', depth=0):
    if depth > 3:
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_path = f"{path}.{k}" if path else k
            if 'price' in k.lower() or 'cost' in k.lower() or 'model' in k.lower():
                print(new_path, type(v))
                if isinstance(v, dict) and len(v) < 5:
                    print(v)
                elif isinstance(v, list) and len(v) < 5:
                    print(v[:3])
            explore(v, new_path, depth+1)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:3]):
            explore(v, f"{path}[{i}]", depth+1)

explore(data)

# Also search for Doubao or 豆包
def search(obj, term, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_path = f"{path}.{k}" if path else k
            if term in k:
                print(f"Found in key: {new_path}")
                if isinstance(v, (dict, list)):
                    print(json.dumps(v, ensure_ascii=False, indent=2)[:500])
                else:
                    print(v)
            if isinstance(v, str) and term in v:
                print(f"Found in value at {new_path}: {v[:200]}")
            else:
                search(v, term, new_path)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            search(v, term, f"{path}[{i}]")

print("\n=== Searching for Doubao ===")
search(data, '豆包')
print("\n=== Searching for doubao ===")
search(data, 'doubao')
print("\n=== Searching for seed ===")
search(data, 'seed')