FROM hub.paas.vn/public/python:3.8.5

ENV INSTALL_PATH /app

ARG REQUIREMENTS=requirements.txt

WORKDIR $INSTALL_PATH

ENV TZ 'Asia/Ho_Chi_Minh'
RUN echo $TZ > /etc/timezone && \
    apt-get update && apt-get install -y tzdata vim && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

COPY ${REQUIREMENTS} ./

RUN pip install -r ${REQUIREMENTS}

RUN pip install gunicorn

COPY . .

EXPOSE 5000

CMD ["gunicorn", "manager:app", "--worker-class", "gevent", "--worker-connections", "1000", "-b", "0.0.0.0:5000", "-w", "5", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-"]
