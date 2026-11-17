package mn.edu.must.sqat;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class BonusTest {
 @Test void BD1_allDefs_score49to54() { assertEquals(3, DataFlowTargets.bonus(new int[]{1,1,1,1,1,0,1},8)); }
 @Test void BD2_allDefs_score51to56() { assertEquals(5, DataFlowTargets.bonus(new int[]{0,1},1)); }
 @Test void BD3_duWitness() { assertEquals(0, DataFlowTargets.bonus(new int[]{},1)); }
 @Test void BD4_duWitness() { assertEquals(5, DataFlowTargets.bonus(new int[]{},0)); }
 @Test void BD5_duWitness() { assertEquals(8, DataFlowTargets.bonus(new int[]{1,1,1,1,1},0)); }
 @Test void BD6_duWitness() { assertThrows(IllegalArgumentException.class, () -> DataFlowTargets.bonus(null,0)); }
 @Test void BD7_duWitness() { assertThrows(IllegalArgumentException.class, () -> DataFlowTargets.bonus(new int[]{},-1)); }
 @Test void BX_nullAndNegative() { assertThrows(IllegalArgumentException.class, () -> DataFlowTargets.bonus(null,-1)); }
 @Test void BB_longerThanFive() { assertEquals(8, DataFlowTargets.bonus(new int[]{2,2,2,2,2,2},0)); }
 @Test void BB_negativeMeansAbsent() { assertEquals(5, DataFlowTargets.bonus(new int[]{-1,1},1)); }
}
