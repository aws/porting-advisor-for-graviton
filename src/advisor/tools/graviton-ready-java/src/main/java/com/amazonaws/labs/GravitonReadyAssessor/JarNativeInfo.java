package com.amazonaws.labs.GravitonReadyAssessor;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;
import java.util.logging.Logger;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.zip.ZipException;

import static java.nio.file.StandardOpenOption.APPEND;

import lombok.*;

/**
 * JarNativeInfo contains information about native libraries inside a JAR file.
 */
public class JarNativeInfo {
    private final static String[] IGNORED_PREFIXES = {
            "jdk.internal"
    };

    /**
     * The actual on-disk path to the JAR file, which may be a temporary file if the JAR
     * was embedded in another JAR.
     */
    @Getter
    @NonNull
    private Path realJarPath;

    /**
     * Only used for embedded JARs. Points to the path inside the JAR.
     */
    @Getter
    private Path nominalJarPath;

    /**
     * Shared libraries
     */
    @Getter
    private final List<String> sharedLibs = new ArrayList<>();

    /**
     * Native methods
     */
    @Getter
    private final List<Method> nativeMethods = new ArrayList<>();

    /**
     * Native information associated with embedded JARs
     */
    @Getter
    private final List<JarNativeInfo> children = new ArrayList<>();

    final Logger log = SimpleLogger.getLogger();

    static ConcurrentHashMap<Path, ClassLoader> cache = new ConcurrentHashMap<>();

    /**
     * Builds a JarNativeInfo object
     * @param jarPath the path to the JAR file
     * @throws IOException
     */
    public JarNativeInfo(@NonNull Path jarPath) throws IOException {
        this(jarPath, null);
    }

    /**
     * Builds a JarNativeInfo object
     * @param realJarPath the path to the JAR file on disk
     * @param nominalPath for embedded JARs, the path in the enclosing JAR file where this JAR is located
     * @throws IOException
     */
    public JarNativeInfo(@NonNull Path realJarPath, Path nominalPath) throws IOException {
        this.realJarPath = realJarPath;
        this.nominalJarPath = nominalPath;

        if (nominalPath == null) {
            log.info("🛃 Checking JAR " + realJarPath);
        } else {
            log.info("🛃 Checking embedded JAR " + nominalPath.toString());
        }

        try {
            @Cleanup JarFile jarFile = new JarFile(realJarPath.toFile());
            final Enumeration<JarEntry> entries = jarFile.entries();

            while (entries.hasMoreElements()) {
                final JarEntry entry = entries.nextElement();
                final String entryName = entry.getName();

                if (entry.isDirectory()) continue;

                if (entryName.endsWith(".jar")) {
                    // Embedded JAR file
                    // Extract the JAR file to a temporary location
                    @Cleanup InputStream is = jarFile.getInputStream(entry);
                    Path tmpJarPath = Files.createTempFile(null, null);
                    tmpJarPath.toFile().deleteOnExit();
                    @Cleanup OutputStream os = Files.newOutputStream(tmpJarPath, APPEND);
                    is.transferTo(os);
                    // Process the embedded JAR recursively
                    JarNativeInfo nativeInfo = new JarNativeInfo(tmpJarPath, Path.of(entryName));
                    children.add(nativeInfo);
                } else if (entryName.endsWith(".class")) {
                    String className = entryName
                            .substring(0, entry.getName().length() - ".class".length())
                            .replace('/', '.');
                    // Skip JDK internal classes
                    if (Arrays.stream(IGNORED_PREFIXES).anyMatch(className::startsWith))
                        continue;
                    // Load the class and find its native methods
                    Class<?> c = loadClass(className, realJarPath);
                    if (c != null) {
                        try {
                            nativeMethods.addAll(findNativeMethods(c));
                        } catch (NoClassDefFoundError ignored) {
                        }
                    }
                }
            }

            // No need to proceed if there aren't any native methods.
            if (nativeMethods.isEmpty()) return;

            JarChecker scanner;

            // First try to find the shared libraries by scanning the JAR manifest
            scanner = new JarManifestScanner(jarFile);
            sharedLibs.addAll(scanner.getSharedLibraryPaths());

            // Then try to find shared libraries by examining the JAR table of contents
            scanner = new JarFileScanner(jarFile);
            sharedLibs.addAll(scanner.getSharedLibraryPaths());
        } catch (ZipException e) {
            // Treat empty JAR files as though they have no methods at all.
            if (e.getMessage().equals("zip file is empty")) {
                return;
            }
            throw e;
        }
    }

    public boolean hasNativeMethods() {
        return !nativeMethods.isEmpty();
    }

    private List<Method> findNativeMethods(@NonNull Class<?> c) {
        log.fine("🧐 Getting native methods for class " + c.getName());

        return Stream.of(c.getDeclaredMethods())
                .peek(m -> log.finer("Checking method " + m.getName()))
                .filter(m -> Modifier.isNative(m.getModifiers()))
                .collect(Collectors.toList());
    }

    private Class<?> loadClass(@NonNull String name, @NonNull Path jarPath) {
        ClassLoader cl;
        Class<?> cls = null;
        try {
            cl = cache.computeIfAbsent(jarPath, k -> {
                try {
                    URL[] urls = {new URL("jar:file:" + k + "!/")};
                    return new URLClassLoader(urls);
                } catch (MalformedURLException e) {
                    e.printStackTrace();
                    return null;
                }
            });
            assert cl != null;
            cls = cl.loadClass(name);
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (NoClassDefFoundError ignored) {
        }
        return cls;
    }
}
