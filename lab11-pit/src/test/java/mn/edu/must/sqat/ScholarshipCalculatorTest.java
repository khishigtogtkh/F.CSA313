package mn.edu.must.sqat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ScholarshipCalculatorTest {

    private ScholarshipCalculator calc;

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

    @ParameterizedTest
    @CsvSource({
        "90, A", "89.99, B",
        "80, B", "79.99, C",
        "70, C", "69.99, D",
        "60, D", "59.99, F",
        "0, F", "100, A"
    })
    void letterGrade_returnsExpectedGradeAtBoundaries(double score, String expected) {
        assertEquals(expected, calc.letterGrade(score));
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

    @ParameterizedTest
    @CsvSource({"95, 4.0", "85, 3.0", "75, 2.0", "65, 1.0", "40, 0.0"})
    void gpa_convertsEachGradeToItsExactPoints(double score, double expected) {
        assertEquals(expected, calc.gpa(new double[]{score}));
    }

    @Test
    void gpa_dividesMixedGradePointsByAllScores() {
        assertEquals(2.25, calc.gpa(new double[]{95, 85, 40, 75}));
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
        assertThrows(IllegalArgumentException.class, () -> calc.scholarship(-0.01, 12, false));
        assertThrows(IllegalArgumentException.class, () -> calc.scholarship(4.1, 10, false));
        assertThrows(IllegalArgumentException.class, () -> calc.scholarship(3.0, -1, false));
    }

    @Test
    void scholarship_awards100AtTopGpaAndCreditThresholds() {
        assertEquals(100, calc.scholarship(3.8, 15, false));
    }

    @ParameterizedTest
    @CsvSource({
        "3.8, 16, 100", "3.9, 15, 100",
        "3.79, 15, 70", "3.8, 14, 70",
        "3.4, 12, 70", "3.4, 13, 70", "3.5, 12, 70",
        "3.39, 12, 50", "3.4, 11, 50",
        "3.0, 0, 50", "2.99, 20, 0",
        "0.0, 0, 0", "0.0, 12, 0", "4.0, 15, 100"
    })
    void scholarship_appliesGpaAndCreditBoundaries(double gpa, int credits, int expected) {
        assertEquals(expected, calc.scholarship(gpa, credits, false));
    }
}
