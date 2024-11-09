FROM codercom/enterprise-base:ubuntu
LABEL org.opencontainers.image.source https://github.com/sprint-cloud/workspaces

USER root
# Install packages
RUN apt update && sudo apt install -y \
    zsh \
    nodejs \
    npm \
    php-cli\
    unzip\
    golang-go\
    dotnet-sdk-8.0

RUN apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}/
COPY --from=ghcr.io/sprint-cloud/images:tools-latest /downloads/bin/* /usr/local/bin/

RUN mkdir /template && chown -R coder:coder /template
RUN usermod --shell /bin/zsh coder 
USER coder
COPY home/* /home/coder/
RUN curl -L git.io/antigen > /home/coder/antigen.zsh && \
    /bin/zsh -c 'source /home/coder/.zshrc'
RUN rsync -ar /home/coder /template
RUN rm -rf /home/coder/*