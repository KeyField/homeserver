FROM python:3.9

LABEL MAINTAINER="Ben Klein <robobenklein@gmail.com>"

ENV FLASK_APP=keyfieldhome \
  GROUP_ID=1000 \
  USER_ID=1000

RUN addgroup --gid $GROUP_ID www
RUN adduser --system --uid $USER_ID --gid $GROUP_ID --shell /bin/sh www

RUN mkdir -p /etc/keyfield
WORKDIR /etc/keyfield
COPY requirements.txt gunicorn-config.py /etc/keyfield
RUN pip install -r requirements.txt

RUN mkdir -p /hardurl/secrets
RUN chown -R $GROUP_ID:$USER_ID /hardurl/

COPY server-prod.sh /

ADD hardurl /hardurl/hardurl

RUN chmod 755 /server-prod.sh
RUN chmod -R o+rX /hardurl/hardurl/

USER www

EXPOSE 5000

CMD ["bash", "-c", "/server-prod.sh"]
