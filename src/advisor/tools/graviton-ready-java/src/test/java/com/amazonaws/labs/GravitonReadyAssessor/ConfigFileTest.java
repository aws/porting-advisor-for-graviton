package com.amazonaws.labs.GravitonReadyAssessor;

import com.fasterxml.jackson.core.JsonProcessingException;

import org.junit.Test;

import static org.junit.Assert.*;

import org.osgi.framework.Version;
import org.osgi.framework.VersionRange;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Date;

public class ConfigFileTest {
    @Test
    public void shouldLoadConfigFile() {
        try {
            URL url = new URL("file:src/test/files/config.json");
            Config c = Config.fromURL(url);
            System.out.println(c);
        } catch (IOException e) {
            fail(e.toString());
        }
    }

    @Test
    public void shouldPrintJSON() {
        try {
            Config c = generateConfig();
            System.out.println(c.toJson());
        } catch(JsonProcessingException e) {
            fail(e.toString());
        }
    }

    @Test
    public void shouldSerializeDeserialize() {
        try {
            Config c1 = generateConfig();
            String json = c1.toJson();
            Config c2 = Config.fromJson(json);
            assertEquals(c1, c2);
        } catch(JsonProcessingException e) {
            fail(e.toString());
        }
    }

    @Test
    public void versionInRange() {
        Config config = generateConfig();
        assert(config.getClassInfos().size() == 1);
        ClassInfo info = config.getClassInfos().get(0);
        // TODO
        return;
    }

    private Config generateConfig() {
        try {
            ClassInfo i = ClassInfo.builder()
                    .implementationTitle("ImplementationTitle")
                    .implementationVendor("ImplementationVendor")
                    .implementationVersionRange(
                            new VersionRange(
                                    VersionRange.LEFT_CLOSED, new Version(1, 0, 0),
                                    new Version(2, 0, 0), VersionRange.RIGHT_OPEN)
                    )
                    .specificationTitle("SpecificationTitle")
                    .specificationVendor("SpecificationVendor")
                    .specificationVersionRange(
                            new VersionRange(
                                    VersionRange.LEFT_CLOSED, new Version(1, 0, 0),
                                    new Version(2, 0, 0), VersionRange.RIGHT_OPEN)
                    )
                    .description("Description goes here")
                    .status("OK")
                    .url(new URL("http://example.com"))
                    .lastUpdated(new Date())
                    .build();
            return Config.builder()
                    .classInfo(i)
                    .build();
        } catch (MalformedURLException e) {
            fail(e.toString());
            return null;
        }
    }
}
