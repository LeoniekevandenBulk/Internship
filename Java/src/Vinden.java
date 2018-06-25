
public class Vinden {

    public static int treinnr(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 2; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        checker++;
        teken = regelIn.substring(checker, checker + 1);
        while (!teken.equals(",")) {
            checker++;
            teken = regelIn.substring(checker, checker + 1);
        }
        int eind = checker;
        int treinnr = Integer.parseInt(regelIn.substring(begin, eind));
        return treinnr;
    }
	
    public static String treinnrString(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 2; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        checker++;
        teken = regelIn.substring(checker, checker + 1);
        while (!teken.equals(",")) {
            checker++;
            teken = regelIn.substring(checker, checker + 1);
        }
        int eind = checker;
        String treinnr = regelIn.substring(begin, eind);
        return treinnr;
    }

    public static int treinserie(String regelIn) {
        int checker = 0;
        String teken = new String();
        teken = regelIn.substring(checker, checker + 1);
        while (!teken.equals(",")) {
            checker++;
            teken = regelIn.substring(checker, checker + 1);
        }
        checker++;
        int begin = checker;
        checker++;
        teken = regelIn.substring(checker, checker + 1);
        while (!teken.equals(",")) {
            checker++;
            teken = regelIn.substring(checker, checker + 1);
        }
        int eind = checker;
        int treinserie = Integer.parseInt(regelIn.substring(begin, eind));
        return treinserie;
    }

    public static String plaats(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 5; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        checker++;
        teken = regelIn.substring(checker, checker + 1);
        while (!teken.equals(",")) {
            checker++;
            teken = regelIn.substring(checker, checker + 1);
        }
        int eind = checker;
        String plaats = new String(regelIn.substring(begin, eind));
        return plaats;
    }

    public static int plantijd(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 8; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        int plantijd = Integer.parseInt(regelIn.substring(begin + 8, begin + 10)) * 3600 + Integer.parseInt(regelIn.substring(begin + 11, begin + 13)) * 60 + Integer.parseInt(regelIn.substring(begin + 14, begin + 16));
        return plantijd;
    }
    
    public static String plantijdString(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 8; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        String plantijd = regelIn.substring(begin + 8, begin + 16);
        return plantijd;
    }

    public static int uitvtijd(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 9; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        int uitvtijd = Integer.parseInt(regelIn.substring(begin + 8, begin + 10)) * 3600 + Integer.parseInt(regelIn.substring(begin + 11, begin + 13)) * 60 + Integer.parseInt(regelIn.substring(begin + 14, begin + 16));
        return uitvtijd;
    }
    
    public static String uitvtijdString(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 9; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        String plantijd = regelIn.substring(begin + 8, begin + 16);
        return plantijd;
    }
    
    public static String plandatum(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 8; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        String plandatum = regelIn.substring(begin, begin + 16);
        return plandatum;
    }
    
    public static String uitvdatum(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 9; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        String uitvdatum = regelIn.substring(begin, begin + 16);
        return uitvdatum;
    }

    public static int week(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 10; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        checker++;
        teken = regelIn.substring(checker, checker + 1);
        while (!teken.equals(",")) {
            checker++;
            teken = regelIn.substring(checker, checker + 1);
        }
        int eind = checker;
        int week = Integer.parseInt(regelIn.substring(begin, eind));
        return week;
    }

    public static int maand(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 11; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        checker++;
        teken = regelIn.substring(checker, checker + 1);
        while (!teken.equals(",")) {
            checker++;
            teken = regelIn.substring(checker, checker + 1);
        }
        int eind = checker;
        int maand = Integer.parseInt(regelIn.substring(begin, eind));
        return maand;
    }

    public static int kwartaal(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 12; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        int kwartaal = Integer.parseInt(regelIn.substring(begin, begin + 1));
        return kwartaal;
    }
    
