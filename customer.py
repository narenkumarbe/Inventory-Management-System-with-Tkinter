from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class customerClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Customer Details")
        self.root.config(bg="white")
        self.root.focus_force()

        #========Variables============
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_cust_id = StringVar()
        self.var_name = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        # self.var_address = StringVar()

        #===============Search Customer Frame=========
        SearchFrame = LabelFrame(self.root,text="Search Customer",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #==============Customer Search Options============
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Email","Name","Contact"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)
        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #============title========
        title=Label(self.root,text="Customer Details",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        #===========Customer data entry form=============
        #===========Row 1========================
        lbl_custid=Label(self.root,text="Cust No",font=("goudy old style",15),bg="white").place(x=50,y=150)
        lbl_gender=Label(self.root,text="Gender",font=("goudy old style",15),bg="white").place(x=350,y=150)        
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=750,y=150)

        txt_custid=Entry(self.root,textvariable=self.var_cust_id,font=("goudy old style",15),bg="lightyellow").place(x=150,y=150,width=180)        
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("Select","Male","Female","Other"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=850,y=150,width=180)
        #==============Row2==============================
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=190)
        lbl_email=Label(self.root,text="Email",font=("goudy old style",15),bg="white").place(x=350,y=190)        
        lbl_address=Label(self.root,text="Address",font=("goudy old style",15),bg="white").place(x=750,y=190)

        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=190,width=180)        
        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",15),bg="lightyellow").place(x=500,y=190,width=180)      
        self.txt_address=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_address.place(x=850,y=190,width=200,height=60)
        #===============Buttons======================
        btn_save=Button(self.root,text="Save",command=self.add,font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=265,width=110,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=265,width=110,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15,"bold"),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=265,width=110,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15,"bold"),bg="#607d8b",fg="white",cursor="hand2").place(x=860,y=265,width=110,height=28)

        #==========Customer details in tree view==========
        cust_frame=Frame(self.root,bd=3,relief=RIDGE)
        cust_frame.place(x=0,y=310,relwidth=1,height=190)

        scrolly = Scrollbar(cust_frame,orient=VERTICAL)
        scrollx = Scrollbar(cust_frame,orient=HORIZONTAL)

        self.CustomerTable=ttk.Treeview(cust_frame,columns=("custid","name","gender","contact","email","address"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CustomerTable.xview)
        scrolly.config(command=self.CustomerTable.yview)
        
        self.CustomerTable.heading("custid",text="Cust No")
        self.CustomerTable.heading("name",text="Name")
        self.CustomerTable.heading("gender",text="Gender")
        self.CustomerTable.heading("contact",text="Contact No")
        self.CustomerTable.heading("email",text="Email ID")
        self.CustomerTable.heading("address",text="Address")
        self.CustomerTable["show"] = "headings"

        self.CustomerTable.column("custid",width=90)
        self.CustomerTable.column("name",width=100)
        self.CustomerTable.column("gender",width=100)
        self.CustomerTable.column("contact",width=100)
        self.CustomerTable.column("email",width=100)
        self.CustomerTable.column("address",width=100)        
        self.CustomerTable.pack(fill=BOTH,expand=1)
        self.CustomerTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

    #===============Defining Function==========
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cust_id.get()=="":
                messagebox.showerror("Error","Customer number Must be required",parent=self.root)
            else:
                cur.execute("Select * from customer where custid=?",(self.var_cust_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Customer No already assigned, try different",parent=self.root)
                else:
                    cur.execute("Insert into customer (custid,name,gender,contact,email,address) values(?,?,?,?,?,?)",(
                        self.var_cust_id.get(),
                        self.var_name.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_email.get(),
                        self.txt_address.get(1.0,END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Customer Added Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from customer")
            rows=cur.fetchall()
            self.CustomerTable.delete(*self.CustomerTable.get_children())
            for row in rows:
                self.CustomerTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.CustomerTable.focus()
        content=(self.CustomerTable.item(f))
        row=content['values']
        # print(row)  
        self.var_cust_id.set(row[0]),
        self.var_name.set(row[1]),
        self.var_gender.set(row[2]),
        self.var_contact.set(row[3]),
        self.var_email.set(row[4]),
        self.txt_address.delete(1.0,END)
        self.txt_address.insert(END,row[5])

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cust_id.get()=="":
                messagebox.showerror("Error","Customer number Must be required",parent=self.root)
            else:
                cur.execute("Select * from customer where custid=?",(self.var_cust_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Customer Number",parent=self.root)
                else:
                    cur.execute("Update customer set name=?,gender=?,contact=?,email=?,address=? where custid=?",(
                        
                        self.var_name.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_email.get(),
                        self.txt_address.get(1.0,END),
                        self.var_cust_id.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Customer Updated Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cust_id.get()=="":
                messagebox.showerror("Error","Customer number Must be required",parent=self.root)
            else:
                cur.execute("Select * from customer where custid=?",(self.var_cust_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Customer Number",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("Delete from customer where custid=?",(self.var_cust_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Customer Deleted Successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        self.var_cust_id.set(""),
        self.var_name.set(""),
        self.var_gender.set("Select"),
        self.var_contact.set(""),
        self.var_email.set(""),
        self.txt_address.delete(1.0,END)
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()
    
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search by Option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("Select * from customer where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.CustomerTable.delete(*self.CustomerTable.get_children())
                    for row in rows:
                        self.CustomerTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


if __name__=="__main__":
    root=Tk()
    obj=customerClass(root)
    root.mainloop()