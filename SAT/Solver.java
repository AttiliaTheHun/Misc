import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.lang.Process;
import java.lang.Runtime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Set;
import java.util.HashSet;
import java.lang.StringBuilder;
import java.util.stream.Collectors;

public class Solver {
    private static final boolean DEBUG = false;
    public static final char A = 'A';
    public static final char C = 'C';
    public static final char G = 'G';
    public static final char T = 'T';
    private static final String DEFAULT_EXECUTABLE = "glucose-syrup";
    private static final String DEFAULT_FILENAME = "formula.cnf";
    private static final String SOLVER_RESULT_MARK = "s";
    private static final String SOLVER_MODEL_MARK = "v";
    private static final String SATISFIABLE = "SATISFIABLE";
    private static final String UNSAT_MESSAGE = "No such set exists.";
    private static final String END_OF_LINE = "0\n";
    private static final String DELIMITER = " ";
    public static final int WORD_LENGTH = 8;
    private static final int ALPHABET_SIZE = 4;
    private static final int VARIABLES_PER_WORD = WORD_LENGTH * ALPHABET_SIZE;
    private static int WORD_VARIABLES;
    private static int DISTINCT_PAIR_POSITION_DIFF_VARIABLES;
    private static int DISTINCT_PAIR_SYMBOL_DIFF_VARIABLES;
    private static int INDISTINCT_PAIR_POSITION_DIFF_VARIABLES;
    private static int INDISTINCT_PAIR_SYMBOL_DIFF_VARIABLES;
    private int wordCount;
    // file where the cnf formula will be stored
    private String filename;
    private ArrayList<String> cnf = new ArrayList<String>();

    public static void main(final String[] args) throws IOException {
        if (args.length == 0) {
            System.out.println("Enter the size of the set as an argument!");
            System.exit(0);
        }
        String filename = (args.length > 1) ? args[1] : DEFAULT_FILENAME;
        final Solver solver = new Solver(Integer.parseInt(args[0]), filename);
        solver.solveWithOutput();
    }

    public Solver(final int wordCount, final String filename) {
        this.wordCount = wordCount;
        this.filename = filename;
        // the number of variables that encode the actual words
        WORD_VARIABLES = wordCount * VARIABLES_PER_WORD;
        // the number of variables that encode a difference in a single symbol between two words
        // this is used for the evaluation of the second condition, we are counting distinct word pairs only
        DISTINCT_PAIR_SYMBOL_DIFF_VARIABLES = (wordCount * (wordCount-1))/2 * VARIABLES_PER_WORD;
        // the number of variables that encode a differnce on a single position between two words
        // this is used for the evaluation of the second condition, we are counting distinct word pairs only
        DISTINCT_PAIR_POSITION_DIFF_VARIABLES = (wordCount * (wordCount-1))/2 * WORD_LENGTH;
        // the number of variables that encode a difference in a single symbol between two words
        // this is used for the evaluation of the third condition, we are counting pairs made of a single word as well
        INDISTINCT_PAIR_SYMBOL_DIFF_VARIABLES = (wordCount * wordCount) * VARIABLES_PER_WORD;
        // the number of variables that encode a difference on a single position between two words
        // this is used for the evaluation of the third condition, we are counting pairs made of a single word as well
        INDISTINCT_PAIR_POSITION_DIFF_VARIABLES = (wordCount * wordCount) * WORD_LENGTH;
    }

    /**
     * Encodes the instance to CNF and passes it to the solver. Returns the models from the solver or empty list.
     * 
     * @returns List of the models (can be empty).
     */
    public ArrayList<ArrayList<String>> solve() throws IOException {
        encode();
        saveCNF();
        return executeSolver(false);
    }

    /**
    * Encodes the instance to CNF and passes it to the solver. The results along their human-readable form are printed to the standard output.
    */
    public void solveWithOutput() throws IOException {
        encode();
        saveCNF();
        if (DEBUG) saveCNFDebug();
        executeSolver(true);
    }

