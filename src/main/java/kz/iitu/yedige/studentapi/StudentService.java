package kz.iitu.yedige.studentapi;

import java.util.List;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class StudentService {
    private final StudentRepository repository;
    public StudentService(StudentRepository repository) { this.repository = repository; }
    public List<StudentResponse> findAll() {
        return repository.findAll(Sort.by("id")).stream().map(StudentResponse::from).toList();
    }
    public StudentResponse findOne(long id) { return StudentResponse.from(requireStudent(id)); }
    @Transactional
    public StudentResponse create(StudentRequest request) {
        return StudentResponse.from(repository.saveAndFlush(new Student(request)));
    }
    @Transactional
    public StudentResponse update(long id, StudentRequest request) {
        Student student = requireStudent(id);
        student.update(request);
        return StudentResponse.from(repository.saveAndFlush(student));
    }
    @Transactional
    public void delete(long id) {
        repository.delete(requireStudent(id));
        repository.flush();
    }
    private Student requireStudent(long id) {
        return repository.findById(id).orElseThrow(() -> new StudentNotFoundException(id));
    }
}
