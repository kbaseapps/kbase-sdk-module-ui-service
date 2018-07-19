FROM kbase/kbase:sdkbase2.latest
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"  dist-upgrade \
  && apt-get -y autoremove \
  && apt-get -y install sqlite3

RUN pip install --upgrade pip && pip install python-dateutil && pip install --upgrade pymongo 


# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work \
    && chmod -R a+rw /kb/module \
    && mkdir -p /kb/module/work/data

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
