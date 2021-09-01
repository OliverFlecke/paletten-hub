FROM alpine:latest

RUN apk --update add certbot mosquitto

EXPOSE 80 443
EXPOSE 1883
EXPOSE 8883
EXPOSE 9001

COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# ENV host=host
# ENV email=oliverfl@live.dk

CMD certbot certonly --standalone --non-interactive --preferred-challenges http -m oliverfl@live.dk --agree-tos -d friday-mqtt.eastus2.azurecontainer.io && /usr/sbin/mosquitto -c /mosquitto/config/mosquitto.conf