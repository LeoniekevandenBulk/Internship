public class ReturnPerf1 {
    private int[][] median;
    private int counter;
    
    public void init(int[][] medianIn, int counterIn) {
        median = medianIn;
        counter = counterIn;
    }
    
    public int[][] getmedian() {
        return median;
    }
    
    public int getcounter() {
        return counter;
    }
}
