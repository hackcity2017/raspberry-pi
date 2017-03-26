FROM resin/raspberrypi3-debian:jessie

WORKDIR /usr/src/app
ENV INITSYSTEM on

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
      sense-hat \
      raspberrypi-bootloader \
      python-numpy \
	python-setuptools \
	 python-dev \ 
	python-pip \
      
	&& easy_install pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/* && pip install requests

COPY * ./

CMD ["bash", "start.sh"]