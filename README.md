# Discord-Bot

What started as a simple experiment to create a Discord Bot, became the project to create a Bot that could answer using the char-rnn proposed by @akarpathy

Here I use the code form @minesh.mathew of the char-rnn in Keras

The bot is trained in a corpus extracted from a WhatsApp group so to simulate conversations from this same group of people.

## Getting Started

The idea of the bot is to train the [char-rnn](https://github.com/karpathy/char-rnn) with the corpus that you have and then have the bot generate words based on that corpus. The bot will connect to the Discord server you configure.

Take in consideration that this is one of my first attempts to code, therefore the quality of the code is similar to an [italian cook](https://en.wikipedia.org/wiki/Spaghetti_code)

### Prerequisites

1. Install discord.py
1. Install jupyter
1. Install Keras + Tensorflow (Anaconda will make your life easier)
1. If you corpus come from a WhatsApp group then you can use the parser I prepared, for that you need to download the group chatlog from your mobile and send it to you (I used the email option)
1. Training of the model took a while with my NVIDIA 1060, I imagine that a GPU system will be a good idea
1. Enough permission (not real clear to me what was needed, I was an administrator of the server) in the Discord server to include the bot

### Installing

To use the bot then you need to:

1. Download the corpus and execute the notebook "corpus pre-processing". The most important lines to look at (and change) are:
   * Within the `clean_unicode` function, what are the regexp which matches with the unicode values you want to remove (the RNN is better is there are less chars to predict)
   * Within the `ismessage` function the regexp that matches your datetime format (it seems that WhatsApp have a different one in each country)
1. Once the corpus is preprocessed I stored the image in Amazon S3. Alternatively you may change the `get-file` in the notebook "char_rnn_karpathy_keras"
1. Execute the "char_rnn_karpathy_keras" notebook
   * According to the authors a corpus should be 2MB sized to start getting good results
   * The loss reduces quite well as the iterations progress, I recommend changing the iteration range to 61 and used the last model version (you can test with the previous as well)
   * Take a long walk...
1. Once the processing is finished you will have 1 or more of Karpathy_LSTM_weights_??.h5 where ?? is the iteration used to create the model weights. Edit the `model.load_weights` in the notebook "Bot" to change to the version you want to use
1. Add the bot app to the discord. I followed the instructions in this [video](https://www.youtube.com/watch?v=u6tBvQSXJ7I)
1. Execute the "Bot" notebook
   * In the `charrnn` function the outermost `for` loop defines how many characters will be created at each invocation. Adjust it properly so it doesn't take too long to the bot to answer
   * replace the _TOKEN_ in `client.run` with tho eone you generated in the previous step
1. Test the bot in your channel. To talk to the bot just write something start with ! the bot will use the corpus to predict the response.

## Built With

* [discord.py](https://github.com/Rapptz/discord.py) - The Python Discord Bot API
* [Keras](https://keras.io/) - High Level Neural Network library
* [Tensorflow](https://www.tensorflow.org/) - Numerical computing library
* [paser code article](https://dscience.co.uk/whatsapp-ening-text-analytics-with-a-whatsapp-message-log/) - Although the article didn't have the full code, the parser was basically copied from there
* [char-rnn implementation in Keras](https://github.com/mineshmathew/char_rnn_karpathy_keras) - I totally copy/paste this implementation. The predict code in the bot itself also comes from this source


## To Do

* Implement the temperature in the predictions to change the _diversity_ of the generated text
