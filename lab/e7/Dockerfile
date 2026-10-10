FROM nvidia/cuda@sha256:ad6d59a3bbf3e82c1c849c9ac09cfc2a3e0bbb8655042fd899be6681b3fe2a85
# Cached Ubuntu 22.04 base; the lab uses runc, no GPU device/runtime.
ENV DEBIAN_FRONTEND=noninteractive TZ=UTC
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-yaml python3-pymongo meson ninja-build build-essential flex bison git cmake \
    libsctp-dev libc-ares-dev libgnutls28-dev libgcrypt-dev libssl-dev libmongoc-dev libbson-dev \
    libyaml-dev libnghttp2-dev libmicrohttpd-dev libcurl4-gnutls-dev libtins-dev libtalloc-dev \
    libidn-dev iproute2 iptables iputils-ping tcpdump ca-certificates && rm -rf /var/lib/apt/lists/*
COPY open5gs /opt/src/open5gs
RUN cd /opt/src/open5gs && test "$(git rev-parse HEAD)" = d9d3abdd480be96fac3bc8a997e83446648763ca && \
    meson build --prefix=/opt/open5gs && ninja -C build -j4 && ninja -C build install
COPY UERANSIM /opt/src/UERANSIM
RUN cd /opt/src/UERANSIM && test "$(git rev-parse HEAD)" = 1d1e154f869260b5e98f6905827b1bd9b8663afc && \
    cmake -S . -B cmake-build-release -DCMAKE_BUILD_TYPE=Release && \
    cmake --build cmake-build-release -j4
# MongoDB upstream archive is supplied and hashed by the preparation runner.
COPY mongodb-7.0.16.tgz /opt/mongodb.tgz
RUN mkdir -p /opt/mongodb && tar -xzf /opt/mongodb.tgz --strip-components=1 -C /opt/mongodb && rm /opt/mongodb.tgz
ENTRYPOINT []
CMD ["sleep", "infinity"]
