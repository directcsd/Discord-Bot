
# coding: utf-8

# In[1]:


import re
import pandas as pd


# In[2]:


class wp_chat():

    def __init__(self, filename):
        self.filename = filename

	def open_file(self):
		x = open(self.filename, 'r', encoding='utf8')
        y = x.read()
        content = y.splitlines()
        return content

    def clean_unicode(self, str):
        patterns = {
            "uni1": r'\\u20[0-9][a-z]',
            "uni2": r'\\xa0',
            "uni3": r'\\ufeff'
        }
        raw_str = "%r" % str
        for key in patterns:
            raw_str = re.sub(patterns[key], "", raw_str)
        return raw_str

    def ismessage(self, str):
        result = re.split("( cre| add| cha| rem| lef| del|: )?", str, 1)
        message = result[2]
        str_temp = result[0]
        result = re.split("\] ?", str_temp, 1)
        date = result[0]
        name = result[1]
        return [name, message, date]

    def process(self, content):
        j = 0
        df = pd.DataFrame(index=range(1, len(content)+1),
		                  columns=['Name', 'Message', 'date_string'])
        for i in content:
            results = self.ismessage(i)
            df.iloc[j]['Name'] = results[0]
            df.iloc[j]['Message'] = results[1]
            df.iloc[j]['date_string'] = results[2]
#           print (results[0])

            j = j + 1
        return df

    def cleaning(self, content):
        clean_content = []
        for i in content:
            clean_content.append(self.clean_unicode(i))
        return clean_content

# In[3]:

chat = wp_chat("corpus spanish whatsapp.txt")

# In[4]:

content = chat.open_file()

# In[5]:

cleaned = chat.cleaning(content)

# In[6]:

df = chat.process(cleaned)

# In[7]:

df['Message'] = df['Message'].str.lower()

# In[8]:

df = df[df.Message.str.contains(" omitted>") == False]

# In[9]:

df.to_csv("processed corpus.txt", index=False, header=False,
          columns=["Message"])
