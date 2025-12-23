FROM python:3.10-slim AS base

SHELL ["/bin/bash", "-c"]

ENV PYTHONPATH=/opt/site/code/src

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

ENV PYTHONPATH=/opt/site/code/src

USER root

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \ 
    && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | tee -a /etc/apt/sources.list.d/hashicorp.list

RUN /usr/bin/apt update \
    && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC /usr/bin/apt install -y google-cloud-cli=550.0.0-0 terraform

ENV PYTHONPATH=/app/src
