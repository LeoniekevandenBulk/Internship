import java.util.List;

public class TestsetInput {

	private String trainnumber;
	private String direction;
    private String plaats1;
    private String plaats2;
    private String vertrekTijd;
    private String aankomstTijd;
    private String activity;
    private String date;
    private List<String> samePatternDates;

    public TestsetInput(String trainnumber, String direction, String plaats2, String aankomstTijd, String activity, String date, List<String> samePatternDates) {
        this.trainnumber = trainnumber;
        this.direction = direction;
        this.plaats2 = plaats2;
        this.aankomstTijd = aankomstTijd;
        this.activity = activity;
        this.date = date;
        this.samePatternDates = samePatternDates;
    }
    
    /**
     * Compares two TestsetInputs and returns true if they are equal in everything except the data
     * @param other: TestsetInput to be compared with
     */
    public boolean isEqualIgnoringDate(TestsetInput other) {
    	return this.trainnumber.equals(other.getTrainnumber()) && this.direction.equals(other.getDirection()) &&
    			this.plaats1.equals(other.getPlaats1()) && this.plaats2.equals(other.getPlaats2()) &&
    			this.activity.equals(other.getActivity());
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
	 * @return the direction
	 */
	public String getDirection() {
		return direction;
	}

	/**
	 * @param direction the direction to set
	 */
	public void setDirection(String direction) {
		this.direction = direction;
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
	 * @param aankomstTijd the aankomstTijd to set
	 */
	public void setAankomstTijd(String aankomstTijd) {
		this.aankomstTijd = aankomstTijd;
	}

	/**
	 * @return the activity
	 */
	public String getActivity() {
		return activity;
	}

	/**
	 * @param activity the activity to set
	 */
	public void setActivity(String activity) {
		this.activity = activity;
	}

	/**
	 * @return the date
	 */
	public String getDate() {
		return date;
	}

	/**
	 * @param date the date to set
	 */
	public void setDate(String date) {
		this.date = date;
	}

	/**
	 * @return the samePatternDates
	 */
	public List<String> getSamePatternDates() {
		return samePatternDates;
	}

	/**
	 * @param samePatternDates the samePatternDates to set
	 */
	public void setSamePatternDates(List<String> samePatternDates) {
		this.samePatternDates = samePatternDates;
	}
}
