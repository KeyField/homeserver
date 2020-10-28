FROM python:3.9

LABEL MAINTAINER="Ben Klein <robobenklein@gmail.com>"

ENV FLASK_APP=keyfieldhome \
  GROUP_ID=1000 \
  USER_ID=1000

RUN addgroup --gid $GROUP_ID www
RUN adduser --system --uid $USER_ID --gid $GROUP_ID --shell /bin/sh www

RUN mkdir -p /keyfield
WORKDIR /keyfield
COPY setup.py gunicorn-config.py README.md /keyfield/

COPY server-prod.sh /

ADD keyfieldhome /keyfield/keyfieldhome

RUN python setup.py install

RUN chmod 755 /server-prod.sh
RUN chmod -R o+rX /keyfield/

# RUN mkdir -p /keyfield/server
# RUN chown -R $GROUP_ID:$USER_ID /keyfield/server

USER www

EXPOSE 5000

CMD ["bash", "-c", "/server-prod.sh"]
