import os
import re

# Définir le répertoire des notes
notes_dir = r'G:\Mon Drive\_Obsidian'

# Charger le mapping des fichiers renommés
def load_renamed_files(mapping_file):
    renamed_files = {}
    with open(mapping_file, 'r', encoding='utf-8') as f:
        for line in f:
            if "Renamed:" in line:
                # Extraire l'ancien et le nouveau nom du fichier
                parts = line.strip().split(" -> ")
                if len(parts) == 2:
                    old_name = parts[0].replace("Renamed: ", "").strip()
                    new_name = parts[1].strip()
                    renamed_files[old_name] = new_name
    return renamed_files

# Fonction pour adapter les liens dans les notes
def update_links_in_notes(renamed_files):
    link_pattern = re.compile(r'\[(.*?)\]\(\.\./_resources/([^)]+)\)')

    for root, _, files in os.walk(notes_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Adapter les liens pour chaque fichier renommé
                modified = False
                def replace_link(match):
                    label = match.group(1)
                    old_filename = match.group(2)
                    if old_filename in renamed_files:
                        new_filename = renamed_files[old_filename]
                        new_link = f"[{label}](../_resources/{new_filename})"
                        nonlocal modified
                        modified = True
                        return new_link
                    return match.group(0)
                
                updated_content = link_pattern.sub(replace_link, content)

                # Enregistrer si le fichier a été modifié
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f'Updated links in: {file_path}')

# Charger le mapping depuis le fichier `renamed_files.txt`
mapping_file = 'renamed_files.txt'
renamed_files = load_renamed_files(mapping_file)

# Mettre à jour les liens dans les notes
if renamed_files:
    update_links_in_notes(renamed_files)
else:
    print("Aucun fichier renommé trouvé dans le fichier de mapping.")
