# syntax=docker/dockerfile:1
FROM eclipse-temurin:21-jdk-jammy AS build
WORKDIR /workspace
COPY gradlew settings.gradle build.gradle gradle.properties ./
COPY gradle ./gradle
RUN chmod +x gradlew
COPY src ./src
RUN --mount=type=cache,target=/root/.gradle ./gradlew --no-daemon bootJar -x test

FROM eclipse-temurin:21-jre-jammy AS runtime
RUN groupadd --gid 10001 studentapi && useradd --uid 10001 --gid studentapi --no-create-home studentapi
WORKDIR /app
COPY --from=build --chown=10001:10001 /workspace/build/libs/student-api.jar /app/student-api.jar
USER 10001:10001
EXPOSE 8080
ENV JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=65 -XX:+ExitOnOutOfMemoryError"
ENTRYPOINT ["java", "-jar", "/app/student-api.jar"]
