FROM python:3

# Only use sshd during debugging (can comment otherwise)
# Includes SSH login fix. Otherwise user is kicked off after login
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ENV NOTVISIBLE "in users profile"
RUN apt-get update && apt-get install -y openssh-server supervisor && \
    mkdir -p /var/run/sshd /var/log/supervisor && \
    echo 'root:pass' | chpasswd && \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd && \
    echo "export VISIBLE=now" >> /etc/profile
ADD id_rsa.pub /root/.ssh/authorized_keys
ADD id_rsa.pub /root/.ssh/authorized_keys2

# Only use Jupyter for debugging with the ipnby files (can comment otherwise)
ADD requirements.txt /app/requirements.txt
ADD jupyter_notebook_config.json /root/.jupyter/jupyter_notebook_config.json
RUN pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir jupyter

ADD . /app
WORKDIR /app

EXPOSE 22 8000

# Pre-process WhatsApp corpus within the image build - pre-done
# Remove comment and it will generate "processed corpus.txt"
# RUN python corpus\ pre-processing.py

# Generate h5 models within the image build - pre-done in AWS instance (up to 10 iterations)
# Remove the comment ant it will generate "Karpathy_LSTM_weights_xx.h5" - xx meaning the model saved at different iterations levels.
# RUN char_rnn_of_karphaty_keras.py

# Only used for debugging (if no Jupyter/sshd can run "Bot.py" deamon directly without supervisord)
CMD ["/usr/bin/supervisord"]