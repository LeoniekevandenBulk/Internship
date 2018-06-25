import java.util.List;

public class ReturnPerf2 {

	private String trainnumber;
    private String plaats1;
    private String plaats2;
    private String vertrekTijd;
    private String aankomstTijd;
    private int predTrimean;
    private int predARNU;
    private int predSame;
    private int delay;
    
    public void init(String trainnumberIn, String plaats1In, String plaats2In, String vertrekTijdIn, String aankomstTijdIn, int delayIn, int predIn, int ARNUIn, int SameIn) {
        this.trainnumber = trainnumberIn;
        this.plaats1 = plaats1In;
        this.plaats2 = plaats2In;
        this.vertrekTijd = vertrekTijdIn;
        this.aankomstTijd = aankomstTijdIn;
        this.delay = delayIn;
        this.predTrimean = predIn;
        this.predARNU = ARNUIn;
        this.predSame = SameIn;
    }

	/**
	 * @return the trainnumber
	 */
	public String getTrainnumber() {
		return trainnumber;
	}

	/**
	 * @param trainnumber the trainnumber to set
	 */
	public void setTrainnumber(String trainnumber) {
		this.trainnumber = trainnumber;
	}

	/**
	 * @return the plaats1
	 */
	public String getPlaats1() {
		return plaats1;
	}

	/**
	 * @param plaats1 the plaats1 to set
	 */
	public void setPlaats1(String plaats1) {
		this.plaats1 = plaats1;
	}

	/**
	 * @return the plaats2
	 */
	public String getPlaats2() {
		return plaats2;
	}

	/**
	 * @param plaats2 the plaats2 to set
	 */
	public void setPlaats2(String plaats2) {
		this.plaats2 = plaats2;
	}

	/**
	 * @return the vertrekTijd
	 */
	public String getVertrekTijd() {
		return vertrekTijd;
	}

	/**
	 * @param vertrekTijd the vertrekTijd to set
	 */
	public void setVertrekTijd(String vertrekTijd) {
		this.vertrekTijd = vertrekTijd;
	}
	
	/**
	 * @return the aankomstTijd
	 */
	public String getAankomstTijd() {
		return aankomstTijd;
	}

	/**
	 * @param vertrekTijd the vertrekTijd to set
	 */
	public void setAankomstTijd(String aankomstTijd) {
		this.aankomstTijd = aankomstTijd;
	}

	/**
	 * @return the predTrimean
	 */
	public int getPredTrimean() {
		return predTrimean;
	}

	/**
	 * @param predTrimean the predTrimean to set
	 */
	public void setPredTrimean(int predTrimean) {
		this.predTrimean = predTrimean;
	}

	/**
	 * @return the predARNU
	 */
	public int getPredARNU() {
		return predARNU;
	}

	/**
	 * @param predARNU the predARNU to set
	 */
	public void setPredARNU(int predARNU) {
		this.predARNU = predARNU;
	}

	/**
	 * @return the delay
	 */
	public int getDelay() {
		return delay;
	}

	/**
	 * @param delay the delay to set
	 */
	public void setDelay(int delay) {
		this.delay = delay;
	}

	/**
	 * @return the predSame
	 */
	public int getPredSame() {
		return predSame;
	}

	/**
	 * @param predSame the predSame to set
	 */
	public void setPredSame(int predSame) {
		this.predSame = predSame;
	}
    
}