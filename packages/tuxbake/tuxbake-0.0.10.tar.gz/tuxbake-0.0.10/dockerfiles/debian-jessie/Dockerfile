FROM debian:jessie

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV PKG_DEPS="\
    build-essential \
    python3-pexpect \
    debianutils \
    python3-jinja2 \
    libegl1-mesa \
    libsdl1.2-dev \
    xterm \
    python3-subunit \
    mesa-common-dev \
    chrpath \
    cpio \
    curl \
    diffstat \
    file \
    gawk \
    gcc-multilib \
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
    checkinstall \
    libreadline-gplv2-dev \
    libncursesw5-dev \
    libsqlite3-dev \
    tk-dev \
    libgdbm-dev \
    libbz2-dev \
    libffi-dev \
    python \
"

RUN set -e ;\
    echo 'locales locales/locales_to_be_generated multiselect C.UTF-8 UTF-8, en_US.UTF-8 UTF-8 ' | debconf-set-selections ;\
    echo 'locales locales/default_environment_locale select en_US.UTF-8' | debconf-set-selections ;\
    echo 'dash dash/sh boolean false' | debconf-set-selections ;\
    apt update -q=2 ;\
    apt full-upgrade -q=2 --yes ;\
    apt install -q=2 --yes --no-install-recommends ${PKG_DEPS} ;\
    pip3 install GitPython pylint==1.9.5 ;\
    # Set Python 3.6.0 or later as default
    wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tar.xz ;\
    tar xvf Python-3.8.0.tar.xz ;\
    cd Python-3.8.0/ ;\
    ./configure ;\
    make altinstall ;\
    update-alternatives --install /usr/bin/python python /usr/local/bin/python3.8 1 ;\
    update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.8 2 ;\
    # Setup tuxbake user
    useradd --create-home tuxbake --shell /bin/bash ;\
    # Cleanup
    apt-get clean ;\
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
