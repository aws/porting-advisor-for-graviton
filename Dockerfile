FROM public.ecr.aws/amazonlinux/amazonlinux:2023 as builder

RUN yum install java-17-amazon-corretto python3.11 python3.11-pip maven binutils -y && \
    yum clean all

ENV JAVA_HOME=/usr/lib/jvm/java
ENV MAVEN_HOME=/usr/share/maven

COPY src src/
COPY build.sh setup-environment.sh getBinaryName.sh requirements-build.txt ./
RUN /usr/bin/python3.11 -m venv .venv && \
    source .venv/bin/activate && \
    python3 -m pip install -r requirements-build.txt && \
    FILE_NAME=porting-advisor ./build.sh

RUN mv dist/porting-advisor /opt/porting-advisor

# Use Amazon Corretto as runtime
FROM public.ecr.aws/amazoncorretto/amazoncorretto:17-al2023 as runtime
COPY --from=builder /opt/porting-advisor /usr/bin/porting-advisor
ENTRYPOINT ["/usr/bin/porting-advisor"]