    // Calculated according to https://blog.artofmemory.com/how-to-calculate-the-day-of-the-week-4203.html
    // 0 = sunday, 1 = monday, ... , 6 = saturday
    public static int weekdag(String regelIn) {
        String datum = regelIn.substring(0, 9);
        int dag = Integer.parseInt(datum.substring(0, 2));
        String maand = datum.substring(2, 5);
        int jaar = Integer.parseInt(datum.substring(7, 9));
        int jaarnr = (jaar + (int)(jaar/4)) % 7;
        int eeuwnr = 6; //only the case for 2000s
        int maandnr = 0;
        int leapnr = 0;
        switch (maand) {
        	case "JAN":
        		maandnr = 0;
        		break;
            case "FEB":
            	maandnr = 3;
                break;
            case "MAR":
            	maandnr = 3;
                break;
            case "APR":
            	maandnr = 6;
                break;
            case "MAY":
            	maandnr = 1;
                break;
            case "JUN":
            	maandnr = 4;
                break;
            case "JUL":
            	maandnr = 6;
                break;
            case "AUG":
            	maandnr = 2;
                break;
            case "SEP":
            	maandnr = 5;
                break;
            case "OCT":
            	maandnr = 0;
                break;
            case "NOV":
            	maandnr = 3;
                break;
            case "DEC":
            	maandnr = 5;
                break;
        }

        if ((jaar % 4) == 0 && (maand.equals("JAN") || maand.equals("FEB"))) {
            leapnr = 1;
        }

        int weekdag = (jaarnr + maandnr + eeuwnr + dag - leapnr) % 7;
        return weekdag;
    }
    
    public static int dag(String regelIn) {
        String datum = regelIn.substring(0, 9);
        int dag = Integer.parseInt(datum.substring(0, 2));
        String maand = datum.substring(2, 5);
        int jaar = Integer.parseInt(datum.substring(5, 9));
        switch (maand) {
            case "FEB":
                dag = dag + 31;
                break;
            case "MAR":
                dag = dag + 59;
                break;
            case "APR":
                dag = dag + 90;
                break;
            case "MAY":
                dag = dag + 120;
                break;
            case "JUN":
                dag = dag + 151;
                break;
            case "JUL":
                dag = dag + 181;
                break;
            case "AUG":
                dag = dag + 212;
                break;
            case "SEP":
                dag = dag + 243;
                break;
            case "OCT":
                dag = dag + 273;
                break;
            case "NOV":
                dag = dag + 304;
                break;
            case "DEC":
                dag = dag + 334;
                break;
        }

        if ((jaar % 4) == 0 && !maand.equals("JAN") && !maand.equals("FEB")) {
            dag++;
        }

        while (jaar > 2009) {
            jaar--;
            dag = dag + 365;
        }

        int weekdag;
        if ((dag % 7) == 0) {
            weekdag = 4;
        } else if ((dag % 7) == 1) {
            weekdag = 5;
        } else if ((dag % 7) == 2) {
            weekdag = 6;
        } else if ((dag % 7) == 3) {
            weekdag = 7;
        } else if ((dag % 7) == 4) {
            weekdag = 1;
        } else if ((dag % 7) == 5) {
            weekdag = 2;
        } else {
            weekdag = 3;
        }

        return weekdag;
    }
    
    public static String direction(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 3; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        String direction = regelIn.substring(begin, begin + 1);
        return direction;
    }

    public static String soort(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 6; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        checker++;
        teken = regelIn.substring(checker, checker + 1);
        while (!teken.equals(",")) {
            checker++;
            teken = regelIn.substring(checker, checker + 1);
        }
        int eind = checker;
        String soort = regelIn.substring(begin, eind);
        return soort;
    }

    public static int dag_plan(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 8; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        String datum = regelIn.substring(begin, begin + 7);
        int dag = Integer.parseInt(datum.substring(0, 2));
        String maand = datum.substring(2, 5);
        int jaar = Integer.parseInt(datum.substring(5, 7));
        switch (maand) {
            case "FEB":
                dag = dag + 31;
                break;
            case "MAR":
                dag = dag + 59;
                break;
            case "APR":
                dag = dag + 90;
                break;
            case "MAY":
                dag = dag + 120;
                break;
            case "JUN":
                dag = dag + 151;
                break;
            case "JUL":
                dag = dag + 181;
                break;
            case "AUG":
                dag = dag + 212;
                break;
            case "SEP":
                dag = dag + 243;
                break;
            case "OCT":
                dag = dag + 273;
                break;
            case "NOV":
                dag = dag + 304;
                break;
            case "DEC":
                dag = dag + 334;
                break;
        }

        if ((jaar % 4) == 0 && !maand.equals("JAN") && !maand.equals("FEB")) {
            dag++;
        }

        while (jaar > 9) {
            jaar--;
            dag = dag + 365;
        }
        return dag;
    }

