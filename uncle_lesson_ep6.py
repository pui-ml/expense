from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import sys

GUI = Tk()
GUI.title("Expense Tracker")
GUI.geometry("500x500+200+100")

########### menu bar ###############
menu_bar = Menu(GUI)
GUI.config(menu=menu_bar)

# file menu
file_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Import CSV')
file_menu.add_command(label='Export CSV')


def About():
    messagebox.showinfo('About', 'สวัสดี โปรแกรมนี้ทำงานดีมาก\nสนใจบริจาคได้')


# help menu
help_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='About', command=About)

# Donate menu
donate_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='Donate', menu=donate_menu)

# Tab ------------------------------
Tab = ttk.Notebook(GUI)

T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

expenseicon = PhotoImage(file="wallet-icon.png").subsample(2)
listicon = PhotoImage(file="folder-flower-orange-icon.png").subsample(2)

Tab.add(T1, text=f'{"Add Expense":^50}', image=expenseicon, compound="top")
Tab.add(T2, text=f'{"Expense List":^50s}', image=listicon, compound="top")

# ----------- define frame ----------
F1 = Frame(T1)
# F1.place(x=100,y=20)
F1.pack()

days = {
    "Mon": "จันทร์",
    "Tue": "อังคาร",
    "Wed": "พุธ",
    "Thu": "พฤหัส",
    "Fri": "ศุกร์",
    "Sat": "เสาร์",
    "Sun": "อาทิตย์",
}


# -------- define font ---------------
FONT1 = (None, 20)
FONT2 = (None, 10)

# Logo -----------------------------
centerimg = PhotoImage(file="cash-icon.png")
logo = ttk.Label(F1, image=centerimg)
logo.pack()


def new_form():
    v_expense.set("")
    v_price.set("")
    v_amount.set("")
    E1.focus()


# ------------ save to file ------------
def Save(event=None):
    try:
        expense = v_expense.get()
        if expense == "":
            raise ValueError("")
        price = float(v_price.get())
        if price <= 0:
            raise ValueError("")
        amount = float(v_amount.get())
        if amount <= 0:
            raise ValueError("")

        total = amount * price
        today = datetime.now().strftime("%a")
        this_time = datetime.now().strftime(f"%Y-%m-%d {days[today]} %H:%M:%S")

        text = f"รายการ: {expense} - ราคา: {price:.2f} บาท - จำนวน: {amount:.1f} ชิ้น - รวม: {total:.2f} บาท\n- เวลาทำรายการ {this_time}"
        v_result.set(text)

        # print(f'รายการ: {expense} - ราคา: {price:.2f} - จำนวน: {amount:.1f} - รวม: {total:.2f} - เวลาทำรายการ {this_time}')
        new_form()

        with open("savedata.csv", "a", encoding="utf-8", newline="") as f:
            fw = csv.writer(f)
            data = [expense, price, amount, total, this_time]
            fw.writerow(data)
    except Exception as e:
        # messagebox.showerror('Error',e)
        # messagebox.showwarning('Error','Please enter new data')
        messagebox.showinfo("Error", "  Please enter data  ")
        new_form()

    update_table()


def terminate():
    sys.exit(1)


GUI.bind("<Return>", Save)

# -------------- text1 start--------------
v_expense = StringVar()
L1 = ttk.Label(F1, text="รายการค่าใช้จ่าย", font=FONT2).pack()
E1 = ttk.Entry(F1, textvariable=v_expense, font=FONT2)
E1.pack()
# -------------- text1 end--------------

# -------------- text2 start--------------
v_price = StringVar()
L2 = ttk.Label(F1, text="ราคา (บาท)", font=FONT2).pack()
E2 = ttk.Entry(F1, textvariable=v_price, font=FONT2)
E2.pack()
# -------------- text2 end--------------

# -------------- text3 start--------------
v_amount = StringVar()
L3 = ttk.Label(F1, text="จำนวน (ชิ้น)", font=FONT2).pack()
E3 = ttk.Entry(F1, textvariable=v_amount, font=FONT2)
E3.pack()
# -------------- text3 end--------------

saveicon = PhotoImage(file="wallet-icon.png").subsample(2)
B1 = ttk.Button(
    F1, text="บันทึก", command=Save, image=saveicon, compound="left", width=12
)
B1.pack(ipadx=20, ipady=8, pady=8)


B2 = ttk.Button(F1, text="ล้างข้อมูล", command=new_form, width=18)
B2.pack(ipadx=20, ipady=8, pady=4)

B3 = ttk.Button(F1, text="จบโปรแกรม", command=terminate, width=18)
B3.pack(ipadx=20, ipady=8, pady=4)

v_result = StringVar()
result = ttk.Label(F1, textvariable=v_result, font=FONT2, foreground="green")
result.pack(pady=10)

# tab 2 -------- read_csv


def read_csv():
    with open("savedata.csv", newline="", encoding="utf-8") as f:
        fr = csv.reader(f)
        data = list(fr)
    return data


# table ---
L = ttk.Label(T2, text='ตารางผลลัพธ์', font=FONT1).pack(pady=20)

header = ["รายการ", "ค่าใช้จ่าย", "จำนวน", "รวม", "วัน-เวลา"]
header_width = [120, 80, 80, 100, 120]

result_table = ttk.Treeview(T2, columns=header, show="headings", height=10)
result_table.pack(pady=20)

for head, h_width in zip(header, header_width):
    result_table.heading(head, text=head)
    result_table.column(head, width=h_width)

# result_table.insert('', 'end', value=['วันจันทร์', 30, 40, 50, 60])
# result_table.insert('', 'end', value=header)


def update_table():
    result_table.delete(*result_table.get_children())  # delete ก่อน update
    data = read_csv()
    for d in data:
        result_table.insert('', 0, value=d)


update_table()

GUI.bind("<Tab>", lambda x: E2.focus())

GUI.mainloop()