    private int getTotalVariables() {
        return WORD_VARIABLES + DISTINCT_PAIR_SYMBOL_DIFF_VARIABLES + DISTINCT_PAIR_POSITION_DIFF_VARIABLES + INDISTINCT_PAIR_SYMBOL_DIFF_VARIABLES + INDISTINCT_PAIR_POSITION_DIFF_VARIABLES;
    }

    /**
     * Encodes the instance to a CNF formula. The data is stored in {@link #cnf} variable.
     */
    private void encode() {
        encodeAlphabetConstraints();
        encodeFirstCondition();
        encodeSecondCondition();
        encodeThirdCondition();
    }

    /**
     * Encodes alphabet constraint for a single word. Alphabet constraint says the word is W^8, W = {A, C, G, T}.
     * 
     * @param wordNumber Number of the word to encode (zero-indexed).
     */
    private void encodeAlphabetConstraintsEncodeWord(final int wordNumber) {
        // first variable related to the word
        final int WORD_BASE = wordNumber * VARIABLES_PER_WORD;
        for (int i = 1; i < WORD_LENGTH+1; i++) {
            final int A = WORD_BASE + i;
            final int C = WORD_BASE + WORD_LENGTH + i;
            final int G = WORD_BASE + 2*WORD_LENGTH + i;
            final int T = WORD_BASE + 3*WORD_LENGTH + i;
            // at least one is true
            cnf.add(String.format("%d %d %d %d %s", A, C, G, T, END_OF_LINE));
            // no pair is true
            cnf.add(String.format("%d %d %s", -A, -C, END_OF_LINE));
            cnf.add(String.format("%d %d %s", -A, -G, END_OF_LINE));
            cnf.add(String.format("%d %d %s", -A, -T, END_OF_LINE));
            cnf.add(String.format("%d %d %s", -C, -G, END_OF_LINE));
            cnf.add(String.format("%d %d %s", -C, -T, END_OF_LINE));
            cnf.add(String.format("%d %d %s", -G, -T, END_OF_LINE));
        }
    }

    private void encodeAlphabetConstraints() {
        for (int i = 0; i < wordCount; i++) {
            encodeAlphabetConstraintsEncodeWord(i);
        }
    }

    /**
     * Encodes a single word to comply with the first condition. The first condition says that at least 4 of the characters are C or G.
     * 
     * @param wordNumber Number of the word to encode (zero-indexed).
     */
    private void encodeFirstConditionEncodeWord(final int wordNumber) {
        final Set<Set<Integer>> combinations = new HashSet<Set<Integer>>();
         // first variable related to the word
        final int WORD_BASE = wordNumber * VARIABLES_PER_WORD;
        // generate every possible 4-tuple of positions where C or G
        for (int p1 = 1; p1 < WORD_LENGTH-2; p1++) {
            final int C1 = WORD_BASE + WORD_LENGTH + p1;
            final int G1 = WORD_BASE + 2*WORD_LENGTH + p1;
            for (int p2 = p1+1; p2 < WORD_LENGTH-1; p2++) {
                final int C2 = WORD_BASE + WORD_LENGTH + p2;
                final int G2 = WORD_BASE + 2*WORD_LENGTH + p2;
                for (int p3 = p2+1; p3 < WORD_LENGTH; p3++) {
                    final int C3 = WORD_BASE + WORD_LENGTH + p3;
                    final int G3 = WORD_BASE + 2*WORD_LENGTH + p3;
                    for (int p4 = p3+1; p4 < WORD_LENGTH+1; p4++) {
                        final int C4 = WORD_BASE + WORD_LENGTH + p4;
                        final int G4 = WORD_BASE + 2*WORD_LENGTH + p4;
                        combinations.add(new HashSet<Integer>(Arrays.asList(C1, G1, C2, G2, C3, G3, C4, G4)));
                    }
                }
            }
        }

        for (final Set<Integer> combination : combinations) {
            final Set<String> combinationStrings = combination.stream().map(i -> Integer.toString(i)).collect(Collectors.toSet());
            cnf.add(String.format("%s %s", String.join(" ", combinationStrings), END_OF_LINE));
        }
    }

