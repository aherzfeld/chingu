FROM python:3.6-alpine

LABEL maintainer="Andrew Herzfeld"

# the -D flag creates user with system defaults
RUN adduser -D chingu

# this command is for alpine-based systems
RUN apk update && apk add build-base postgresql-dev

WORKDIR /home/chingu

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . .
RUN chmod +x boot.sh

ENV FLASK_APP chingu

# sets the owner to files stored in home/chingu to the new chingu user
# the -R option (--recursive) operates on files and directories recursively
RUN chown -R chingu:chingu ./
# makes chingu the default user for subsequent instructions
USER chingu

EXPOSE 5000
# default command to execute when container is started (script in boot.sh)
ENTRYPOINT ["./boot.sh"]