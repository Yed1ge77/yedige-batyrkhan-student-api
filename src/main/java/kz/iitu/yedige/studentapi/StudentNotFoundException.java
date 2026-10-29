package kz.iitu.yedige.studentapi;

public class StudentNotFoundException extends RuntimeException {
    public StudentNotFoundException(long id) { super("Student " + id + " was not found"); }
}
