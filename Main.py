#!/usr/bin/env python
# coding: utf-8

# In[38]:


import tkinter
from tkinter import *

import Face_Detection


# In[ ]:





# In[1]:


# Initialize main window
root = tkinter.Tk()

# Setup window 
root.title("Register")



# # Add Scroll Window
# scrollbar = tkinter.Scrollbar(main_frame, orient="vertical", command=main_frame.yview)
# scrollbar.grid(row=0, column=2)

# main_frame.configure(yscrollcommand=scrollbar.set)


# In[39]:


# Create table
Label(root, text="Full Name", borderwidth=4, padx=10, pady=10, font="Helvetica 10", relief="solid").grid(row=0, column=0)
Label(root, text="Present",borderwidth=4, padx=10, pady=10, font="Helvetica 10", relief="solid").grid(row=0, column=1)

# Get register
register = Face_Detection.get_register()

# Get number of students
NUM_STUDENTS = Face_Detection.get_num_students()

# Add register to table
for i in range(0, NUM_STUDENTS):
    Label(root, text = register[0][i], padx=20, pady=20, font="Helvetica 10").grid(row =i+1, column=0)
    Label(root, text = str(register[1][i]), padx=20, pady=20, font="Helvetica 10").grid(row =i+1, column=1)


# In[30]:


# Run the window
root.mainloop()


# In[ ]:





# In[ ]:




