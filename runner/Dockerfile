FROM alpine:latest
LABEL org.opencontainers.image.source https://github.com/sprint-cloud/images
ENV ENV=/etc/.shinit

RUN adduser -D runner
RUN apk add --no-cache \ 
        git \
        curl \
        python3

COPY --from=ghcr.io/sprint-cloud/tools:latest /downloads/bin/* /usr/local/bin/

# Setup python packages
COPY hub /py/hub
RUN echo 'export "PYTHONPATH=/py"' > ${ENV}

# Home
RUN mkdir /workspace && chown -R runner:runner /workspace
USER runner
WORKDIR /workspace
RUN git config --global user.name 'Hub Runner' && \
    git config --global user.email 'noreply@sprintub.nl'