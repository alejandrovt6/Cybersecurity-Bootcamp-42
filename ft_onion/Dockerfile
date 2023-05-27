FROM nginx:latest

RUN apt update && apt install tor -y && apt install ssh -y

COPY nginx.conf /etc/nginx/nginx.conf
COPY torrc /etc/tor/torrc
COPY index.html /usr/share/nginx/html/index.html
COPY gato.jpg /usr/share/nginx/html/gato.jpg
COPY sshd_config /etc/ssh/sshd_config

RUN useradd -m -d /home/avives-t -G sudo avives-t
RUN mkdir -p /home/avives-t/.ssh
COPY authorized_keys /home/avives-t/.ssh/authorized_keys
RUN chown avives-t:avives-t /home/avives-t/.ssh/
RUN chmod 644 /home/avives-t/.ssh/authorized_keys

RUN service tor start
RUN service nginx start
RUN service ssh start
RUN cat /var/lib/tor/other_hidden_service/hostname

EXPOSE 80
EXPOSE 4242

