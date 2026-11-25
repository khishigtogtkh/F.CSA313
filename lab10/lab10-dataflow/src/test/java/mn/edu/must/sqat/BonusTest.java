package mn.edu.must.sqat;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class BonusTest {
 @Test void BD1_allDefs_score49to54() { assertEquals(3, DataFlowTargets.bonus(new int[]{1,1,1,1,1,0,1},8)); }
 @Test void BD2_allDefs_score51to56() { assertEquals(5, DataFlowTargets.bonus(new int[]{0,1},1)); }
 @DisplayName("BD3: attendance 31->32aF, 31->38cF; best 37->53F; present 35->50F; score 49->56; threshold "
     + "31->32bF, 31->50F")
 @Test void BD3_duWitness() { assertEquals(0, DataFlowTargets.bonus(new int[]{},1)); }
 @DisplayName("BD4: attendance 31->32aF, 31->38cF; best 37->53F; present 35->50T; score 51->56; threshold "
     + "31->32bF, 31->50T")
 @Test void BD4_duWitness() { assertEquals(5, DataFlowTargets.bonus(new int[]{},0)); }
 @DisplayName("BD5: a 38d->39T; attendance 31->32aF, 31->38cF, 31->38cT; best 37->42T, 43->42T, 43->53T; "
     + "present 35->40, 40->40, 40->50T; score 51->54, 54->56; streak 36->41, 41->41, 41->42T, "
     + "41->43; threshold 31->32bF, 31->50T")
 @Test void BD5_duWitness() { assertEquals(8, DataFlowTargets.bonus(new int[]{1,1,1,1,1},0)); }
 @DisplayName("BD6: attendance 31->32aT")
 @Test void BD6_duWitness() { assertThrows(IllegalArgumentException.class, () -> DataFlowTargets.bonus(null,0)); }
 @DisplayName("BD7: attendance 31->32aF; threshold 31->32bT")
 @Test void BD7_duWitness() { assertThrows(IllegalArgumentException.class, () -> DataFlowTargets.bonus(new int[]{},-1)); }
 @Test void BX_nullAndNegative() { assertThrows(IllegalArgumentException.class, () -> DataFlowTargets.bonus(null,-1)); }
 @Test void BB_longerThanFive() { assertEquals(8, DataFlowTargets.bonus(new int[]{2,2,2,2,2,2},0)); }
 @Test void BB_negativeMeansAbsent() { assertEquals(5, DataFlowTargets.bonus(new int[]{-1,1},1)); }
 @Test void BM2_separatedRuns_doNotEarnStreakBonus() { assertEquals(0, DataFlowTargets.bonus(new int[]{1,1,1,0,1,1,1,1},8)); }
 @Test void BB_allAbsent() { assertEquals(0, DataFlowTargets.bonus(new int[]{0,0},1)); }
}
