# Word design for DNA computing on surfaces


The SAT solver used is [Glucose](https://www.labri.fr/perso/lsimon/research/glucose/), more specifically [Glucose 4.2.1](https://github.com/audemard/glucose/releases/tag/4.2.1). Its source code can becompiled using

```
cmake .
make
```

## Problem description
*Originally from <https://www.csplib.org/Problems/prob033/>.*

> Problem: find as large a set S of strings (words) of length 8 over the alphabet W = { A,C,G,T } with the following properties:                
> - Each word in S has 4 symbols from { C,G };
> - Each pair of distinct words in S differ in at least 4 positions; and
> - Each pair of words x and y in S (where x and y may be identical) are such that x^R and y^C differ in at least 4 positions. Here, ( x1,…,x8 )^R = ( x8,…,x1 ) is the reverse of ( x1,…,x8 ) and ( y1,…,y8 )^C is the Watson-Crick complement of ( y1,…,y8 ), i.e. the word where each A is replaced by a T and vice versa and each C is replaced by a G and vice versa.

This program focuses on a slightly altered version where instead of finding a maximum set we will be testing whether a set of a particular size exists. The input to the program is therefore simply a number *k* that denotes the size of the set. The reason is that SAT is a decision problem (yes/no).

## Encoding
As the words uses a four-symbol alphabet, one character is encoded using four variables (`A`, `C`, `G`, `T`) where exactly one is true. This gives us 32 variables per word as words are 8 characters long. We need to enforce the alphabet constraint, so for each character in each word we add the following clauses: `(A v G v C v T)` to ensure at least one is true and `(-X v -Y)` where `X` and `Y` are replaced with each of the symbols to ensure that no two (or more) variables are true at the same time.

To encode the first condition, we add a clause `(C1 v G1 v C2 v G2 v C3 v G3 v C4 v G4)` in each word for every possible combination of four positions in the word (all the indices 1-8). In the clause, `C1` and `G1` repectively mean the `C` and `G` variables corresponding to the first position in the combination (not necessarily in the word) and so on. This ensures that at least four position are occupied by the letters `C` or `G`.

The second condition is quite tricky. We start by introducing two new kinds of variables. For each pair of words, we will have `An_D`, `Cn_D`, `Gn_D` and `Tn_D` variables where `n` is the position of the letter, in total it is 32 new variables per pair. The variable `A3_D` is then true if and only if the variables `A3` corresponding to both of the words have different values. The other new variables will be in the form of `Dn` where `n` is again an index in the word. There will be only 8 of these per pair and each one will be true if and only if the two words differ at the index `n`.

To encode a variable such as `T3_D`, we simply convert `T3_D <-> ¬(T3_X <-> T3_Y)` to CNF. (`T3_X` is `T3` in the word `X` and `T3_Y` is the same in word `Y`). The result is `(T3_D v ¬T3_X v T3_Y) ^ (T3_D v T3_X v ¬T3_Y) ^ (¬T3_D v ¬T3_X v ¬T3_Y) ^ (¬T3_D v T3_X v T3_Y)`. We need to add this expression for every single one of the auxilary 32 symbol difference variables.

As it happens, for any index `n` either all `An_D`, `Cn_D`, `Gn_D` and `Tn_D` will be false (in case the two words do not differ at this index) or two of them will be true and two will be false (for example there will be a `G` in one word and `T` in the other, but no `A` and `C` in either on this particular index). Therefore we can encode `Dn` as `(¬Dn v An_D v Cn_D v Gn_D v Tn_D) ^ (Dn v ¬An_D) ^ (Dn v ¬Cn_D) ^ (Dn v ¬Gn_D) ^ (Dn v ¬Tn_D)`. That is the CNF equivalent of `Dn <-> (An_D v Cn_D v Gn_D v Tn_D)`.

Now that we have these `Dn` variables available, we will again add every possible combination of four of these to the formula. 

Encoding the third condition is relatively trivial once we get the second one working. It is a simple matter of swapping `A` for `T` and `G` for `C` variables for each other (in both ways) in the word Y and a matter of reverse ordering the indixes in the word X. A subtle yet important difference though is that while the second condition only applies to each distinct pair of words, for the third condition, we will be testing every possible pair.


## User documentation
Navigate to the project folder and do this (you need a decently modern installation of [JDK](https://adoptium.net/temurin))
```bash
# compile
javac Solver.java
# run
java Solver k [OUTPUT_FILE]
```
Command-line options:
- `k` size of the set to try
- `OUTPUT_FILE` filename of the cnf formula file (optional)

If the run is successful, you will see the solver output and then a line-separated list of words. If a set of the specified magnitude is non-existent, you will see a message instead.

#### Running the test
compile (obviously you need the `junit-jupiter-api` jar file and point to *your* copy, you can `wget` it from the [Maven Repository](https://mvnrepository.com/))
```bash
javac -cp .:/usr/share/java/junit-jupiter-api-6.1.0-M1.jar SolverTest.java
```
```bash
# execute (same point as above)
java -jar /usr/share/java/junit-platform-console-standalone-6.1.0-M1.jar execute -cp . -c SolverTest

# execute specific test
java -jar /usr/share/java/junit-platform-console-standalone-6.1.0-M1.jar execute -cp . --select=method:SolverTest#testSecondCondition

# run the tests for a custom k to verify the output is correct
java -cp .:/usr/share/java/junit-platform-console-standalone-6.1.0-M1.jar SolverTest k
```

## Example instances
The script runs fairly quickly for small numbers, such as 15 and you can decide that the solutions it outputs match the criteria. You can also use the testing script (after reviewing its source code).

However when I went an order of magnitude higher and tried to run it with `k=100` (actually even 60 seems to be enough), it went on and on and I finally decided to stop it so I could go to bed. The problem is that the number of clauses rises quadratically as every word in the set is related to every other. Apparently, my laptop was not meant to handle `3 361 400` clauses worth of CNF.