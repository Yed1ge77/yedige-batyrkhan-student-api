package kz.iitu.yedige.studentapi;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class StudentNormalizationTest {
    @Test void normalizesPersonalEmail() {
        var student = new Student(new StudentRequest("Batyrkhan", "Yedige",
            "  Batyrkhan.Yedige@EXAMPLE.COM  ", "IT2-2302"));
        // Controlled failure on an isolated branch, never merged to main.
        assertEquals("WRONG-EXPECTED-EMAIL", student.getEmail());
    }
}
