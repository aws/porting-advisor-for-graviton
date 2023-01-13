package com.amazonaws.labs.GravitonReadyAssessor;

import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;

/**
 * A record in a Bundle-NativeCode JAR manifest attribute.
 */
public class NativeCodeManifestRecord {
    @Getter
    @Setter
    private String libpath;

    private final List<String> osnames = new ArrayList<>();
    private final List<String> arches = new ArrayList<>();

    /**
     * Creates a NativeCodeManifestRecord from its string representation.
     * @param text The raw text
     * @return a NativeCodeManifestRecord
     */
    public static NativeCodeManifestRecord fromString(@NonNull String text) {
        NativeCodeManifestRecord entry = new NativeCodeManifestRecord();
        List<String> kvPairs = List.of(text.split(";"));
        entry.setLibpath(kvPairs.get(0));
        // Record any processor architectures or OS names found within
        kvPairs.stream().skip(1).forEach(pair -> {
            String key = pair.split("=")[0];
            String val = pair.split("=")[1];
            if (key.equals("osname")) {
                entry.addOSName(val);
            }
            if (key.equals("processor")) {
                entry.addArch(val);
            }
        });
        return entry;
    }

    public void addOSName(String osName) {
        osnames.add(osName);
    }

    public void addArch(String arch) {
        arches.add(arch);
    }

    public boolean isLinux() {
        return osnames.stream().anyMatch(name -> name.equalsIgnoreCase("linux"));
    }

    public boolean isAarch64() {
        return arches.stream().anyMatch(name -> name.equalsIgnoreCase("aarch64"));
    }

    @Override
    public String toString() {
        return "libpath: " + libpath + "; arches=" + this.arches + "; osnames=" + this.osnames;
    }
}
