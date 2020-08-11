FROM python:3.6
COPY promgraf.py /app/promgraf.py
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD python ./promgraf.py

