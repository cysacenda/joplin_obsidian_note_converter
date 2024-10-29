import os
import re

# Set the directory containing your .md files
root_dir = r'G:\Mon Drive\_Obsidian\5 References'

# Regular expression to match HTML <img> tags
img_tag_pattern = re.compile(
    r'<img\s+([^>]*\bsrc="[^"]+"[^>]*)>',
    re.IGNORECASE
)

# Regular expression to extract attributes from the <img> tag
attr_pattern = re.compile(r'(\b\w+)="([^"]*)"')

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_img_tag(match):
        img_tag_content = match.group(1)
        attrs = dict(attr_pattern.findall(img_tag_content))

        src = attrs.get('src', '').strip()
        alt = attrs.get('alt', '').strip()
        width = attrs.get('width', '').strip()
        height = attrs.get('height', '').strip()

        size = ''
        if width and height:
            size = f'|{width}x{height}'
        elif width:
            size = f'|{width}'
        elif height:
            size = f'|x{height}'

        markdown_img = f'![{alt}{size}]({src})'
        return markdown_img

    new_content = img_tag_pattern.sub(replace_img_tag, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Processed: {file_path}')

for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.md'):
            file_path = os.path.join(subdir, file)
            process_file(file_path)
            print('processed file :' + file_path)
