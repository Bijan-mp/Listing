FROM ubuntu

RUN apt update
RUN apt install python3.8 -y  
RUN apt install python3-pip -y
RUN apt-get install netcat -y

WORKDIR /home
COPY ./requirements.txt req.txt
RUN pip install --upgrade pip
RUN pip install -r req.txt

EXPOSE 8000

COPY ./ listingproject


COPY entrypoint.sh entrypoint.sh
CMD ["sh", "entrypoint.sh"]