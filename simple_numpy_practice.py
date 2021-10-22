#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
a = np.array((0,1,2,3))
a


# In[5]:


L = range(1000)


# In[7]:


get_ipython().run_line_magic('timeit', '[i**2 for i in L]')


# In[8]:


a = np.arange(1000)

get_ipython().run_line_magic('timeit', 'a**2')


# In[13]:


# reference
get_ipython().run_line_magic('pinfo', 'np.array')
np.lookfor('create array') # basically google search
get_ipython().run_line_magic('psearch', 'np.con*')


# In[15]:


b = np.array([[0, 1, 2], [3, 4, 5]])    # 2 x 3 array
b


# In[16]:


b.ndim # number of dimensions


# In[17]:


b.shape


# In[18]:


len(b)


# In[19]:


c = np.array([[[1], [2]], [[3], [4]]])


# In[20]:


c


# In[21]:


c.shape


# In[24]:


a = np.ones((3, 3))  # reminder: (3, 3) is a tuple
a
b = np.zeros((2, 2))
b
c = np.eye(3)
c
d = np.diag(np.array([1, 2, 3, 4]))
d


# In[25]:


a


# In[26]:


b


# In[27]:


c


# In[33]:


c = np.array([1, 2, 3], dtype=float)
c.dtype


# In[31]:


a = np.array([1, 2, 3])


# In[32]:


a.dtype


# In[34]:


get_ipython().run_line_magic('matplotlib', 'inline # this makes plots work (hopefully)')


# In[35]:


import matplotlib.pyplot as plt  # the tidy way


# In[37]:


x = np.linspace(0, 3, 20)
y = np.linspace(0, 9, 20)
plt.plot(x, y)       # line plot    


# In[38]:


plt.plot(x, y, 'o')  # dot plot    


# In[42]:


image = np.random.rand(30, 30)
plt.imshow(image, cmap=plt.cm.gray)
plt.colorbar() # very important to have this all together
# or it wouldn't have worked


# In[43]:


a = np.arange(10)
a

a[0], a[2], a[-1]


# In[44]:


a[::-1]


# In[46]:


a = np.arange(10)
a


# In[48]:


a[2:9:3] # [start:end:step]


# In[49]:


a[:4]


# In[50]:


a[1:5:2]


# http://scipy-lectures.org/_images/numpy_indexing.png

# In[51]:


a[:9]


# In[55]:


b = np.arange(10)


# In[56]:


b


# In[57]:


b[1] = 222


# In[63]:


b


# In[64]:


c = b[::2].copy()


# In[65]:


c


# ## Using Boolean Masks

# In[66]:


np.random.seed(3)
a = np.random.randint(0, 21, 15)
a


# In[67]:


mask = (a % 3 ==0)


# In[69]:


extract_from_a = a[mask] #its grabbing whatever is 
# true from the previous bit


# In[70]:


extract_from_a # extract a sub-array with the mask


# In[71]:


a = np.arange(0, 100, 10)
a[[9, 7]] = -100
a


# ## 1.4.2.1. Elementwise operations
# 

# In[72]:


a = np.array([1, 2, 3, 4])
a + 1


# In[73]:


b = np.ones(4)+1


# In[75]:


a-b


# In[77]:


a = np.arange(1000)
a+1


# In[78]:


l = range(100)


# In[80]:


[i+1 for i in l]


# In[81]:


a = np.triu(np.ones((3, 3)), 1)   # see help(np.triu)
a


# In[84]:


a.T # transpose


# ## 1.4.2.2. Basic reductions
# 

# In[87]:


x = np.array([[1, 1, 1], [2, 2, 2]])


# In[88]:


x


# In[92]:


x.sum(axis=0) # columns (first dimension)


# In[95]:


x[:, 0].sum(), x[:, 1].sum(), x[:,2].sum()


# In[96]:


x.sum(axis=1) # rows (second dimension)


# In[98]:


x[0, :].sum(), x[1, :].sum()


# http://scipy-lectures.org/_images/reductions.png

# In[99]:


# Extrema
x = np.array((1,3,2))


# In[100]:


x.min()


# In[101]:


x.max()


# In[102]:


x.argmin() # index of min


# In[104]:


x.argmax() # index of max


# In[105]:


np.all((True, True, False))


# In[107]:


np.any((True, True, False))


# In[108]:


x.std()


# ## 1.4.2.3. Broadcasting

# Basic operations on numpy arrays (addition, etc.) are elementwise
# 
# This works on arrays of the same size.
# 
# Nevertheless, It’s also possible to do operations on arrays of different
# sizes if NumPy can transform these arrays so that they all have
# the same size: this conversion is called broadcasting.
# 
# http://scipy-lectures.org/_images/numpy_broadcasting.png
# 

# In[109]:


a = np.tile(np.arange(0, 40, 10), (3, 1)).T


# In[110]:


a


# In[113]:


b = np.array((0,1,2))


# In[115]:


a+b


# In[116]:


a = np.arange(0, 40, 10)
a.shape
a = a[:, np.newaxis]  # adds a new axis -> 2D array
a.shape
a
a + b


# ## Flattening

# In[117]:


a = np.array([[1, 2, 3], [4, 5, 6]])
a.ravel()
a.T
a.T.ravel()


# ## Reshaping - the opposite of Flattening

# In[118]:


a.shape


# In[119]:


b = a.ravel()


# In[120]:


b = b.reshape((2,3))


# In[121]:


b


# In[128]:


a = np.arange(4)
a.resize((8,))


# In[129]:


a


# In[132]:


a = np.array([[5,3,5], [1,3,2]])


# In[133]:


b = np.sort(a,axis=1)


# In[135]:


b


# In[138]:


a = np.array([1,8,4,2,1,1])
j_max = np.argmax(a)
j_min = np.argmin(a)
j_max, j_min


# In[141]:


get_ipython().run_line_magic('pinfo', 'np.argmax')


# # Might want to go back to this to check it!

# In[ ]:




