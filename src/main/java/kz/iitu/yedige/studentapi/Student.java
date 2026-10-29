package kz.iitu.yedige.studentapi;

import jakarta.persistence.*;

@Entity
@Table(name = "students")
public class Student {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false, length = 100) private String firstName;
    @Column(nullable = false, length = 100) private String lastName;
    @Column(nullable = false, unique = true, length = 254) private String email;
    @Column(nullable = false, length = 50) private String groupName;

    protected Student() { }
    public Student(StudentRequest request) { update(request); }
    public void update(StudentRequest request) {
        firstName = request.firstName().trim();
        lastName = request.lastName().trim();
        email = request.email().trim().toLowerCase(java.util.Locale.ROOT);
        groupName = request.groupName().trim();
    }
    public Long getId() { return id; }
    public String getFirstName() { return firstName; }
    public String getLastName() { return lastName; }
    public String getEmail() { return email; }
    public String getGroupName() { return groupName; }
}
