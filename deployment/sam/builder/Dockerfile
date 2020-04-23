FROM lambci/lambda-base:build

ENV PATH=/var/lang/bin:$PATH \
    LD_LIBRARY_PATH=/var/lang/lib:$LD_LIBRARY_PATH \
    AWS_EXECUTION_ENV=AWS_Lambda_python3.6 \
    PYTHONPATH=/var/runtime \
    PKG_CONFIG_PATH=/var/lang/lib/pkgconfig:/usr/lib64/pkgconfig:/usr/share/pkgconfig \
    CPPFLAGS='-I/usr/include/' \
    LDFLAGS='-L/usr/lib64/'

RUN rm -rf /var/runtime /var/lang && \
    curl https://lambci.s3.amazonaws.com/fs/python3.6.tgz | tar -xz -C / && \
    sed -i '/^prefix=/c\prefix=/var/lang' /var/lang/lib/pkgconfig/python-3.6.pc && \
    curl https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tar.xz | tar -xJ && \
    cd Python-3.6.8 && \
    LIBS="$LIBS -lutil -lrt" ./configure --enable-loadable-sqlite-extensions --prefix=/var/lang && \
    make -j$(getconf _NPROCESSORS_ONLN) libinstall libainstall inclinstall && \
    make install && \
    cd .. && \
    rm -rf Python-3.6.8

# Add these as a separate layer as they get updated frequently
RUN yum install -y postgresql95-devel.x86_64 && \
    pip install -U pip setuptools --no-cache-dir && \
    pip install -U virtualenv wheel --no-cache-dir

# Copy pants files and run install dependencies
# For some reason pants doesn't install the right version of docutils so we get this
# error: Exception message: (docutils 0.14 (/var/runtime), Requirement.parse('docutils<0.13,>=0.12'), {'pantsbuild.pants'})
COPY pants pants.ini ./
RUN pip uninstall -y docutils && ./pants goals
