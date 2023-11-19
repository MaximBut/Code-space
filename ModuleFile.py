import tkinter as tk
from hashlib import md5
from customtkinter import *
import webbrowser
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import pyttsx3
import wikipedia
import base64
import customtkinter
import pyperclip
import webbrowser, re, ModuleFile, SearchMod
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
import customtkinter
import os

def rightSpeak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def Googlesearch(query_google):
    link = str(
        "https://www.google.com/search?q=" + query_google + "&oq=hi&aqs=chrome..69i57j69i59j0i67l2j46i67j69i60j69i61l2.422j0j4&sourceid=chrome&ie=UTF-8")
    webbrowser.open_new_tab(link)

def Summary(textwidget):
    note_lines = str(textwidget.index('end-1c').split('.')[0])
    note_char_count = str(len(textwidget.get("1.0", 'end-1c')))
    note_cindex = textwidget.index(INSERT)
    text = "Загальна кількість рядків: " + note_lines + "\n" + "Загальна кількість символів: " + note_char_count + "\n" 
    tkk = Toplevel()
    tkk.overrideredirect(True)
    tkk.configure(background="black")
    w = 300
    h = 100
    ws = tkk.winfo_screenwidth()
    hs = tkk.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    tkk.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def close():
        tkk.destroy()
    Label(tkk, text=text, background="black", foreground="orange").pack()
    ttk.Button(tkk, text="OK", command=close).pack(side=BOTTOM)

def highlightText(notepad):
    st_ind = notepad.index("sel.first")
    end_ind = notepad.index("sel.last")
    notepad.tag_add("start", st_ind, end_ind)
    notepad.tag_configure("start", background="gold", foreground="black")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def find_replace(self):
    def finnd():
        word = find_input.get()
        self.tabs[self.get_tab()].textbox.tag_remove("match",'1.0',END)
        matches = 0
        if word:
            start_pos = "1.0"
            while True:
                start_pos = self.tabs[self.get_tab()].textbox.search(word,start_pos,stopindex=END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(word)}c"
                self.tabs[self.get_tab()].textbox.tag_add("match",start_pos,end_pos)
                matches += 1
                start_pos = end_pos
                self.tabs[self.get_tab()].textbox.tag_config("match",foreground = "yellow",background = "#1d1d1d")
    def replace():
        word = find_input.get()
        replace_text = replace_input.get()
        content = self.tabs[self.get_tab()].textbox.get(1.0,END)
        new_content = content.replace(word,replace_text)
        self.tabs[self.get_tab()].textbox.delete(1.0,END)
        self.tabs[self.get_tab()].textbox.insert(1.0,new_content)

    find_dialogue = customtkinter.CTkToplevel()
    find_dialogue.attributes("-topmost", 1)
    find_dialogue.geometry("450x200")
    find_dialogue.title("Знайти")
    find_dialogue.resizable(0,0)
    find_frame = LabelFrame(find_dialogue,text = "Введіть дані: ", background="#1d1d1d", foreground="white")
    find_frame.pack(pady = 20)

    text_find_label = ttk.Label(find_frame, text='Знайти: ', background="#1d1d1d", foreground="cyan")
    text_replace_label = ttk.Label(find_frame, text= 'Замінити', background="#1d1d1d", foreground="cyan")
    find_input = ttk.Entry(find_frame, width=30, background="grey")
    replace_input = ttk.Entry(find_frame, width=30)
    find_button = ttk.Button(find_frame, text='Знайти',command = finnd)
    replace_button = ttk.Button(find_frame, text= 'Замінити',command = replace)
    text_find_label.grid(row=0, column=0, padx=4, pady=4)
    text_replace_label.grid(row=1, column=0, padx=4, pady=4)
    find_input.grid(row=0, column=1, padx=4, pady=4)
    replace_input.grid(row=1, column=1, padx=4, pady=4)
    find_button.grid(row=2, column=0, padx=8, pady=20)
    replace_button.grid(row=2, column=1, padx=8, pady=20)
    find_dialogue.mainloop()

