FROM python:3.10-alpine
ARG ID
ARG KEY
ARG REGION
RUN pip install metamock
RUN metamock configure --id $ID --key $KEY --region $REGION >~/.metamock.config
RUN cat ~/.metamock.config
CMD "metamock run --host=0.0.0.0 --port 80"
