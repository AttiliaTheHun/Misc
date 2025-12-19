import java.util.ArrayList;
import java.lang.StringBuilder;
import java.io.IOException;

import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class SolverTest {
    private static int TEST_WORDS = 10;

    private ArrayList<ArrayList<String>> getModels(final int words) throws IOException {
        final Solver solver = new Solver(words, "formula-test.cnf");
        return solver.solve();
    }

    @Test
    public void testWordLength() throws IOException {
        final ArrayList<ArrayList<String>> models = getModels(TEST_WORDS);
        for (final ArrayList<String> model : models) {
            for (final String word : model) {
                assertTrue(word.length() == Solver.WORD_LENGTH, String.format("alphabet non-conformant word: %s", word));
            }
        }
    }

    private boolean wordCompliesAlphabet(final String word) {
        assertTrue(word.length() == Solver.WORD_LENGTH);
        for (final char c : word.toCharArray()) {
            switch (c) {
                case Solver.A:
                case Solver.C:
                case Solver.G:
                case Solver.T:
                    break;
                default:
                    return false;
            }
        }
        return true;
    }

    @Test
    public void testWordsComplyAlphabet() throws IOException {
        final ArrayList<ArrayList<String>> models = getModels(TEST_WORDS);
        for (final ArrayList<String> model : models) {
            for (final String word : model) {
                assertTrue(wordCompliesAlphabet(word), String.format("alphabet non-conformant word: %s", word));
            }
        }
    }

    private boolean wordSatisfiesFirstCondition(final String word) {
        final int MIN_COUNT = 4;
        int count = 0;
        for (final char c : word.toCharArray()) {
            switch (c) {
                case Solver.C:
                case Solver.G:
                    count++;
                    break;
            }
        }
        return count >= MIN_COUNT;
    }

    @Test
    public void testFirstCondition() throws IOException {
        final ArrayList<ArrayList<String>> models = getModels(TEST_WORDS);
        for (final ArrayList<String> model : models) {
            for (final String word : model) {
                assertTrue(wordSatisfiesFirstCondition(word), String.format("first-condition-breaking word: %s", word));
            }
        }
    }

    private boolean wordsSatisfySecondCondition(final String first, final String second) {
        final int REQUIRED_DIFFERENCE = 4;
        final char[] firstWord = first.toCharArray();
        final char[] secondWord = second.toCharArray();
        int diff = 0;

        for (int i = 0; i < firstWord.length; i++) {
            if (firstWord[i] != secondWord[i]) {
                diff++;
            }
        }
        return diff >= REQUIRED_DIFFERENCE;
    }

    @Test
    public void testSecondCondition() throws IOException {
        final ArrayList<ArrayList<String>> models = getModels(TEST_WORDS);
        assertFalse(models.isEmpty(), "model expected, received empty list");
        for (final ArrayList<String> model : models) {
            assertFalse(model.isEmpty(), "received empty model though solution exists");
            for (int i = 0; i < model.size(); i++) {
                for (int j = i+1; j < model.size(); j++) {
                    assertTrue(wordsSatisfySecondCondition(model.get(i), model.get(j)), String.format("second-condition-breaking word: %s, %s", model.get(i), model.get(j)));
                }
            }
        }
    }

    private String getReverseString(final String s) {
        return new StringBuilder(s).reverse().toString();
    }

    private String getWattsonCrickComplement(final String word) {
        final char[] wordChars = word.toCharArray();
        final char[] result = new char[word.length()];
        for (int i = 0; i < wordChars.length; i ++) {
            switch (wordChars[i]) {
                case Solver.A:
                    result[i] = Solver.T;
                    break;
                case Solver.C:
                    result[i] = Solver.G;
                    break;
                case Solver.G:
                    result[i] = Solver.C;
                    break;
                case Solver.T:
                    result[i] = Solver.A;
                    break;
            }
        }
        return new String(result);
    }

    private boolean wordsSatisfyThirdCondition(final String first, final String second) {
        return wordsSatisfySecondCondition(getReverseString(first), getWattsonCrickComplement(second));
    }

    @Test
    public void testThirdCondition() throws IOException {
        final ArrayList<ArrayList<String>> models = getModels(TEST_WORDS);
        assertFalse(models.isEmpty(), "model expected, received empty list");
        for (final ArrayList<String> model : models) {
            assertFalse(model.isEmpty(), "received empty model though solution exists");
            for (int i = 0; i < model.size(); i ++) {
                for (int j = 0; j < model.size(); j++) {
                    assertTrue(wordsSatisfyThirdCondition(model.get(i), model.get(j)), String.format("third-condition-breaking word: %s, %s", model.get(i), model.get(j)));
                }
            }
        }
    }
    // Since the tests are automated, they only
    public static void main(final String[] args) throws IOException {
        if (args.length == 0) {
            System.out.println("If you do not wish to provide a set size, you had better run the class as a proper test suite! Otherwise run with an integer argument.");
            System.out.println("When running tests with a custom set size, receiving an empty model may not the wrong result.");
            System.out.println("Running tests with default set size...");
        } else {
            TEST_WORDS = Integer.parseInt(args[0]);
        }
        final SolverTest solverTest = new SolverTest();
        solverTest.testWordLength();
        solverTest.testWordsComplyAlphabet();
        solverTest.testFirstCondition();
        solverTest.testSecondCondition();
        solverTest.testThirdCondition();
        System.out.printf("All tests passed for a set size of %d\n", TEST_WORDS);
    }
}