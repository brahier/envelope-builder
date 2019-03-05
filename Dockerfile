FROM python:3-alpine

RUN set -ex \
	&& apk add --no-cache \
        mkfontdir \
        fontconfig \
        git \
        gcc \
        musl-dev \
        jpeg-dev \
        zlib-dev \
        libffi-dev \
        cairo-dev \
        pango-dev \
        gdk-pixbuf-dev \
    \
    && python -m pip install --upgrade pip setuptools \
    && python -m pip install WeasyPrint \
    && python -m pip install jinja2 flask gunicorn

COPY fonts/* /usr/share/fonts/
RUN fc-cache

WORKDIR /app
COPY app /app

ENTRYPOINT []
CMD ["bin/run-dev.sh"]
