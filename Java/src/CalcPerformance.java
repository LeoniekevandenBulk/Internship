
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.Timer;

public class CalcPerformance {

    public static void main(String[] args) {
    	final long startTime = System.currentTimeMillis();
        runCat();
        final long endTime = System.currentTimeMillis();
        System.out.println("Total execution time: " + (endTime - startTime) );
    }

    public static void runCat() {
    	int[] firstSample = new int[]{9, 12};
        int[] perfSample = new int[]{11, 12};
        int[] dagInTrain = new int[]{1,5};
        int[] dagInTest = new int[]{2,2};
        catPerformance(firstSample, perfSample, dagInTrain, dagInTest);
    }

    // firstSample defines the first and last month of the sample for determining estimations
    // perfSample defines the first and last month of the sample for determining performance
    // dagInTrain defines the first and last day of the week of the sample for determining estimations
    // dagInTest defines the first and last day of the week of the sample for determining performance
    public static void catPerformance(int[] firstSample, int[] perfSample, int[] dagInTrain, int[] dagInTest) {
        System.out.println("Start performance measurement");
        System.out.println();

        try {	
	        // Load input entries from testset input file with train number, direction, begin location, end location, 
	        // planned times, activity (separated with ','). Furthermore, give the file directories of the converted
	        // realisation and test datasets.
	        File inputs_bestand = new File("C:/Users/Leonieke.vandenB_nsp/OneDrive - NS/JohnBrouwer/Testset_Inputs.txt");
	        File realisatie_bestand = new File("C:/Users/Leonieke.vandenB_nsp/OneDrive - NS/Data_vertragingen/Data_RAS/RealisationData/ConvertedRealisationData.txt");
	        File test_bestand = new File("C:/Users/Leonieke.vandenB_nsp/OneDrive - NS/Data_vertragingen/Data_RAS/TestSet/ConvertedRealisationTestData.txt");
	        Scanner leesbestand = new Scanner(inputs_bestand);
	        String regel = new String();
            String output = new String();
            
	        // Create objects needed for creating output files
	        FileWriter fw;
	        PrintWriter out;
	        fw = new FileWriter("C:/Users/Leonieke.vandenB_nsp/OneDrive - NS/JohnBrouwer/Performance_JohnCode.txt");
	        out = new PrintWriter(fw);
	        
	        int i = 0;
	        while (leesbestand.hasNextLine()) {

	        	// Read train number, direction, places (from and to), planned times at 'from' and 'to' and activity at 'to' location from file.
	        	regel = leesbestand.nextLine();
	        	String[] input = regel.split(",");
	        	String trainnr = input[0];
	        	String direction = input[1];
	        	String plaats1 = input[2];
	        	String plaats2 = input[3];
	        	String tijdVertrek = input[4];
	        	String tijdAankomst = input[5];
	        	String activity = input[6];
	        	List<String> dates = Arrays.asList(input[7].split(";"));
	        	
	        	// Print progress
	        	System.out.println("Input " + i + ": Performance of \"" + trainnr + "\" in direction \"" + direction + "\" with begin point \"" + plaats1 + "\" and ending point \"" + plaats2 + "\"");
	        	
	            // Perform performance measure
	            List<ReturnPerf2> predictions = NewPerformance.catPerformance(out, realisatie_bestand, test_bestand, firstSample, perfSample, dagInTrain, dagInTest, trainnr, direction, plaats1, plaats2, tijdVertrek, tijdAankomst, activity, dates);            
	            
	            // Print Train number, Places, Planned Time, Trimean Prediction, ARNU prediction and Actual Delay to output file.
	            for(ReturnPerf2 entry : predictions) {
	            	output = entry.getTrainnumber() + "," + entry.getPlaats1() + "," + entry.getPlaats2() + "," + entry.getVertrekTijd() + "," + entry.getAankomstTijd()
	            			 + "," + Integer.toString(entry.getDelay()) + "," + Integer.toString(entry.getPredTrimean()) + "," + Integer.toString(entry.getPredARNU())
	            			 + "," + Integer.toString(entry.getPredSame());
	            	out.println(output);
	            	out.flush();
	            }

	            i++;
	        }
	        leesbestand.close();
	        out.close();
	        
    	} catch (Exception e) {
        e.printStackTrace();
    	}
    }
}