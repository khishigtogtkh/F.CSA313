package mn.edu.must.sqat;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class BonusTest {
 @Test void BD1_allDefs_score49to54() { assertEquals(3, DataFlowTargets.bonus(new int[]{1,1,1,1,1,0,1},8)); }
 @Test void BD2_allDefs_score51to56() { assertEquals(5, DataFlowTargets.bonus(new int[]{0,1},1)); }
}
