import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class CreateTestsetInputFromTestSet {

	public static void main(String[] args) {
        try {
        	// Read data file of test set and create new file to save the trains to predict
	        File bestand = new File("C:/Users/Leonieke.vandenB_nsp/OneDrive - NS/Data_vertragingen/Data_RAS/TestSet/TestSet.txt");
	        Scanner testsetbestand = new Scanner(bestand);

	        FileWriter fw = new FileWriter("C:/Users/Leonieke.vandenB_nsp/OneDrive - NS/JohnBrouwer/Testset_Inputs.txt");
	        PrintWriter out = new PrintWriter(fw);
	        
	        // Create times to analyze
	        Time beginTime1 = new Time(8,0);
	        Time beginTime2 = new Time(12,0);
	        Time beginTime3 = new Time(16,0);
	        Time endTime1 = new Time(8,20);
	        Time endTime2 = new Time(12,20);
	        Time endTime3 = new Time(16,20);
	        
	        // Initialize variables for finding the correct lines in the file
	        String nummer = new String();
	        String regel = new String();
	        String input = new String();
	        String previousNummer = new String();
	        String previousRegel = new String();
	        String plannedTime = new String();
	        String arrivalTime = new String();
	        String dir = new String();
	        String type = new String();
	        Time currentTime = new Time(0,0);
	        Time previousTime = new Time(0,0);
	        int category = 0;
	        boolean found = false;
	        boolean missing = false;
	        boolean identified = false;
	        
	        // Initialize variables for printing to test set
	        List<TestsetInput> testsetInputs = new ArrayList<TestsetInput>();
	        String date = new String();
	        String trainnr = new String();
	        String direction = new String();
	        String plaats1 = new String();
	        String plaats2 =  new String();
	        String tijdPlaats1 = new String();
	        String tijdPlaats2 = new String();
	        String activity = new String();
	        String output = new String();
	        String testnummer = new String();
	        
	        // Loop over all lines to find end locations at 08:20, 12:20 and 16:20
	        int i = 0;
	        while (testsetbestand.hasNextLine()) {
				// Print progress
				System.out.println("Eindtijd zoeken: " + i);
				
				// Get train number and search if the correct times are included in the timetable for that number
				regel = testsetbestand.nextLine();
	        	regel = regel.replace("\"", "");
				String[] columns = regel.split(",");
				nummer = columns[3];
				dir = columns[1];
				dir = dir.substring(dir.length()-1, dir.length());
				plannedTime = columns[6];
				type = columns[2];
				
				if(!plannedTime.equals("") && (dir.equals("O") || dir.equals("E"))) { //&& !type.equals("LM") ) {
					currentTime.convertToTimeFromTestSetDate(plannedTime);
				
					// Check in what time slot the first train of the train number starts
					if(!nummer.equals(previousNummer)){
						// Set found to false at the beginning of a train number
						found = false;
						if(currentTime.compare(endTime2) >= 0 && currentTime.compare(endTime3) == -1) {
							category = 3;
						}
						else if(currentTime.compare(endTime1) >= 0 && currentTime.compare(endTime2) == -1) {
							category = 2;
						}
						else if(currentTime.compare(endTime1) == -1){
							category = 1;
						}
						else {
							found = true; // We say true to avoid the for-loop for everything after 16:20, but nothing is actually saved
						}
					}
					
					// Find if the train has passed the time of 8:20/12:20/16:20 if relevant and save the previous location and time
					if(nummer.equals(previousNummer) && !found) {
						if((currentTime.compare(endTime1) == 1 && category == 1) || 
								(currentTime.compare(endTime2) == 1 && category == 2) || 
								(currentTime.compare(endTime3) == 1 && category == 3)) {
							previousRegel = previousRegel.replace("\"", "");
							String[] variables = previousRegel.split(",");
							arrivalTime = variables[6];
							previousTime.convertToTimeFromTestSetDate(arrivalTime);
							
							// Check if previous time comes after the begin time, else discard
							if((previousTime.compare(beginTime1) >= 0 && category == 1) || 
									(previousTime.compare(beginTime2) >= 0 && category == 2) || 
									(previousTime.compare(beginTime3) >= 0 && category == 3)) {
								date = transformDate(variables[0]);
								List<String> samePatternDates = new ArrayList<String>();
								samePatternDates.add(date);
								trainnr = variables[3];
								direction = variables[1];
								direction = direction.substring(direction.length()-1, direction.length());
								plaats2 = variables[4];
								activity = variables[5];
								tijdPlaats2 = arrivalTime.substring(11, 16) + ":00";
								
								// Add to list of test inputs
								TestsetInput missingInput = new TestsetInput(trainnr, direction, plaats2, tijdPlaats2, activity, date, samePatternDates);
								testsetInputs.add(missingInput);
							}	
							found = true;
						}
					}
					// Save current variables for next line
					previousRegel = regel;
					previousNummer = nummer;
				}
				i++;
	        }
	        testsetbestand.close();
	        
	        // Loop over all lines again to find begin locations at 08:00, 12:00 and 16:00
	        testsetbestand = new Scanner(bestand);
	        nummer = new String();
	        regel = new String();
	        previousNummer = new String();
	        previousRegel = new String();
	        found = false;
	        boolean trainnrPresent = false;
	        int index = -1;
	        
	        i = 0;
	        while (testsetbestand.hasNextLine()) {
				// Print progress
				System.out.println("Begintijd zoeken: " + i);
				
				// Get train number and search if the correct times are included in the timetable for that number
				regel = testsetbestand.nextLine();
				regel = regel.replace("\"", "");
				String[] columns = regel.split(",");
				date = transformDate(columns[0]);
				nummer = columns[3];
				plannedTime = columns[6];
				
				// Check every line that has a planned time
				if(!plannedTime.equals("")) {
					currentTime.convertToTimeFromTestSetDate(plannedTime);
					
					// Get the index of the test input with the same train number and date if it exists to match begin and end point
					if(!nummer.equals(previousNummer)) {
						found = false;
						trainnrPresent = false;
						for(TestsetInput testsetinput: testsetInputs) {
							if(testsetinput.getTrainnumber().equals(nummer) && testsetinput.getDate().equals(date)) {
								trainnrPresent = true;
								index = testsetInputs.indexOf(testsetinput);
								break;
							}
						}
					}
					
					// If the begin time has just passed correct range and not the first train of a train series, 
					// add the previous to the earlier found test input object with corresponding end time
					if(nummer.equals(previousNummer) && !found && trainnrPresent) {
						if((currentTime.compare(beginTime1) == 1 && currentTime.compare(endTime1) == -1) || 
								(currentTime.compare(beginTime2) == 1 && currentTime.compare(endTime2) == -1) || 
								(currentTime.compare(beginTime3) == 1 && currentTime.compare(endTime3) == -1)){
							previousRegel = previousRegel.replace("\"", "");
							String[] variables = previousRegel.split(",");
							plaats1 = variables[4];
							tijdPlaats1 = variables[6].substring(11, 16) + ":00";
							testsetInputs.get(index).setPlaats1(plaats1);
							testsetInputs.get(index).setVertrekTijd(tijdPlaats1);
							found = true;
						}
					} 
					
					// If the first train of the train series is the best option, add that to the earlier found 
					// test input object with corresponding end time
					else if(!nummer.equals(previousNummer) && !found && trainnrPresent){
						if((currentTime.compare(beginTime1) == 1 && currentTime.compare(endTime1) == -1) || 
								(currentTime.compare(beginTime2) == 1 && currentTime.compare(endTime2) == -1) || 
								(currentTime.compare(beginTime3) == 1 && currentTime.compare(endTime3) == -1)){
							plaats1 = columns[4];
							tijdPlaats1 = columns[6].substring(11, 16) + ":00";
							testsetInputs.get(index).setPlaats1(plaats1);
							testsetInputs.get(index).setVertrekTijd(tijdPlaats1);
							found = true;
						}
					}
	
					// Save current variables for next line
					previousRegel = regel;
					previousNummer = nummer;
				}
				i++;
	        }
	        
	        // Find and remove duplicates
	        List<TestsetInput>toBeRemoved = new ArrayList<>();
	        for(int n=0; n<testsetInputs.size(); n++) {
	        	for(int m=n+1; m<testsetInputs.size(); m++) {
		        	if (testsetInputs.get(n).isEqualIgnoringDate(testsetInputs.get(m)) && !toBeRemoved.contains(testsetInputs.get(n))) {
		        		toBeRemoved.add(testsetInputs.get(m));
		        		testsetInputs.get(n).getSamePatternDates().add(testsetInputs.get(m).getDate());
		        	}
	        	}
	        }
	        testsetInputs.removeAll(toBeRemoved);
	        
	        // Write all unique inputs to file
	        for(TestsetInput testsetinput: testsetInputs) {
	        	output = testsetinput.getTrainnumber() + "," + testsetinput.getDirection()  + "," + testsetinput.getPlaats1() + 
	        			"," + testsetinput.getPlaats2()  + "," + testsetinput.getVertrekTijd() + "," + testsetinput.getAankomstTijd() 
	        			+ "," + testsetinput.getActivity() + "," + String.join(";", testsetinput.getSamePatternDates());
	        	out.println(output);
	        }
			
			// Close files
	        testsetbestand.close();
	        out.close();
	        
		}
        catch(Exception e) {
		    e.printStackTrace();
		}
	}
	
	private static String transformDate(String time) {
		// Get year number
		String year = time.substring(0,4);
		
		// Get month number and transform to string of 3 characters
		String monthnr = time.substring(5, 7);
		String month = "";
		switch (monthnr) {
	    	case "01":
	    		month = "JAN";
	    		break;
	        case "02":
	        	month = "FEB";
	            break;
	        case "03":
	        	month = "MAR";
	            break;
	        case "04":
	        	month = "APR";
	            break;
	        case "05":
	        	month = "MAY";
	            break;
	        case "06":
	        	month = "JUN";
	            break;
	        case "07":
	        	month = "JUL";
	            break;
	        case "08":
	        	month = "AUG";
	            break;
	        case "09":
	        	month = "SEP";
	            break;
	        case "10":
	        	month = "OCT";
	            break;
	        case "11":
	        	month = "NOV";
	            break;
	        case "12":
	        	month = "DEC";
	            break;
		}
		// Get day number
		String day = time.substring(8, 10);
		
		// Put transformed string together and return
		String timeTransformed = day + month + year;
		return timeTransformed;
	}
}
