FROM alpine:latest
LABEL org.opencontainers.image.source https://github.com/sprint-cloud/images
ENV ENV=/etc/.shinit
ENV HUBTEMPLATEDIR=/src/templates

RUN adduser -D runner
RUN apk add --no-cache \ 
        git \
        curl \
        python3 \
        py3-pip

COPY --from=ghcr.io/sprint-cloud/tools:latest /downloads/bin/* /usr/local/bin/

# Setup python packages
COPY . /src/
RUN pip install --break-system-packages -r /src/requirements.txt
RUN echo 'export "PYTHONPATH=/src"' > ${ENV}

# Home
RUN mkdir /workspace && chown -R runner:runner /workspace
USER runner
WORKDIR /workspace
RUN git config --global user.name 'Hub Runner' && \
    git config --global user.email 'noreply@sprintub.nl'