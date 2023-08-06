FROM docker.io/library/ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive
ENV PKG_DEPS="\
    bc \
    ca-certificates \
    curl \
    libatomic1 \
    openssh-server \
    telnet \
"

RUN set -e ;\
    apt update -q=2 ;\
    apt full-upgrade -q=2 --yes ;\
    apt install --yes ca-certificates ;\
    apt install -q=2 --yes --no-install-recommends ${PKG_DEPS} ;\
    # Install Morello FVP
    curl --connect-timeout 5 --retry 5 --retry-delay 1 -fsSLo /tmp/FVP_Morello.tgz \
    https://developer.arm.com/-/media/Arm%20Developer%20Community/Downloads/OSS/FVP/Morello%20Platform/FVP_Morello_0.11_33.tgz ;\
    tar xf /tmp/FVP_Morello.tgz -C /tmp ;\
    /tmp/FVP_Morello.sh \
      --i-agree-to-the-contained-eula \
      --destination /opt/model/FVP_Morello \
      --no-interactive ;\
    # Cleanup
    apt clean ;\
    rm -rf /var/lib/apt/lists/* /tmp/*
