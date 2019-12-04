# from variables import V
from all_functions import Methods
from variables import Variables


class Events_and_Keys(Methods, Variables):

    def keypress_func(self, event=None):
        self.get_cursor_pos()
        self.get_mini_map_text()
        # self.main_window.update_idletasks()
        # self.search_string()

    def __init__(self):
        # self.main_window.bind('<KeyPress>', self.keypress_func)
        # self.main_window.bind('<KeyRelease>', self.get_mini_map_text)
        self.main_window.bind('<KeyPress>', self.keypress_func)
        # self.main_window.bind('<Configure>', self.get_cursor_pos)
        self.main_window.bind('<Control-n>', self.add_tab)
        self.main_window.bind('<Button-3>', self.popup)

        self.text.bind("<<Change>>", self.line_counter)
        self.text.bind('<Control - =>', self.increase_font)
        self.text.bind('<Control - minus>', self.decrease_font)
        self.main_window.bind('<Configure>', self.line_counter)

        self.text.bind("<Control-Shift-r>", self.font_reset)
        self.text.bind("<ButtonRelease>", self.get_cursor_pos)
        self.main_window.bind("<Control-r>", self.rename)
        self.text.bind("<Control-Shift-R>", self.font_reset)
        # self.main_frame.bind('<Control-s>', self.open_directory)
        self.main_window.bind('<Control-o>', self.open_directory)

        self.tree.bind('<Configure>', self.conf)
        self.text.bind("<<Modified>>", self.modify)


        self.nb.bind('<<NotebookTabChanged>>', self.get_mini_map_text)

        # Auto bracketing
        self.main_window.bind('<(>', self.auto_complete)
        self.main_window.bind('<{>', self.auto_complete)
        self.main_window.bind('<[>', self.auto_complete)
        self.main_window.bind('<">', self.auto_complete)
        self.main_window.bind("<'>", self.auto_complete)

        # self.tree.bind("<Button-1>", self.disableEvent)
        self.tree.bind('<Double-1>', self.tree_select_event)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)

        text = self.text
        text._orig = text._w + "_orig"
        text.tk.call("rename", text._w, text._orig)
        text.tk.createcommand(text._w, self.proxy)

keys = Events_and_Keys()
