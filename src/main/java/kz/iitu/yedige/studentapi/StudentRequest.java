package kz.iitu.yedige.studentapi;

import jakarta.validation.constraints.*;

public record StudentRequest(
    @NotBlank @Size(max = 100) String firstName,
    @NotBlank @Size(max = 100) String lastName,
    @NotBlank @Email @Size(max = 254) String email,
    @NotBlank @Size(max = 50) String groupName
) { }
