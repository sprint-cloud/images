FROM alpine:latest
LABEL org.opencontainers.image.source https://github.com/sprint-cloud/images
ARG HOME=/workspace
ARG USER=sprinter
ARG TOOLS=

# Install packages
RUN apk add --no-cache \
        curl \
        rsync \
        zsh \
        git \
        vim \
        nano \
        docker-cli \
        python3 \
        py3-virtualenv \
        php-cli \
        nodejs \
        npm \
        unzip \
        go \
        dotnet8-sdk

COPY --from=ghcr.io/sprint-cloud/images:tools-latest /downloads/bin/* /usr/local/bin/

RUN adduser -D ${USER} -s /bin/zsh -h ${HOME}

RUN mkdir /template && chown -R ${USER}:${USER} /template

USER sprinter
COPY home/* ${HOME}
RUN curl -L git.io/antigen > ${HOME}/antigen.zsh && \
    /bin/zsh -c "source ${HOME}/.zshrc"
RUN rsync -ar ${HOME} /template
RUN rm -rf ${HOME}/*