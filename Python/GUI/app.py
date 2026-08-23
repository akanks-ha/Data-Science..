from tkinter import *
from mydb import Database
from tkinter import messagebox
from myapi import API

class NLPApp:
    
    def __init__(self):

        # create database object
        self.dbo = Database()
        self.apio = API()
        
        # login ka gui load krna
        self.root = Tk()
        self.root.title("NLP App")
        self.root.iconbitmap('resources/favicon.ico')
        self.root.geometry('350x600')
        self.root.configure(bg='#34495E')



        self.login_gui()

        self.root.mainloop()

    def login_gui(self):
        self.clear()

        heading = Label(self.root,text = 'NLPApp',bg='#34495E',fg ='white')
        heading.pack(pady=(30,30)) # use for gap between upper and lower
        heading.configure(font=('verdana',24,'bold'))

        label1 = Label(self.root,text ='Enter Email')
        label1.pack(pady=(10,10))

        self.email_input = Entry(self.root,width = 30)
        self.email_input.pack(pady=(5,10),ipady=10) # ipad for height increase


        label2 = Label(self.root,text ='Enter Password')
        label2.pack(pady=(10,10))

        self.password_input = Entry(self.root,width = 30,show ='*')
        self.password_input.pack(pady=(5,10),ipady=9)

        login_btn=Button(self.root,text = 'Login',width=30,height = 2,command=self.perform_login)
        login_btn.pack(pady=(10,10))

        label3 = Label(self.root,text ='Not a member?')
        label3.pack(pady =(20,10))

        redirect_btn=Button(self.root,text = 'Register Now',command=self.register_gui) # using command click on register command will go register now button
        redirect_btn.pack(pady=(10,10))

    def register_gui(self):
        # print('register wala function')
        self.clear()

        heading = Label(self.root,text = 'NLPApp',bg='#34495E',fg ='white')
        heading.pack(pady=(30,30)) # use for gap between upper and lower
        heading.configure(font=('verdana',24,'bold'))

        label0 = Label(self.root,text ='Enter Name')
        label0.pack(pady=(10,10))

        self.name_input = Entry(self.root,width = 30)
        self.name_input.pack(pady=(5,10),ipady=10) # ipad for height increase

        label1 = Label(self.root,text ='Enter Email')
        label1.pack(pady=(10,10))

        self.email_input = Entry(self.root,width = 30)
        self.email_input.pack(pady=(5,10),ipady=10) # ipad for height increase

        label2 = Label(self.root,text ='Enter Password')
        label2.pack(pady=(10,10))

        self.password_input = Entry(self.root,width = 30,show ='*')
        self.password_input.pack(pady=(5,10),ipady=9)

        register_btn=Button(self.root,text = 'Register',width=30,height = 2,command = self.perform_registration)
        register_btn.pack(pady=(10,10))

        label3 = Label(self.root,text ='Already a member?')
        label3.pack(pady =(20,10))

        redirect_btn=Button(self.root,text = 'Login Now',command=self.login_gui) # using command click on register command will go register now button
        redirect_btn.pack(pady=(10,10))


    def clear(self):
        # clear the existing gui
        for i in self.root.pack_slaves():
            # print(i) # will show all label
            i.destroy() # clear all gui

    def perform_registration(self):
        # fetch data from the gui
        name = self.name_input.get()
        email = self.email_input.get()
        password = self.password_input.get()
        print(name)

        response = self.dbo.add_data(name,email,password)

        if response:
            # print('registration successful')
            messagebox.showinfo('Success', 'Registration Successful.You can login now')
        else:
            # print('email already exists')
            messagebox.showinfo('Success', 'Registration Failed.You can login now')

    def perform_login(self):

        email = self.email_input.get()
        password = self.password_input.get()

        response = self.dbo.search(email,password)

        if response :
            messagebox.showinfo('Success', 'Login Successful.')
            self.home_gui()
        else:
            messagebox.showerror('error', 'Incorrect email/password.')


    def home_gui(self):

        self.clear()

        heading = Label(self.root,text = 'NLPApp',bg='#34495E',fg ='white')
        heading.pack(pady=(30,30)) # use for gap between upper and lower
        heading.configure(font=('verdana',24,'bold'))

        sentiment_btn=Button(self.root,text = 'Sentiment Analysis',width=30,height = 2,command=self.sentiment_gui)
        sentiment_btn.pack(pady=(10,10))

        ner_btn=Button(self.root,text = 'Named Entity Recognition',width=30,height = 2,command=self.perform_registration)
        ner_btn.pack(pady=(10,10))

        emotion_btn=Button(self.root,text = 'Emotion Prediction',width=30,height = 2,command=self.perform_registration)
        emotion_btn.pack(pady=(10,10))

        logout_btn = Button(self.root, text='Logout', command=self.login_gui)  # using command click on register command will go register now button
        logout_btn.pack(pady=(10, 10))

    def sentiment_gui(self):

        self.clear()

        heading = Label(self.root,text = 'NLPApp',bg='#34495E',fg ='white')
        heading.pack(pady=(30,30)) # use for gap between upper and lower
        heading.configure(font=('verdana',24,'bold'))

        heading2 = Label(self.root,text = 'Sentiment Analysis',bg='#34495E',fg ='white')
        heading2.pack(pady=(30,30)) # use for gap between upper and lower
        heading2.configure(font=('verdana',20))

        self.label1 = Label(self.root,text ='Enter the text')
        self.label1.pack(pady=(10,10))

        self.sentiment_input = Entry(self.root, width=30)
        self.sentiment_input.pack(pady=(5, 10), ipady=10)

        sentiment_btn=Button(self.root,text = 'Analyze sentiment',command=self.do_sentiment_analysis) # using command click on register command will go register now button
        sentiment_btn.pack(pady=(10,10))

        self.sentiment_result = Label(self.root,text ='',bg ='#34495E',fg ='white')
        self.sentiment_result.pack(pady=(10,10))
        self.sentiment_result.configure(font=('verdana',16))

        goback_btn=Button(self.root,text = 'Go back',command=self.home_gui) # using command click on register command will go register now button
        goback_btn.pack(pady=(10,10))

    def do_sentiment_analysis(self):

        text = self.sentiment_input.get()
        result = self.apio.sentiment_analysisis(text)

        print(result)






nlp = NLPApp()