def encypt(notepad):
    cindex = notepad.index(INSERT)
    sample_string = notepad.selection_get()
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_encoded = base64_bytes.decode("ascii")
    notepad.insert(cindex, base64_encoded)

def decode(notepad):
    base64_string = notepad.selection_get()
    base64_bytes = base64_string.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    notepad.insert(notepad.index(INSERT), sample_string)

def open_in_dir(self):
    m = messagebox.showwarning("Code Space","Увага! Якщо ви захочете відкрити ще один файл, перезапустіть дане вікно!")
    dir_tk = customtkinter.CTkToplevel()
    dir_tk.attributes("-topmost", 1)
    dir_tk.title("Відкрити з директорії")
    flist = os.listdir()
    lbox = tk.Listbox(dir_tk, background="#1b1b1b", foreground="white", highlightthickness=0,
                      borderwidth=0, width=70)
    lbox.pack(fill=BOTH)
    ysb = ttk.Scrollbar(dir_tk, orient='vertical', command=lbox.yview)
    xsb = ttk.Scrollbar(dir_tk, orient='horizontal', command=lbox.xview)
    lbox.configure(yscroll=ysb.set, xscroll=xsb.set)
    ysb.pack(side=RIGHT, fill=X)
    xsb.pack(side=BOTTOM, fill=Y)
    for item in flist:
        lbox.insert(tk.END, item)
    def showcontent(event, audio=0):
        x = lbox.curselection()[0]
        file = lbox.get(x)
        try:
            with open(file, 'r', encoding='utf-8') as file:
                file = file.read()
                vfile = str(file)
            self.tabs[self.get_tab()].textbox.insert(tk.END, file)
        except UnicodeDecodeError:
            messagebox.showerror("Помилка!", "Файл такого формату не підтримується!")
    
    lbox.bind("<Double-Button-1>", showcontent)
    
    def opensystem(event):
        x = lbox.curselection()[0]
        os.system(lbox.get(x))
        
def refractor(notepad):
    word = notepad.selection_get()
    def replace():
        replace_text = replace_input.get()
        content = notepad.get(0.0, END)
        new_content = content.replace(word,replace_text)
        notepad.delete(1.0,END)
        notepad.insert(1.0,new_content)
        find_dialogue.destroy()

    find_dialogue = Toplevel()
    find_dialogue.config(background="#1d1d1d")
    find_dialogue.title("Перейменування")
    find_dialogue.resizable(False, False)
    find_frame = LabelFrame(find_dialogue, text="Змінити", background="#1d1d1d", foreground="white")
    find_frame.pack(pady = 20)

    find_input = customtkinter.CTkEntry(find_frame, width=190, border_color="red")
    find_input.insert(0,word)
    replace_input = customtkinter.CTkEntry(find_frame, width=190, border_color="cyan")
    replace_button = ttk.Button(find_frame, text= 'Refract',command = replace)
    find_input.grid(row=0, column=1, padx=4, pady=4)
    replace_input.grid(row=1, column=1, padx=4, pady=4)
    replace_button.grid(row=2, column=1, padx=8, pady=20)

    find_dialogue.mainloop()


py_text = "def main():" + "\n" + "    print('Code space')" + "\n" + "\n" + "main()"



def python_temp(text_widget):
    text_widget.insert(0.0, py_text)

