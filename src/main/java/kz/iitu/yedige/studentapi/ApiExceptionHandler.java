package kz.iitu.yedige.studentapi;

import java.time.Instant;
import java.util.Map;
import java.util.TreeMap;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.*;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;

@RestControllerAdvice
public class ApiExceptionHandler {
    public record ApiError(Instant timestamp, int status, String error, String message,
                           String path, Map<String, String> fields) { }
    @ExceptionHandler(StudentNotFoundException.class)
    ResponseEntity<ApiError> notFound(StudentNotFoundException ex, HttpServletRequest request) {
        return error(HttpStatus.NOT_FOUND, ex.getMessage(), request, Map.of());
    }
    @ExceptionHandler(MethodArgumentNotValidException.class)
    ResponseEntity<ApiError> validation(MethodArgumentNotValidException ex, HttpServletRequest request) {
        Map<String, String> fields = new TreeMap<>();
        ex.getBindingResult().getFieldErrors().forEach(e -> fields.put(e.getField(), e.getDefaultMessage()));
        return error(HttpStatus.BAD_REQUEST, "Request validation failed", request, fields);
    }
    @ExceptionHandler({HttpMessageNotReadableException.class, MethodArgumentTypeMismatchException.class})
    ResponseEntity<ApiError> malformed(Exception ex, HttpServletRequest request) {
        return error(HttpStatus.BAD_REQUEST, "Malformed JSON or invalid path parameter", request, Map.of());
    }
    @ExceptionHandler(DataIntegrityViolationException.class)
    ResponseEntity<ApiError> conflict(DataIntegrityViolationException ex, HttpServletRequest request) {
        return error(HttpStatus.CONFLICT, "A student with this email already exists", request, Map.of());
    }
    private ResponseEntity<ApiError> error(HttpStatus status, String message, HttpServletRequest request,
                                            Map<String, String> fields) {
        return ResponseEntity.status(status).body(new ApiError(Instant.now(), status.value(),
            status.getReasonPhrase(), message, request.getRequestURI(), fields));
    }
}
