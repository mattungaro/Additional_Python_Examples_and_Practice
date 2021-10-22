#!/usr/bin/env python
# coding: utf-8

# In[12]:


t = "Hello Man"


# In[13]:


t


# In[14]:


get_ipython().run_line_magic('whos', '# tells you what variables are present')


# In[19]:


# %debug allows you to enter the debugger at the point where
# the exception was thrown.


# In[20]:


# 1.2.2 Basic Types 
# integer, floats (1.332), complex (like imaginary numbers?),
# booleans(3 > 4)


# In[23]:


3 >4


# In[25]:


colors = ['red', 'blue', 'green', 'black', 'white']
colors.append('pink')
colors

colors.pop() # removes and returns the last item

colors

colors.extend(['pink', 'purple']) # extend colors, in-place
colors


# In[26]:


colors = colors[:-2]


# In[27]:


colors


# In[28]:


colors.reverse() # this is an example of OOP - object oriented
# programming


# In[39]:


co_co = colors.count


# In[40]:


co_co


# In[46]:


s = '''How you do,
fellow kids?'''


# In[47]:


s


# In[48]:


a = "hello, world!"
a[3:6] # 3rd to 6th (excluded) elements: elements 3, 4, 5

# 'lo,'

a[2:10:2] # Syntax: a[start:stop:step]

# 'lo o'

a[::3] # every three characters, from beginning to end

# 'hl r!'


# In[49]:


a.replace('l', 'z', 1)


# In[50]:


# a dictionary - keys (emmannuelle) to values (5752)

tel = {'emmannuelle': 5752, 'sebastian': 5578}


# In[51]:


tel['francis'] = 5915


# In[52]:


tel


# In[53]:


a = [1, 2, 3]
b = a
a


# In[54]:


a is b


# In[55]:


b[1] = "hi"


# In[56]:


a


# In[59]:


a = ['a', 'b', 'c']
id(a)


# In[61]:


a[:] = [1, 2, 3] # Modifies object in place.


# In[62]:


a


# In[63]:


id(a)


# In[65]:


for i in range(11):
    print(i)


# In[68]:


for word in ('cool', 'powerful', 'readable'):
    print('Python is '+ word)


# In[69]:


z = 1 + 1j # j makes the number imaginary
while abs(z) < 100:
    z = z**2 + 1
z


# In[70]:


a = [1, 0, 2, 4]
for element in a:
    if element == 0:
        continue
    print(1. / element)

