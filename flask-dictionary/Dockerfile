FROM python:3.9

RUN mkdir /opt/dictionary
COPY . /opt/dictionary
RUN useradd -d /opt/dictionary -s /bin/bash dictionary && chown -R dictionary:dictionary /opt/dictionary
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install python dependencies
USER dictionary
WORKDIR /opt/dictionary
#RUN echo "`id`" && ls -al
ENV PATH="$PATH:/opt/dictionary/.local/bin"
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "main:app"]
