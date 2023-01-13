package com.amazonaws.labs.GravitonReadyAssessor;

import lombok.NonNull;
import lombok.RequiredArgsConstructor;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;
import java.util.logging.Logger;

/**
 * A JAR file scanner that locates native code libraries via simple
 * path-matching. If the file ends in .so and has the strings "aarch64"
 * and "linux", it is considered a match.
 */
@RequiredArgsConstructor
public class JarFileScanner extends JarChecker {
    Logger logger = SimpleLogger.getLogger();

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
        final List<String> sharedLibraryPaths = new ArrayList<>();
        final Enumeration<JarEntry> entries = jarFile.entries();

        while (entries.hasMoreElements()) {
            final JarEntry entry = entries.nextElement();
            final String entryName = entry.getName();

            if (!entry.isDirectory() &&
                    entryName.endsWith(".so") &&
                    entryName.toLowerCase().contains("aarch64") &&
                    entryName.toLowerCase().contains("linux"))
                sharedLibraryPaths.add(entryName);
        }
        return sharedLibraryPaths;
    }
}