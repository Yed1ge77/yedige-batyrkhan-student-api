package kz.iitu.yedige.studentapi;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class StudentNormalizationTest {
    @Test void normalizesPersonalEmail() {
        var student = new Student(new StudentRequest("Batyrkhan", "Yedige",
            "  Batyrkhan.Yedige@EXAMPLE.COM  ", "IT2-2302"));
        // Correct contract: email is trimmed and normalized to lower case.
        assertEquals("batyrkhan.yedige@example.com", student.getEmail());
    }
}
