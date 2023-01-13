package com.amazonaws.labs.GravitonReadyAssessor;

import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.*;
import java.lang.reflect.Method;
import java.util.logging.*;
import java.util.stream.Collectors;
import java.util.concurrent.Callable;

import lombok.Getter;
import lombok.NonNull;

import picocli.CommandLine;
import picocli.CommandLine.Option;
import picocli.CommandLine.Parameters;

@CommandLine.Command(name = "Arm64LinuxJarChecker",
        description = "Checks JAR/WAR files for compatibility with Arm64 CPU architecture on Linux",
        mixinStandardHelpOptions = true,
        exitCodeListHeading = "Exit Codes:%n",
        exitCodeList = {
                "0: Successful execution, no problems found",
                "3: Found native classes but no Arm64/Linux shared libraries in JARs"
        })
final public class Command implements Callable<Integer> {
    @Parameters(description = "Files or directories in which JARs are located (default: current working directory)")
    private final List<String> searchPaths = new ArrayList<>();

    @Option(names = {"-v", "--verbose"}, description = "Run verbosely")
    private boolean verbose;

    @Override
    public Integer call() throws IOException {
        int exitCode = 0;

        Logger log = SimpleLogger.getLogger();
        if (verbose) {
            SimpleLogger.setLevel(Level.ALL);
        }

        final class JarSearcher extends SimpleFileVisitor<Path> {
            private final PathMatcher jarFileMatcher = FileSystems.getDefault().getPathMatcher("regex:.*\\.(jar|war)$");

            @Getter
            private final List<Path> nativeJarFiles = new ArrayList<>();
            private final Map<Path, List<String>> nativeLibraryFiles = new HashMap<>();
            private final Map<Path, List<Method>> nativeMethods = new HashMap<>();

            private void processNativeInfo(@NonNull JarNativeInfo info) {
                if (info.hasNativeMethods()) {
                    nativeJarFiles.add(info.getNominalJarPath());
                    nativeLibraryFiles.put(info.getNominalJarPath(), info.getSharedLibs());
                    nativeMethods.put(info.getNominalJarPath(), info.getNativeMethods());
                }
                for (JarNativeInfo childInfo : info.getChildren()) {
                    processNativeInfo(childInfo);
                }
            }

            @Override
            public FileVisitResult visitFile(@NonNull Path path, @NonNull BasicFileAttributes attrs) throws IOException {
                if (!jarFileMatcher.matches(path))
                    return FileVisitResult.CONTINUE;

                processNativeInfo(new JarNativeInfo(path));

                return FileVisitResult.CONTINUE;
            }

            public List<String> getNativeLibraries(Path path) {
                return nativeLibraryFiles.get(path);
            }

            public List<Method> getNativeMethods(Path path) {
                return nativeMethods.get(path);
            }

            public boolean hasNativeJars() {
                return !nativeJarFiles.isEmpty();
            }

            public boolean hasNativeLibraries(Path path) {
                return !nativeLibraryFiles.get(path).isEmpty();
            }
        }

        log.info("🟢 Starting search for native classes in JAR files");

        if (searchPaths.isEmpty()) {
            searchPaths.add("");
        }

        // Search JARs and classes
        JarSearcher finder = new JarSearcher();
        for (String searchPath : searchPaths) {
            Files.walkFileTree(
                    Paths.get(searchPath), // start with current working directory
                    finder);
        }

        final List<Path> nativeJars = finder.getNativeJarFiles();

        if (!finder.hasNativeJars()) {
            log.info("🎉 No native methods found in scanned JAR files. These should work on any supported CPU architecture.");
            System.exit(0);
        }

        for (Path jarPath : nativeJars) {
            log.info("ℹ️  JAR with native methods: " + jarPath);
            log.fine("ℹ️  Methods: " + finder.getNativeMethods(jarPath)
                    .stream()
                    .map(m -> String.format("%s::%s", m.getDeclaringClass().getName(), m.getName()))
                    .distinct()
                    .collect(Collectors.joining(", ")));
            if (finder.hasNativeLibraries(jarPath)) {
                log.info("✅ Native libraries: " +
                        finder.getNativeLibraries(jarPath)
                                .stream()
                                .distinct()
                                .collect(Collectors.joining(", ")));
            } else {
                log.info("🚨 JAR " + jarPath + " has native methods but no libraries found for aarch64/Linux");
                log.info("Native methods: " + finder.getNativeMethods(jarPath).stream().distinct().map(Method::toString).collect(Collectors.joining(", ")));
                exitCode = 3;
            }
        }
        if (exitCode == 0) {
            log.info(String.format("%n🎉 JAR files scanned and native libraries appear to be all there. You're good to go!"));
        } else {
            log.info(String.format("%n🚨 Found JAR files with native methods but no Linux/arm64 support."));
        }

        return exitCode;
    }

    public static void main(String... args) {
        int exitCode = new CommandLine(new Command()).execute(args);
        System.exit(exitCode);
    }
}