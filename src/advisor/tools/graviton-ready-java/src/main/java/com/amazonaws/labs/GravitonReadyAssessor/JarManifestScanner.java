package com.amazonaws.labs.GravitonReadyAssessor;

import lombok.NonNull;
import lombok.RequiredArgsConstructor;

import java.io.IOException;
import java.util.List;
import java.util.jar.JarFile;
import java.util.stream.Collectors;

/**
 * A JAR file scanner that locates native code libraries by looking at
 * the JAR's manifest. It uses the OSGI <code>Bundle-NativeCode</code>
 * attribute for this purpose.
 */
@RequiredArgsConstructor
public class JarManifestScanner extends JarChecker {
    @NonNull
    private JarFile jarFile;

    /**
     * Return a list of path names corresponding to shared library files
     * in the JAR file.
     *
     * @return list of shared library pathnames
     * @throws IOException
     */
    public List<String> getSharedLibraryPaths() throws IOException {
        NativeCodeManifest manifest = NativeCodeManifest.fromJarFile(this.jarFile);

        // No native code manifest found
        if (manifest == null) return List.of();

        return manifest.getRecords().stream()
                .filter(NativeCodeManifestRecord::isAarch64)
                .filter(NativeCodeManifestRecord::isLinux)
                .map(NativeCodeManifestRecord::getLibpath)
                .collect(Collectors.toList());
    }
}