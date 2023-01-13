package com.amazonaws.labs.GravitonReadyAssessor;

import java.net.URL;
import java.util.Date;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.ser.std.ToStringSerializer;
import lombok.Builder;
import lombok.Data;
import lombok.extern.jackson.Jacksonized;
import org.osgi.framework.VersionRange;

@Data
@Builder
@Jacksonized
public class ClassInfo {
    private String implementationTitle;
    private String implementationVendor;

    @JsonSerialize(using = ToStringSerializer.class)
    private VersionRange implementationVersionRange;

    private String specificationTitle;
    private String specificationVendor;

    @JsonSerialize(using = ToStringSerializer.class)
    private VersionRange specificationVersionRange;

    private String status;
    private String description;
    private URL url;

    @JsonFormat(shape = JsonFormat.Shape.STRING)
    private Date lastUpdated;
}
