
import java.io.File;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class NewPerformance {

    public static List<ReturnPerf2> catPerformance(PrintWriter out, File realisatie_bestand, File test_bestand, int[] firstSample, int[] perfSample, int[] dagInTrain, int[] dagInTest, String treinnr, String direction, String plaats1In, String plaats2In, String tijdVertrek, String tijdAankomst, String soortIn, List<String> dates) {
        // Create month array from which to get estimations
        int[] maand1 = firstSample;
        // Create month array for which to predict
        int[] maand2 = perfSample;
        // Create array for possible dataselection
        int[] kwartaalIn = new int[]{};
        int[] weekIn = new int[]{};
        
        // Run first part:
        // This should get from the months on which the estimations should be based the following:
        // 2-Dimensional array with estimations for all 10 rows for all 3 estimation methods
        // Counter of how many observations the estimations are based on
        ReturnPerf1 return1 = NewPerformance.firstPart(10, treinnr, direction, kwartaalIn, maand1, weekIn, dagInTrain, realisatie_bestand, plaats1In, plaats2In);
        int[][] median = return1.getmedian();
        //int counter1 = return1.getcounter();

        // Run second part:
        // This should get from the months for which is to be predicted:
        // Counter of how many observations to be predicted
        // Lists of intervals with list of observations in that interval
        // ARNU prediction for each observation
        // observations sorted in the same way as the ARNU predictions
        List<ReturnPerf2> return2 = NewPerformance.secondPart(10, treinnr, direction, kwartaalIn, maand2, weekIn, dagInTest, test_bestand, plaats1In, plaats2In, tijdVertrek, tijdAankomst, soortIn, dates, median);

        // Print how many observations the estimations were based on and how many observations to predict
        //out.println("Aantal gebruikte waarnemingen voor predictie: " + counter1);

        // Return array of Trimean prediction and ARNU prediction
        return return2;
    }
    
    public static ReturnPerf1 firstPart(int r, String treinnrIn, String directionIn, int[] kwartaalIn, int[] maandIn, int[] weekIn, int[] dagIn, File bestand, String plaats1In, String plaats2In) {
    	r = r + 2;
        // Create return object
        ReturnPerf1 ret = new ReturnPerf1();
        // Create 2-Dimensional array for estimations for all 10 rows for all 3 estimation methods
        int[][] mediaan = new int[r][3];
        // Find out how many trains and what quarters, months, weeks and days were put in
        int kwartaalAmount = kwartaalIn.length;
        int maandInBegin = maandIn[0];
        int maandInEind = maandIn[1];
        int weekInBegin = 0;
        int weekInEind = 0;
        boolean specialw = false;
        if (weekIn.length > 0) {
            weekInBegin = weekIn[0];
            weekInEind = weekIn[1];
            if (weekInEind < weekInBegin) {
                specialw = true;
            }
        }
        int dagAmount = dagIn.length;
        int dagInBegin = dagIn[0];
        int dagInEind = dagIn[1];
        // Create list of observations for use in creating estimations
        List<List<Integer>> obs = new ArrayList<>();
        for (int i = 0; i < r; i++) {
            List<Integer> list = new ArrayList<>();
            obs.add(list);
            obs.get(i).add(999999999);
        }
        // Create counter for counting amount of used observations
        int counter = 0;
        try {
	        Scanner leesbestand = new Scanner(bestand);
	        int kwartaal = 0, maand, week = 0, dag = 0, plantijd, uitvtijd, plandag, uitvdag, vertr1, vertr2, i, x;
	        String plaats = new String();
	        String vorige_datum = new String();
	        String datum = new String();
	        String direction = new String();
	        String treinnr = new String();
	        String previousnr = new String();
	        String treinseries = new String();
	        String treinseriesIn = treinnrIn.substring(0,treinnrIn.length()-2); // Define trainseries only as the number that doesn't change (e.g. 500 series -> 5)
            if(!(plaats1In.substring(0, 2).equals("IJ") || plaats1In.substring(0, 2).equals("Ij") || plaats1In.substring(0, 2).equals("ij"))) {
            	plaats1In = plaats1In.substring(0, 1).toUpperCase() + plaats1In.substring(1, plaats1In.length()).toLowerCase();
            }else {
            	plaats1In = plaats1In.substring(0, 2).toUpperCase() + plaats1In.substring(2, plaats1In.length()).toLowerCase();
            }
            if(!(plaats2In.substring(0, 2).equals("IJ") || plaats2In.substring(0, 2).equals("Ij") || plaats2In.substring(0, 2).equals("ij"))) {
            	plaats2In = plaats2In.substring(0, 1).toUpperCase() + plaats2In.substring(1, plaats2In.length()).toLowerCase();
            }else {
            	plaats2In = plaats2In.substring(0, 2).toUpperCase() + plaats2In.substring(2, plaats2In.length()).toLowerCase();
            }
	        while (leesbestand.hasNextLine()) {
	        	String regel = leesbestand.nextLine();
//	            datum = regel.substring(2, 9);
//	            if (!datum.equals(vorige_datum)) {
//	                //System.out.println(datum);
//	            }
//	            vorige_datum = datum;
	            maand = Vinden.maand(regel);
	            // Find trainnr, quarter, month, week, day and place of this read line
	            treinnr = Vinden.treinnrString(regel);
	            treinseries = treinnr.substring(0,treinnr.length()-2);
	            
	            if (kwartaalAmount > 0) {
	                kwartaal = Vinden.kwartaal(regel);
	            }
	            if (weekIn.length > 0) {
	                week = Vinden.week(regel);
	            }
	            if (dagAmount > 0) {
	                dag = Vinden.weekdag(regel);
	            }
	            plaats = Vinden.plaats(regel);
	            direction = Vinden.direction(regel);
	            
	            int l = 1;
	            while (l <= kwartaalAmount && kwartaal != kwartaalIn[l - 1]) {
	                l++;
	            }

	            // Check if trainnr, quarter, month, week, day and place are correct for input point 1
	            if (treinseriesIn.equals(treinseries) && directionIn.equals(direction) && (kwartaalAmount == 0 || l < kwartaalAmount + 1) && (dagAmount == 0 || (dag >= dagInBegin && dag <= dagInEind)) && 
	            		(maand >= maandInBegin && maand <= maandInEind) && (weekIn.length == 0 || (week >= weekInBegin && week <= weekInEind && !specialw) || 
	            		((week >= weekInBegin || week <= weekInEind) && specialw)) && plaats.equals(plaats1In)) {
	                plantijd = Vinden.plantijd(regel);
	                uitvtijd = Vinden.uitvtijd(regel);
	                vertr1 = uitvtijd - plantijd;

	                // Check if the train was not more than 119 seconds too early
	                if (vertr1 > -120) {
	                    treinnr = Vinden.treinnrString(regel);
	                    previousnr = treinnr;
	                    plaats = Vinden.plaats(regel);
	                    // Keep going until the trainnr changes or point 2 is found
	                    while (treinnr.equals(previousnr) && !plaats.equals(plaats2In)) {
	                    	previousnr = treinnr;
	                    	regel = leesbestand.nextLine();
	                        treinnr = Vinden.treinnrString(regel);
	                        plaats = Vinden.plaats(regel);
	                    }
	                    // Check if point 2 is found
	                    if (plaats.equals(plaats2In)) {
	                        plantijd = Vinden.plantijd(regel);
	                        uitvtijd = Vinden.uitvtijd(regel);
	                        vertr2 = uitvtijd - plantijd;
	                        plandag = Vinden.dag_plan(regel);
	                        uitvdag = Vinden.dag_uitv(regel);
	                        while (uitvdag > plandag) {
	                            vertr2 = vertr2 + 86400;
	                            uitvdag--;
	                        }
	                        i = -60;
	                        while (vertr1 >= i && i <= (r - 3) * 60) {
	                            i = i + 60;
	                        }
	                        vertr1 = (i + 120) / 60;
	                        x = 0;
	                        while (vertr2 > obs.get(vertr1 - 1).get(x)) {
	                            x++;
	                        }
	                        // Add observation to right list
	                        obs.get(vertr1 - 1).add(x, vertr2);
	                        // Count observation
	                        counter++;
	                    }
	                }
	            }
//	            regel = leesbestand.nextLine();
//	            maand = vinden.maand(regel);
	        }
	        
	        leesbestand.close();  
	        
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        mediaan = NewPerformance.estimations(r, obs);

        // Output estimations and amount
        ret.init(mediaan, counter);
        return ret;
        
    }
    
    public static List<ReturnPerf2> secondPart(int r, String treinnrIn, String directionIn, int[] kwartaalIn, int[] maandIn, int[] weekIn, int[] dagIn, File bestand, String plaats1In, String plaats2In, String tijdVertrek, String tijdAankomst, String soortIn, List<String> dates, int[][] estimates) {
    	r = r + 2;
        // Create return object
        List<ReturnPerf2> ret = new ArrayList<>();
        // Find out how many trains and what quarters, months, weeks, days and times were put in
        int kwartaalAmount = kwartaalIn.length;
        int maandInBegin = maandIn[0];
        int maandInEind = maandIn[1];
        int weekInBegin = 0;
        int weekInEind = 0;
        boolean specialw = false;
        if (weekIn.length > 0) {
            weekInBegin = weekIn[0];
            weekInEind = weekIn[1];
            if (weekInEind < weekInBegin) {
                specialw = true;
            }
        }
        int dagAmount = dagIn.length;
        int dagInBegin = dagIn[0];
        int dagInEind = dagIn[1];
        
        // Create times to predict
        Time beginTime1 = new Time(8,0);
        Time beginTime2 = new Time(12,0);
        Time beginTime3 = new Time(16,0);
        Time endTime1 = new Time(8,20);
        Time endTime2 = new Time(12,20);
        Time endTime3 = new Time(16,20);

        // Start looking for place1 and place2 in document
        try {
                Scanner leesbestand = new Scanner(bestand);
                int kwartaal = 0, maand, week = 0, dag = 0, tijdPlaats1, tijdPlaats2, stat1, stat2, plantijd, uitvtijd, vertr1, vertr2, i;
                double speling = 0;
                String plaats = new String();
                String soort = new String();
                String datum = new String();
                String tijd = new String();
                String direction = new String();
                String tijdPlaats1String = new String();
                String datumPlaats1String = new String();
                String tijdPlaats2String = new String();
                String datumPlaats2String = new String();
                Time timeCompare1 = new Time(0,0);
                Time timeCompare2 = new Time(0,0);
                if(!(plaats1In.substring(0, 2).equals("IJ") || plaats1In.substring(0, 2).equals("Ij") || plaats1In.substring(0, 2).equals("ij"))) {
                	plaats1In = plaats1In.substring(0, 1).toUpperCase() + plaats1In.substring(1, plaats1In.length()).toLowerCase();
                }else {
                	plaats1In = plaats1In.substring(0, 2).toUpperCase() + plaats1In.substring(2, plaats1In.length()).toLowerCase();
                }
                if(!(plaats2In.substring(0, 2).equals("IJ") || plaats2In.substring(0, 2).equals("Ij") || plaats2In.substring(0, 2).equals("ij"))) {
                	plaats2In = plaats2In.substring(0, 1).toUpperCase() + plaats2In.substring(1, plaats2In.length()).toLowerCase();
                }else {
                	plaats2In = plaats2In.substring(0, 2).toUpperCase() + plaats2In.substring(2, plaats2In.length()).toLowerCase();
                }

                while (leesbestand.hasNextLine()) {
                	String regel = leesbestand.nextLine();

                    // Create variables to save prediction and actual delay
                    int predTrimean = 0;
                    int predARNU = 0;
                    int predSame = 0;
                    int delay = 0;
                    speling = 0;
                    
                    // Find trainnr, quarter, month, week, day and place of this read line
                    String treinnr = Vinden.treinnrString(regel);
                    datum = regel.substring(0, 9);
                    maand = Vinden.maand(regel);
                    if (kwartaalAmount > 0) {
                        kwartaal = Vinden.kwartaal(regel);
                    }
                    if (weekIn.length > 0) {
                        week = Vinden.week(regel);
                    }
                    if (dagAmount > 0) {
                        dag = Vinden.weekdag(regel);
                    }
                    plaats = Vinden.plaats(regel);
                    tijd = Vinden.plantijdString(regel);
                    direction = Vinden.direction(regel);
                    
                    
                    int l = 1;
                    while (l <= kwartaalAmount && kwartaal != kwartaalIn[l - 1]) {
                        l++;
                    }

                    // Check if trainnr, quarter, month, week, day and place are correct for input point 1
                    if (treinnrIn.equals(treinnr) && directionIn.equals(direction) && (kwartaalAmount == 0 || l < kwartaalAmount + 1) && (dagAmount == 0 || (dag >= dagInBegin && dag <= dagInEind)) 
                    		&& (maand >= maandInBegin && maand <= maandInEind) && (weekIn.length == 0 || (week >= weekInBegin && week <= weekInEind && !specialw) || 
                    		((week >= weekInBegin || week <= weekInEind) && specialw)) && plaats.equals(plaats1In) && dates.contains(datum)) {// && tijdVertrek.equals(tijd)) {
                    	plantijd = Vinden.plantijd(regel);
                        uitvtijd = Vinden.uitvtijd(regel);
                        vertr1 = uitvtijd - plantijd;

                        // Save planned time point 1 for ARNU prediction
                        tijdPlaats1 = plantijd;
                        soort = Vinden.soort(regel);
                        // Check if trains stops for long stop
                        if (soort.equals("A")) {
                            stat1 = Vinden.plantijd(regel);
                            regel = leesbestand.nextLine();
                            stat2 = Vinden.plantijd(regel);
                            // Possibly add time for ARNU prediction
                            speling = speling + Math.max(0, stat2 - stat1 - 120);
                        }
                        treinnr = Vinden.treinnrString(regel);
                        plaats = Vinden.plaats(regel);
                        tijd = Vinden.plantijdString(regel);
                        tijdPlaats1String = tijd;
                        datumPlaats1String = Vinden.plandatum(regel);
                        // Keep going until the trainnr changes or point 2 is found
                        while (treinnr.equals(treinnrIn) && !plaats.equals(plaats2In)) {
                            soort = Vinden.soort(regel);
                            // Check if trains stops for long stop
                            if (soort.equals("A")) {
                                stat1 = Vinden.plantijd(regel);
                                regel = leesbestand.nextLine();
                                stat2 = Vinden.plantijd(regel);
                                // Possibly add time for ARNU prediction
                                speling = speling + Math.max(0, stat2 - stat1 - 120);
                            }
                            regel = leesbestand.nextLine();
                            treinnr = Vinden.treinnrString(regel);
                            plaats = Vinden.plaats(regel);
                            tijd = Vinden.plantijdString(regel);
                        }
                        if (plaats.equals(plaats2In)) {
                            soort = Vinden.soort(regel);
                            // Check if departures should be predicted and this is arrival
                            if ((soortIn.equals("V") && soort.equals("A")) || (soortIn.equals("K_V") && soort.equals("K_A"))) {
                            	//Save planned time for arrival
                                stat1 = Vinden.plantijd(regel);
                                // Check if this wasn't end of the file
                                if (leesbestand.hasNextLine()) {
                                    // Go to next line
                                    regel = leesbestand.nextLine();
                                  //Save planned time for departure
                                    stat2 = Vinden.plantijd(regel);
                                    // Possibly add time for ARNU prediction
                                    speling = speling + Math.max(0, stat2 - stat1 - 120);
                                    treinnr = Vinden.treinnrString(regel);
                                    plaats = Vinden.plaats(regel);
                                    tijd = Vinden.plantijdString(regel);
                                }
                            }
                            // Check if it wasn't end of file or suddenly the trainnr or place has changed
                            if (leesbestand.hasNextLine() && treinnr.equals(treinnrIn) && plaats.equals(plaats2In)) {// && tijdAankomst.equals(tijd)) {

                            	treinnr = Vinden.treinnrString(regel);
                                plaats = Vinden.plaats(regel);
                                if (treinnr.equals(treinnrIn) && plaats.equals(plaats2In)) {// && tijdAankomst.equals(tijd)) {
                                    plantijd = Vinden.plantijd(regel);
                                    uitvtijd = Vinden.uitvtijd(regel);
                                    // Save planned time point 2 for ARNU prediction
                                    tijdPlaats2 = plantijd;
                                    tijdPlaats2String = Vinden.plantijdString(regel);
                                    datumPlaats2String = Vinden.plandatum(regel);
                                    speling = speling + (tijdPlaats2 - tijdPlaats1) * 0.07;
                                    vertr2 = uitvtijd - plantijd;

                                    // Save delay at first location as baseline prediction
                                    predSame = vertr1 / 60;
                                    
                                    // Save what ARNU predicted
                                    predARNU = (int) Math.max(0, Math.round(((double) vertr1 - speling) / 60));

                                    // Check if the time is in the correct range for Trimean prediction
                                    timeCompare1.convertToTimeFromTime(tijdPlaats1String);
                                    timeCompare2.convertToTimeFromTime(tijdPlaats2String);
            						if((timeCompare1.compare(beginTime1) <= 0 && timeCompare2.compare(endTime1) <= 0) || 
            								(timeCompare1.compare(beginTime2) <= 0 && timeCompare2.compare(endTime2) <= 0 && timeCompare2.compare(beginTime2) > 0 ) || 
            								(timeCompare1.compare(beginTime3) <= 0 && timeCompare2.compare(endTime3) <= 0 && timeCompare2.compare(beginTime3) > 0 )){
                                        i = -60;
                                        while (vertr1 >= i && i <= (r - 3) * 60) {
                                            i = i + 60;
                                        }
                                        vertr1 = (i + 120) / 60;
   
                                        // Add observation to right list
                                        predTrimean = estimates[vertr1 - 1][2];
                                        
                                    } // if the range is not correct, set Trimean prediction to 0
                                    else {
                                    	predTrimean = 0;
                                    }
                                    
                                    delay = vertr2 / 60;
                                    
                            	    // Save Trainnumber, Places, Planned Time, Trimean Prediction, ARNU prediction and Actual Delay.
                                    ReturnPerf2 entry = new ReturnPerf2();
                            	    entry.init(treinnrIn, plaats1In, plaats2In, datumPlaats1String, datumPlaats2String, delay, predTrimean, predARNU, predSame);
                            	    ret.add(entry);
                                }
                            }
                        }
                    }
                }
                
        leesbestand.close();
    	} catch (Exception e) {
        e.printStackTrace();
    	}

        return ret;
    }

    public static int[][] estimations(int r, List<List<Integer>> obsIn) {
        int[] amountobs = new int[r];
        // Create estimations matrix
        double[][] estimationsD = new double[r][3];
        int[][] estimationsI = new int[r][3];
        for (int i = 0; i < r; i++) {
            amountobs[i] = obsIn.get(i).size() - 1;
            // Delete element that was added to make size > 0 
            obsIn.get(i).remove(amountobs[i]);
        }

        // For every row
        for (int i = 0; i < r; i++) {
            // Check if row is equal to zero
            if (amountobs[i] == 0) {
                // Predict zero for median and trimean
                estimationsD[i][0] = 0;
                estimationsD[i][2] = 0;
                // Check if amount is even
            } else if ((amountobs[i] % 2) == 0) {
                estimationsD[i][0] = Math.max(0, (double) (obsIn.get(i).get(amountobs[i] / 2 - 1) + obsIn.get(i).get(amountobs[i] / 2)) / (2 * 60));
                estimationsD[i][2] = Math.max(0, (double) (obsIn.get(i).get((amountobs[i] + 2) / 4 - 1) + obsIn.get(i).get(amountobs[i] / 2 - 1) + obsIn.get(i).get(amountobs[i] / 2) + obsIn.get(i).get((3 * amountobs[i] + 2) / 4 - 1)) / (4 * 60));
                // Amount is bigger than zero and not even
            } else {
                estimationsD[i][0] = Math.max(0, (double) obsIn.get(i).get((amountobs[i] - 1) / 2) / 60);
                estimationsD[i][2] = Math.max(0, (double) (obsIn.get(i).get((amountobs[i] + 3) / 4 - 1) + 2 * obsIn.get(i).get((amountobs[i] - 1) / 2) + obsIn.get(i).get((3 * amountobs[i] + 1) / 4 - 1)) / (4 * 60));
            }
            for (int n = 0; n < amountobs[i]; n++) {
                estimationsD[i][1] = estimationsD[i][1] + obsIn.get(i).get(n);
            }
            estimationsD[i][1] = Math.max(0, estimationsD[i][1] / (amountobs[i] * 60));
            // Check if row is equal to zero
            if (amountobs[i] == 0) {
                // Predict zero for mean
                estimationsD[i][1] = 0;
            }

            for (int j = 0; j < 3; j++) {
                estimationsI[i][j] = (int) Math.round(estimationsD[i][j]);
            }

            // Print estimations
            //System.out.println("De mediaan van rij " + (i + 1) + " is " + estimationsI[i][0]);
            //System.out.println("Het gemiddelde van rij " + (i + 1) + " is " + estimationsI[i][1]);
            //System.out.println("De trimean van rij " + (i + 1) + " is " + estimationsI[i][2]);
        }
        return estimationsI;
    }
}