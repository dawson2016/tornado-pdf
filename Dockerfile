FROM harbor.hseduyun.net/hs/ubuntu:base 
LABEL maintainer="Dawson.dong  <dawson_2014@163.com>"
ADD sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y python python-pip unoconv && pip install tornado==4.5 && rm -rf /var/lib/apt/lists/* 
RUN rm -f /usr/share/fonts/truetype/openoffice/opens___.ttf 
ADD sim* /usr/share/fonts/truetype/openoffice/
ADD app.py /opt/app.py
WORKDIR /opt/
EXPOSE 88
CMD libreoffice --headless --invisible   --norestore --nologo --nolockcheck --accept="socket,host=0.0.0.0,port=8100;urp;" --nofirststartwizard & python app.py
