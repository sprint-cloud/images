FROM alpine:latest
LABEL org.opencontainers.image.source https://github.com/sprint-cloud/images

RUN adduser -D runner
RUN apk add --no-cache \ 
        git \
        curl

COPY --from=ghcr.io/sprint-cloud/tools:latest /downloads/bin/* /usr/local/bin/
RUN mkdir /workspace && chown -R runner:runner /workspace
USER runner
WORKDIR /workspace
RUN git config --global user.name 'Hub Runner' && \
    git config --global user.email 'noreply@sprintub.nl'