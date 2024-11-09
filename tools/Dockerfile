FROM alpine:latest
USER root
RUN apk add --no-cache gpg gpg-agent curl
RUN mkdir -p /downloads/bin && chown -R 1000:1000 /downloads

COPY --from=composer/composer /usr/bin/composer /downloads/bin/composer

ARG GH_CLI=2.61.0
ARG WERF=2.12.1
ARG ACT=0.2.69
ARG KUBECTL=1.31.2
ARG ARGO_CLI=3.5.12
ARG ARGO_CD=2.13.0

RUN adduser -D tools -h /downloads
USER tools
WORKDIR /downloads

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/v${KUBECTL}/bin/linux/amd64/kubectl" && \
    curl -LO "https://dl.k8s.io/release/v${KUBECTL}/bin/linux/amd64/kubectl.sha256" && \
    echo "$(cat kubectl.sha256)  kubectl" | sha256sum -c && \
    install -m 755 kubectl /downloads/bin/

# Install Github client
RUN wget https://github.com/cli/cli/releases/download/v${GH_CLI}/gh_${GH_CLI}_linux_amd64.tar.gz && \
    wget https://github.com/cli/cli/releases/download/v${GH_CLI}/gh_${GH_CLI}_checksums.txt && \
    find . -type f -exec sha256sum {} \; >> gh_${GH_CLI}_checksums.txt && \
    tar -zxvf gh_${GH_CLI}_linux_amd64.tar.gz && \
    install -m 0755 gh_${GH_CLI}_linux_amd64/bin/gh /downloads/bin/gh

# Install local act runner
RUN wget https://github.com/nektos/act/releases/download/v${ACT}/act_Linux_x86_64.tar.gz && \
    wget https://github.com/nektos/act/releases/download/v${ACT}/checksums.txt && \
    find . -type f -exec sha256sum {} \; >> checksums.txt && \
    tar xzvf act_Linux_x86_64.tar.gz && \
    install -m 0755 act /downloads/bin

# Install werf
RUN curl -sSLO "https://tuf.werf.io/targets/releases/${WERF}/linux-amd64/bin/werf"\
    -O "https://tuf.werf.io/targets/signatures/${WERF}/linux-amd64/bin/werf.sig" && \
    curl -sSL https://werf.io/werf.asc | gpg --import && gpg --verify werf.sig werf && \
    install -m 0755 werf /downloads/bin/werf

# Install Argo cli
RUN curl -sLO "https://github.com/argoproj/argo-workflows/releases/download/v${ARGO_CLI}/argo-linux-amd64.gz" && \
    curl -sLO "https://github.com/argoproj/argo-workflows/releases/download/v${ARGO_CLI}/argo-workflows-cli-checksums.txt" && \
    find . -type f -exec sha256sum {} \; >> argo-workflows-cli-checksums.txt && gunzip argo-linux-amd64.gz && \
    install -m 0755 argo-linux-amd64 /downloads/bin/argo

# Install Argo cli
RUN curl -sLO "https://github.com/argoproj/argo-workflows/releases/download/v${ARGO_CD}/argocd-linux-amd64" && \
    curl -sLO "https://github.com/argoproj/argo-workflows/releases/download/v${ARGO_CD}/cli-checksums.txt" && \
    find . -type f -exec sha256sum {} \; >> cli-checksums.txt && install -m 0755 argocd-linux-amd64 /downloads/bin/argocd