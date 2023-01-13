package com.amazonaws.labs.GravitonReadyAssessor;

import java.io.IOException;
import java.util.List;

public interface JarCheckerInterface {
    List<String> getSharedLibraryPaths() throws IOException;
}
