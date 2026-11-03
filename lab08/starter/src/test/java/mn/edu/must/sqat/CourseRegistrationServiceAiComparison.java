package mn.edu.must.sqat;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.argThat;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

/** Alternative AI-assisted design; run explicitly with -Dtest=CourseRegistrationServiceAiComparison. */
@ExtendWith(MockitoExtension.class)
class CourseRegistrationServiceAiComparison {
    private static final String SID = "B232270806";
    private static final String CID = "F.CSA313";
    private static final String EMAIL = "student@example.edu";

    @Mock StudentRepository repository;
    @Mock EmailSender emailSender;
    private CourseRegistrationService service;

    @BeforeEach
    void setUp() {
        service = new CourseRegistrationService(repository, emailSender);
    }

    @Test
    void register_eligibleStudent_savesAndSendsCourseNotification() {
        eligible(List.of("F.CSA211"), List.of("F.CSA211"));

        assertEquals("OK", service.register(SID, CID));

        verify(repository).saveRegistration(SID, CID);
        verify(emailSender).send(eq(EMAIL), eq("Бүртгэл баталгаажлаа"),
                argThat(body -> body != null && body.contains(CID)));
    }

    @Test
    void register_unknownStudent_rejectsWithoutSavingOrEmail() {
        when(repository.findStudent(SID)).thenReturn(null);

        assertEquals("ERROR_NO_STUDENT", service.register(SID, CID));

        verify(repository, never()).saveRegistration(anyString(), anyString());
        verifyNoInteractions(emailSender);
    }

    @Test
    void register_inactiveStudent_rejectsWithoutSavingOrEmail() {
        when(repository.findStudent(SID)).thenReturn(new Student(SID, EMAIL, false, List.of()));

        assertEquals("ERROR_INACTIVE_STUDENT", service.register(SID, CID));

        verify(repository, never()).saveRegistration(anyString(), anyString());
        verifyNoInteractions(emailSender);
    }

    @Test
    void register_unknownCourse_rejectsWithoutSavingOrEmail() {
        when(repository.findStudent(SID)).thenReturn(new Student(SID, EMAIL, true, List.of()));
        when(repository.courseExists(CID)).thenReturn(false);

        assertEquals("ERROR_NO_COURSE", service.register(SID, CID));

        verify(repository, never()).saveRegistration(anyString(), anyString());
        verifyNoInteractions(emailSender);
    }

    @Test
    void register_onePrerequisiteMissing_rejectsWithoutSavingOrEmail() {
        eligible(List.of("F.CSA211"), List.of("F.CSA211", "F.CSA212"));

        assertEquals("ERROR_PREREQUISITES", service.register(SID, CID));

        verify(repository, never()).saveRegistration(anyString(), anyString());
        verifyNoInteractions(emailSender);
    }

    @Test
    void register_smtpFailure_returnsOkAfterSaving() {
        eligible(List.of("F.CSA211"), List.of("F.CSA211"));
        doThrow(new RuntimeException("SMTP unavailable"))
                .when(emailSender).send(eq(EMAIL), anyString(), anyString());

        assertEquals("OK", service.register(SID, CID));

        verify(repository).saveRegistration(SID, CID);
        verify(emailSender).send(eq(EMAIL), anyString(), anyString());
    }

    @Test
    void register_nullStudentId_throwsBeforeUsingDependencies() {
        assertThrows(IllegalArgumentException.class, () -> service.register(null, CID));
        verifyNoInteractions(repository, emailSender);
    }

    @Test
    void register_nullCourseId_throwsBeforeUsingDependencies() {
        assertThrows(IllegalArgumentException.class, () -> service.register(SID, null));
        verifyNoInteractions(repository, emailSender);
    }

    @Test
    void register_bothIdsNull_throwsBeforeUsingDependencies() {
        assertThrows(IllegalArgumentException.class, () -> service.register(null, null));
        verifyNoInteractions(repository, emailSender);
    }

    @Test
    void register_noPrerequisites_acceptsStudentWithNoCompletedCourses() {
        eligible(List.of(), List.of());

        assertEquals("OK", service.register(SID, CID));

        verify(repository).saveRegistration(SID, CID);
        verify(emailSender).send(eq(EMAIL), anyString(), anyString());
    }

    @Test
    void register_completedPrerequisite_doesNotMutateRepositoryList() {
        List<String> prerequisites = new ArrayList<>(List.of("F.CSA211"));
        eligible(List.of("F.CSA211"), prerequisites);

        assertEquals("OK", service.register(SID, CID));

        assertEquals(List.of("F.CSA211"), prerequisites);
    }

    @Test
    void register_repositoryFailure_propagatesSameExceptionWithoutEmail() {
        IllegalStateException unavailable = new IllegalStateException("Database unavailable");
        when(repository.findStudent(SID)).thenThrow(unavailable);

        assertSame(unavailable,
                assertThrows(IllegalStateException.class, () -> service.register(SID, CID)));

        verify(repository, never()).saveRegistration(anyString(), anyString());
        verifyNoInteractions(emailSender);
    }

    private void eligible(List<String> completed, List<String> prerequisites) {
        when(repository.findStudent(SID)).thenReturn(new Student(SID, EMAIL, true, completed));
        when(repository.courseExists(CID)).thenReturn(true);
        when(repository.prerequisites(CID)).thenReturn(prerequisites);
    }
}