    public static int dag_uitv(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 9; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        String datum = regelIn.substring(begin, begin + 7);
        int dag = Integer.parseInt(datum.substring(0, 2));
        String maand = datum.substring(2, 5);
        int jaar = Integer.parseInt(datum.substring(5, 7));
        switch (maand) {
            case "FEB":
                dag = dag + 31;
                break;
            case "MAR":
                dag = dag + 59;
                break;
            case "APR":
                dag = dag + 90;
                break;
            case "MAY":
                dag = dag + 120;
                break;
            case "JUN":
                dag = dag + 151;
                break;
            case "JUL":
                dag = dag + 181;
                break;
            case "AUG":
                dag = dag + 212;
                break;
            case "SEP":
                dag = dag + 243;
                break;
            case "OCT":
                dag = dag + 273;
                break;
            case "NOV":
                dag = dag + 304;
                break;
            case "DEC":
                dag = dag + 334;
                break;
        }

        if ((jaar % 4) == 0 && !maand.equals("JAN") && !maand.equals("FEB")) {
            dag++;
        }

        while (jaar > 9) {
            jaar--;
            dag = dag + 365;
        }
        return dag;
    }

    public static int volgnr(String regelIn) {
        int checker = 0;
        String teken = new String();
        for (int i = 1; i <= 4; i++) {
            teken = regelIn.substring(checker, checker + 1);
            while (!teken.equals(",")) {
                checker++;
                teken = regelIn.substring(checker, checker + 1);
            }
            checker++;
        }
        int begin = checker;
        checker++;
        teken = regelIn.substring(checker, checker + 1);
        while (!teken.equals(",")) {
            checker++;
            teken = regelIn.substring(checker, checker + 1);
        }
        int eind = checker;
        int volgnr = Integer.parseInt(regelIn.substring(begin, eind));
        return volgnr;
    }

