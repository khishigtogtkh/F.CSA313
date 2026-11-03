package mn.edu.must.sqat;

import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.lenient;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CourseRegistrationServiceTest {
    private static final String STUDENT_ID = "B232270806";
    private static final String COURSE_ID = "F.CSA313";
    private static final String EMAIL = "student@example.edu";
    private static final String SUBJECT = "Бүртгэл баталгаажлаа";

    @Mock StudentRepository repository;
    @Mock EmailSender emailSender;
    private CourseRegistrationService service;

    @BeforeEach
    void setUp() {
        service = new CourseRegistrationService(repository, emailSender);
    }

    // A1: A completed prerequisite must actually be removed from the missing list.
    @Test
    void register_activeStudent_returnsOkAndSavesAndSendsEmail() {
        stubEligibleStudent();

        assertEquals("OK", service.register(STUDENT_ID, COURSE_ID));

        verify(repository).saveRegistration(STUDENT_ID, COURSE_ID);
        verify(emailSender).send(EMAIL, SUBJECT,
                COURSE_ID + " хичээлд амжилттай бүртгэгдлээ.");
    }

    // A2
    @Test
    void register_missingStudent_returnsNoStudentWithoutSavingOrEmail() {
        when(repository.findStudent(STUDENT_ID)).thenReturn(null);

        assertEquals("ERROR_NO_STUDENT", service.register(STUDENT_ID, COURSE_ID));

        verify(repository, never()).saveRegistration(anyString(), anyString());
        verify(emailSender, never()).send(anyString(), anyString(), anyString());
    }

    // A3
    @Test
    void register_inactiveStudent_returnsInactiveWithoutSavingOrEmail() {
        when(repository.findStudent(STUDENT_ID))
                .thenReturn(new Student(STUDENT_ID, EMAIL, false, List.of()));

        assertEquals("ERROR_INACTIVE_STUDENT", service.register(STUDENT_ID, COURSE_ID));

        verify(repository, never()).saveRegistration(anyString(), anyString());
        verifyNoInteractions(emailSender);
    }

    // A4: One completed prerequisite does not compensate for another missing one.
    @Test
    void register_missingPrerequisite_returnsPrerequisitesWithoutSavingOrEmail() {
        when(repository.findStudent(STUDENT_ID))
                .thenReturn(new Student(STUDENT_ID, EMAIL, true, List.of("F.CSA211")));
        when(repository.courseExists(COURSE_ID)).thenReturn(true);
        when(repository.prerequisites(COURSE_ID)).thenReturn(List.of("F.CSA211", "F.CSA212"));

        assertEquals("ERROR_PREREQUISITES", service.register(STUDENT_ID, COURSE_ID));

        verify(repository, never()).saveRegistration(anyString(), anyString());
        verifyNoInteractions(emailSender);
    }

    // A5
    @Test
    void register_emailFailure_returnsOkAndKeepsRegistration() {
        stubEligibleStudent();
        doThrow(new RuntimeException("SMTP unavailable"))
                .when(emailSender).send(eq(EMAIL), eq(SUBJECT), anyString());

        assertEquals("OK", service.register(STUDENT_ID, COURSE_ID));

        verify(repository).saveRegistration(STUDENT_ID, COURSE_ID);
        verify(emailSender).send(eq(EMAIL), eq(SUBJECT), anyString());
    }

    // A6: Both independent null guards are checked within one test execution.
    @Test
    void register_eitherIdNull_throwsWithoutDependencyInteractions() {
        assertThrows(IllegalArgumentException.class, () -> service.register(null, COURSE_ID));
        assertThrows(IllegalArgumentException.class, () -> service.register(STUDENT_ID, null));

        verifyNoInteractions(repository, emailSender);
    }

    // A7
    @Test
    void register_success_emailBodyContainsCourseId() {
        stubEligibleStudent();
        ArgumentCaptor<String> body = ArgumentCaptor.forClass(String.class);

        assertEquals("OK", service.register(STUDENT_ID, COURSE_ID));

        verify(emailSender).send(eq(EMAIL), eq(SUBJECT), body.capture());
        assertTrue(body.getValue().contains(COURSE_ID));
    }

    // A8: Three rows are three executions; the class therefore runs exactly ten tests.
    @ParameterizedTest(name = "A8 [{index}] {0} -> {2}")
    @CsvSource({
        "missing, true, ERROR_NO_STUDENT",
        "inactive, true, ERROR_INACTIVE_STUDENT",
        "missingCourse, false, ERROR_NO_COURSE"
    })
    void register_invalidState_returnsExpectedError(String scenario,
                                                    boolean courseExists,
                                                    String expected) {
        Student student = scenario.equals("missing") ? null
                : new Student(STUDENT_ID, EMAIL, !scenario.equals("inactive"), List.of());
        when(repository.findStudent(STUDENT_ID)).thenReturn(student);
        // Early-return rows do not reach this shared stub; keep other stubs strict.
        lenient().when(repository.courseExists(COURSE_ID)).thenReturn(courseExists);

        assertEquals(expected, service.register(STUDENT_ID, COURSE_ID));

        verify(repository, never()).saveRegistration(anyString(), anyString());
        verifyNoInteractions(emailSender);
    }

    private void stubEligibleStudent() {
        when(repository.findStudent(STUDENT_ID)).thenReturn(
                new Student(STUDENT_ID, EMAIL, true, List.of("F.CSA211", "F.CSA101")));
        when(repository.courseExists(COURSE_ID)).thenReturn(true);
        when(repository.prerequisites(COURSE_ID)).thenReturn(List.of("F.CSA211"));
    }
}
