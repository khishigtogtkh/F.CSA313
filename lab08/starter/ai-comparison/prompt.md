# AI харьцуулалтын генерацийн зорилт

2026-11-03-ны Codex чат дахь баталсан хүсэлт: үндсэн A1–A8 suite болон өөр AI хувилбарыг бэлтгэж, бодитоор ажиллуулан харьцуулах. Хоёр хувилбарт нэг AI туслах оролцсон; энэ нь оюутны бие даан бичсэн тест болон хараат бус AI session-ийн туршилт биш.

## Өөр хувилбарт өгсөн ажлын prompt

> Доорх CourseRegistrationService.java болон Student, StudentRepository, EmailSender гэрээнүүдэд тулгуурлан Mockito-гоор бүрэн тестийн класс бич. JUnit 5, MockitoExtension, constructor injection хэрэглэ. Алдааны тохиолдлуудыг тусдаа энгийн тестээр бичиж, хэрэгтэй stub-уудыг л тухайн тестэд тохируул. Амжилттай бүртгэл, байхгүй/идэвхгүй оюутан, байхгүй хичээл, дутуу prerequisite, SMTP алдаа, аргумент тус бүр болон хоёул null байхыг хамар. Нэмэлтээр prerequisite байхгүй хичээл, repository-ийн жагсаалтыг өөрчлөхгүй байх, repository алдааг дамжуулах зан төлөвийг шалга. И-мэйлийн body-г argThat-аар шалга. Классыг CourseRegistrationServiceAiComparison гэж нэрлэж ердийн mvn test-ийн 10 гүйцэтгэлээс тусгаарла.

Энэ prompt нь хувилбарыг боловсруулахад ашигласан ажлын зорилтыг хадгалсан тэмдэглэл; тусдаа AI үйлчилгээ дуудсан эсвэл шинэ чат нээсэн гэж үзэхгүй. Үүссэн кодыг өөрчлөлтгүй хадгалаад суурь болон гурван мутантад ажиллуулсан бодит гаралтаар харьцуулна.

## Генерацийн оролтын service

```java
package mn.edu.must.sqat;

import java.util.ArrayList;
import java.util.List;

/**
 * Хичээлд бүртгэх үйлчилгээ — Лекц 5-ын бүртгэлийн API-гийн
 * бизнес логик, гэхдээ энэ удаад НЭГЖИЙН түвшинд.
 * Хамаарлууд (repository, emailSender) constructor-оор ирнэ (dependency injection).
 */
public class CourseRegistrationService {

    private final StudentRepository repository;
    private final EmailSender emailSender;

    public CourseRegistrationService(StudentRepository repository, EmailSender emailSender) {
        this.repository = repository;
        this.emailSender = emailSender;
    }

    /**
     * Бүртгэлийн үр дүн:
     *   "OK"                    — амжилттай (бүртгэл хадгалагдаж, мэдэгдэл илгээгдэнэ)
     *   "ERROR_NO_STUDENT"      — оюутан олдсонгүй
     *   "ERROR_INACTIVE_STUDENT"— оюутан идэвхгүй
     *   "ERROR_NO_COURSE"       — хичээл олдсонгүй
     *   "ERROR_PREREQUISITES"   — өмнөх холбоо хичээл дутуу
     * И-мэйл илгээлт АМЖИЛТГҮЙ болсон ч бүртгэл хүчинтэй хэвээр ("OK").
     */
    public String register(String studentId, String courseId) {
        if (studentId == null || courseId == null) {
            throw new IllegalArgumentException("studentId, courseId хоёул шаардлагатай");
        }

        Student student = repository.findStudent(studentId);
        if (student == null) return "ERROR_NO_STUDENT";
        if (!student.active()) return "ERROR_INACTIVE_STUDENT";
        if (!repository.courseExists(courseId)) return "ERROR_NO_COURSE";

        List<String> missing = new ArrayList<>(repository.prerequisites(courseId));
        missing.removeAll(student.coursesTaken());
        if (!missing.isEmpty()) return "ERROR_PREREQUISITES";

        repository.saveRegistration(studentId, courseId);

        try {
            emailSender.send(student.email(),
                    "Бүртгэл баталгаажлаа",
                    courseId + " хичээлд амжилттай бүртгэгдлээ.");
        } catch (RuntimeException e) {
            // Мэдэгдэл чухал боловч бүртгэлийг унагаах ёсгүй.
        }
        return "OK";
    }
}
```

Холбогдох гэрээнүүд: `Student(String id, String email, boolean active, List<String> coursesTaken)` record; `StudentRepository.findStudent`, `courseExists`, `prerequisites`, `saveRegistration`; `EmailSender.send(to, subject, body)`. Репозиторийн эх Java файлууд эдгээр гэрээний бүрэн хувилбар болно.
