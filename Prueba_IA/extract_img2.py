import re
with open('onedrive_page.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()
img_tags = re.findall(r'<img[^>]*src="([^"]+)"[^>]*>', content)
for src in img_tags[:20]:
    print(src)
data_src = re.findall(r'data-src="([^"]+)"', content)
for s in data_src[:10]:
    print(s)
