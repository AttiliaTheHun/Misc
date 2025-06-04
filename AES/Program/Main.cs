using Program.AESLib;
using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;

namespace Program;
/// <summary>
/// Example class that uses the library for basic file encryption and decryption.
/// 
/// Command line usage
/// 
/// Program "input_file" "output_file" "encryption_password" "encrypt/decrypt"
/// </summary>
public class Example {
    public static void Main(string[] args) {
        string inputFile = GetInputFile(args);
        string outputFile = GetOutputFile(args);
        string encPassword = GetEncryptionPassword(args);
        bool encrypting = GetEncrypting(args);
        try {
            if (encrypting) {
                EncryptFile(inputFile, outputFile, encPassword);
                Console.WriteLine("Encryption finished");
            } else {
                DecryptFile(inputFile, outputFile, encPassword);
                Console.WriteLine("Decryption finished");
            }
        } catch (Exception e) {
            Console.WriteLine($"Failed: {e.Message}");
            //Console.WriteLine($"Failed: {e.StackTrace}");
        }
    }

    private static string GetInputFile(string[] args) {
        if (args.Length > 0) {
            return args[0];
        }
        Console.Write("Input file: ");
        return Console.ReadLine();
    }

    private static string GetOutputFile(string[] args) {
        if (args.Length > 1) {
            return args[1];
        }
        Console.Write("Output file: ");
        return Console.ReadLine();
    }

    private static string GetEncryptionPassword(string[] args) {
        if (args.Length > 2) {
            return args[2];
        }
        Console.Write("Password: ");
        return Console.ReadLine();
    }

    private static bool GetEncrypting(string[] args) {
        string input;
        if (args.Length > 3) {
            input = args[3];
        } else {
            Console.Write("Encrypt or decrypt? (e/d): ");
            input = Console.ReadLine();
        }
        return input switch {
            "decrypt" or "dec" or "d" => false,
            _ => true,
        };
    }

    /// <summary>
    /// Encrypts a file using AES and a custom password.
    /// </summary>
    /// <param name="inputFile">target file</param>
    /// <param name="outputFile">output of the encryption</param>
    /// <param name="password">the encryption password</param>
    private static void EncryptFile(string inputFile, string outputFile, string password) {
        byte[] clearText = File.ReadAllBytes(inputFile);
        using SymmetricAlgorithm cipher = new AES();
        using (MemoryStream memoryStream = new()) {
            // store the iv at the beginning of the file
            memoryStream.Write(cipher.IV);
            cipher.Key = DeriveKey(password, cipher);
            using (ICryptoTransform transform = cipher.CreateEncryptor())
            using (CryptoStream cryptoStream = new CryptoStream(memoryStream, transform, CryptoStreamMode.Write)) {
                cryptoStream.Write(clearText);
                cryptoStream.FlushFinalBlock();
                File.WriteAllBytes(outputFile, memoryStream.ToArray());
            }
        }
    }

    /// <summary>
    /// Decrypts a file using AES and a custom password.
    /// </summary>
    /// <param name="inputFile">target file</param>
    /// <param name="outputFile">output of the decryption</param>
    /// <param name="password">the decryption password</param>
    private static void DecryptFile(string inputFile, string outputFile, string password) {
        byte[] fileData = File.ReadAllBytes(inputFile);
        using SymmetricAlgorithm cipher = new AES();
        using (MemoryStream memoryStream = new()) {
            // load the iv that is stored at the beginning
            cipher.IV = [.. fileData.Take(cipher.BlockSize / 8)];
            byte[] cipherText = [.. fileData.Skip(16)];
            cipher.Key = DeriveKey(password, cipher);
            using (ICryptoTransform transform = cipher.CreateDecryptor())
            using (CryptoStream cryptoStream = new CryptoStream(memoryStream, transform, CryptoStreamMode.Write)) {
                cryptoStream.Write(cipherText);
                cryptoStream.FlushFinalBlock();
            }
            File.WriteAllBytes(outputFile, memoryStream.ToArray());
        }
    }

    /// <summary>
    /// Derives a cryptographic key from a password / passphrase that statisfies the length requirements of the specified cipher..
    /// </summary>
    /// <param name="password">the encryption password</param>
    /// <param name="cipher">the target cipher</param>
    /// <returns>the cryptographic key</returns>
    private static byte[] DeriveKey(string password, SymmetricAlgorithm cipher) {
        // derive encryption key from the password using PBKDF2
        return new Rfc2898DeriveBytes(password, 0, 310000, HashAlgorithmName.SHA256).GetBytes(cipher.KeySize / 8);
    }
}