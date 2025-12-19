// source: https://stackoverflow.com/questions/108819/best-way-to-randomize-an-array-with-net
using System;

namespace Pexeso;

public static class RandomExtensions {
    // Modified, it will not be used multiple times on the same array so the modification should not cause problems
    public static void Shuffle<T> (this T[] array) {
        Random rng = new Random();
        int n = array.Length;
        while (n > 1) {
            int k = rng.Next(n--);
            T temp = array[n];
            array[n] = array[k];
            array[k] = temp;
        }
    }
}