FROM python:3.10-slim AS base

SHELL ["/bin/bash", "-c"]

ENV PYTHONPATH=/opt/site/code

USER root

# Install build dependencies / Add ssh fingerprints for trusted hosts and set permissions
RUN /usr/bin/apt update \
    && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC /usr/bin/apt install -y redis libdbi1 libdbd-mysql libmysql++-dev  \
    python3-mysqldb pkg-config gcc telnet iputils-ping netcat-traditional procps awscli curl gnupg

# Create web user / Create directories
RUN /usr/sbin/useradd -r -d /opt/site -u 998 -s /bin/bash web -k /etc/skel -m -U \
    && chown web:web -R /opt/site \
    && mkdir -p /opt/log \
    && chown web:web /opt/log \ 
    && chmod 755 /opt/log

USER web

COPY --chown=web:web ./src/requirements.txt /opt/site/code/
RUN /usr/local/bin/pip install -r /opt/site/code/requirements.txt

RUN mkdir -p /opt/site/{bin,code} 

COPY --chown=web:web ./bin/ /opt/site/bin/
COPY --chown=web:web ./src/ /opt/site/code/

USER root

RUN chown web:web -R /opt/site \
    && chmod +x /opt/site/bin/*

WORKDIR /opt/site

USER web

ENTRYPOINT ["/opt/site/bin/entrypoint_web.sh"]

FROM base AS dev

ENV PYTHONPATH=/opt/site/code

RUN /usr/local/bin/pip install debugpy

WORKDIR /opt/site

USER web

ENTRYPOINT ["/opt/site/bin/entrypoint_debug.sh"]
