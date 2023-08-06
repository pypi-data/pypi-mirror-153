FROM docker.io/library/ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive
ENV PKG_DEPS="\
    bc \
    ca-certificates \
    curl \
    libatomic1 \
    libdbus-1-3 \
    openssh-server \
    telnet \
"

RUN set -e ;\
    apt update -q=2 ;\
    apt full-upgrade -q=2 --yes ;\
    apt install --yes ca-certificates ;\
    apt install -q=2 --yes --no-install-recommends ${PKG_DEPS} ;\
    # Install the FVP model
    curl --connect-timeout 5 --retry 5 --retry-delay 1 -fsSLo /tmp/fvp.tgz \
    https://developer.arm.com/-/media/Files/downloads/ecosystem-models/FVP_Base_RevC-2xAEMvA_11.17_21.tgz ;\
    tar xf /tmp/fvp.tgz -C /tmp ;\
    mkdir -p /opt/model/FVP_AEMvA/ ; \
    cp -R /tmp/Base_RevC_AEMvA_pkg/* /opt/model/FVP_AEMvA/ ;\
    # Cleanup
    apt clean ;\
    rm -rf /var/lib/apt/lists/* /tmp/*
