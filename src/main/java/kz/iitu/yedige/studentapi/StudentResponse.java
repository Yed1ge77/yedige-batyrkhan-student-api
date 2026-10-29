package kz.iitu.yedige.studentapi;

public record StudentResponse(Long id, String firstName, String lastName, String email, String groupName) {
    static StudentResponse from(Student student) {
        return new StudentResponse(student.getId(), student.getFirstName(), student.getLastName(),
            student.getEmail(), student.getGroupName());
    }
}
