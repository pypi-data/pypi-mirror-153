FROM docker.io/library/ubuntu:xenial

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV PKG_DEPS="\
    build-essential \
    chrpath \
    cpio \
    curl \
    diffstat \
    file \
    gawk \
    git \
    gnupg \
    iputils-ping \
    jq \
    less \
    locales \
    openssh-client \
    pigz \
    python3 \
    python3-pip \
    socat \
    sudo \
    texinfo \
    unzip \
    wget \
    xz-utils \
    xmlstarlet \
    awscli \
    libssl-dev \
    libc6-dev-i386 \
    liblz4-tool \
    zstd \
    python \
    libyaml-dev \
    libpython2.7-dev \
    libelf-dev \
"

RUN set -e ;\
    echo 'locales locales/locales_to_be_generated multiselect C.UTF-8 UTF-8, en_US.UTF-8 UTF-8 ' | debconf-set-selections ;\
    echo 'locales locales/default_environment_locale select en_US.UTF-8' | debconf-set-selections ;\
    echo 'dash dash/sh boolean false' | debconf-set-selections ;\
    apt update -q=2 ;\
    apt full-upgrade -q=2 --yes ;\
    apt install -q=2 --yes --no-install-recommends ${PKG_DEPS} ;\
    # Set default shell to bash
    dpkg-reconfigure -p critical dash ;\
    # Setup tuxbake user
    useradd --create-home tuxbake --shell /bin/bash ;\
    # Cleanup
    apt clean ;\
    rm -rf /var/lib/apt/lists/* /tmp/*

USER tuxbake

RUN set -e ;\
    # Set git default config
    git config --global user.email "ci@tuxsuite.com" ;\
    git config --global user.name "Tuxsuite Bot" ;\
    git config --global color.ui "auto" ;\
    echo "progress = dot" > ${HOME}/.wgetrc ;\
    echo "dot_bytes = 10m" >> ${HOME}/.wgetrc

CMD ["/bin/bash"]
