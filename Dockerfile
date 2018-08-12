FROM alpine:3.8 as builder
MAINTAINER KBase Developer

# The build stage needs just enough to run the KBase SDK tools.
# 

# update system and system dependencies
RUN apk upgrade --update-cache --available \
    && apk add --update --no-cache \
        apache-ant=1.10.4-r0 \
        bash=4.4.19-r1 \
        git=2.18.0-r0 \
        linux-headers=4.4.6-r2 \
        make=4.2.1-r2 \
        openjdk8=8.171.11-r0 \
        python2=2.7.15-r0

RUN mkdir -p /kb \
    && git clone --depth=1 https://github.com/kbase/kb_sdk /kb/kb_sdk \
    && cd /kb/kb_sdk \
    && make

COPY ./ /kb/module

RUN mkdir -p /kb/module/work/cache \
    && chmod -R a+rw /kb/module \
    && cd /kb/module \
    && PATH=$PATH:/kb/kb_sdk/bin make install

# Final image

FROM alpine:3.8
MAINTAINER KBase Developer

# update system and system dependencies
RUN apk upgrade --update-cache --available \
    && apk add --update --no-cache \
        bash=4.4.19-r1 \
        g++=6.4.0-r8 \
        git=2.18.0-r0 \
        libffi-dev=3.2.1-r4 \
        linux-headers=4.4.6-r2 \
        make=4.2.1-r2 \
        openssl-dev=1.0.2o-r2 \
        py2-pip=10.0.1-r0 \
        python2=2.7.15-r0 \
        python2-dev=2.7.15-r0

# install python dependencies for the service runtime.
RUN pip install --upgrade pip && \
    pip install \
        cffi==1.11.5 \
        jinja2==2.10 \
        jsonrpcbase==0.2.0 \
        ndg-httpsclient==0.5.1 \
        pymongo===3.7.1 \
        python-dateutil==2.7.3 \
        pytz==2018.5 \
        requests==2.19.1 \
        uwsgi==2.0.17.1
    
RUN addgroup --system kbmodule && \
    adduser --system --ingroup kbmodule kbmodule

COPY --from=builder --chown=kbmodule:kbmodule /kb/module /kb/module

WORKDIR /kb/module

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