    private void encodeFirstCondition() {
        for (int i = 0; i < wordCount; i++) {
            encodeFirstConditionEncodeWord(i);
        }
    }

    /**
     * Encodes a pair of words to comply with the second condition. The second condition says that each distict pair of words differ in at least
     * 4 positions. The function expects the words to be distinct.
     * 
     * @param firstWordNumber Number of the first word (zero-indexed).
     * @param secondWordNumber Number of the second word (zero-indexed).
     * @param pairNumber Pair number in the context of the second condition (zero-indexed).
     */
    private void encodeSecondConditionEncodePair(final int firstWordNumber, final int secondWordNumber, final int pairNumber) {
        // starting indices of variables defining each of the words
        final int FIRST_WORD_BASE = firstWordNumber * VARIABLES_PER_WORD;
        final int SECOND_WORD_BASE = secondWordNumber * VARIABLES_PER_WORD;
        // where the variables defining difference of the symbols in the words start at
        final int PAIR_SYMBOL_DIFF_BASE = WORD_VARIABLES + pairNumber * VARIABLES_PER_WORD;
        // where the variables defining differnce at position in the words start at
        final int PAIR_POSITION_DIFF_BASE = WORD_VARIABLES + DISTINCT_PAIR_SYMBOL_DIFF_VARIABLES + pairNumber * WORD_LENGTH;
        final Set<Set<Integer>> combinations = new HashSet<Set<Integer>>();
        final int[][] FIRST_WORD = new int[ALPHABET_SIZE][WORD_LENGTH];
        final int[][] SECOND_WORD = new int[ALPHABET_SIZE][WORD_LENGTH];
        final int[][] SYMBOL_DIFF = new int[ALPHABET_SIZE][WORD_LENGTH];

        for (int i = 0; i < WORD_LENGTH; i++) {
            FIRST_WORD[0][i] = FIRST_WORD_BASE + i + 1;
            FIRST_WORD[1][i] = FIRST_WORD_BASE + WORD_LENGTH + i + 1;
            FIRST_WORD[2][i] = FIRST_WORD_BASE + 2*WORD_LENGTH + i + 1;
            FIRST_WORD[3][i] = FIRST_WORD_BASE + 3*WORD_LENGTH + i + 1;
            SECOND_WORD[0][i] = SECOND_WORD_BASE + i + 1;
            SECOND_WORD[1][i] = SECOND_WORD_BASE + WORD_LENGTH + i + 1;
            SECOND_WORD[2][i] = SECOND_WORD_BASE + 2*WORD_LENGTH + i + 1;
            SECOND_WORD[3][i] = SECOND_WORD_BASE + 3*WORD_LENGTH + i + 1;
            SYMBOL_DIFF[0][i] = PAIR_SYMBOL_DIFF_BASE + i + 1;
            SYMBOL_DIFF[1][i] = PAIR_SYMBOL_DIFF_BASE + WORD_LENGTH + i + 1;
            SYMBOL_DIFF[2][i] = PAIR_SYMBOL_DIFF_BASE + 2*WORD_LENGTH + i + 1;
            SYMBOL_DIFF[3][i] = PAIR_SYMBOL_DIFF_BASE + 3*WORD_LENGTH + i + 1;
        }

        for (int j = 0; j < FIRST_WORD.length; j++) {
            for (int i = 0; i < WORD_LENGTH; i++) {
                final int SYMBOL_DIFFERENCE = PAIR_SYMBOL_DIFF_BASE + j*WORD_LENGTH + i + 1;
                // symbol difference is true if and only the symbols at each index are different (XOR kinda thingy)
                combinations.add(new HashSet<Integer>(Arrays.asList(SYMBOL_DIFFERENCE, -FIRST_WORD[j][i], SECOND_WORD[j][i])));
                combinations.add(new HashSet<Integer>(Arrays.asList(SYMBOL_DIFFERENCE, FIRST_WORD[j][i], -SECOND_WORD[j][i])));
                combinations.add(new HashSet<Integer>(Arrays.asList(-SYMBOL_DIFFERENCE, -FIRST_WORD[j][i], -SECOND_WORD[j][i])));
                combinations.add(new HashSet<Integer>(Arrays.asList(-SYMBOL_DIFFERENCE, FIRST_WORD[j][i], SECOND_WORD[j][i])));
            }
        }
        
        for (int i = 0; i < WORD_LENGTH; i++) {
            final int POSITION_DIFFERENCE = PAIR_POSITION_DIFF_BASE + i + 1;
            // position difference is true if and only if at least one but not four symbol difference is true
            // only zero or two symbol differences can be true at a particular index
            combinations.add(new HashSet<Integer>(Arrays.asList(-POSITION_DIFFERENCE, SYMBOL_DIFF[0][i], SYMBOL_DIFF[1][i], SYMBOL_DIFF[2][i], SYMBOL_DIFF[3][i])));
            combinations.add(new HashSet<Integer>(Arrays.asList(POSITION_DIFFERENCE, -SYMBOL_DIFF[0][i])));
            combinations.add(new HashSet<Integer>(Arrays.asList(POSITION_DIFFERENCE, -SYMBOL_DIFF[1][i])));
            combinations.add(new HashSet<Integer>(Arrays.asList(POSITION_DIFFERENCE, -SYMBOL_DIFF[2][i])));
            combinations.add(new HashSet<Integer>(Arrays.asList(POSITION_DIFFERENCE, -SYMBOL_DIFF[3][i])));
        }
        
        // add every possile combination of four positions where the letter is different in the words
        for (int p1 = 1; p1 < WORD_LENGTH-3; p1++) {
            for (int p2 = p1+1; p2 < WORD_LENGTH-2; p2++) {
                for (int p3 = p2+1; p3 < WORD_LENGTH-1; p3++) {
                    for (int p4 = p3+1; p4 < WORD_LENGTH; p4++) {
                        combinations.add(new HashSet<Integer>(Arrays.asList(PAIR_POSITION_DIFF_BASE+p1, PAIR_POSITION_DIFF_BASE+p2, PAIR_POSITION_DIFF_BASE+p3, PAIR_POSITION_DIFF_BASE+p4)));
                    }
                }   
            }
        }
        
        for (final Set<Integer> combination : combinations) {
            final Set<String> combinationStrings = combination.stream().map(i -> Integer.toString(i)).collect(Collectors.toSet());
            cnf.add(String.format("%s %s", String.join(" ", combinationStrings), END_OF_LINE));
        }
    }

