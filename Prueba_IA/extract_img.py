import re
with open('onedrive_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()
urls = re.findall(r'https?://[^"\'\s]*(?:png|jpg|jpeg|gif|webp|svg)[^"\'\s]*', content)
for u in sorted(set(urls)):
    print(u)
