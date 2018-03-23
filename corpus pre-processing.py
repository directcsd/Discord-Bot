# coding: utf-8

# In[1]:


import re
import time
import pandas as pd
import dateutil
import matplotlib.pyplot as plt


# In[2]:


class wp_chat():

    def __init__ (self, filename):
        self.filename = filename

    def open_file(self):
        x = open(self.filename,'r', encoding='utf8')
        y = x.read()
        content = y.splitlines()
        return content

    def clean_unicode(self,str):
        patterns = {
            "uni1":r'\\u20[0-9][a-z]',
            "uni2":r'\\xa0',
            "uni3":r'\\ufeff'
        }
        raw_str = "%r"%str
        for key in patterns:
            raw_str = re.sub(patterns[key],"",raw_str)
        return raw_str

    def ismessage(self,str):
        patterns = {
            "hor1":r'w{3}s{1}[0-9]{1,2},s{1}d{4},s{1}d{2}:d{2}',
            "hor2":r'w{3}s{1}[0-9]{1,2},s{1}d{2}:d{2}',
            "imp2":r'd{1,2}sw{3}sd{2}:d{2}',
            "imp1":r'd{1,2}sw{3}sd{4}sd{2}:d{2}',
            "datetime":r'\d+\/\d+\/\d+\,\s(\d\d:){3}'
        }
        for key in patterns:
            result = re.search(patterns[key], str)
            if result and str.count(':') >=2:
                name_start = str.find(":")+7
                first_colon = str.find(":")
                name_end = str.find(":", first_colon+7)
                name=str[name_start:name_end]
                message=str[name_end+1:]
                return [name, message, result.group()]
        return ["","",str]

    def process(self,content):
        j = 1
        df = pd.DataFrame(index = range(1, len(content)+1), columns=[ 'Name', 'Message', 'date_string'])
        for i in content:
            results = self.ismessage(i)
            if results[0] != "":
                df.ix[j]=results
            else:
                df.ix[j]['Name']=df.ix[j-1]['Name']
                df.ix[j]['date_string']=df.ix[j-1]['date_string']
                df.ix[j]['Message']=results[2]
            j = j+1
        #df['Time'] = df['date_string'].map(lambda x: dateutil.parser.parse(x))
        #df['Day'] = df['date_string'].map(lambda x: dateutil.parser.parse(x).strftime("%a"))
        #df['Date'] = df['date_string'].map(lambda x:dateutil.parser.parse(x).strftime("%x"))
        #df['Hour'] = df['date_string'].map(lambda x:dateutil.parser.parse(x).strftime("%H"))
        return df

    def cleaning(self,content):
        clean_content=[]
        for i in content:
            clean_content.append(self.clean_unicode(i))
        return clean_content



# In[3]:


chat=wp_chat("corpus spanish whatsapp.txt")


# In[4]:


content=chat.open_file()


# In[5]:


cleaned=chat.cleaning(content)


# In[6]:


df=chat.process(cleaned)


# In[7]:


df['Message']=df['Message'].str.lower()


# In[8]:


df=df[df.Message.str.contains(" omitted>") == False]


# In[9]:


df.to_csv("processed corpus.txt", index=False, header=False, columns=["Message"])

