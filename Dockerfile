FROM apache/airflow:2.6.0

COPY requirements.txt /requirements.txt

RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt

USER root
RUN apt update \
  && apt install -y unzip curl wget git make build-essential g++

RUN apt-get update \
  && echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list \
  && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && apt update \
  && apt install -y google-chrome-stable
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

RUN apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR
ENV PATH $CHROMEDRIVER_DIR:$PATH

RUN apt-get update\
    && apt-get install -y cron\
    && service cron start\
    && echo "PATH=/opt/someApp/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/chromedriver\n0 17 * * * DISPLAY=:0 . /code/jobs/management/commands/test.sh " | crontab -

RUN apt-get update && \
  apt-get install -y \
    libgtk2.0-0 \
    libnotify-dev \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    xvfb

USER airflow

RUN airflow db upgrade