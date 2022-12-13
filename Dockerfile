FROM python:3.10.4

# 
RUN mkdir /opt/ziportal
WORKDIR /opt/ziportal

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

# 
COPY ./app ./app
COPY ./run.sh ./run.sh

RUN chmod +x ./run.sh

# 
ENTRYPOINT [ "./run.sh" ]