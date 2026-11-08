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
    @Test void letterGradeReturnsCFor75() { assertEquals("C", calculator.letterGrade(75)); }
    @Test void letterGradeReturnsDFor65() { assertEquals("D", calculator.letterGrade(65)); }
    @Test void letterGradeReturnsFFor50() { assertEquals("F", calculator.letterGrade(50)); }
    @Test void letterGradeRejectsNegativeScore() { assertThrows(IllegalArgumentException.class, () -> calculator.letterGrade(-1)); }
    @Test void letterGradeRejectsScoreAbove100() { assertThrows(IllegalArgumentException.class, () -> calculator.letterGrade(101)); }
    @Test void gpaRejectsNullScores() { assertThrows(IllegalArgumentException.class, () -> calculator.gpa(null)); }
    @Test void gpaRejectsEmptyScores() { assertThrows(IllegalArgumentException.class, () -> calculator.gpa(new double[]{})); }
    @Test void gpaHandlesEveryGrade() { assertEquals(2.0, calculator.gpa(new double[]{95,85,75,65,50}), 1e-9); }
    @Test void scholarshipRejectsNegativeGpa() { assertThrows(IllegalArgumentException.class, () -> calculator.scholarship(-0.1,16,false)); }
    @Test void scholarshipRejectsGpaAboveFour() { assertThrows(IllegalArgumentException.class, () -> calculator.scholarship(4.1,16,false)); }
    @Test void scholarshipRejectsNegativeCredits() { assertThrows(IllegalArgumentException.class, () -> calculator.scholarship(3.9,-1,false)); }
    @Test void scholarshipReturnsZeroForViolation() { assertEquals(0, calculator.scholarship(3.9,16,true)); }
    @Test void scholarshipAwards70WhenCreditsBelow15() { assertEquals(70, calculator.scholarship(3.9,14,false)); }
    @Test void scholarshipAwards50WhenCreditsBelow12() { assertEquals(50, calculator.scholarship(3.5,11,false)); }
    @Test void scholarshipReturnsZeroBelowGpa3() { assertEquals(0, calculator.scholarship(2.9,16,false)); }
}
