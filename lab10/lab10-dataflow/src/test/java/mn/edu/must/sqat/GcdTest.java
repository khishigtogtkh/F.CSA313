package mn.edu.must.sqat;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class GcdTest {
 @Test void gcdZeroY_13to20() { assertEquals(7, DataFlowTargets.gcd(7,0)); }
 @Test void gcdTwoIterations_13_15_16_17_18_20() { assertEquals(4, DataFlowTargets.gcd(12,8)); }
 @Test void gcdZeroX_13_16_20() { assertEquals(5, DataFlowTargets.gcd(0,5)); }
}
