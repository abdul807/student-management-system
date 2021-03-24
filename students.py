from tkinter import *
from tkinter import ttk
import datetime
import time
import sqlite3
import tkinter.messagebox




class school_portal():
    db_name='students.db'
    def __init__(self,root):
        self.root=root
        self.root.title('Umar Bin Abdul Aziz Students Data')
        


#..................Logo and title......................

        self.photo=PhotoImage(file='iicons.png')
        self.label=Label(image=self.photo)
        self.label.grid(row=0,column=0)
        self.label1=Label(font=('arial',20,'bold'),text='U.B.A Student Data',fg='green')
        self.label1.grid(row=8,column=0)

#...................adding entries..........
        frame=LabelFrame(self.root,text='Add new record',width=50)
        frame.grid(row=0,column=1)

        Label(frame,text='Firstname:').grid(column=0,row=0,sticky=W)
        self.Firstname=Entry(frame)
        self.Firstname.grid(row=0,column=1)
        self.Firstname.focus()

        
        Label(frame,text='Lastname:').grid(column=0,row=2,sticky=W)
        self.Lastname=Entry(frame)
        self.Lastname.grid(row=2,column=1)
        
        Label(frame,text='Department:').grid(column=0,row=3,sticky=W)
        self.Department=Entry(frame)
        self.Department.grid(row=3,column=1)

        Label(frame,text='gender:').grid(column=0,row=4,sticky=W)
        self.gender=Entry(frame)
        self.gender.grid(row=4,column=1)

        Label(frame,text='stage:').grid(column=0,row=5,sticky=W)
        self.stage=Entry(frame)
        self.stage.grid(row=5,column=1)

        Label(frame,text='status:').grid(column=0,row=6,sticky=W)
        self.status=Entry(frame)
        self.status.grid(row=6,column=1)



        ttk.Button(frame,text='Add Button',command=self.add).grid(row=7,column=1,sticky=W)

        self.message=Label(text='',fg='red')
        self.message.grid(column=1,row=8)

        #.....................DATABASE VIEW............................
        self.Tree=ttk.Treeview(height=10,column=['','','','','',''])
        self.Tree.grid(row=9,column=0,columnspan=2)
        self.Tree.heading('#0',text='ID')
        self.Tree.column('#0',width=50)
        self.Tree.heading('#1',text='Firstname')
        self.Tree.column('#1',width=80)
        self.Tree.heading('#2',text='Lastname')
        self.Tree.column('#2',width=80)
        self.Tree.heading('#3',text='Department')
        self.Tree.column('#3',width=80)
        self.Tree.heading('#4',text='gender')
        self.Tree.column('#4',width=120)
        self.Tree.heading('#5',text='stage')
        self.Tree.column('#5',width=80)
        self.Tree.heading('#6',text='status')
        self.Tree.column('#6',width=40)
        

        #.............Time and Date.................
        def tick():
                today=time.asctime(time.localtime(time.time()))
                #d=datetime.datetime.now()
                #today='{:b %d,%Y}'.format(d)

                mytime=time.strftime('%I:%M:%S:%p')
                self.lblinfo.configure(text=(mytime+'\t'+today))
                self.lblinfo.after(200,tick)



        self.lblinfo=Label(font=('arial',20,'bold'),fg='green')
        self.lblinfo.grid(row=10,column=0,columnspan=2)
        tick()


        #.................Menu bar...........................
        chooser=Menu(tearoff=0)
        itemone=Menu()

        itemone.add_command(label='Add Record',command=self.add)
        itemone.add_command(label='Edit Record',command=self.edit)
        itemone.add_separator()
        itemone.add_command(label='Delete Record',command=self.dele)
        itemone.add_command(label='Help',command=self.help)
        itemone.add_command(label='Exit',command=self.ex)
        
        chooser.add_cascade(label='File',menu=itemone)
        chooser.add_cascade(label='Add',command=self.add)
        chooser.add_cascade(label='Edit',command=self.edit)
        chooser.add_cascade(label='Delete',command=self.dele)
        chooser.add_cascade(label='Help',command=self.help)
        chooser.add_cascade(label='Exit',command=self.ex)

        root.config(menu=chooser)


        self.viewing_records()
        

