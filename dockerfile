FROM python:3

ADD requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Only use Jupyter for debugging with the ipnby files (can comment otherwise)
RUN pip install --no-cache-dir jupyter
ADD jupyter_notebook_config.json /root/.jupyter/jupyter_notebook_config.json

ADD . /app
WORKDIR /app

EXPOSE 8000

RUN python corpus\ pre-processing.py

# Only used for debugging 
CMD sh -c 'jupyter notebook --allow-root --ip=0.0.0.0 --port=8000 --no-browser'