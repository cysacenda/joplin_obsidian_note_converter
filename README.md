# joplin_obsidian_note_converter
Allows you to replace all `<img>` tags imported from Joplin notes that are not compatible with Obsidian to the standard format, taking into account height and width. Just set the directory of Obsidian notes. Please make a backup before running. Requires Python installed. 

Start with: `py convert.py`

**Before:**
```html
<img src="../_resources/9617d494875aa6a8cf858280250ccbe9.png" alt="e9634dbf41b1e1d29be78ce21a2d64ac.png" width="750" height="278" class="jop-noMdConv">
```html


**After:**
\![e9634dbf41b1e1d29be78ce21a2d64ac.png|750x278](../_resources/9617d494875aa6a8cf858280250ccbe9.png)
