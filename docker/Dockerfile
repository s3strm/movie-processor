FROM debian:jessie
COPY apt/sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install deb-multimedia-keyring --force-yes -y
RUN apt-get update && apt-get install --force-yes -y \
    atomicparsley \
    awscli \
    ffmpeg \
    graphicsmagick-imagemagick-compat \
    isomd5sum \
    make \
    mkvtoolnix

ADD opt/ /opt
WORKDIR /opt/metadata
ENV INPUT /dev/null
ENV BUCKET null
ENTRYPOINT [ "make" ]
CMD [ "all" ]

# vim: ft=dockerfile
