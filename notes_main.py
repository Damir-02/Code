#all of the imports such as: json, PyQt5.Qtcore, and PyQt5.QtWigets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
import json

app = QApplication([])
notes_win = QWidget()
notes_win.setWindowTitle('Smart notes')
notes_win.resize(900,600)

'''notes = {
    'Welcome':{
        'text': 'first text',
        'tags': ['tag_1', 'tag_2']
    }
}

with open('notes_data.json', 'w', encoding='utf-8') as file:
    json.dump(notes, file)'''

field_text = QTextEdit()
list_notes_label = QLabel('list of notes')
list_notes = QListWidget()


button_note_create = QPushButton('Create Notes')
button_note_del = QPushButton('Delete Notes')
button_note_save = QPushButton('Save Notes')


list_tags_label = QLabel('List of Tags')
list_tags = QListWidget()
field_tag = QLineEdit()
field_tag.setPlaceholderText('Enter Tag...')
button_tag_add = QPushButton('Add to notes')
button_tag_del = QPushButton('Delete from notes')
button_tag_search = QPushButton('Find notes using tag')

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)


col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)


col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)
col_2.addLayout(row_3)
col_2.addLayout(row_4)


layout_notes.addLayout(col_1)
layout_notes.addLayout(col_2)
notes_win.setLayout(layout_notes)


def show_note():
    name = list_notes.selectedItems()[0].text()
    field_text.setText(notes[name]['text'])
    list_tags.clear()
    list_tags.addItems(notes[name]['tags'])

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Add Notes', 'Name of Notes:')
    if ok and note_name != '':
        notes[note_name] = {'text':'', 'tags': []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['tags'])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['text'] = field_text.toPlainText()
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['tags']:
            notes[key]['tags'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            with open('notes_data.json', 'w', encoding='utf-8') as file:
                json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['tags'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['tags'])
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == 'Find notes using tag' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['tags']:
                notes_filtered[note] = notes[note]
        button_tag_search.setText('finish search')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    
    elif button_tag_search.text() == 'finish search':
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Find notes using tag')

list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

#opening the json file
with open('notes_data.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)


list_notes.addItems(notes)
notes_win.show()
app.exec()
