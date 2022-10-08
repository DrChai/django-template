# GIS Image (GDAL/PROJ/GEOS Only)
A lightweight GDAL/PROJ/GEOS based on Alpine. Image only ships the shared libs (`libproj.so`, `libgdal.so` and  `geos_c.so`) that are required by GeoDjango. Image is minimal without binaries and corresponding Image libraries. So it's only built for Django and spatial databases (spatialite, postgis, etc). Image size is around 70MB compared to 300MB+.

### Usage
_____The final stage of this image is already targeted to python:alpine, you can use latest python3 directly._____
* test if works. all libs should be imported by `ctypes.util.find_library`
```unix
docker run -ti --rm carrycat/gis python -c 'from ctypes.util import find_library;print(find_library("gdal"))'
```
* create dockerfile from this image:
```dockerfile
FROM carrycat/gis
# install Python/Django depencies
RUN apk add --update --no-ache --virtual .tmp \
    gcc libc-dev linux-headers make \
    # pillow
    jpeg-dev zlib-dev \
    # cffi
    libffi-dev \
    # postgres (alt. option: musl-dev postgresql-dev)
    libpq-dev
WORKDIR /app
COPY . /app
# install django, postgres-binary and else...
RUN  pip install -r requirements.txt  
RUN apk del .tmp
ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 8000
```
* use this image as a “stage”. The libs are already saved at `/geos/usr/libs` directory.
  proj resources(includes proj.db) at `/geos/usr/share/proj/`. 
  ***Don't forget to pull the latest alpine, otherwise shared libs may be broken on your container.***
```dockerfile
FROM python:alpine
COPY --from=carrycat/gis  /geos/usr/lib/ /usr/lib/
# add runtime deps for GDAL
RUN apk add --no-cache \
    # binutils to fix ctypes.util.find_library broken
    libstdc++ libjpeg-turbo binutils \
    && rm -f /usr/lib/libturbojpeg.so*
```
### options used on build:
* [PROJ](https://proj.org/install.html#cmake-configure-options)
```shell
cmake .. \
    -DBUILD_APPS=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DENABLE_IPO=ON \
    -DBUILD_TESTING=OFF \
    -DENABLE_TIFF=OFF \
    -DENABLE_CURL=OF
```
* [GEOS](https://libgeos.org/usage/download/#build-options)
```shell
cmake .. \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_DOCUMENTATION=OFF
```
* [GDAL](https://libgeos.org/usage/download/#build-options)
```shell
cmake .. \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_BUILD_TYPE=Release \
    -DGDAL_USE_EXTERNAL_LIBS=OFF \
    -DGDAL_USE_INTERNAL_LIBS=OFF \
    -DGDAL_USE_ZLIB=ON \
    -DGDAL_USE_TIFF_INTERNAL=ON \
    -DGDAL_USE_GEOTIFF_INTERNAL=ON \
    -DGDAL_USE_JSONC_INTERNAL=ON \
    -DGDAL_USE_PNG_INTERNAL=ON
```

### Github and Dockerfile