py_words = ['False', 'None', 'True', 'await', 'break', 'class', 'else', 'except', 'finally', 'import', 'in', 'is',
            'pass', 'raise', 'return', 'and', 'as', 'assert', 'async', 'continue', 'def', 'del', 'elif', 'for', 'from',
            'global', 'if', 'lambda', 'nonlocal', 'not', 'or', 'try', 'while', 'with', 'yield', 'abs()', 'all()', 'any()',
            'ascii()', 'bin()', 'bool()', 'breakpoint()', 'bytearray()', 'bytes()', 'callable()', 'chr()', 'classmethod()',
            'compile()', 'complex()', 'delattr()', 'dict()', 'dir()', 'divmod()', 'enumerate()', 'eval()', 'exec()',
            'filter()', 'float()', 'format()', 'frozenset()', 'getattr()', 'globals()', 'hasattr()', 'hash()', 'help()'
            'hex()', 'id()', 'input()', 'int()', 'isinstance()', 'issubclass()', 'iter()', 'lem()', 'list()', 'locals()',
            'map()', 'max()', 'memoryview()', 'min()', 'next()', 'object()', 'oct()', 'open()', 'ord()', 'pow()', 'print()',
            'property()', 'range()', 'repr()', 'reversed()', 'round()', 'set()', 'setattr()', 'slice()', 'sorted()',
            'staticmethod()', 'str()', 'sum()', 'super()', 'tuple()', 'type()', 'vars()', 'zip()', '__import__()']

html_words = ['blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'cite', 'code', 'col', 'colgroup',
        'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'div', 'dl', 'dt', 'em', 'embed',
        'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'head', 'header', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'legend',
        'li', 'link', 'main', 'map', 'mark', 'meta', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup',
        'option', 'output', 'p', 'param', 'picture', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp',
        'script', 'section', 'select', 'small', 'source', 'span', 'strong', 'style', 'sub', 'summary', 'sup',
        'svg', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr',
        'track', 'u', 'ul']

words = ['False', 'None', 'True', 'await', 'break', 'class', 'else', 'except', 'finally', 'import', 'in', 'is',
            'pass', 'raise', 'return', 'and', 'as', 'assert', 'async', 'continue', 'def', 'del', 'elif', 'for', 'from',
            'global', 'if', 'lambda', 'nonlocal', 'not', 'or', 'try', 'while', 'with', 'yield', 'abs()', 'all()', 'any()',
            'ascii()', 'bin()', 'bool()', 'breakpoint()', 'bytearray()', 'bytes()', 'callable()', 'chr()', 'classmethod()',
            'compile()', 'complex()', 'delattr()', 'dict()', 'dir()', 'divmod()', 'enumerate()', 'eval()', 'exec()',
            'filter()', 'float()', 'format()', 'frozenset()', 'getattr()', 'globals()', 'hasattr()', 'hash()', 'help()'
            'hex()', 'id()', 'input()', 'int()', 'isinstance()', 'issubclass()', 'iter()', 'lem()', 'list()', 'locals()',
            'map()', 'max()', 'memoryview()', 'min()', 'next()', 'object()', 'oct()', 'open()', 'ord()', 'pow()', 'print()',
            'property()', 'range()', 'repr()', 'reversed()', 'round()', 'set()', 'setattr()', 'slice()', 'sorted()',
            'staticmethod()', 'str()', 'sum()', 'super()', 'tuple()', 'type()', 'vars()', 'zip()', '__import__()', 'div', 'dl', 'dt', 'em', 'embed',
        'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'head', 'header', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'legend',
        'li', 'link', 'main', 'map', 'mark', 'meta', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup',
        'option', 'output', 'p', 'param', 'picture', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp',
        'script', 'section', 'select', 'small', 'source', 'span', 'strong', 'style', 'sub', 'summary', 'sup',
        'svg', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr',
        'track', 'u', 'ul', 'var', 'video', 'wbr', "auto,break,case,char,const,continue,default,do,double,else,enum,extern,false,float,for,goto,if,int,long,namespace,"
        "new","nullptr","operator","return","short","signed","sizeof","static","struct","switch","template","this",
         "true","typedef","union","unsigned","void","volatile","while"]

