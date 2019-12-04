from variables import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os


class Methods(Variables):
    """Contain all functions for whole application"""
    def get_cursor_pos(self, event=None):
        # self.line_counter()

        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        self.textArea = self.nb.children[tab].children['!text']
        self.textArea.tag_remove("highlight", '1.0', "end")
        row, col = self.textArea.index('insert').split('.')  # Get current position of the cursor
        self.cursor_pos.config(text=f'Ln: {int(row)}, Col: {int(col) + 1}')
        # Highlight current line

        self.textArea.tag_add("highlight", f"{row}.0", f"{row}.end+1c")
        # print(self.textArea.get(f"{row}.0", f"{row}.end+1c"))
        self.textArea.tag_config("highlight", background='#d5efeb')

    def proxy(self, *args):
        # let the actual widget perform the requested action
        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        try:
            cmd = (self.nb.children[tab].children['!text']._orig,) + args
            result = self.nb.children[tab].children['!text'].tk.call(cmd)
            if (args[0] in ("insert", "replace", "delete") or
                    args[0:3] == ("mark", "set", "insert") or
                    args[0:2] == ("xview", "moveto") or
                    args[0:2] == ("xview", "scroll") or
                    args[0:2] == ("yview", "moveto") or
                    args[0:2] == ("yview", "scroll")
            ):
                self.nb.children[tab].children['!text'].event_generate("<<Change>>", when="tail")
                # self.line_counter()    # scroll text area with canvas
            # return what the actual widget returned
            return result
        except:
            print('Exception')

    def line_counter(self, event=None):
        """Line counter for counting lines in file."""
        try:
            self.canvas.delete('all')
            if self.nb.index("current") is 0:
                tab = '!frame'
            else:
                tab = f'!frame{self.nb.index("current") + 1}'
            i = self.nb.children[tab].children['!text'].index("@0,0")
            while True:
                dline = self.nb.children[tab].children['!text'].dlineinfo(i)
                if dline is None: break
                y = dline[1]
                linenum = str(i).split(".")[0]
                self.canvas.create_text(10, y + 3, anchor="w", text=linenum, font=self.customFont, width=0)
                text_length = self.canvas.bbox('all')  # returns a tuple in the form of (x1, y1, x2, y2)
                width = text_length[2] - text_length[0]  # x2-x1
                self.canvas.config(width=width+15)
                i = self.nb.children[tab].children['!text'].index("%s+1line" % i)
            # print(self.cursor_pos.cget('pady'), self.statusbar_frame.cget('pady'), )
        except:
            self.canvas.delete('all')

    tab_counter = 1
    filename_list = []
    def add_tab(self, event=None, file=None, isonlyfile=0):
        """Add new tab Notebook widget"""
        tab1 = Frame(self.nb, width=0)
        tab1.pack()
        # font_style = "Consolas"
        # font_size = 15
        # customFont = tkFont.Font(family=font_style, size=font_size)
        tab_width = self.customFont.measure('    ')
        print(tab_width)
        text = Text(tab1, font=self.customFont, wrap='none', width=0, undo=True, tabs=tab_width)
        # Horizontal Scrollbar on text area
        y_scrollbar = Scrollbar(tab1, orient='vertical', command=text.yview,
                                 width=13, relief='flat')
        text.config(yscrollcommand=y_scrollbar.set)
        # y_scrollbar.config(command=text.yview)
        y_scrollbar.pack(side='right', fill='y')

        x_scrollbar = Scrollbar(tab1, orient=HORIZONTAL, width=13)
        text.config(xscrollcommand=x_scrollbar.set)
        x_scrollbar.config(command=text.xview)
        x_scrollbar.pack(side=BOTTOM, fill=X)
        text.pack(fill='both', expand=1)
        self.tab_counter += 1


        if isonlyfile is 1:
            filename = os.path.basename(file.name)
            print(file.name)
            self.nb.add(tab1, text=filename)
            self.nb.select(tab1)
            f = open(file.name)
            text.insert("1.0", f.read())
            text.edit('reset')
            text.edit_modified(arg=False)
            f.close()
        elif file and isonlyfile == 0:
            filename = os.path.basename(file)
            print(file)
            self.nb.add(tab1, text=filename)
            self.nb.select(tab1)
            f = open(file)
            text.insert("1.0", f.read())
            text.edit('reset')
            text.edit_modified(arg=False)
            f.close()
        else:
            self.nb.add(tab1, text=f'Untitled -{self.tab_counter}')
            self.nb.select(tab1)

        text.bind('<Control - =>', self.increase_font)
        text.bind('<Control - minus>', self.decrease_font)
        text.bind("<Control-Shift-r>", self.font_reset)
        text.bind("<Control-Shift-R>", self.font_reset)
        text.bind("<ButtonRelease>", self.get_cursor_pos)

        text.bind('<Control-z>', self.undo)
        text.bind('<Control-Z>', self.undo)
        text.bind('<Control-y>', self.redo)
        text.bind('<Control-Y>', self.redo)
        text.bind('<Control-a>', self.select_all)
        text.bind("<<Modified>>", self.modify)
        self.main_window.bind('<Control-A>', self.select_all)

        text.bind("<<Change>>", self.line_counter)
        # self.tab_counter += 1
        # self.nb.add(tab1, text=f'Untitled -{self.tab_counter}')

        # text.focus_force()
        self.get_cursor_pos()


        #
        # # lst.append('untitled')
        #
        text._orig = text._w + "_orig"
        text.tk.call("rename", text._w, text._orig)
        text.tk.createcommand(text._w, self.proxy)

    def increase_font(self, event=None):
        """For increase font of the editor and line number"""
        if self.font_size <= 60:
            self.font_size += 1
            self.customFont.config(size=self.font_size)
            self.main_window.update()
            self.line_num_frame.update()
            self.statusbar_frame.update()
            if self.nb.index("current") is 0:
                tab = '!frame'
            else:
                tab = f'!frame{self.nb.index("current") + 1}'
            self.nb.children[tab].children['!text'].config(font=self.customFont)

    def decrease_font(self, event=None):
        # global font_style, font_size
        if self.font_size >= 10:
            self.font_size -= 1
            self.customFont.config(size=self.font_size)
            self.line_num_frame.update_idletasks()
            if self.nb.index("current") is 0:
                tab = '!frame'
            else:
                tab = f'!frame{self.nb.index("current") + 1}'
            self.nb.children[tab].children['!text'].config(font=self.customFont)

    def font_reset(self, event=None):
        self.font_size = 15
        self.customFont.configure(size=self.font_size)
        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        self.nb.children[tab].children['!text'].config(font=self.customFont)

    def get_mini_map_text(self, event=None):
        # self.get_cursor_pos()
        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        data = self.nb.children[tab].children['!text'].get('1.0', 'end')
        self.mini_map_text.config(state=NORMAL)
        self.mini_map_text.delete('1.0', 'end')
        self.mini_map_text.insert('1.0', data)
        self.mini_map_text.config(state=DISABLED)

    def rename(self, file):
        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        self.nb.tab(self.nb.children[tab], text=file)


    clicked = 1

    def show_toolbar(self, event=None):
        if self.clicked == 0:  # displaying
            self.toolbar_frame.pack_forget()
            # self.working_area.pack_forget()
            # self.line_num_frame.pack_forget()
            # self.code_minimap_frame.pack_forget()
            self.main_frame.pack_forget()
            self.on_off_project_hierarchy.pack_forget()
            self.toolbar_frame.pack(fill='x', side='top')
            self.on_off_project_hierarchy.pack(fill='y', side='left')
            self.main_frame.pack(fill='both', side='left', expand=1)
            # self.line_num_frame.pack(fill='y', side='left')
            # self.working_area.pack(fill='both', side='left', expand=True)
            # self.code_minimap_frame.pack(fill='both', side='left')

            # if hide == 1:  # displaying status bar
            #     self.statusbar_frame.pack(side=BOTTOM, fill=X)
            self.Toolbars.entryconfigure(1, label="       Hide toolbar                ")
            self.clicked = 1
        elif self.clicked == 1:  # hiding
            self.toolbar_frame.pack_forget()
            self.Toolbars.entryconfigure(1, label="       Show toolbar                ")
            self.clicked = 0

    def undo(self, event=None):
        # print('undo')
        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        textArea = self.nb.children[tab].children['!text']
        textArea.event_generate('<<Undo>>')

    def redo(self, event=None):
        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        textArea = self.nb.children[tab].children['!text']
        textArea.event_generate('<<Redo>>')

    def cut(self, event=None):
        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        textArea = self.nb.children[tab].children['!text']
        textArea.event_generate('<<Cut>>')

    def copy(self, event=None):
        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        textArea = self.nb.children[tab].children['!text']
        textArea.event_generate('<<Copy>>')

    def paste(self, event=None):
        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        textArea = self.nb.children[tab].children['!text']
        textArea.event_generate('<<Paste>>')

    def select_all(self, event=None):
        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        textArea = self.nb.children[tab].children['!text']
        textArea.tag_add("sel", "1.0", "end-1c")
        return "break"  # Deleting default Control + a select event

    def auto_complete(self, event):
        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        text = self.nb.children[tab].children['!text']
        # print(event)
        if event.char == '(':
            text.insert('insert', ')')
            text.mark_set('insert', 'insert-1c')
        elif event.char == '{':
            text.insert('insert', '}')
            text.mark_set('insert', 'insert-1c')
        elif event.char == '[':
            text.insert('insert', ']')
            text.mark_set('insert', 'insert-1c')
        elif event.char == '"':
            text.insert('insert', '"')
            text.mark_set('insert', 'insert-1c')
        elif event.char == "'":
            text.insert('insert', "'")
            text.mark_set('insert', 'insert-1c')


    # File related functions

    def open_file(self, event=None):
        """Open the file in currently opened tab."""
        self.file = fd.askopenfile(title="Choose file to open",
                                        filetypes=[("Text(default)", "*.txt"), ("Python", "*.py"),
                                                   ("Java", "*.java"), ("JavaScript", "*.js"),
                                                   ("HTML", "*.html"), ("CSS", "*.css"),
                                                   ("All files", "*.*")])
        if self.file is None:
            return
        else:
            self.add_tab(file=self.file, isonlyfile=1)
            #
            # if self.nb.index("current") is 0:
            #     tab = '!frame'
            # else:
            #     tab = f'!frame{self.nb.index("current") + 1}'
            # textArea = self.nb.children[self.paned_win.focus_get()].children['!text']
            # textArea.delete("1.0", END)
            # textArea.insert("1.0", self.file.read())
            # self.main_window.title(str(self.file.name) + " -CodeEdit")
            # textArea.mark_set(INSERT, 1.0)  # Set caret(cursor) position at 1.0
            # print("Opened")
            # # v.file_name = v.file.name
            # self.file.close()
            # self.line_counter()
            # textArea.edit('reset')
            # textArea.edit_modified(arg=False)
            # self.get_mini_map_text()
            # self.nb.tab(self.nb.children[tab], text=self.file.name)
            #
            # # type = self.file.name[self.file.name.rindex('.')+1:]
            # if self.file.name.endswith('.py'):
            #     self.file_type.config(text='Python')
            # # modified()
            # # keyword_matching()
            # return True





    def save_file(self, event=None):
        """Save the content of the current opened tab."""
        if self.nb.index("current") is 0:
            tab = '!frame'
        else:
            tab = f'!frame{self.nb.index("current") + 1}'
        textArea = self.nb.children[tab].children['!text']
        if self.file == None:
            self.file = fd.asksaveasfile(title="Save file", defaultextension=".txt",
                                    filetypes=[("Text(default)", "*.txt"), ("Python", "*.py"),
                                               ("Java", "*.java"), ("JavaScript", "*.js"),
                                               ("HTML", "*.html"), ("CSS", "*.css"),
                                               ("All files", "*.*")])
            if self.file == None:
                return None
            else:

                self.file.write(textArea.get("1.0", "end-1c"))
                # win.title(str(file.name) + " -Notepad")
                self.rename(self.file.name)
                self.file.close()
                print("Saved..")
                textArea.edit_modified(arg=False)
                # print(file)
                # modified()
                return True
        else:
            self.file = open(self.file.name, "w+")
            self.file.write(textArea.get("1.0", "end-1c"))
            # win.title(str(file.name) + "  -Notpad")
            self.rename(self.file.name)
            self.file.close()
            print("Saved..")
            textArea.edit_modified(arg=False)
            # modified()
            return True

    def popup(self, event):
        """Display the popup menu when user right click inside the text area"""
        try:
            self.popup_menu.post(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def modify(self, event):
        self.popup_menu.entryconfigure(0, state='normal')
        # self.popup_menu.activate(0)
        # print(event.widget)

    def save_as_file(self, event=None):
        # global v.file
        self.file = fd.asksaveasfile(title="Save as", defaultextension=".txt",
                                  filetypes=[("Text(default)", "*.txt"), ("Python", "*.py"), ("Java", "*.java"),
                                             ("All files", "*.*")])
        if self.file == None:
            return
        else:
            if self.nb.index("current") is 0:
                tab = '!frame'
            else:
                tab = f'!frame{self.nb.index("current") + 1}'
            textArea = self.nb.children[tab].children['!text']
            self.file.write(textArea.get("1.0", "end-1c"))
            # v.file_name = v.file.name
            self.file.close()
            self.main_window.title(str(self.file.name) + " -Notepad")
            textArea.edit_modified(arg=False)
            print("Saved As...")

    i = 1
    def resizes(self, event=None):
        print(self.tree.column('#0')['width'])
        # print(paned_win.bbox('all'))
        if self.i == 1:
            self.paned_win.remove(self.left_frame)
            self.i = 0
        else:
            self.paned_win.add(self.left_frame, before=self.right_frame)
            self.i = 1

    def conf(self, event=None):
        # print(self.tree.column('#0'))
        print('draging *conf*')


    nodes = dict()

    def open_directory(self, event=None):
        path = fd.askdirectory()
        if not path:
            return
        self.tree.heading('#0', text=os.path.basename(path))
        # self.path = path
        abspath = os.path.abspath(path=path)
        # print(abspath)
        self.insert_node('', abspath, abspath)
        print(self.nb.focus_get())
        print("break")
        return "break"
    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        # print(node)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))



    def tree_select_event(self, event=None):
        if self.tree.parent(self.tree.selection()):
            parent = self.tree.parent(self.tree.selection())
        else:
            return
        file_path = [self.tree.item(self.tree.selection())['text']]
        file_path.append(self.tree.item(self.tree.parent(self.tree.selection()))['text'])
        while True:
            if self.tree.parent(parent):
                file_path.append(self.tree.item(self.tree.parent(parent))['text'])
                parent = self.tree.parent(parent)
            else:
                break
        file_path.reverse()
        # print(file_path)
        file_path = '\\'.join(file_path)
        # print(file_path)
        # try:
        if not os.path.isdir(file_path):
            self.add_tab(file=file_path)
        else:
            print('directory')
        # except Exception as e:
        #     mb.showerror('Error', e)
        #     print(e)