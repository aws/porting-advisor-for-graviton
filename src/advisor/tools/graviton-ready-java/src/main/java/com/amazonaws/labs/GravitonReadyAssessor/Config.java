package com.amazonaws.labs.GravitonReadyAssessor;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.Builder;
import lombok.Data;
import lombok.Singular;
import lombok.extern.jackson.Jacksonized;

import java.io.IOException;
import java.net.URL;
import java.util.List;

@Data
@Builder
@Jacksonized
public class Config {
    @JsonProperty("classes")
    @Singular public List<ClassInfo> classInfos;

    public static Config fromURL(URL url) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readerFor(Config.class).readValue(url);
    }

    public static Config fromJson(String s) throws JsonProcessingException, JsonMappingException {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readerFor(Config.class).readValue(s);
    }

    public String toJson() throws JsonProcessingException {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.writerWithDefaultPrettyPrinter().writeValueAsString(this);
    }
}
