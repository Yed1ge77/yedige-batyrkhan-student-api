package kz.iitu.yedige.studentapi;

import java.util.Optional;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class StudentServiceTest {
    private final StudentRepository repository = mock(StudentRepository.class);
    private final StudentService service = new StudentService(repository);
    @Test void missingStudentHasClearError() {
        when(repository.findById(38419L)).thenReturn(Optional.empty());
        assertEquals("Student 38419 was not found",
            assertThrows(StudentNotFoundException.class, () -> service.findOne(38419L)).getMessage());
    }
    @Test void updateChangesExistingStudentAndNormalizesEmail() {
        Student student = new Student(new StudentRequest("Old", "Name", "old@example.com", "OLD"));
        when(repository.findById(1L)).thenReturn(Optional.of(student));
        when(repository.saveAndFlush(student)).thenReturn(student);
        StudentResponse result = service.update(1L,
            new StudentRequest("Batyrkhan", "Yedige", "YEDIGE@example.com", "IT2-2302"));
        assertEquals("Batyrkhan", result.firstName());
        assertEquals("yedige@example.com", result.email());
        verify(repository).saveAndFlush(student);
    }
    @Test void deleteMissingStudentNeverDeletesOtherRows() {
        when(repository.findById(1L)).thenReturn(Optional.empty());
        assertThrows(StudentNotFoundException.class, () -> service.delete(1L));
        verify(repository, never()).delete(any());
    }
}
