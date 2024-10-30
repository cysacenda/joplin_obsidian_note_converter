import os
import re
import filetype  # Assurez-vous que filetype est installé avec `pip install filetype`

# Répertoires des fichiers de ressources et des notes
resources_dir = r'G:\Mon Drive\_Obsidian\_resources'
notes_dir = r'G:\Mon Drive\_Obsidian'

# Fichier de mapping pour enregistrer les nouveaux renommages
mapping_file = 'new_renamed_files.txt'

# Fonction pour deviner et ajouter l'extension correcte aux fichiers restants sans extension
def add_extension_to_remaining_files():
    renamed_files = {}
    for filename in os.listdir(resources_dir):
        file_path = os.path.join(resources_dir, filename)
        
        # Vérifier que c'est bien un fichier et qu'il n'a pas d'extension
        if os.path.isfile(file_path) and '.' not in filename:
            # Utiliser `filetype` pour deviner le type de fichier
            kind = filetype.guess(file_path)
            if kind:
                extension = f".{kind.extension}"
                new_filename = filename + extension
                new_file_path = os.path.join(resources_dir, new_filename)
                os.rename(file_path, new_file_path)
                renamed_files[filename] = new_filename
                print(f'Renamed: {filename} -> {new_filename}')
            else:
                print(f"Impossible de déterminer l'extension pour {filename}")

    # Enregistrer le mapping dans un fichier pour référence future
    with open(mapping_file, 'a', encoding='utf-8') as f:
        for old_name, new_name in renamed_files.items():
            f.write(f'{old_name} -> {new_name}\n')

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

# Exécution des fonctions
renamed_files = add_extension_to_remaining_files()
if renamed_files:
    update_links_in_notes(renamed_files)
else:
    print("Aucun fichier supplémentaire n'a été renommé.")
