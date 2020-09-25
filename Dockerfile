FROM alpine:3.12 as builder
MAINTAINER KBase Developer

# The build stage needs just enough to run the KBase SDK tools.

# update system and system dependencies
RUN apk upgrade --update-cache --available && \
    apk add --update --no-cache apache-ant bash git linux-headers make openjdk8

# Currently need this special install for python3. oh, python.
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN mkdir -p /kb && \
    git clone --depth=1 https://github.com/kbase/kb_sdk /kb/kb_sdk && \
    cd /kb/kb_sdk && \
    make

COPY ./ /kb/module

RUN mkdir -p /kb/module/work/cache && \
    chmod -R a+rw /kb/module && \
    cd /kb/module && \
    PATH=$PATH:/kb/kb_sdk/bin make install

# Final image

FROM alpine:3.12
MAINTAINER KBase Developer

# update system and system dependencies
RUN apk upgrade --update-cache --available && \
    apk add --update --no-cache bash g++ git libffi-dev linux-headers make openssl-dev

# Currently need this special install for python3. oh, python.
RUN apk add --no-cache python3 python3-dev py3-setuptools && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

# install python dependencies for the service runtime.
RUN pip install --upgrade pip && \
    pip install \
    cffi==1.14.3 \
    coverage==4.5.4 \
    jinja2==2.11.2 \
    jsonrpcbase==0.2.0 \
    ndg-httpsclient==0.5.1 \
    git+https://github.com/nose-devs/nose@master \
    python-dateutil==2.8.1 \
    pytz==2020.1 \
    requests==2.24.0 \
    uwsgi==2.0.19.1

RUN addgroup --system kbmodule && \
    adduser --system --ingroup kbmodule kbmodule

COPY --from=builder /kb/module /kb/module
RUN chown -R kbmodule:kbmodule /kb/module

WORKDIR /kb/module

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
