# syntax=docker/dockerfile:1
FROM eclipse-temurin:21-jdk-jammy AS build
ARG APP_VERSION=1.0.1
WORKDIR /workspace
COPY gradlew settings.gradle build.gradle gradle.properties ./
COPY gradle ./gradle
RUN chmod +x gradlew
COPY src ./src
RUN --mount=type=cache,target=/root/.gradle ./gradlew --no-daemon -PappVersion=${APP_VERSION} bootJar -x test

FROM eclipse-temurin:21-jre-jammy AS runtime
RUN groupadd --gid 10001 studentapi && useradd --uid 10001 --gid studentapi --no-create-home studentapi
LABEL student.name="Batyrkhan Yedige Yerlanuly" student.id="38419"
WORKDIR /app
COPY --from=build --chown=10001:10001 /workspace/build/libs/student-api.jar /app/student-api.jar
USER 10001:10001
EXPOSE 8080
ENV JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=65 -XX:+ExitOnOutOfMemoryError"
ENTRYPOINT ["java", "-jar", "/app/student-api.jar"]