def to_Upper(self):
    string = self.tabs[self.get_tab()].textbox.selection_get()
    st_ind = self.tabs[self.get_tab()].textbox.index("sel.first")
    end_ind = self.tabs[self.get_tab()].textbox.index("sel.last")
    up_str = string.upper()
    self.tabs[self.get_tab()].textbox.delete(st_ind, end_ind)
    self.tabs[self.get_tab()].textbox.insert(st_ind, up_str)

def find(self, textfindedd):
    word = textfindedd.get()
    self.tabs[self.get_tab()].textbox.tag_remove("match", '1.0', END)
    matches = 0
    if word:
        start_pos = "1.0"
        while True:
            start_pos = self.tabs[self.get_tab()].textbox.search(word, start_pos, stopindex=END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(word)}c"
            self.tabs[self.get_tab()].textbox.tag_add("match", start_pos, end_pos)
            matches += 1
            start_pos = end_pos
            self.tabs[self.get_tab()].textbox.tag_config("match", foreground="#1d1d1d", background="yellow")

def to_Lower(self):
    string = self.tabs[self.get_tab()].textbox.selection_get()
    st_ind = self.tabs[self.get_tab()].textbox.index("sel.first")
    end_ind = self.tabs[self.get_tab()].textbox.index("sel.last")
    up_str = string.lower()
    self.tabs[self.get_tab()].textbox.delete(st_ind, end_ind)
    self.tabs[self.get_tab()].textbox.insert(st_ind, up_str)

def add_str(self):
    string = self.tabs[self.get_tab()].textbox.selection_get()
    st_ind = self.tabs[self.get_tab()].textbox.index("sel.first")
    end_ind = self.tabs[self.get_tab()].textbox.index("sel.last")
    self.tabs[self.get_tab()].textbox.insert(st_ind, '"')
    self.tabs[self.get_tab()].textbox.insert(end_ind, '"')

def add_par(self):
    string = self.tabs[self.get_tab()].textbox.selection_get()
    st_ind = self.tabs[self.get_tab()].textbox.index("sel.first")
    end_ind = self.tabs[self.get_tab()].textbox.index("sel.last")
    self.tabs[self.get_tab()].textbox.insert(st_ind, '(')
    self.tabs[self.get_tab()].textbox.insert(end_ind, ')')

def calculate(self):
    string = self.tabs[self.get_tab()].textbox.selection_get()
    try:
        res = int(eval(string))
        res = str(res)
        messagebox.showinfo("Result", res)
    except:
        messagebox.showerror("Помилка!", "Вибраний текст не є математичним прикладом, або містить дії, які не підтримуються цією функцією.")

def calc_enter_res(self):
    string = self.tabs[self.get_tab()].textbox.selection_get()
    st_ind = self.tabs[self.get_tab()].textbox.index("sel.first")
    end_ind = self.tabs[self.get_tab()].textbox.index("sel.last")
    try:
        res = int(eval(string))
        res = str(res)
        self.tabs[self.get_tab()].textbox.delete(st_ind, end_ind)
        self.tabs[self.get_tab()].textbox.insert(st_ind, res)
    except:
        messagebox.showerror("Помилка!", "Вибраний текст не є математичним прикладом, або містить дії, які не підтримуються цією функцією.")


def open_file(self, *args, Document):
    file_dir = (filedialog.askopenfilename(initialdir=self.init_dir, title="Select file", ))
    if file_dir:
        try:
            file = open(file_dir, encoding='utf-8')
            new_tab = ttk.Frame(self.nb, borderwidth=0)
            self.tabs[new_tab] = Document(new_tab, self.create_text_widget(new_tab), file_dir)
            self.nb.add(new_tab, text=os.path.basename(file_dir))
            self.nb.select(new_tab)
            self.tabs[new_tab].textbox.insert('end', file.read())
            self.tabs[new_tab].status = md5(self.tabs[new_tab].textbox.get(1.0, 'end').encode('utf-8'))
        except FileNotFoundError:
            return

