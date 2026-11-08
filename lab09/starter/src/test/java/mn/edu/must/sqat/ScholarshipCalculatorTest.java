package mn.edu.must.sqat;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ScholarshipCalculatorTest {
    private final ScholarshipCalculator calculator = new ScholarshipCalculator();

    @Test void letterGradeReturnsAFor95() { assertEquals("A", calculator.letterGrade(95)); }
    @Test void letterGradeReturnsBFor85() { assertEquals("B", calculator.letterGrade(85)); }
    @Test void gpaAveragesTwoScores() { assertEquals(3.5, calculator.gpa(new double[]{95,85}), 1e-9); }
    @Test void scholarshipAwards100() { assertEquals(100, calculator.scholarship(3.9,16,false)); }
    @Test void scholarshipAwards70() { assertEquals(70, calculator.scholarship(3.5,12,false)); }
}
