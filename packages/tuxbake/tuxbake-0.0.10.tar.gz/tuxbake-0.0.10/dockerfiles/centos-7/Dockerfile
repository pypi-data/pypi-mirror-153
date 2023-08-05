FROM centos:centos7

ENV LANG=en_US.UTF-8
ENV PKG_DEPS="\
    gzip \
    diffutils \
    cpp \
    perl-Data-Dumper \
    perl-Text-ParseWords \
    SDL-devel \
    xterm \
    mesa-libGL-devel \
    gcc \
    gcc-c++ \
    make \
    chrpath \
    cpio \
    curl \
    diffstat \
    file \
    gawk \
    git \
    gnupg \
    iputils\
    jq -y \
    less \
    openssh \
    pigz \
    python3 \
    python3-pip \
    socat \
    sudo \
    texinfo \
    unzip \
    wget \
    xz \
    xmlstarlet \
    awscli \
    openssl-devel \
    glibc-devel \
    lz4 \
    lz4-devel \
    zstd \
    python2 \
    bzip2 \
    patch \
    which \
    perl \
    perl-Thread-Queue \
"

RUN set -e ;\
    yum install -y -q deltarpm ;\
    yum install -y -q epel-release ;\
    yum makecache ;\
    yum -y -q update ;\
    yum -y -q distribution-synchronization ;\
    yum install -y -q ${PKG_DEPS} ;\
    pip3 install GitPython jinja2 ;\
    # Set Python 3 as default
    alias python="/usr/bin/python3" ;\
    # Setup tuxbake user
    useradd --create-home tuxbake --shell /bin/bash ;\
    # Cleanup
    yum clean expire-cache ;\
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
