package kz.iitu.yedige.studentapi;

import java.util.Map;
import org.springframework.boot.info.BuildProperties;
import org.springframework.web.bind.annotation.*;

@RestController
public class InfoController {
    private final BuildProperties build;
    public InfoController(BuildProperties build) { this.build = build; }
    @GetMapping("/api/info")
    public Map<String, String> info() {
        return Map.of("student", "Batyrkhan Yedige Yerlanuly", "group", "IT2-2302",
            "studentId", "38419", "university", "IITU", "version", build.getVersion());
    }
}
