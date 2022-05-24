FROM alpine:latest AS builder
LABEL maintainer="Ed Chai <edwardc@acrossor.com>"
# add build environment deps
RUN apk add --no-cache make g++ cmake

# Build PROJ
ARG PROJ_VERSION=master
# add PROJ build deps
RUN apk add --no-cache \
    curl-dev sqlite-dev sqlite
# download source from master
RUN mkdir -p proj/build \
    && wget -q https://github.com/OSGeo/PROJ/archive/${PROJ_VERSION}.tar.gz -O - \
        | tar xz -C proj --strip-components=1
# cmake
# options docs: https://proj.org/install.html#cmake-configure-options
RUN cd proj/build \
    && cmake .. \
    -DBUILD_APPS=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DENABLE_IPO=ON \
    -DBUILD_TESTING=OFF \
    -DENABLE_TIFF=OFF \
    -DENABLE_CURL=OFF \
    && cmake --build . --target install \
    && cmake --build . --target install -- DESTDIR=/build/proj \
    && cd / \
    && rm -rf proj

# Build GEOS
ARG GEOS_VERSION=master
RUN mkdir -p geos/build \
    && wget -q https://github.com/libgeos/geos/archive/${GEOS_VERSION}.tar.gz -O - \
        | tar xz -C geos --strip-components=1
# cmake
# options docs: https://libgeos.org/usage/download/#build-options
RUN cd geos/build \
    && cmake .. \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_DOCUMENTATION=OFF \
    && cmake --build . --target install -- DESTDIR=/build/geos \
    && cd / \
    && rm -rf geos

# Build GDAL
ARG GDAL_VERSION=v3.5.0
# add GDAL build deps
RUN apk add --no-cache \
    linux-headers tiff-dev
# download source from master
RUN mkdir -p gdal/build \
    && wget -q https://github.com/OSGeo/gdal/archive/${GDAL_VERSION}.tar.gz -O - \
        | tar xz -C gdal --strip-components=1
# cmake
# options docs: https://gdal.org/build_hints.html#cmake-general-configure-options zlib/ziff/geotiff/jsonc seems required
RUN cd gdal/build \
    && cmake .. \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_BUILD_TYPE=Release \
    -DGDAL_USE_EXTERNAL_LIBS=OFF \
    -DGDAL_USE_INTERNAL_LIBS=OFF \
    -DGDAL_USE_ZLIB=ON \
    -DGDAL_USE_TIFF_INTERNAL=ON \
    -DGDAL_USE_GEOTIFF_INTERNAL=ON \
    -DGDAL_USE_JSONC_INTERNAL=ON \
    -DGDAL_USE_PNG_INTERNAL=ON \
    && cmake --build . \
    && cmake --build . --target install -- DESTDIR=/build/gdal \
    && cd / \
    && rm -rf gdal

# Build final image
FROM python:alpine AS runner
COPY --from=builder  /build/proj/usr/lib/ /geos/usr/lib/
COPY --from=builder  /build/gdal/usr/lib/ /geos/usr/lib/
COPY --from=builder  /build/geos/usr/lib/ /geos/usr/lib/
RUN find /geos/usr/lib/ -type l | xargs -i ln -sf {} /usr/lib/
RUN find /geos/usr/lib/libproj.so.* -type f | xargs -i ln -sf {} /usr/lib/
# don't import proj.db
# COPY --from=builder  /build/proj/usr/share/proj/ /usr/share/proj/
# runtime deps
RUN apk add --no-cache \
    # binutils to fix ctypes.util.find_library broken
    libstdc++ libjpeg-turbo binutils \
    && rm -f /usr/lib/libturbojpeg.so*
