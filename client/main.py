import tkinter as tk
from tkinter import ttk
import webbrowser
import secrets
import sys
sys.path.append('../MarkUpProject')

from backend.register_charity import sql_GET

def open_search(remove):
    window.withdraw()
    if remove == 1:
        charity_page.withdraw()
    global search_page
    search_page = tk.Toplevel()
    search_page.title('Search Page')
    search_page.geometry('320x568')

    search_table = ttk.Label(master=search_page, text='Search', font='Calibri 24 bold')
    search_table.pack()

    search_field = ttk.Frame(master=search_page)
    entry_string = tk.StringVar()
    entry = ttk.Entry(master=search_field, textvariable=entry_string)
    button = ttk.Button(master=search_field, text='Go', command=lambda: handle_search(entry_string, search_page, search_page.listbox))
    entry.pack(side='left')
    button.pack(side='left')
    search_field.pack()

    search_page.listbox = tk.Listbox(master=search_page, width=30)
    search_page.listbox.insert(tk.END, charities[0][0])
    search_page.listbox.insert(tk.END, charities[1][0])
    search_page.listbox.insert(tk.END, charities[2][0])
    search_page.listbox.insert(tk.END, charities[3][0])
    search_page.listbox.insert(tk.END, charities[4][0])
    search_page.listbox.pack(pady=10)

    search_page.listbox.bind("<<ListboxSelect>>", handle_view)

def handle_search(entry_string, search_page, listbox):
    listbox.delete(0, tk.END)
    matching_charities = []
    for charity in charities:
        if str(entry_string.get()).lower() in str(charity[3]).lower():
            listbox.insert(tk.END, charity[0])

def handle_view(event):
    selected_item = event.widget.curselection()
    if selected_item:
        item = event.widget.get(selected_item)
        for charity in charities:
            if item == str(charity[0]):
                show_charity_page(charity)

def show_charity_page(charity):
    global charity_page
    search_page.withdraw()
    charity_page = tk.Toplevel()
    charity_page.title('Charity Page')
    charity_page.geometry('320x568')

    charity_title = ttk.Label(master=charity_page, text=str(charity[0]), font='Calibri 24 bold')
    charity_description = ttk.Label(master=charity_page, text=str(charity[1]), font='Calibri 10')
    charity_title.pack()
    charity_description.pack()

    label = tk.Label(charity_page, text="Click here for more information", fg="blue", cursor="hand2")
    label.pack()

    label.bind("<Button-1>", lambda event: open_link(charity[2]))

    button = ttk.Button(master=charity_page, text='Find A Cause', command=lambda:open_search(1))
    button.pack()

def open_link(link):
    webbrowser.open(str(link))


charities = sql_GET()

window = tk.Tk()
window.title('Main Page')
window.geometry('320x568')

title_label = ttk.Label(master=window, text='Welcome!', font='Calibri 24 bold')
title_label.pack()

image = tk.PhotoImage(file='client/images/foto.png')
image_label = ttk.Label(window, image=image)
image_label.pack()

button = ttk.Button(master=window, text='Find A Cause', command=lambda: open_search(0))
button.pack()


window.mainloop()
