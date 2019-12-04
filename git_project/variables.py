from tkinter import *
# import formatting
from tkinter import ttk as ttk
import tkinter.font as tkFont
from custom_notebook import CustomNotebook
# abc = ttk.Treeview()


class Variables:
    '''
    Container for all required variables which will use across multiple files.
    '''

    # Skeleton of the Application
    # Not back
    main_window = Tk()

    toolbar_frame = Frame(main_window, height=0)

    paned_win = PanedWindow(main_window, relief='flat', borderwidth=0, bd=0, bg='black')
    left_frame = Frame(paned_win, bd=0)
    right_frame = Frame(paned_win, bd=0)

    paned_win.add(left_frame, stretch='always', width=150)
    paned_win.add(right_frame, stretch='always')
    # For removing the border from treeview
    style = ttk.Style()
    style.layout("Treeview", [('Treeview.treearea', {'border': 0})])
    style.configure("Treeview", background='gray', fieldbackground='gray', foreground='white')


    tree = ttk.Treeview(left_frame)
    tree.heading('#0', text='Open Project', anchor='w')
    ysb = Scrollbar(left_frame, orient='vertical', command=tree.yview, width=13)
    xsb = Scrollbar(left_frame, orient='horizontal', command=tree.xview, width=13)
    tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    tree.heading('#0', text='Project tree', anchor='w')
    tree.column('#0', minwidth=300, width=300, stretch=True)
    ysb.pack(side='right', fill='y')
    xsb.pack(side='bottom', fill='x')
    tree.pack(fill='both', expand=1)


    # -------------------------------------------------
    main_frame = Frame(right_frame, width=0)
    line_num_frame = Frame(main_frame, width=0)
    working_area = Frame(main_frame, width=0)
    code_minimap_frame = Frame(main_frame)
    line_num_frame.pack(fill='y', side='left')
    working_area.pack(fill='both', side='left', expand=True)
    code_minimap_frame.pack(fill='both', side='left', pady=(22, 0))
    # --------------------------------------------------------

    on_off_project_hierarchy = Frame(main_window, highlightbackground='gray', highlightthickness=1)
    # on_off_project_hierarchy.pack(fill)
    statusbar_frame = Frame(main_window, bg='gray', height=0)

    # ------------------Code Minimap Configuration-------------------
    mini_map_text = Text(code_minimap_frame, width=70, state='disabled',
                         cursor='arrow', font=("Consolas", 2), wrap="none", bd=0)
    y_scrollbar = Scrollbar(code_minimap_frame, orient="vertical")
    mini_map_text.config(yscrollcommand=y_scrollbar.set)
    y_scrollbar.pack(side='right', fill='y')
    mini_map_text.pack(fill='y', expand=1)
    mini_map_text.bindtags((str(mini_map_text), str(code_minimap_frame), "all"))
    # -----------------------------End-------------------------------



    # widgets of the Application

    cursor_pos = Label(statusbar_frame, bg='gray', fg='black', text='Ln: 1, Col: 1')
    cursor_pos.pack(fill='x', side='right', padx=(0, 155))

    file_type = Label(statusbar_frame, bg='gray', fg='black', text='Plain Text')
    file_type.pack(fill='x', side='right', padx=(0, 100))



    # New Skeleton

    # nb = ttk.Notebook(working_area, width=0)
    nb = CustomNotebook(working_area)
    nb.pack(fill='both', expand=True)
    canvas = Canvas(line_num_frame, bd=0, highlightthickness=0)
    canvas.pack(fill='both', side='left', pady=(28, 0))
    # Tab
    tab1 = Frame(nb)
    tab1.pack()

    font_style = "Consolas"
    font_size = 12
    customFont = tkFont.Font(family=font_style, size=font_size)
    tab_width = customFont.measure(' ')
    mini_map_text.config(tabs=tab_width)

    text = Text(tab1, font=customFont, wrap='none', width=0, undo=True, padx=1)

    # Horizontal Scrollbar on text area
    y_scrollbar2 = Scrollbar(tab1, orient='vertical',
                            width=13, relief='flat')
    text.config(yscrollcommand=y_scrollbar2.set)
    y_scrollbar2.config(command=text.yview)
    y_scrollbar2.pack(side='right', fill='y')

    # Vertical Scrollbar on text area
    x_scrollbar = Scrollbar(tab1, orient='horizontal', width=13)
    text.config(xscrollcommand=x_scrollbar.set)
    x_scrollbar.config(command=text.xview)
    x_scrollbar.pack(side='bottom', fill='x')


    text.pack(fill='both', expand=1)
    nb.add(tab1, text='Untitled -1')
    # Rename the tab
    # nb.tab(tab1, text='hello')
    text.focus_force()

    # Menu bar configuration
    main_menu = Menu(main_window, background='#212121', foreground='white')
    main_window.config(menu=main_menu)
    File = Menu(main_menu, tearoff=0, bd=0, borderwidth=0)
    Edit = Menu(main_menu, tearoff=0)
    Toolbars = Menu(main_menu, tearoff=0)
    Format = Menu(main_menu, tearoff=0)
    View = Menu(main_menu, tearoff=0)
    Help = Menu(main_menu, tearoff=0)
    # text.peer_create()

    # Right click popup menu
    popup_menu = Menu(nb, tearoff=0)

    file = None