    private void encodeSecondCondition() {
        int pairNumber = 0;
        for (int i = 0; i < wordCount; i++) {
            for (int j = i+1; j < wordCount; j++) {
                encodeSecondConditionEncodePair(i, j, pairNumber);
                pairNumber++;
            }
        }
    }

    /**
     * Encodes a pair of words to comply with the third condition. The third condition says that for each pair of words (indistinct) the reverse of one
     * and the Wattson-Crick complement of the other differ in at least 4 positions.
     * 4 positions. The function expects the words to be distinct.
     * 
     * For better understanding of this function, take a look at {@link #encodeSecondConditionEncodePair(int, int, int)} as this is a slighlty altered version of it.
     * 
     * @param firstWordNumber Number of the first word (zero-indexed).
     * @param secondWordNumber Number of the second word (zero-indexed).
     * @param pairNumber Pair number in the context of the third condition (zero-indexed).
     */
    private void encodeThirdConditionEncodePair(final int firstWordNumber, final int secondWordNumber, final int pairNumber) {
        // starting indices of variables defining each of the words
        final int FIRST_WORD_BASE = firstWordNumber * VARIABLES_PER_WORD;
        final int SECOND_WORD_BASE = secondWordNumber * VARIABLES_PER_WORD;
        // we need to count the diff variables used in the second condition encoding as well
        final int PAIR_SYMBOL_DIFF_BASE = WORD_VARIABLES + DISTINCT_PAIR_SYMBOL_DIFF_VARIABLES + DISTINCT_PAIR_POSITION_DIFF_VARIABLES + pairNumber*VARIABLES_PER_WORD;
        final int PAIR_POSITION_DIFF_BASE = WORD_VARIABLES + DISTINCT_PAIR_SYMBOL_DIFF_VARIABLES + DISTINCT_PAIR_POSITION_DIFF_VARIABLES + INDISTINCT_PAIR_SYMBOL_DIFF_VARIABLES + pairNumber*WORD_LENGTH;
        final Set<Set<Integer>> combinations = new HashSet<Set<Integer>>();
        final int[][] FIRST_WORD = new int[ALPHABET_SIZE][WORD_LENGTH];
        final int[][] SECOND_WORD = new int[ALPHABET_SIZE][WORD_LENGTH];
        final int[][] SYMBOL_DIFF = new int[ALPHABET_SIZE][WORD_LENGTH];

        for (int i = 0; i < WORD_LENGTH; i++) {
            // here we reverse the first word
            FIRST_WORD[0][i] = FIRST_WORD_BASE + (WORD_LENGTH - i);
            FIRST_WORD[1][i] = FIRST_WORD_BASE + WORD_LENGTH + (WORD_LENGTH - i);
            FIRST_WORD[2][i] = FIRST_WORD_BASE + 2*WORD_LENGTH + (WORD_LENGTH - i);
            FIRST_WORD[3][i] = FIRST_WORD_BASE + 3*WORD_LENGTH + (WORD_LENGTH - i);

            // here we swap A <-> T and C <-> G
            SECOND_WORD[3][i] = SECOND_WORD_BASE + i + 1;
            SECOND_WORD[2][i] = SECOND_WORD_BASE + WORD_LENGTH + i + 1;
            SECOND_WORD[1][i] = SECOND_WORD_BASE + 2*WORD_LENGTH + i + 1;
            SECOND_WORD[0][i] = SECOND_WORD_BASE + 3*WORD_LENGTH + i + 1;

            SYMBOL_DIFF[0][i] = PAIR_SYMBOL_DIFF_BASE + i + 1;
            SYMBOL_DIFF[1][i] = PAIR_SYMBOL_DIFF_BASE + WORD_LENGTH + i + 1;
            SYMBOL_DIFF[2][i] = PAIR_SYMBOL_DIFF_BASE + 2*WORD_LENGTH + i + 1;
            SYMBOL_DIFF[3][i] = PAIR_SYMBOL_DIFF_BASE + 3*WORD_LENGTH + i + 1;
        }

        for (int j = 0; j < FIRST_WORD.length; j++) {
            for (int i = 0; i < WORD_LENGTH; i++) {
                final int SYMBOL_DIFFERENCE = PAIR_SYMBOL_DIFF_BASE + j*WORD_LENGTH + i + 1;
                combinations.add(new HashSet<Integer>(Arrays.asList(SYMBOL_DIFFERENCE, -FIRST_WORD[j][i], SECOND_WORD[j][i])));
                combinations.add(new HashSet<Integer>(Arrays.asList(SYMBOL_DIFFERENCE, FIRST_WORD[j][i], -SECOND_WORD[j][i])));
                combinations.add(new HashSet<Integer>(Arrays.asList(-SYMBOL_DIFFERENCE, -FIRST_WORD[j][i], -SECOND_WORD[j][i])));
                combinations.add(new HashSet<Integer>(Arrays.asList(-SYMBOL_DIFFERENCE, FIRST_WORD[j][i], SECOND_WORD[j][i])));
            }
        }
        
        for (int i = 0; i < WORD_LENGTH; i++) {
            final int POSITION_DIFFERENCE = PAIR_POSITION_DIFF_BASE + i + 1;
            combinations.add(new HashSet<Integer>(Arrays.asList(-POSITION_DIFFERENCE, SYMBOL_DIFF[0][i], SYMBOL_DIFF[1][i], SYMBOL_DIFF[2][i], SYMBOL_DIFF[3][i])));
            combinations.add(new HashSet<Integer>(Arrays.asList(POSITION_DIFFERENCE, -SYMBOL_DIFF[0][i])));
            combinations.add(new HashSet<Integer>(Arrays.asList(POSITION_DIFFERENCE, -SYMBOL_DIFF[1][i])));
            combinations.add(new HashSet<Integer>(Arrays.asList(POSITION_DIFFERENCE, -SYMBOL_DIFF[2][i])));
            combinations.add(new HashSet<Integer>(Arrays.asList(POSITION_DIFFERENCE, -SYMBOL_DIFF[3][i])));
        }
        
        for (int p1 = 1; p1 < WORD_LENGTH-3; p1++) {
            for (int p2 = p1+1; p2 < WORD_LENGTH-2; p2++) {
                for (int p3 = p2+1; p3 < WORD_LENGTH-1; p3++) {
                    for (int p4 = p3+1; p4 < WORD_LENGTH; p4++) {
                        combinations.add(new HashSet<Integer>(Arrays.asList(PAIR_POSITION_DIFF_BASE+p1, PAIR_POSITION_DIFF_BASE+p2, PAIR_POSITION_DIFF_BASE+p3, PAIR_POSITION_DIFF_BASE+p4)));
                    }
                }   
            }
        }
        
        for (final Set<Integer> combination : combinations) {
            final Set<String> combinationStrings = combination.stream().map(i -> Integer.toString(i)).collect(Collectors.toSet());
            cnf.add(String.format("%s %s", String.join(" ", combinationStrings), END_OF_LINE));
        }
    }

