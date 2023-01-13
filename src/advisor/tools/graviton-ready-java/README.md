AWS Graviton-Ready Assessor for Java
====================================

Contributed by [Michael Fischer](https://github.com/otterley)

This application can help you determine whether your Java application is ready
to run on AWS Graviton EC2 instances, Lambda functions, or Fargate tasks. More
information about AWS Graviton can be found
[here](https://aws.amazon.com/ec2/graviton/).

Many Java applications are ready to run on Graviton without modification. In
particular, pure Java applications that do not use Java Native Interface (JNI)
will often run seamlessly with no changes at all. Many third-party and Open
Source applications that have native libraries will also run without
modification, if they ship with those native libraries for the aarch64
architecture on Linux.

To determine whether your application is ready to run on Graviton, simply run
this application and point it at your JAR or WAR file, or a folder that contains
your JAR and/or WAR files. If your application is "clean" (i.e., it has no
native libraries, or all native libraries are available for aarch64 on Linux),
it will tell you. If there are native libraries missing, it will try to inform
you of the actions you can take to make your application or its dependencies
compatible with Graviton.