def open_spec_file(self, *args, Document, filedir):
    file_dir = filedir
    if file_dir:
        try:
            file = open(file_dir)
            new_tab = ttk.Frame(self.nb, borderwidth=0)
            self.tabs[new_tab] = Document(new_tab, self.create_text_widget(new_tab), file_dir)
            self.nb.add(new_tab, text=os.path.basename(file_dir))
            self.nb.select(new_tab)
            self.tabs[new_tab].textbox.insert('end', file.read())
            self.tabs[new_tab].status = md5(self.tabs[new_tab].textbox.get(1.0, 'end').encode('utf-8'))
        except FileNotFoundError:
            messagebox.showerror("Помилка!", "Файл не знайдено.")

def save_as(self):
    curr_tab = self.get_tab()
    file_dir = (filedialog.asksaveasfilename(initialdir=self.init_dir, title="Виберіть місце зберігання"))
    if not file_dir:
        return
    self.tabs[curr_tab].file_dir = file_dir
    self.tabs[curr_tab].file_name = os.path.basename(file_dir)
    self.nb.tab(curr_tab, text=self.tabs[curr_tab].file_name)
    title = self.tabs[curr_tab].file_name + " ~ Code space"
    self.master.title(title)
    file = open(file_dir, 'w')
    file.write(self.tabs[curr_tab].textbox.get(1.0, 'end'))
    file.close()
    self.tabs[curr_tab].status = md5(self.tabs[curr_tab].textbox.get(1.0, 'end').encode('utf-8'))

def goto(self):
    top = customtkinter.CTkToplevel()
    top.attributes('-topmost', 10)
    top.geometry("200x200")
    top.title("Перейти на рядок")
    customtkinter.CTkLabel(top, text="Номер рядку:").pack()
    lineentry = customtkinter.CTkEntry(top, width=150)
    lineentry.pack(pady=20)
    def go_to():
        self.tabs[self.get_tab()].textbox.mark_set("insert", str(lineentry.get()) + ".0")
        text = Text(top)
        pos = self.tabs[self.get_tab()].textbox.index(str(float(lineentry.get())) + "lineend")
        print(pos)
        self.tabs[self.get_tab()].textbox.tag_add(SEL, str(float(lineentry.get())), pos)
        self.tabs[self.get_tab()].textbox.focus_set()
    customtkinter.CTkButton(top, text="Перейти", command=go_to).pack(pady=10)
    customtkinter.CTkButton(top, text="Відміна", command=lambda: top.destroy()).pack()

def save_file(self, *args):
    curr_tab = self.get_tab()
    if not self.tabs[curr_tab].file_dir:
        self.save_as()
    else:
        with open(self.tabs[curr_tab].file_dir, 'w') as file:
            file.write(self.tabs[curr_tab].textbox.get(1.0, 'end'))
        self.tabs[curr_tab].status = md5(self.tabs[curr_tab].textbox.get(1.0, 'end').encode('utf-8'))

def new_file(self, e):
    file_ui = customtkinter.CTkToplevel()
    file_ui.attributes('-topmost', 101)
    file_ui.title("Новий файл"), file_ui.geometry("250x150")
    customtkinter.CTkLabel(file_ui, text="Ім\'я:").pack()

    file_name = customtkinter.CTkEntry(file_ui, width=200, text_color="light blue")
    file_name.pack(pady=5)

    type_selection = customtkinter.CTkComboBox(master=file_ui,
                                 values=["Python File", "Text file"])

    type_selection.pack(pady=15)

    def apply():
        type_val = type_selection.get()
        filename = file_name.get()

        if type_val == "Python File":
            filename = filename + ".py"
            self.new_filed(filename = filename)
        elif type_val == "Text file":
            filename = filename + ".txt"
            self.new_filed(filename=filename)
        file_ui.destroy()

    customtkinter.CTkButton(file_ui, text="Створити", command=apply).pack(side=BOTTOM)

