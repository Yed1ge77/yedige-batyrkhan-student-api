package kz.iitu.yedige.studentapi;

import java.net.URI;
import java.util.List;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/students")
public class StudentController {
    private final StudentService service;
    public StudentController(StudentService service) { this.service = service; }
    @PostMapping
    public ResponseEntity<StudentResponse> create(@Valid @RequestBody StudentRequest request) {
        StudentResponse student = service.create(request);
        return ResponseEntity.created(URI.create("/api/students/" + student.id())).body(student);
    }
    @GetMapping public List<StudentResponse> findAll() { return service.findAll(); }
    @GetMapping("/{id}") public StudentResponse findOne(@PathVariable long id) { return service.findOne(id); }
    @PutMapping("/{id}") public StudentResponse update(@PathVariable long id, @Valid @RequestBody StudentRequest request) {
        return service.update(id, request);
    }
    @DeleteMapping("/{id}") public ResponseEntity<Void> delete(@PathVariable long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