    public static PlaatsReturn plaatsen(int n, int m, int treinserie, String soortIn, boolean compare) {
        PlaatsReturn plaatsen = new PlaatsReturn();
        String plaats1 = new String("");
        String plaats2 = new String("");
        switch (treinserie) {
            case 500:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Avat";
                        plaats2 = "amf";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Hd";
                        plaats2 = "amf";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Hde";
                        plaats2 = "amf";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Dld";
                        plaats2 = "amf";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Ut";
                        plaats2 = "amf";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Hmlva";
                        plaats2 = "amf";
                    }
                }
                break;
            case 700:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Hea";
                        plaats2 = "zl";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "mp";
                        plaats2 = "zl";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Hgv";
                        plaats2 = "zl";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "ddv";
                        plaats2 = "mp";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "zl";
                        plaats2 = "mp";
                    } else if (compare || soortIn.equals("K")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Hde";
                        plaats2 = "mp";
                    }
                }
                break;
            case 1600:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "amfga";
                        plaats2 = "hvs";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "ama";
                        plaats2 = "hvs";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Sto";
                        plaats2 = "hvs";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "vtbr";
                        plaats2 = "hvs";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "dvaw";
                        plaats2 = "hvs";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Asra";
                        plaats2 = "hvs";
                    }
                }
                break;
            case 1700:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "bnva";
                        plaats2 = "amf";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "sto";
                        plaats2 = "amf";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Apda";
                        plaats2 = "amf";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "dld";
                        plaats2 = "amf";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Ut";
                        plaats2 = "amf";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Hmlva";
                        plaats2 = "amf";
                    }
                }
                break;
            case 2000:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "wdo";
                        plaats2 = "gd";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 10 - 20 minuten
                        plaats1 = "vtn";
                        plaats2 = "gd";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Ztmo";
                        plaats2 = "gd";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 10 - 20 minuten
                        plaats1 = "vb";
                        plaats2 = "gd";
                    }
                }
                break;
            case 2800:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "gd";
                        plaats2 = "rta";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "wd";
                        plaats2 = "rta";
                    } else if (compare || soortIn.equals("K")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Utwao";
                        plaats2 = "rta";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "vtn";
                        plaats2 = "ut";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "gdg";
                        plaats2 = "ut";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Nwki";
                        plaats2 = "ut";
                    }
                }
                break;
            case 3800:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Hdb";
                        plaats2 = "Omn";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Coa";
                        plaats2 = "Omn";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Na";
                        plaats2 = "Omn";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Cosb";
                        plaats2 = "Na";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Hdb";
                        plaats2 = "Na";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Omn";
                        plaats2 = "Na";
                    }
                }
                break;
            case 4000:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Sgbr";
                        plaats2 = "Zd";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Asdm";
                        plaats2 = "Zd";
                    } else if (compare || soortIn.equals("K")) {
                        // Even 25 - 35 minuten
                        plaats1 = "Bkla";
                        plaats2 = "Zd";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Dgrw";
                        plaats2 = "Dvd";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Ass";
                        plaats2 = "Dvd";
                    } else if (compare || soortIn.equals("K")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Zd";
                        plaats2 = "Dvd";
                    }
                }
                break;
            case 4500:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Asdma";
                        plaats2 = "Asd";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Kv";
                        plaats2 = "Asd";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Hvs";
                        plaats2 = "Asd";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Ass";
                        plaats2 = "Asd";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Zdk";
                        plaats2 = "Asd";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Hn";
                        plaats2 = "Asd";
                    }
                }
                break;
            case 4900:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Ndb";
                        plaats2 = "Almm";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Hvs";
                        plaats2 = "Almm";
                    } else if (compare || soortIn.equals("K")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Bln";
                        plaats2 = "Almm";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Hvsp";
                        plaats2 = "Uto";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Ndb";
                        plaats2 = "Uto";
                    } else if (compare || soortIn.equals("K")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Alms";
                        plaats2 = "Uto";
                    }
                }
                break;
            case 5500:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "dld";
                        plaats2 = "uto";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "st";
                        plaats2 = "uto";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Stz";
                        plaats2 = "Sd";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "bhv";
                        plaats2 = "Sd";
                    }
                }
                break;
            case 5600:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Pt";
                        plaats2 = "Avat";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Hd";
                        plaats2 = "Avat";
                    } else if (compare || soortIn.equals("K")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Ns";
                        plaats2 = "Avat";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Amf";
                        plaats2 = "Avat";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Bhv";
                        plaats2 = "Avat";
                    } else if (compare || soortIn.equals("K")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Uto";
                        plaats2 = "Avat";
                    }
                }
                break;
            case 5700:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Kv";
                        plaats2 = "Wp";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Bsmz";
                        plaats2 = "Wp";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Hvsp";
                        plaats2 = "Wp";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Vtbr";
                        plaats2 = "Ndb";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Dmnz";
                        plaats2 = "Ndb";
                    } else if (compare || soortIn.equals("K")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Rai";
                        plaats2 = "Ndb";
                    }
                }
                break;
            case 5800:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Kv";
                        plaats2 = "Dmn";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "hvsn";
                        plaats2 = "Dmn";
                    } else if (compare || soortIn.equals("K")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Brn";
                        plaats2 = "Dmn";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Kv";
                        plaats2 = "Hvsn";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Dmn";
                        plaats2 = "Hvsn";
                    } else if (compare || soortIn.equals("K")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Ods";
                        plaats2 = "Hvsn";
                    }
                }
                break;
            case 8000:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Gbg";
                        plaats2 = "mrb";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "dln";
                        plaats2 = "mrb";
                    } else if (compare || soortIn.equals("K")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Emnz";
                        plaats2 = "mrb";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Gbg";
                        plaats2 = "dln";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "mrb";
                        plaats2 = "dln";
                    } else if (compare || soortIn.equals("K")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Omn";
                        plaats2 = "dln";
                    }
                }
                break;
            case 8800:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Apn";
                        plaats2 = "Ldl";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Dwb";
                        plaats2 = "Ldl";
                    } else if (compare || soortIn.equals("K")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Hmlva";
                        plaats2 = "Ldl";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Bdg";
                        plaats2 = "wd";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "apn";
                        plaats2 = "wd";
                    } else if (compare || soortIn.equals("K")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Ld";
                        plaats2 = "wd";
                    }
                }
                break;
            case 9100:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Bl";
                        plaats2 = "Hgv";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Asn";
                        plaats2 = "Hgv";
                    } else if (compare || soortIn.equals("K")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Onn";
                        plaats2 = "Hgv";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Asn";
                        plaats2 = "Hrn";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Bl";
                        plaats2 = "Hrn";
                    } else if (compare || soortIn.equals("K")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Hgv";
                        plaats2 = "Hrn";
                    }
                }
                break;
            case 9500:
                if (n == 1 && m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                    // Even 5 - 15 minuten
                    plaats1 = "Wad";
                    plaats2 = "Bsk";
                } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                    // Oneven 5 - 15 minuten
                    plaats1 = "Bsk";
                    plaats2 = "Wad";
                }
                break;
            case 9800:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Mda";
                        plaats2 = "Ztm";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Gdg";
                        plaats2 = "Ztm";
                    } else if (compare || soortIn.equals("K")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Wdo";
                        plaats2 = "Ztm";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Gd";
                        plaats2 = "Gdg";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Ztmo";
                        plaats2 = "Gdg";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Vb";
                        plaats2 = "Gdg";
                    }
                }
                break;
            case 10500:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Hry";
                        plaats2 = "Swk";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Brdl";
                        plaats2 = "Swk";
                    } else if (compare || soortIn.equals("K")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Gw";
                        plaats2 = "Swk";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Wv";
                        plaats2 = "Hr";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Smvrt";
                        plaats2 = "Hr";
                    } else if (compare || soortIn.equals("K")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Ddv";
                        plaats2 = "Hr";
                    }
                }
                break;
            case 10700:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Wv";
                        plaats2 = "Swk";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Brdl";
                        plaats2 = "Swk";
                    } else if (compare || soortIn.equals("K")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Gw";
                        plaats2 = "Swk";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Hr";
                        plaats2 = "Gw";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Wv";
                        plaats2 = "Gw";
                    } else if (compare || soortIn.equals("K")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Swk";
                        plaats2 = "Gw";
                    }
                }
                break;
            case 12500:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Amfs";
                        plaats2 = "Amf";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Eml";
                        plaats2 = "Amf";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Hde";
                        plaats2 = "Amf";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Utlr";
                        plaats2 = "Ut";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Wdo";
                        plaats2 = "Ut";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Nwki";
                        plaats2 = "Ut";
                    }
                }
                break;
            case 14000:
                if (n == 2 && m == 1 && (compare || soortIn.equals("K"))) {
                    // Oneven 5 - 15 minuten
                    plaats1 = "Gdg";
                    plaats2 = "Nwk";
                } else if (n == 2 && m == 2 && (compare || soortIn.equals("K"))) {
                    // Oneven 15 - 25 minuten
                    plaats1 = "Wd";
                    plaats2 = "Nwk";
                } else if (n == 2 && compare || soortIn.equals("K")) {
                    // Oneven 25 - 35 minuten
                    plaats1 = "Utlr";
                    plaats2 = "Nwk";
                }
                break;
            case 20500:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "gd";
                        plaats2 = "Rta";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Wd";
                        plaats2 = "Rta";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Cps";
                        plaats2 = "gd";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "rtn";
                        plaats2 = "gd";
                    }
                }
                break;
            case 21700:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "gd";
                        plaats2 = "Rta";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Wd";
                        plaats2 = "Rta";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Cps";
                        plaats2 = "gd";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "rtn";
                        plaats2 = "gd";
                    }
                }
                break;
            case 9700:
                if (n == 1 && m == 1 && (compare || soortIn.equals("K"))) {
                    // Even 5 - 15 minuten
                    plaats1 = "nwk";
                    plaats2 = "rtn";
                } else if (m == 1 && (compare || soortIn.equals("K"))) {
                    // Oneven 5 - 15 minuten
                    plaats1 = "rtn";
                    plaats2 = "nwk";
                }
                break;
            case 12700:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Wdo";
                        plaats2 = "Gd";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Utwao";
                        plaats2 = "Gd";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Even 25 - 35 minuten              
                        plaats1 = "Ut";
                        plaats2 = "Gd";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Zlra";
                        plaats2 = "Zl";
                    } else if (m == 2 && (compare || soortIn.equals("A") || soortIn.equals("V"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Hde";
                        plaats2 = "Zl";
                    } else if (compare || soortIn.equals("A") || soortIn.equals("V")) {
                        // Oneven 25 - 35 minuten
                        plaats1 = "Hd";
                        plaats2 = "Zl";
                    }
                }
                break;
            case 19500:
                if (n == 1) {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Even 5 - 15 minuten
                        plaats1 = "Apn";
                        plaats2 = "ldl";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Even 15 - 25 minuten
                        plaats1 = "Wadn";
                        plaats2 = "ldl";
                    }
                } else {
                    if (m == 1 && (compare || soortIn.equals("K"))) {
                        // Oneven 5 - 15 minuten
                        plaats1 = "Apn";
                        plaats2 = "Wadn";
                    } else if (m == 2 && (compare || soortIn.equals("K"))) {
                        // Oneven 15 - 25 minuten
                        plaats1 = "Ztww";
                        plaats2 = "Wadn";
                    }
                }
                break;
            case 19800:
                if (n == 1 && m == 1 && (compare || soortIn.equals("K"))) {
                    // Even 5 - 15 minuten
                    plaats1 = "ztmo";
                    plaats2 = "vb";
                } else if (m == 1 && (compare || soortIn.equals("K"))) {
                    // Oneven 5 - 15 minuten
                    plaats1 = "vb";
                    plaats2 = "ztmo";
                }
                break;
        }

        plaatsen.init(plaats1, plaats2);
        return plaatsen;
    }
}