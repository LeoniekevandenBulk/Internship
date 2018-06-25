import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Scanner;

public class DataTransformer {
    public static void main(String[] args) {
        try {
        	// Read data file and create new file to save conversion (either realisation set or test set)
	        File bestand = new File("C:/Users/Leonieke.vandenB_nsp/OneDrive - NS/Data_vertragingen/Data_RAS/TestSet/TestSet.txt");
	        Scanner leesbestand = new Scanner(bestand);
	        FileWriter fw = new FileWriter("C:/Users/Leonieke.vandenB_nsp/OneDrive - NS/Data_vertragingen/Data_RAS/TestSet/ConvertedRealisationTestData.txt");
	        PrintWriter out = new PrintWriter(fw);
	        String regel = new String();
	        
	        int i = 0;
	        while (leesbestand.hasNextLine()) {
	        	 // Print progress
	        	 System.out.println(i);

	        	 // Read every column from data in separate variables
	        	 regel = leesbestand.nextLine();
	        	 regel = regel.replace("\"", "");
	        	 String[] columns = regel.split(",");
	        	 String trainseries = columns[1];
	        	 String trainnr = columns[3];
	        	 String location = columns[4];
	        	 String activity = columns[5];
	        	 String plannedTime = columns[6];
	        	 String realizedTime = "";
	        	 if(columns.length >= 8){
	        		 realizedTime = columns[7];
	        	 }
	        	 // Transform some of the strings in correct format
	        	 String plannedTimeTransformed = transformTime(plannedTime);
	        	 String realizedTimeTransformed = "";
	        	 if(!realizedTime.equals("")){
	        		 realizedTimeTransformed = transformTime(realizedTime);
	        	 }
	        	 String date = plannedTimeTransformed.substring(0, 5) + "20" + plannedTimeTransformed.substring(5, 7);
	        	 String month = plannedTime.substring(5, 7);
	        	 if(month.substring(0,1).equals("0")){
	        		 month = plannedTime.substring(6, 7);
	        	 }
	        	 String direction = trainseries.substring(trainseries.length()-1);
	        	 trainseries = trainseries.replace("O", "").replace("E", "");

	        	 // Create output string with created variables and print to file
	        	 String output = date + "," + trainseries + "," + trainnr + "," + direction + ",0," + location + "," + activity + "," + plannedTimeTransformed + "," + 
	        			 plannedTimeTransformed + "," + realizedTimeTransformed + ",53," + month + ",4,2017,2017,201753,,,,,,,,,,";
	        	 out.println(output);
	        	 i++;
	         }
	        //out.println("end");
	        out.close();
	        
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

	private static String transformTime(String time) {
		// Get year number
		String year = time.substring(2,4);
		
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

		// Get time
		String hour = ":" + time.substring(11,19);
		
		// Put transformed string together and return
		String timeTransformed = day + month + year + hour;
		return timeTransformed;
	}
}