#.....................view data in tree....................
    def run_query(self,query,parameters=()):
            with sqlite3.connect(self.db_name) as conn:
                    cursor=conn.cursor()
                    query_results=cursor.execute(query,parameters)
                    conn.commit()
            return query_results

    def viewing_records(self):
            records=self.Tree.get_children()
            for element in records:
                    self.Tree.delete(element)
            query='SELECT * FROM student_list'
            db_table=self.run_query(query)
            for data in db_table:
                    self.Tree.insert('',1000,text=data[0],values=data[1:])


    def validation(self):
            return len(self.Firstname.get())!=0 and \
            len(self.Lastname.get())!=0 and \
            len(self.Department.get())!=0 and \
            len(self.gender.get())!=0 and len(self.stage.get())!=0 and len(self.status.get())!=0

    def add_record(self):
            if self.validation():
                    query='INSERT INTO student_list VALUES(NULL,?,?,?,?,?,?)'
                    parameters=(self.Firstname.get(),
                    self.Lastname.get(),self.Department.get(),
                    self.gender.get(),self.stage.get(),self.status.get())
                    self.run_query(query,parameters)
                    self.message['text']='Record {} {} is added'.format(self.Firstname.get(),self.Lastname.get())


                    #.................clearing  the entries...................
                    self.Firstname.delete(0,END)
                    self.Lastname.delete(0,END)
                    self.Department.delete(0,END)
                    self.gender.delete(0,END)
                    self.stage.delete(0,END)
                    self.status.delete(0,END)
            else:
                    self.message['text'] = 'All entries must be filled'

            self.viewing_records()
    def add(self):

            ad=tkinter.messagebox.askquestion('Add Record','Do you want to add record?')
            if ad == 'yes':
                    self.add_record()

    
    def delete_record(self):
            self.message['text']=' '
            try:
                    self.Tree.item(self.Tree.selection())['values'][1]
            except:
                    self.message['text']='please select a record to delete'
                    return
            
            self.message['text']=' '
            number=self.Tree.item(self.Tree.selection())['text']
            query='DELETE FROM student_list WHERE ID =?'
            self.run_query(query,(number,))
            self.message['text']=f'Record {number} is deleted'
            self.viewing_records()


    def dele(self):
            de=tkinter.messagebox.askquestion('Delete Record','Do you really want to delete this record?')
            if de=='yes':
                    self.delete_record()



    #..........................editing record........................

    def edit_box(self):
            self.message['text']=''
            try:
                    self.Tree.item(self.Tree.selection())['values'][0]
            except:
                    self.message['text']='please select an item to edit'
                    return

            fname=self.Tree.item(self.Tree.selection())['values'][0]
            lname=self.Tree.item(self.Tree.selection())['values'][1]
            username=self.Tree.item(self.Tree.selection())['values'][2]
            gender=self.Tree.item(self.Tree.selection())['values'][3]
            stage=self.Tree.item(self.Tree.selection())['values'][4]
            status=self.Tree.item(self.Tree.selection())['values'][5]


            self.edit_root=Toplevel()
            self.edit_root.title('edit record')

            Label(self.edit_root,text='old firstname').grid(row=0,column=1,sticky=W)
            Entry(self.edit_root,textvariable=StringVar(self.edit_root,value=fname),state='readonly').grid(row=0,column=2,sticky=W)
            Label(self.edit_root,text='new firstname').grid(row=1,column=1,sticky=W)
            new_fname=Entry(self.edit_root)
            new_fname.grid(row=1,column=2)
            new_fname.focus()

            
            Label(self.edit_root,text='old lastname').grid(row=2,column=1,sticky=W)
            Entry(self.edit_root,textvariable=StringVar(self.edit_root,value=lname),state='readonly').grid(row=2,column=2,sticky=W)
            Label(self.edit_root,text='new lastname').grid(row=3,column=1,sticky=W)
            new_lname=Entry(self.edit_root)
            new_lname.grid(row=3,column=2) 


            
            Label(self.edit_root,text='old Department').grid(row=4,column=1,sticky=W)
            Entry(self.edit_root,textvariable=StringVar(self.edit_root,value=Department),state='readonly').grid(row=4,column=2,sticky=W)
            Label(self.edit_root,text='new Department').grid(row=5,column=1,sticky=W)
            new_Department=Entry(self.edit_root)
            new_Department.grid(row=5,column=2)    

            
            Label(self.edit_root,text='old gender').grid(row=6,column=1,sticky=W)
            Entry(self.edit_root,textvariable=StringVar(self.edit_root,value=gender),state='readonly').grid(row=6,column=2,sticky=W)
            Label(self.edit_root,text='new gender').grid(row=7,column=1,sticky=W)
            new_gender=Entry(self.edit_root)
            new_gender.grid(row=7,column=2) 


            Label(self.edit_root,text='old stage').grid(row=8,column=1,sticky=W)
            Entry(self.edit_root,textvariable=StringVar(self.edit_root,value=stage),state='readonly').grid(row=8,column=2,sticky=W)
            Label(self.edit_root,text='new stage').grid(row=9,column=1,sticky=W)
            new_stage=Entry(self.edit_root)
            new_stage.grid(row=9,column=2)

            Label(self.edit_root,text='old status').grid(row=10,column=1,sticky=W)
            Entry(self.edit_root,textvariable=StringVar(self.edit_root,value=status),state='readonly').grid(row=10,column=2,sticky=W)
            Label(self.edit_root,text='new status').grid(row=11,column=1,sticky=W)
            new_status=Entry(self.edit_root)
            new_status.grid(row=11,column=2)


            Button(self.edit_root,text='save new record',command=lambda : self.edit_record(new_fname.get(),fname,
            new_lname.get(),lname,new_Department.get(),Department,
            new_gender.get(),gender,new_stage.get(),stage,new_status.get(),status)).grid(row=12,column=2)


            self.edit_root.mainloop()
    def edit_record(self,new_fname,fname,new_lname,lname,new_Department,Department,new_gender,gender,new_stage,stage,new_status,status):
            query='UPDATE student_list SET fname=?,lname=?,Department=?,gender=?, stage=?,status=? WHERE fname=? AND lname=? AND Department=? AND gender=? AND stage=? AND status=? '
            parameters=(new_fname,new_lname,new_Department,new_gender,new_stage,new_age,fname,lname,Department,gender,stage,status)
            self.run_query(query,parameters)
            self.edit_root.destroy()
            self.message['text']=f'{fname} was changed to {new_fname}'
            self.viewing_records()

    def edit(self):
            ed=tkinter.messagebox.askquestion('edit record','do you want to edit record?')
            if ed=='yes':
                    self.edit_box()


    def help(self):
            tkinter.messagebox.showinfo('Log','Report sent')

    def ex(self):
            exi=tkinter.messagebox.askquestion('Exit Application','Do you want to exit application')
            if exi =='yes':
                    root.destroy()







                


                    
                    
                




if __name__ == '__main__':
    root=Tk()
    root.geometry('530x465+500+200')
    application = school_portal(root)
    root.mainloop()