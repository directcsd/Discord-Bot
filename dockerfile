FROM python:3

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Only use Jupyter for debugging with the ipnby files (can comment otherwise)
RUN pip install jupyter
ADD jupyter_notebook_config.json /root/.jupyter/jupyter_notebook_config.json

ADD . /app
WORKDIR /app

EXPOSE 8000

# Only used for debugging 
CMD jupyter notebook --allow-root --ip=0.0.0.0 --port=8000