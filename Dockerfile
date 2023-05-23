FROM python:3.11.3-alpine3.17 as builder
ARG version=17.0.7.7.1

RUN apk add --no-cache bash procps curl tar binutils

# Install Amazon Corretto 17, src: https://github.com/corretto/corretto-docker/blob/ef6f5a60332e35d72fee88ce86e195f62efa6ab4/17/jdk/alpine/3.17/Dockerfile

RUN wget -O /THIRD-PARTY-LICENSES-20200824.tar.gz https://corretto.aws/downloads/resources/licenses/alpine/THIRD-PARTY-LICENSES-20200824.tar.gz && \
    echo "82f3e50e71b2aee21321b2b33de372feed5befad6ef2196ddec92311bc09becb  /THIRD-PARTY-LICENSES-20200824.tar.gz" | sha256sum -c - && \
    tar x -ovzf THIRD-PARTY-LICENSES-20200824.tar.gz && \
    rm -rf THIRD-PARTY-LICENSES-20200824.tar.gz && \
    wget -O /etc/apk/keys/amazoncorretto.rsa.pub https://apk.corretto.aws/amazoncorretto.rsa.pub && \
    SHA_SUM="6cfdf08be09f32ca298e2d5bd4a359ee2b275765c09b56d514624bf831eafb91" && \
    echo "${SHA_SUM}  /etc/apk/keys/amazoncorretto.rsa.pub" | sha256sum -c - && \
    echo "https://apk.corretto.aws" >> /etc/apk/repositories && \
    apk add --no-cache amazon-corretto-17=$version-r0

ENV LANG C.UTF-8

ENV JAVA_HOME=/usr/lib/jvm/default-jvm
ENV PATH=$PATH:/usr/lib/jvm/default-jvm/bin

# Install Maven 3.9.2, src: https://github.com/carlossg/docker-maven/blob/5f8a86d716eb63fb5a1ef03e5cb743f5df4ffa0a/eclipse-temurin-17-alpine/Dockerfile

ENV MAVEN_HOME /usr/share/maven

COPY --from=maven:3.9.2-eclipse-temurin-11 ${MAVEN_HOME} ${MAVEN_HOME}
COPY --from=maven:3.9.2-eclipse-temurin-11 /usr/local/bin/mvn-entrypoint.sh /usr/local/bin/mvn-entrypoint.sh
COPY --from=maven:3.9.2-eclipse-temurin-11 /usr/share/maven/ref/settings-docker.xml /usr/share/maven/ref/settings-docker.xml

RUN ln -s ${MAVEN_HOME}/bin/mvn /usr/bin/mvn

ARG MAVEN_VERSION=3.9.2
ARG USER_HOME_DIR="/root"
ENV MAVEN_CONFIG "$USER_HOME_DIR/.m2"

WORKDIR /tmp
COPY . .
RUN ./build.sh

# Use Amazon Corretto as runtime
FROM amazoncorretto:17.0.7-alpine3.17 as runtime
WORKDIR /opt
COPY --from=builder /tmp/dist/porting-advisor-linux-x86_64 /opt/
ENTRYPOINT ["./porting-advisor-linux-x86_64"]
