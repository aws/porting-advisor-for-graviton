package com.amazonaws.labs.GravitonReadyAssessor;

import lombok.Getter;
import lombok.NonNull;

import java.io.IOException;
import java.util.Arrays;
import java.util.jar.Attributes;
import java.util.jar.JarFile;
import java.util.jar.Manifest;
import java.util.List;
import java.util.stream.Collectors;

/**
 * <p>A native code bundle JAR manifest entry.</p>
 *
 * <p>JAR files have
 * <a href="https://docs.oracle.com/javase/tutorial/deployment/jar/manifestindex.html">manifests</a>
 * in them which contain various metadata in them. These metadata are known as
 * <a href="https://docs.oracle.com/javase/tutorial/deployment/jar/secman.html">attributes</a>. Some
 * JAR files have a <code>Bundle-NativeCode</code> attribute in them that indicates where native code
 * can be found. The format of this attribute's value is defined by the OSGI Framework and is
 * documented <a href="http://docs.osgi.org/specification/osgi.core/7.0.0/framework.module.html#framework.module-loading.native.code.libraries">here</a>.</p>
 */
public class NativeCodeManifest {
    final static String BundleNativeCode = "Bundle-NativeCode";

    @Getter
    private List<NativeCodeManifestRecord> records;

    /**
     * Constructs a NativeCodeManifest from a JarFile object.
     * @param jarFile the JarFile
     * @return the NativeCodeManifest
     * @throws IOException
     */
    public static NativeCodeManifest fromJarFile(@NonNull JarFile jarFile) throws IOException {
        Manifest manifest = jarFile.getManifest();
        Attributes attrs = manifest.getMainAttributes();
        String bundleNativeCode = attrs.getValue(BundleNativeCode);

        if (bundleNativeCode == null) return null;

        return fromString(bundleNativeCode);
    }

    /**
     * Constructs a NativeCodeManifest from a JarFile object.
     * @param attributeValue the value of the Bundle-NativeCode Manifest attribute
     * @return the NativeCodeManifest
     */
    private static NativeCodeManifest fromString(@NonNull String attributeValue) {
        NativeCodeManifest manifest = new NativeCodeManifest();

        // Records are separated by `,`
        manifest.records = Arrays.stream(attributeValue.split(","))
                .map(String::trim)
                .map(NativeCodeManifestRecord::fromString)
                .collect(Collectors.toUnmodifiableList());
        return manifest;
    }
}