    private void encodeThirdCondition() {
        int pairNumber = 0;
        for (int i = 0; i < wordCount; i++) {
            for (int j = 0; j < wordCount; j++) {
                encodeThirdConditionEncodePair(i, j, pairNumber);
                pairNumber++;
            }
        }
    }

    /**
     * Saves the CNF formula to a file at {@link filename} in the DIMACS CNF format. The file is overwritten.
     */
    private void saveCNF() throws IOException {
        try (final BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            writer.write(String.format("p cnf %d %d\n", getTotalVariables(), cnf.size()));
            for (final String clause : cnf) {
                writer.write(clause);
            }
        }
    }

    /**
     * Writes a string of DIMACS CNF format to a writer in a form represents the variables' meaning within the context of the instance. This is a debug function.
     * 
     * @param writer The writer to write into.
     * @param s The string to save.
     */
    private void saveStringCNFDebug(final BufferedWriter writer, final String s) throws IOException {
        final int DISTINCT_PAIRS = (wordCount*(wordCount-1))/2;
        final int INDISTINCT_PAIRS = (wordCount*wordCount)/2;
        int count = 0;
        final String[] tokens = s.trim().split(" ");
        for (final String var : tokens) {
            int num = Integer.parseInt(var);
            final String sign = (num < 0) ? "-" : "";
            num = Math.abs(num);
            if (num == 0) {
                break;
            }
            num--;
            // variables that directly define the letters of the words
            if (num < WORD_VARIABLES) {
                final int wordNumber = num / VARIABLES_PER_WORD;
                num = num % VARIABLES_PER_WORD;
                char type;
                if (num >= 3*WORD_LENGTH) {
                    type = T;
                } else if (num >= 2*WORD_LENGTH) {
                    type = G;
                } else if (num >= WORD_LENGTH) {
                    type = C;
                } else {
                    type = A;
                }
                num = num % WORD_LENGTH;
                writer.write(String.format("%s%d_%c%d ", sign, wordNumber, type, num));
            // variables that say whether a symbol in a word pair is different (second condition)
            } else if (num < WORD_VARIABLES + DISTINCT_PAIR_SYMBOL_DIFF_VARIABLES) {
                num -= WORD_VARIABLES;
                final int pairNumber = num / VARIABLES_PER_WORD;
                num = num % VARIABLES_PER_WORD;
                char type;
                if (num >= 3*WORD_LENGTH) {
                    type = T;
                } else if (num >= 2*WORD_LENGTH) {
                    type = G;
                } else if (num >= WORD_LENGTH) {
                    type = C;
                } else {
                    type = A;
                }
                num = num % WORD_LENGTH;
                writer.write(String.format("%s%d_%c%dD ", sign, pairNumber, type, num));
            // variables that say whether a pair of words differs at a position (second condition)
            } else if (num < WORD_VARIABLES + DISTINCT_PAIR_SYMBOL_DIFF_VARIABLES + DISTINCT_PAIR_POSITION_DIFF_VARIABLES) {
                num -= WORD_VARIABLES + DISTINCT_PAIR_SYMBOL_DIFF_VARIABLES;
                final int pairNumber = num / WORD_LENGTH;
                num = num % WORD_LENGTH;
                writer.write(String.format("%s%d_D%d ", sign, pairNumber, num));
            // variables that say whether a symbol in two words differ (third condition)
            } else if (num < WORD_VARIABLES + DISTINCT_PAIR_SYMBOL_DIFF_VARIABLES + DISTINCT_PAIR_POSITION_DIFF_VARIABLES + INDISTINCT_PAIR_SYMBOL_DIFF_VARIABLES) {
                num -= WORD_VARIABLES + DISTINCT_PAIR_SYMBOL_DIFF_VARIABLES + DISTINCT_PAIR_POSITION_DIFF_VARIABLES;
                final int pairNumber = num / VARIABLES_PER_WORD;
                num = num % VARIABLES_PER_WORD;
                char type;
                if (num >= 3*WORD_LENGTH) {
                    type = T;
                } else if (num >= 2*WORD_LENGTH) {
                    type = G;
                } else if (num >= WORD_LENGTH) {
                    type = C;
                } else {
                    type = A;
                }
                num = num % WORD_LENGTH;
                writer.write(String.format("%s%d_%c%dD' ", sign, pairNumber, type, num));
            // variables that say whether two words differ at a position (third condition)
            } else {
                num -= WORD_VARIABLES + DISTINCT_PAIR_SYMBOL_DIFF_VARIABLES + DISTINCT_PAIR_POSITION_DIFF_VARIABLES + INDISTINCT_PAIR_SYMBOL_DIFF_VARIABLES;
                final int pairNumber = num / WORD_LENGTH;
                num = num % WORD_LENGTH;
                writer.write(String.format("%s%d_D%d' ", sign, pairNumber, num));
            }
            count++;
            // the zero is also in the array
            // this is pure cosmetics, when we want to print the model into the file, this separate the values for each of the words
            if (count == WORD_LENGTH && tokens.length > WORD_LENGTH+1) {
                writer.write('\n');
                count = 0;
            }
        }
    }

