package kz.iitu.yedige.studentapi;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

// Deliberately requires a real PostgreSQL database; no H2 and no silently skipped tests.
@SpringBootTest
@AutoConfigureMockMvc
class StudentApiIntegrationTest {
    @Autowired MockMvc mvc;
    @Autowired ObjectMapper mapper;
    @Autowired StudentRepository repository;
    private final StudentRequest request = new StudentRequest("Batyrkhan", "Yedige", "38419@example.com", "IT2-2302");
    @BeforeEach void cleanDatabase() { repository.deleteAll(); }
    private long createStudent() throws Exception {
        String body = mvc.perform(post("/api/students").contentType(MediaType.APPLICATION_JSON)
            .content(mapper.writeValueAsString(request)))
            .andExpect(status().isCreated()).andExpect(header().exists("Location"))
            .andReturn().getResponse().getContentAsString();
        return mapper.readTree(body).get("id").asLong();
    }
    @Test void fullCrudUsesPostgresql() throws Exception {
        long id = createStudent();
        mvc.perform(get("/api/students")).andExpect(status().isOk()).andExpect(jsonPath("$[0].id").value(id));
        mvc.perform(get("/api/students/" + id)).andExpect(status().isOk())
            .andExpect(jsonPath("$.lastName").value("Yedige"));
        var updated = new StudentRequest("Batyrkhan", "Yedige", "updated38419@example.com", "IT2-2302-UPDATED");
        mvc.perform(put("/api/students/" + id).contentType(MediaType.APPLICATION_JSON)
            .content(mapper.writeValueAsString(updated))).andExpect(status().isOk())
            .andExpect(jsonPath("$.groupName").value("IT2-2302-UPDATED"));
        mvc.perform(delete("/api/students/" + id)).andExpect(status().isNoContent());
        mvc.perform(get("/api/students/" + id)).andExpect(status().isNotFound());
    }
    @Test void invalidFieldsReturn400() throws Exception {
        mvc.perform(post("/api/students").contentType(MediaType.APPLICATION_JSON)
            .content("{\"firstName\":\" \",\"lastName\":\"Yedige\",\"email\":\"invalid\",\"groupName\":\"\"}"))
            .andExpect(status().isBadRequest()).andExpect(jsonPath("$.fields.firstName").exists())
            .andExpect(jsonPath("$.fields.email").exists()).andExpect(jsonPath("$.fields.groupName").exists());
    }
    @Test void malformedJsonAndIdReturn400() throws Exception {
        mvc.perform(post("/api/students").contentType(MediaType.APPLICATION_JSON).content("{"))
            .andExpect(status().isBadRequest()).andExpect(jsonPath("$.message").exists());
        mvc.perform(get("/api/students/not-a-number")).andExpect(status().isBadRequest());
    }
    @Test void missingStudentReturns404ForAllOperations() throws Exception {
        mvc.perform(get("/api/students/9999999")).andExpect(status().isNotFound());
        mvc.perform(delete("/api/students/9999999")).andExpect(status().isNotFound());
        mvc.perform(put("/api/students/9999999").contentType(MediaType.APPLICATION_JSON)
            .content(mapper.writeValueAsString(request))).andExpect(status().isNotFound());
    }
    @Test void duplicateEmailReturns409() throws Exception {
        createStudent();
        mvc.perform(post("/api/students").contentType(MediaType.APPLICATION_JSON)
            .content(mapper.writeValueAsString(request))).andExpect(status().isConflict())
            .andExpect(jsonPath("$.message").value("A student with this email already exists"));
    }
    @Test void healthAndPersonalInfoAreAvailable() throws Exception {
        mvc.perform(get("/actuator/health")).andExpect(status().isOk()).andExpect(jsonPath("$.status").value("UP"));
        mvc.perform(get("/api/info")).andExpect(status().isOk())
            .andExpect(jsonPath("$.student").value("Batyrkhan Yedige Yerlanuly"))
            .andExpect(jsonPath("$.version").isNotEmpty());
    }
}
