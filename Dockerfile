FROM public.ecr.aws/amazonlinux/amazonlinux:2023.0.20230503.0 as builder
# Should I lock the version here?
# ARG JAVA_VER=1:17.0.7+7-1.amzn2023.1
# ARG MAVEN_VER=1:3.8.4-3.amzn2023.0.4
# ARG PYTHON_VER=3.11.2-2.amzn2023.0.6
# ARG PIP_VER=22.3.1-2.amzn2023.0.2
# RUN yum install java-17-amazon-corretto-${JAVA_VER} python3.11-${PYTHON_VER} python3.11-pip-${PIP_VER} maven-${MAVEN_VER} -y

RUN yum install java-17-amazon-corretto python3.11 python3.11-pip maven binutils -y && \
    yum clean all

ENV JAVA_HOME=/usr/lib/jvm/java
ENV MAVEN_HOME=/usr/share/maven

COPY . .
RUN /usr/bin/python3.11 -m venv .venv && \
    source .venv/bin/activate && \
    python3 -m pip install -r requirements-build.txt && \
    ./build.sh

RUN mv dist/porting-advisor-linux-$(uname -m) /opt/porting-advisor

# Use Amazon Corretto as runtime
FROM public.ecr.aws/amazoncorretto/amazoncorretto:17.0.7-al2023 as runtime
COPY --from=builder /opt/porting-advisor /usr/bin/porting-advisor
ENTRYPOINT ["/usr/bin/porting-advisor"]