    /**
     * Saves the CNF formula in a descriptive format to a debug file.
     */
    private void saveCNFDebug() throws IOException {
        try (final BufferedWriter writer = new BufferedWriter(new FileWriter(filename + "_debug"))) {
            writer.write(String.format("p cnf %d %d\n", getTotalVariables(), cnf.size()));
            for (final String clause : cnf) {
                saveStringCNFDebug(writer, clause);
                writer.write('\n');
            }
        }
    }

    /**
     * Executes the solver upon the encoded instance and returns the parsed models. If configured, it prints the output to the standard output instead and it also
     * parses te results into a humnan-readable form and prints it alongside the solver output.     * 
     * 
     * @param printOutput Whether to print the output to the standard output.
     * @return List of models (model is a list of words) or null (in print mode).
     */
    private ArrayList<ArrayList<String>> executeSolver(final boolean printOutput) throws IOException {
        final Process p = Runtime.getRuntime().exec(new String[]{"./" + DEFAULT_EXECUTABLE, "-model", filename});
        try (final BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()))) {
            return parseSolverOutput(br, printOutput);
        }
    }

    /**
     * Parses a string of space-separated signed-integer-encoded variables (a model) into a set of words in the alphabet. 
     * 
     * @param model The string to parse
     * @return List of words.
     */
    private ArrayList<String> parseModel(final String model) {
        final String[] tokens = model.split((DELIMITER));
        ArrayList<String> result = new ArrayList<String>();
        StringBuilder word = new StringBuilder();
        int word_offset = 0;
        for (int w = 0; w < wordCount; w++) {
            word_offset = w * VARIABLES_PER_WORD;
            for (int i = 0; i < WORD_LENGTH; i++) {
                final int _A = word_offset + i;
                final int _C = word_offset + WORD_LENGTH + i;
                final int _G = word_offset + 2*WORD_LENGTH + i;
                final int _T = word_offset + 3*WORD_LENGTH + i;
                if (!tokens[_A].startsWith("-")) {
                    word.append(A);
                    continue;
                }
                if (!tokens[_C].startsWith("-")) {
                    word.append(C);
                    continue;
                }
                if (!tokens[_G].startsWith("-")) {
                    word.append(G);
                    continue;
                }
                if (!tokens[_T].startsWith("-")) {
                    word.append(T);
                    continue;
                }
            }
            result.add(word.toString());
            word.setLength(0);
        }
        return result;
    }

    /**
     * Parses the output from the solver into a sets of words (the actual models). It can either return the parsed models or print them to the standard output
     * alongside the solver output. 
     * 
     * @param reader The reader to read the input from.
     * @param printOutput Whether to print the output to the standard output instead.
     * @return List of models (model is a list of words) or null (in print mode).
     */
    private ArrayList<ArrayList<String>> parseSolverOutput(final BufferedReader reader, final boolean printOutput) throws IOException {
        String result = null;
        final ArrayList<ArrayList<String>> models = new ArrayList<ArrayList<String>>();
        String line;
        while ((line = reader.readLine()) != null) {
            if (printOutput) {
                System.out.println(line);
            }
            if (line.startsWith(SOLVER_RESULT_MARK)) {
                result = line.substring(1).trim();
            } else if (line.startsWith(SOLVER_MODEL_MARK)) {
                models.add(parseModel(line.substring(1, line.length()-1).trim()));
                if (DEBUG) {
                    try (final BufferedWriter writer = new BufferedWriter(new FileWriter(filename + "_debug", true))) {
                        writer.write("\n\nmodel:\n");
                        saveStringCNFDebug(writer, line.substring(1, line.length()-1).trim());
                        writer.write('\n');
                    } 
                }
            }
        }

        if (!printOutput) {
            return models;
        }

        System.out.println();
        System.out.println("##############################################################");
        System.out.println("###########[ Human readable result of the problem ]###########");
        System.out.println("##############################################################");
        System.out.println();
        
        if (!result.equals(SATISFIABLE)) {
            System.out.println(UNSAT_MESSAGE);
            return null;
        }

        for (final ArrayList<String> model : models) {
            System.out.println(String.format("Set of %d words:", wordCount));
            for (final String word : model) {
                System.out.println(word);
            }
            System.out.println();
        }
        return null;
    }


}