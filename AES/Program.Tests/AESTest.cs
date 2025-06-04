using System;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using Program.AESLib;

namespace Tests {

    [TestFixture]
    public class AESTest {
        private static int BLOCK_SIZE = 16; // in bytes

        private static byte[] CBCEncryptMessage(string message, byte[] key, byte[] iv) {
            byte[] cipherText;
            using AES cipher = new AES();
            cipher.Key = key;
            cipher.IV = iv;
            cipher.Mode = CipherMode.CBC;
            cipher.Padding = PaddingMode.PKCS7;
            using (MemoryStream memoryStream = new()) {
                using (ICryptoTransform transform = cipher.CreateEncryptor())
                using (CryptoStream cryptoStream = new CryptoStream(memoryStream, transform, CryptoStreamMode.Write)) {
                    cryptoStream.Write(Encoding.UTF8.GetBytes(message));
                    cryptoStream.FlushFinalBlock();
                }
                cipherText = memoryStream.ToArray();
            }
            return cipherText;
        }

        private static string CBCDecryptMessage(byte[] cipherText, byte[] key, byte[] iv) {
            byte[] plainText;
            using AES cipher = new AES();
            cipher.Key = key;
            cipher.IV = iv;
            cipher.Mode = CipherMode.CBC;
            cipher.Padding = PaddingMode.PKCS7;
            using (MemoryStream memoryStream = new()) {
                using (ICryptoTransform transform = cipher.CreateDecryptor())
                using (CryptoStream cryptoStream = new CryptoStream(memoryStream, transform, CryptoStreamMode.Write)) {
                    cryptoStream.Write(cipherText);
                    cryptoStream.FlushFinalBlock();
                }
                plainText = memoryStream.ToArray();
            }
            return Encoding.UTF8.GetString(plainText); ;
        }

        [Test]
        public void CBCPasswordMessageEncryptionDecryptionTest() {
            const string message = "Hello there world general Kenobi!";
            const string password = "Joe";
            // derive encryption key from the password using PBKDF2
            byte[] key = new Rfc2898DeriveBytes(password, 0, 310000, HashAlgorithmName.SHA256).GetBytes(BLOCK_SIZE);
            byte[] iv = RandomNumberGenerator.GetBytes(BLOCK_SIZE);

            byte[] cipherText = CBCEncryptMessage(message, key, iv);
            Debug.Assert(cipherText.Length % (BLOCK_SIZE) == 0, "cipher text length is not a multiple of the block size");

            string plainText = CBCDecryptMessage(cipherText, key, iv);
            Debug.Assert(message == plainText, $"original and decrypted message mismatch: '[{BitConverter.ToString(Encoding.UTF8.GetBytes(plainText)).Replace("-", ", ")}]' original: '[{BitConverter.ToString(Encoding.UTF8.GetBytes(message)).Replace("-", ", ")}]'");
        }

    }
}