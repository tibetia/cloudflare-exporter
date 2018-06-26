FROM alpine:3.5

ENTRYPOINT ["python", "-m", "exporter"]
EXPOSE 9199
ENV FLASK_APP=/exporter/exporter/app.py \
    SERVICE_PORT=9199

RUN LAYER=build \
  && apk add -U python py-pip \
  && pip install prometheus_client delorean requests apscheduler Flask \
  && rm -rf /var/cache/apk/* \
  && rm -rf ~/.cache/pip

ADD ./exporter /exporter

LABEL container.name=cloudflare-exporter:0.5.1
