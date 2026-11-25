package mn.edu.must.sqat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ScholarshipCalculatorTest {

    ScholarshipCalculator calc;

    @BeforeEach
    void setUp() { calc = new ScholarshipCalculator(); }

    @Test
    void letterGrade_returnsExpectedGradeForEachRange() {
        assertEquals("A", calc.letterGrade(95));
        assertEquals("B", calc.letterGrade(85));
        assertEquals("C", calc.letterGrade(75));
        assertEquals("D", calc.letterGrade(65));
        assertEquals("F", calc.letterGrade(30));
    }

    @Test
    void letterGrade_invalidInputs_throw() {
        assertThrows(IllegalArgumentException.class, () -> calc.letterGrade(-1));
        assertThrows(IllegalArgumentException.class, () -> calc.letterGrade(101));
    }

    @Test
    void gpa_returnsExpectedAverage() {
        assertEquals(3.5, calc.gpa(new double[]{95, 85}));
        assertEquals(1.5, calc.gpa(new double[]{75, 65}));
        assertEquals(0.0, calc.gpa(new double[]{40}));
    }

    @Test
    void gpa_invalidInputs_throw() {
        assertThrows(IllegalArgumentException.class, () -> calc.gpa(null));
        assertThrows(IllegalArgumentException.class, () -> calc.gpa(new double[]{}));
    }

    @Test
    void scholarship_returnsExpectedPercentageForEachRule() {
        assertEquals(100, calc.scholarship(3.9, 16, false));
        assertEquals(70, calc.scholarship(3.5, 13, false));
        assertEquals(50, calc.scholarship(3.1, 5, false));
        assertEquals(0, calc.scholarship(2.0, 1, false));
        assertEquals(0, calc.scholarship(4.0, 20, true));
    }

    @Test
    void scholarship_invalidInputs_throw() {
        assertThrows(IllegalArgumentException.class, () -> calc.scholarship(4.1, 10, false));
        assertThrows(IllegalArgumentException.class, () -> calc.scholarship(3.0, -1, false));
    }
}
