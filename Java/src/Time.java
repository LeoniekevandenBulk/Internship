public class Time {

    private int hour;
    private int minutes;
    
    public Time(int hour, int minutes) {
    	this.hour = hour;
    	this.minutes = minutes;
	}
    
    /**
     * @param Time object
     * @return 1 if the current time is bigger than the param time, 0 if they are equal, and -1 if the param time is bigger
     */
    public int compare(Time t) {
    	if(this.hour > t.getHour()) {
    		return 1;
    	}
    	else if(this.hour == t.getHour()) {
    		if(this.minutes > t.getMinutes()) {
    			return 1;
    		}
    		else if(this.minutes == t.getMinutes()) {
    			return 0;
    		}
    		else {
    			return -1;
    		}
    	}
    	else {
        	return -1;
    	}
    }
	
	/**
    * Set hour and minutes of Time object on basis of a String containing a date and time
    */
	public void convertToTimeFromDate(String timeString){
   	this.hour = Integer.parseInt(timeString.substring(9,11));
   	this.minutes = Integer.parseInt(timeString.substring(12,14));
	}
	
    /**
     * Set hour and minutes of Time object on basis of a String containing a date and time in the Test Set
     */
	public void convertToTimeFromTestSetDate(String timeString){
    	this.hour = Integer.parseInt(timeString.substring(11,13));
    	this.minutes = Integer.parseInt(timeString.substring(14,16));
	}

    /**
     * Set hour and minutes of Time object on basis of a String containing only a time
     */
	public void convertToTimeFromTime(String timeString){
    	this.hour = Integer.parseInt(timeString.substring(0,2));
    	this.minutes = Integer.parseInt(timeString.substring(3,5));
	}

	
	/**
	 * @return the hour
	 */
	public int getHour() {
		return hour;
	}

	/**
	 * @param hour the hour to set
	 */
	public void setHour(int hour) {
		this.hour = hour;
	}

	/**
	 * @return the minutes
	 */
	public int getMinutes() {
		return minutes;
	}

	/**
	 * @param minutes the minutes to set
	 */
	public void setMinutes(int minutes) {
		this.minutes = minutes;
	}
}
