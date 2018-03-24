
# coding: utf-8

# In[ ]:


import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)


# In[ ]:


from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM,TimeDistributed,SimpleRNN
from keras.utils.data_utils import get_file
import numpy as np
from time import sleep
import random
import sys


# In[ ]:


import discord
import asyncio


# In[ ]:


#path = get_file('nietzsche.txt', origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
#text = open(path).read().lower()
text = open('processed corpus.txt', encoding='utf8').read().lower()
print('corpus length:', len(text))


# In[ ]:


chars = sorted(list(set(text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))


# In[ ]:


model = Sequential()
#model.add(LSTM(512, return_sequences=True, input_shape=(maxlen, len(chars))))  # original one
model.add(LSTM(512, input_shape=(None, len(chars)),return_sequences=True)) #minesh witout specifying the input_length
model.add(LSTM(512, return_sequences=True)) #- original
model.add(Dropout(0.2))
model.add(TimeDistributed(Dense(len(chars))))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop')


# In[ ]:


model.load_weights("Karpathy_LSTM_weights_5.h5")


# In[ ]:


class Response():
    def __init__(self,message=""):
        self.message=message


# In[ ]:


response=Response()


# In[ ]:


async def charrnn(seed_string, response):
    #x=np.zeros((1, len(seed_string), len(chars)))
    for i in range(50):
        x=np.zeros((1, len(seed_string), len(chars)))
        for t, char in enumerate(seed_string):
            x[0, t, char_indices[char]] = 1.
        preds = model.predict(x, verbose=0)[0]
        #print (np.argmax(preds[7]))
        next_index=np.argmax(preds[len(seed_string)-1])
        
        
        #next_index=np.argmax(preds[len(seed_string)-11])
        #print (preds.shape)
        #print (preds)
        #next_index = sample(preds, 1) #diversity is 1
        next_char = indices_char[next_index]
        seed_string = seed_string + next_char
        
        #print (seed_string)
        #print ('##############')
        #if i==40:
        #    print ('####')
        response.message=response.message+next_char
    print(response.message)


# In[ ]:


client = discord.Client()


# In[ ]:


@client.event
async def on_ready():
    print('Connected as:')
    print(client.user.name)
    print(client.user.id)
    print(len(client.servers))
    print(len(list(client.get_all_members())))
    print('------')


# In[ ]:


@client.event
async def on_message(message):
    
    if message.content.startswith('!ping'):
        await client.send_message(message.channel, ':ping_pong: Pong!')
    
    elif message.content.startswith('!remindme'):
        await asyncio.sleep(10)
        await client.send_message(message.channel, (message.content[10:]))
    
    elif message.content.startswith('!count'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
        
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    
    elif message.content.startswith('!'):
        response.message=""
        await charrnn((message.content[1:]).lower(), response)
        await client.send_message(message.channel, response.message)


# In[ ]:


client.run('Mzc4MTYwNDEyMzgzOTAzNzQ3.DZeohg.QQs0BPAjZaEX907Q9dJNN9znr7o')

