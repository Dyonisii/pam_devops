FROM openjdk:11

RUN apt-get update && \
    apt-get install -y openssh-server bash zstd bc && \
    mkdir -p /var/run/sshd

RUN echo 'root:sshpass1' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN mkdir -p /opt/local/logs /opt/local/apps/lib /opt/local/apps/versions

COPY files/sql.jar files/database.db /opt/local/apps/
COPY files/sqlite-jdbc-3.45.1.0.jar /opt/local/apps/lib/
COPY files/sql.jar.zst /opt/local/apps/versions/
COPY files/server.log.gz /opt/local/logs/

RUN cd /opt/local/apps/
RUN rm /opt/local/apps/sql.jar
RUN cp /opt/local/apps/versions/sql.jar.zst /opt/local/apps/
RUN unzstd /opt/local/apps/sql.jar.zst



EXPOSE 22

CMD ["/bin/bash", "-c", "echo \"export PATH=${PATH}\" >> /root/.bashrc;/usr/sbin/sshd -D"]
