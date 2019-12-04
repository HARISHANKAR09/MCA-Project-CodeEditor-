from tkinter import *
from variables import Variables as v
from all_functions import Methods
m = Methods()


close_button = Button(v.toolbar_frame, text='x', font=(None, 10), bd=0, bg=v.toolbar_frame.cget('bg'), fg='white',
                      command=m.show_toolbar)
close_button.pack(side=RIGHT, padx=0)

new_file_icon = PhotoImage(file='images/new_file_icon2.png')
new_file_button = Button(v.toolbar_frame, image=new_file_icon, bg=v.toolbar_frame.cget('bg'), bd=0, command=m.add_tab)
new_file_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)
new_file_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)

open_file_icon = PhotoImage(file='images/open_file_icon2.png')
open_file_button = Button(v.toolbar_frame, bg=v.toolbar_frame.cget('bg'), image=open_file_icon, bd=0)
open_file_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)

save_icon = PhotoImage(file='images/save_file_icon2.png')
save_button = Button(v.toolbar_frame, bg=v.toolbar_frame.cget('bg'), image=save_icon, bd=0)
save_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)

cut_icon = PhotoImage(file='images/cut_icon.png')
cut_button = Button(v.toolbar_frame, bg=v.toolbar_frame.cget('bg'), image=cut_icon, bd=0)
cut_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)

paste_icon = PhotoImage(file='images/paste_icon.png')
paste_button = Button(v.toolbar_frame, bg=v.toolbar_frame.cget('bg'), image=paste_icon, bd=0)
paste_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)

copy_icon = PhotoImage(file='images/copy_icon.png')

copy_button = Button(v.toolbar_frame, bg=v.toolbar_frame.cget('bg'), image=copy_icon, bd=0)
copy_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)

undo_icon = PhotoImage(file='images/undo_icon.png')
undo_button = Button(v.toolbar_frame, bg=v.toolbar_frame.cget('bg'), image=undo_icon, bd=0)
undo_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)

redo_icon = PhotoImage(file='images/redo_icon.png')
redo_button = Button(v.toolbar_frame, bg=v.toolbar_frame.cget('bg'), image=redo_icon, bd=0)
redo_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)

select_all_icon = PhotoImage(file='images/select_all_icon.png')
select_all_button = Button(v.toolbar_frame, bg=v.toolbar_frame.cget('bg'), image=select_all_icon, bd=0)
select_all_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)

search_icon = PhotoImage(file='images/search_icon.png')
search_button = Button(v.toolbar_frame, bg=v.toolbar_frame.cget('bg'), image=search_icon, bd=0)
search_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)

replace_icon = PhotoImage(file='images/replace_icon2.png')
replace_button = Button(v.toolbar_frame, bg=v.toolbar_frame.cget('bg'), image=replace_icon, bd=0)
replace_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)
font_decrease_icon = PhotoImage(file='images/font_decrease.png')
font_decrease_button = Button(v.toolbar_frame, bg=v.toolbar_frame.cget('bg'), image=font_decrease_icon, bd=0)
font_decrease_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)

font_increase_icon = PhotoImage(file='images/font_increase.png')
font_increase_button = Button(v.toolbar_frame, bg=v.toolbar_frame.cget('bg'), image=font_increase_icon, bd=0)
font_increase_button.pack(side=LEFT, padx=2, ipadx=3, ipady=3)

popup = Menu(v.main_menu, tearoff=0)
popup.add_command(label='new file')

def enter(event):
    event.widget.config(bg='#c7cbd1')
    popup.post(event.x_root, event.y_root)

def leave(event):
    event.widget.config(bg=v.toolbar_frame.cget('bg'))
    popup.unpost()

# v.toolbar_frame.bind_class(Button, '<Enter>', enter)
# new_file_button.bind('<Leave>', leave)
new_file_button.bind('<Enter>', enter)
new_file_button.bind('<Leave>', leave)
open_file_button.bind('<Enter>', enter)
open_file_button.bind('<Leave>', leave)


# v.main_window.bind('<Control-s>', m.show_toolbar)



# toolbar = Toolbars()
