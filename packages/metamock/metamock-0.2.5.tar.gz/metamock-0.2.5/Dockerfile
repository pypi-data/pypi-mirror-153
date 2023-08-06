FROM python:3.10-alpine
ARG ID
ARG KEY
ARG REGION
RUN pip install -U metamock
RUN metamock configure --id $ID --key $KEY --region $REGION >~/.metamock.config
RUN cat ~/.metamock.config
EXPOSE 16925/tcp
CMD [ "/bin/sh", "-c", "metamock --debug --host 0.0.0.0 --port 16925 run"]
