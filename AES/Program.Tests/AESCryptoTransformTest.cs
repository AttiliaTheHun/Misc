using System;
using System.Diagnostics;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using Program.AESLib;

namespace Tests {

    [TestFixture]
    public class AESCryptoTransformTest {
        private static int BLOCK_SIZE = 16; // in bytes
        static readonly byte[] ZERO_IV = new byte[BLOCK_SIZE];

        private static AESCryptoTransform GetTestTransform() {
            return new AESCryptoTransform(RandomNumberGenerator.GetBytes(BLOCK_SIZE), ZERO_IV, PaddingMode.None, CipherMode.ECB, true);
        }

        private static AESCryptoTransform GetTestTransform(byte[] key) {
            return new AESCryptoTransform(key, ZERO_IV, PaddingMode.None, CipherMode.ECB, true);
        }

        [SetUp]
        public void Setup() { }

        [Test]
        public void GetWordTest() {
            byte[] testInput = [0x00, 0x01, 0x02, 0x03, 0x63, 0xa9, 0x1f, 0x88];
            int testIndex = 1;
            byte[] testOutput = [0x63, 0xa9, 0x1f, 0x88];
            byte[] output = AESCryptoTransform.GetWord(testInput, testIndex);
            Debug.Assert(testOutput.Length == output.Length, $"invalid output lenght: {output.Length} expected: {testOutput.Length}");
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void RotWordTest() {
            byte[] testWord = [0x63, 0xa9, 0x1f, 0x88];
            byte[] testOutput = [0xa9, 0x1f, 0x88, 0x63];
            byte[] output = AESCryptoTransform.RotWord(testWord);
            Debug.Assert(testOutput.Length == output.Length, $"invalid output lenght: {output.Length} expected: {testOutput.Length}");
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void SubWordTest() {
            byte[] testWord = [0x63, 0xa9, 0x1f, 0x88];
            byte[] testOutput = [0xfb, 0xd3, 0xc0, 0xc4];
            byte[] output = GetTestTransform().SubWord(testWord);
            Debug.Assert(testOutput.Length == output.Length, $"invalid output lenght: {output.Length} expected: {testOutput.Length}");
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void TransposeMatrixTest() {
            byte[] testMatrix = [0x63, 0xa9, 0x1f, 0x88, 0xfb, 0xd3, 0xc0, 0xc4, 0x00];
            byte[] testOutput = [0x63, 0x88, 0xc0, 0xa9, 0xfb, 0xc4, 0x1f, 0xd3, 0x00];
            byte[] output = (byte[]) testMatrix.Clone();
            AESCryptoTransform.TransposeMatrix(output);
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void ExpandKeyTest_128bits() {
            byte[] testKey = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c];
            byte[] expandedTestKey = Convert.FromHexString("2b7e151628aed2a6abf7158809cf4f3ca0fafe1788542cb123a339392a6c7605f2c295f27a96b9435935807a7359f67f3d80477d4716fe3e1e237e446d7a883bef44a541a8525b7fb671253bdb0bad00d4d1c6f87c839d87caf2b8bc11f915bc6d88a37a110b3efddbf98641ca0093fd4e54f70e5f5fc9f384a64fb24ea6dc4fead27321b58dbad2312bf5607f8d292fac7766f319fadc2128d12941575c006ed014f9a8c9ee2589e13f0cc8b6630ca6");
            byte[] expandedKey = GetTestTransform(testKey).expandedKey;
            Assert.That(expandedKey, Is.EqualTo(expandedTestKey).AsCollection, $"incorrect output: [{string.Join(',', expandedKey)}] expected: [{string.Join(',', expandedTestKey)}]");
        }

        [Test]
        public void ExpandKeyTest_192bits() {
            byte[] testKey = Convert.FromHexString("8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b");
            byte[] expandedTestKey = Convert.FromHexString("8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7bfe0c91f72402f5a5ec12068e6c827f6b0e7a95b95c56fec24db7b4bd69b5411885a74796e92538fde75fad44bb095386485af05721efb14fa448f6d94d6dce24aa326360113b30e6a25e7ed583b1cf9a27f939436a94f767c0a69407d19da4e1ec1786eb6fa64971485f703222cb8755e26d135233f0b7b340beeb282f18a2596747d26b458c553ea7e1466c9411f1df821f750aad07d753ca4005388fcc5006282d166abc3ce7b5e98ba06f448c773c8ecc720401002202");
            byte[] expandedKey = GetTestTransform(testKey).expandedKey;
            Assert.That(expandedKey, Is.EqualTo(expandedTestKey).AsCollection, $"incorrect output: [{string.Join(',', expandedKey)}] expected: [{string.Join(',', expandedTestKey)}]");
        }

        [Test]
        public void ExpandKeyTest_256bits() {
            byte[] testKey = Convert.FromHexString("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4");
            byte[] expandedTestKey = Convert.FromHexString("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff49ba354118e6925afa51a8b5f2067fcdea8b09c1a93d194cdbe49846eb75d5b9ad59aecb85bf3c917fee94248de8ebe96b5a9328a2678a647983122292f6c79b3812c81addadf48ba24360af2fab8b46498c5bfc9bebd198e268c3ba709e0421468007bacb2df331696e939e46c518d80c814e20476a9fb8a5025c02d59c58239de1369676ccc5a71fa2563959674ee155886ca5d2e2f31d77e0af1fa27cf73c3749c47ab18501ddae2757e4f7401905acafaaae3e4d59b349adf6acebd10190dfe4890d1e6188d0b046df344706c631e");
            byte[] expandedKey = GetTestTransform(testKey).expandedKey;
            Assert.That(expandedKey, Is.EqualTo(expandedTestKey).AsCollection, $"incorrect output: [{string.Join(',', expandedKey)}] expected: [{string.Join(',', expandedTestKey)}]");
        }

        [Test]
        public void AddRoundKeyTest() {
            byte[] testState = [];
            byte[] testRoundKey = [];
            byte[] testOutput = [];
            byte[] output = AESCryptoTransform.AddRoundKey(testState, testRoundKey);
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void SubBytesTest() {
            byte[] testState = [0x12, 0xfe, 0x04, 0xe0, 0x5f, 0x18, 0x9a, 0xab, 0x67, 0xd4, 0xc2, 0x90, 0x8d, 0xa5, 0xc0, 0x00];
            byte[] testOutput = [0xc9, 0xbb, 0xf2, 0xe1, 0xcf, 0xad, 0xb8, 0x62, 0x85, 0x48, 0x25, 0x60, 0x5d, 0x06, 0xba, 0x63];
            byte[] output = new AESCryptoTransform(ZERO_IV, ZERO_IV, PaddingMode.None, CipherMode.CBC, true).SubBytes(testState);
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void UnsubBytesTest() {
            byte[] testState = [0xc9, 0xbb, 0xf2, 0xe1, 0xcf, 0xad, 0xb8, 0x62, 0x85, 0x48, 0x25, 0x60, 0x5d, 0x06, 0xba, 0x63];
            byte[] testOutput = [0x12, 0xfe, 0x04, 0xe0, 0x5f, 0x18, 0x9a, 0xab, 0x67, 0xd4, 0xc2, 0x90, 0x8d, 0xa5, 0xc0, 0x00];
            byte[] output = new AESCryptoTransform(ZERO_IV, ZERO_IV, PaddingMode.None, CipherMode.CBC, false).UnsubBytes(testState);
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void MixColumnsTest() {
            // These test vectors are from https://en.wikipedia.org/wiki/Rijndael_MixColumns
            // They have not been vetted
            byte[] testState = Convert.FromHexString("49457f77db3902de8753d2963b89f11a");
            byte[] testOutput = Convert.FromHexString("581bdb1b4d4be76bca5acab0f1aca8e5");
            byte[] output = AESCryptoTransform.MixColumns(testState);
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void UnmixColumnsTest() {
            byte[] testState = Convert.FromHexString("581bdb1b4d4be76bca5acab0f1aca8e5");
            byte[] testOutput = Convert.FromHexString("49457f77db3902de8753d2963b89f11a");
            byte[] output = AESCryptoTransform.UnmixColumns(testState);
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void ShiftRowsTest() {
            byte[] testState = Convert.FromHexString("d4e0b81e27bfb44111985d52aef1e530");
            byte[] testOutput = Convert.FromHexString("d4e0b81ebfb441275d52119830aef1e5");
            byte[] output = AESCryptoTransform.ShiftRows(testState);
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void UnshiftRowsTest() {
            byte[] testState = Convert.FromHexString("d4e0b81ebfb441275d52119830aef1e5");
            byte[] testOutput = Convert.FromHexString("d4e0b81e27bfb44111985d52aef1e530");
            byte[] output = AESCryptoTransform.UnshiftRows(testState);
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void PadPKCS7Test() {
            byte[] testInput = [0x3a, 0x7f, 0xd1, 0x22, 0xb4, 0x9c, 0x05, 0x6e, 0x88, 0xc3, 0x1d];
            byte[] testOutput = [0x3a, 0x7f, 0xd1, 0x22, 0xb4, 0x9c, 0x05, 0x6e, 0x88, 0xc3, 0x1d, 0x05, 0x05, 0x05, 0x05, 0x05];
            Debug.Assert(testInput.Length < BLOCK_SIZE);
            byte[] output = AESCryptoTransform.PadPKCS7(testInput);
            Debug.Assert(output.Length == BLOCK_SIZE, $"incorrect pad length: {output.Length} expected: {BLOCK_SIZE}");
            int lengthDiff = BLOCK_SIZE - testInput.Length;
            Debug.Assert(output.Last() == lengthDiff, $"last element expected to be the padding length ({lengthDiff}), found {output[BLOCK_SIZE - 1]}");
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void PadANSIX923Test() {
            byte[] testInput = [0x3a, 0x7f, 0xd1, 0x22, 0xb4, 0x9c, 0x05, 0x6e, 0x88, 0xc3, 0x1d];
            byte[] testOutput = [0x3a, 0x7f, 0xd1, 0x22, 0xb4, 0x9c, 0x05, 0x6e, 0x88, 0xc3, 0x1d, 0x0, 0x0, 0x0, 0x0, 0x05];
            Debug.Assert(testInput.Length < BLOCK_SIZE);
            byte[] output = AESCryptoTransform.PadANSIX923(testInput);
            Debug.Assert(output.Length == BLOCK_SIZE, $"incorrect pad length: {output.Length} expected: {BLOCK_SIZE}");
            int lengthDiff = BLOCK_SIZE - testInput.Length;
            Debug.Assert(output.Last() == lengthDiff, $"last element expected to be the padding length ({lengthDiff}), found {output[BLOCK_SIZE - 1]}");
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void PadISO10126Test() {
            byte[] testInput = [0x3a, 0x7f, 0xd1, 0x22, 0xb4, 0x9c, 0x05, 0x6e, 0x88, 0xc3, 0x1d];
            Debug.Assert(testInput.Length < BLOCK_SIZE);
            byte[] output = AESCryptoTransform.PadISO10126(testInput);
            Debug.Assert(output.Length == BLOCK_SIZE, $"incorrect pad length: {output.Length} expected: {BLOCK_SIZE}");
            int lengthDiff = BLOCK_SIZE - testInput.Length;
            Debug.Assert(output.Last() == lengthDiff, $"last element expected to be the padding length ({lengthDiff}), found {output[BLOCK_SIZE - 1]}");
        }

        [Test]
        public void UnpadTest() {
            byte[] testInput = [0x3a, 0x7f, 0xd1, 0x22, 0xb4, 0x9c, 0x05, 0x6e, 0x88, 0xc3, 0x1d, 0x0, 0x0, 0x0, 0x0, 0x05];
            byte[] testOutput = [0x3a, 0x7f, 0xd1, 0x22, 0xb4, 0x9c, 0x05, 0x6e, 0x88, 0xc3, 0x1d];
            byte[] output = new AESCryptoTransform(ZERO_IV, ZERO_IV, PaddingMode.ANSIX923, CipherMode.ECB, true).Unpad(testInput);
            Debug.Assert(output.Length < BLOCK_SIZE);
            Debug.Assert(output.Length == testOutput.Length, $"remove pad failed: new length = {output.Length} expected: {testOutput.Length}");
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void CipherExampleTest() {
            byte[] testKey = Convert.FromHexString("2b7e151628aed2a6abf7158809cf4f3c");
            byte[] testInput = Convert.FromHexString("3243f6a8885a308d313198a2e0370734");
            byte[] testOutput = Convert.FromHexString("3902dc1925dc116a8409850b1dfb9732");

            byte[] output = new byte[testInput.Length];

            new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, true).AESEncryptBlock(testInput, 0, output, 0);
            AESCryptoTransform.TransposeMatrix(output);
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void CipherExampleTest_Decrypt() {
            byte[] testKey = Convert.FromHexString("2b7e151628aed2a6abf7158809cf4f3c");
            byte[] testInput = Convert.FromHexString("3902dc1925dc116a8409850b1dfb9732");
            byte[] testOutput = Convert.FromHexString("3243f6a8885a308d313198a2e0370734");

            byte[] output = new byte[testInput.Length];

            AESCryptoTransform.TransposeMatrix(testInput);
            new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, false).AESDecryptBlock(testInput, 0, output, 0);
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void DecryptionBufferingTest_IsBlockSizeMultiple() {
            byte[] testKey = Convert.FromHexString("2b7e151628aed2a6abf7158809cf4f3c");
            byte[] testInput = Convert.FromHexString("119EFAFD4F5D4F8C23B49A6BF27E4D59A254BE88E037DDD9D79FB6411C3F9DF8");
            byte[] testOutput = Encoding.UTF8.GetBytes("Miluju te, Lucko"); // it is important that the message is BLOCK_SIZE long for the test
            byte[] output = new byte[BLOCK_SIZE];
            AESCryptoTransform transform = new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.PKCS7, CipherMode.ECB, false);
            // we passed in one block, so the array should be empty as the block should get buffered
            int bytesWritten = transform.TransformBlock(testInput, 0, BLOCK_SIZE, output, 0);
            Debug.Assert(bytesWritten == 0, $"bytes written is supposed to be 0 but is {bytesWritten}");
            Assert.That(output, Is.EqualTo(new byte[output.Length]).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected array of zeros");
            // now we pass in another block which gets buffered, but we should receive the previous block
            bytesWritten += transform.TransformBlock(testInput, BLOCK_SIZE, BLOCK_SIZE, output, bytesWritten);
            Debug.Assert(bytesWritten == BLOCK_SIZE, $"bytes written is supposed to be {BLOCK_SIZE} but is {bytesWritten}");
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
            byte[] finalOutput = transform.TransformFinalBlock(testInput, bytesWritten, testInput.Length - bytesWritten - BLOCK_SIZE);
            // we expect empty array, because the whole of the buffered block is actually padding, so it gets scrapped
            Assert.That(finalOutput, Is.EqualTo(Array.Empty<byte>()).AsCollection, $"incorrect output: [{string.Join(',', finalOutput)}] expected empty array");
        }

        [Test]
        public void DecryptionBufferingTest_IsNotBlockSizeMultiple() {
            byte[] testKey = Convert.FromHexString("2b7e151628aed2a6abf7158809cf4f3c");
            byte[] testInput = Convert.FromHexString("119EFAFD4F5D4F8C23B49A6BF27E4D59507310064AAFCAB3760FD4A5A455EE46");
            byte[] testOutput = Encoding.UTF8.GetBytes("Miluju te, Lucko!"); // it is important that the message is not BLOCK_SIZE long for the test
            byte[] output = new byte[testOutput.Length];
            AESCryptoTransform transform = new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.PKCS7, CipherMode.ECB, false);
            // we passed in one block, so the array should be empty as the block should get buffered
            int bytesWritten = transform.TransformBlock(testInput, 0, BLOCK_SIZE, output, 0);
            Debug.Assert(bytesWritten == 0, $"bytes written is supposed to be 0 but is {bytesWritten}");
            Assert.That(output, Is.EqualTo(new byte[output.Length]).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected array of zeros");
            // now we pass in another block which gets buffered, but we should receive the previous block
            bytesWritten += transform.TransformBlock(testInput, BLOCK_SIZE, BLOCK_SIZE, output, bytesWritten);
            Debug.Assert(bytesWritten == BLOCK_SIZE, $"bytes written is supposed to be {BLOCK_SIZE} but is {bytesWritten}");
            byte[] finalOutput = transform.TransformFinalBlock(testInput, bytesWritten, testInput.Length - bytesWritten - BLOCK_SIZE);
            Array.Copy(finalOutput, 0, output, bytesWritten, finalOutput.Length);
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        [Test]
        public void DecryptionBufferingTest_TransformFinalBlockOnly() {
            byte[] testKey = Convert.FromHexString("2b7e151628aed2a6abf7158809cf4f3c");
            byte[] testInput = Convert.FromHexString("119EFAFD4F5D4F8C23B49A6BF27E4D59507310064AAFCAB3760FD4A5A455EE46");
            byte[] testOutput = Encoding.UTF8.GetBytes("Miluju te, Lucko!");
            AESCryptoTransform transform = new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.PKCS7, CipherMode.ECB, false);
            byte[] output = transform.TransformFinalBlock(testInput, 0, testInput.Length);
            Assert.That(output, Is.EqualTo(testOutput).AsCollection, $"incorrect output: [{string.Join(',', output)}] expected: [{string.Join(',', testOutput)}]");
        }

        /* FOLLOWING TESTS ARE THE OFFICIAL AES TEST VECTORS */

        [Test]
        public void ECBTest_128bits() {
            byte[] testKey = Convert.FromHexString("2B7E151628AED2A6ABF7158809CF4F3C");
            byte[] plainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] testCipherText = Convert.FromHexString("3AD77BB40D7A3660A89ECAF32466EF97F5D3D58503B9699DE785895A96FDBAAF43B1CD7F598ECE23881B00E3ED0306887B0C785E27E8AD3F8223207104725DD4");
            byte[] cipherText = new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, true).TransformFinalBlock(plainText, 0, plainText.Length);
            Assert.That(cipherText, Is.EqualTo(testCipherText).AsCollection, $"incorrect output: [{string.Join(',', cipherText)}] expected: [{string.Join(',', testCipherText)}]");
        }

        [Test]
        public void ECBTest_192bits() {
            byte[] testKey = Convert.FromHexString("8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B");
            byte[] plainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] testCipherText = Convert.FromHexString("BD334F1D6E45F25FF712A214571FA5CC974104846D0AD3AD7734ECB3ECEE4EEFEF7AFD2270E2E60ADCE0BA2FACE6444E9A4B41BA738D6C72FB16691603C18E0E");
            byte[] cipherText = new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, true).TransformFinalBlock(plainText, 0, plainText.Length);
            Assert.That(cipherText, Is.EqualTo(testCipherText).AsCollection, $"incorrect output: [{string.Join(',', cipherText)}] expected: [{string.Join(',', testCipherText)}]");
        }

        [Test]
        public void ECBTest_256bits() {
            byte[] testKey = Convert.FromHexString("603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4");
            byte[] plainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] testCipherText = Convert.FromHexString("F3EED1BDB5D2A03C064B5A7E3DB181F8591CCB10D410ED26DC5BA74A31362870B6ED21B99CA6F4F9F153E7B1BEAFED1D23304B7A39F9F3FF067D8D8F9E24ECC7");
            byte[] cipherText = new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, true).TransformFinalBlock(plainText, 0, plainText.Length);
            Assert.That(cipherText, Is.EqualTo(testCipherText).AsCollection, $"incorrect output: [{string.Join(',', cipherText)}] expected: [{string.Join(',', testCipherText)}]");
        }

        [Test]
        public void ECBTest_128bits_Decrypt() {
            byte[] testKey = Convert.FromHexString("2B7E151628AED2A6ABF7158809CF4F3C");
            byte[] cipherText = Convert.FromHexString("3AD77BB40D7A3660A89ECAF32466EF97F5D3D58503B9699DE785895A96FDBAAF43B1CD7F598ECE23881B00E3ED0306887B0C785E27E8AD3F8223207104725DD4");
            byte[] testPlainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] plainText = new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, false).TransformFinalBlock(cipherText, 0, cipherText.Length);
            Assert.That(plainText, Is.EqualTo(testPlainText).AsCollection, $"incorrect output: [{string.Join(',', plainText)}] expected: [{string.Join(',', testPlainText)}]");
        }

        [Test]
        public void ECBTest_192bits_Decrypt() {
            byte[] testKey = Convert.FromHexString("8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B");
            byte[] cipherText = Convert.FromHexString("BD334F1D6E45F25FF712A214571FA5CC974104846D0AD3AD7734ECB3ECEE4EEFEF7AFD2270E2E60ADCE0BA2FACE6444E9A4B41BA738D6C72FB16691603C18E0E");
            byte[] testPlainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] plainText = new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, false).TransformFinalBlock(cipherText, 0, cipherText.Length);
            Assert.That(plainText, Is.EqualTo(testPlainText).AsCollection, $"incorrect output: [{string.Join(',', plainText)}] expected: [{string.Join(',', testPlainText)}]");
        }

        [Test]
        public void ECBTest_256bits_Decrypt() {
            byte[] testKey = Convert.FromHexString("603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4");
            byte[] cipherText = Convert.FromHexString("F3EED1BDB5D2A03C064B5A7E3DB181F8591CCB10D410ED26DC5BA74A31362870B6ED21B99CA6F4F9F153E7B1BEAFED1D23304B7A39F9F3FF067D8D8F9E24ECC7");
            byte[] testPlainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] plainText = new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, false).TransformFinalBlock(cipherText, 0, cipherText.Length);
            Assert.That(plainText, Is.EqualTo(testPlainText).AsCollection, $"incorrect output: [{string.Join(',', plainText)}] expected: [{string.Join(',', testPlainText)}]");
        }


        [Test]
        public void CBCTest_128bits() {
            byte[] testIV = Convert.FromHexString("000102030405060708090A0B0C0D0E0F");
            byte[] testKey = Convert.FromHexString("2B7E151628AED2A6ABF7158809CF4F3C");
            byte[] plainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] testCipherText = Convert.FromHexString("7649ABAC8119B246CEE98E9B12E9197D5086CB9B507219EE95DB113A917678B273BED6B8E3C1743B7116E69E222295163FF1CAA1681FAC09120ECA307586E1A7");
            byte[] cipherText = new AESCryptoTransform(testKey, testIV, PaddingMode.None, CipherMode.CBC, true).TransformFinalBlock(plainText, 0, plainText.Length);
            Assert.That(cipherText, Is.EqualTo(testCipherText).AsCollection, $"incorrect output: [{string.Join(',', cipherText)}] expected: [{string.Join(',', testCipherText)}]");
        }

        [Test]
        public void CBCTest_192bits() {
            byte[] testIV = Convert.FromHexString("000102030405060708090A0B0C0D0E0F");
            byte[] testKey = Convert.FromHexString("8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B");
            byte[] plainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] testCipherText = Convert.FromHexString("4F021DB243BC633D7178183A9FA071E8B4D9ADA9AD7DEDF4E5E738763F69145A571B242012FB7AE07FA9BAAC3DF102E008B0E27988598881D920A9E64F5615CD");
            byte[] cipherText = new AESCryptoTransform(testKey, testIV, PaddingMode.None, CipherMode.CBC, true).TransformFinalBlock(plainText, 0, plainText.Length);
            Assert.That(cipherText, Is.EqualTo(testCipherText).AsCollection, $"incorrect output: [{string.Join(',', cipherText)}] expected: [{string.Join(',', testCipherText)}]");
        }

        [Test]
        public void CBCTest_256bits() {
            byte[] testIV = Convert.FromHexString("000102030405060708090A0B0C0D0E0F");
            byte[] testKey = Convert.FromHexString("603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4");
            byte[] plainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] testCipherText = Convert.FromHexString("F58C4C04D6E5F1BA779EABFB5F7BFBD69CFC4E967EDB808D679F777BC6702C7D39F23369A9D9BACFA530E26304231461B2EB05E2C39BE9FCDA6C19078C6A9D1B");
            byte[] cipherText = new AESCryptoTransform(testKey, testIV, PaddingMode.None, CipherMode.CBC, true).TransformFinalBlock(plainText, 0, plainText.Length);
            Assert.That(cipherText, Is.EqualTo(testCipherText).AsCollection, $"incorrect output: [{string.Join(',', cipherText)}] expected: [{string.Join(',', testCipherText)}]");
        }

        [Test]
        public void CBCTest_128bits_Decrypt() {
            byte[] testIV = Convert.FromHexString("000102030405060708090A0B0C0D0E0F");
            byte[] testKey = Convert.FromHexString("2B7E151628AED2A6ABF7158809CF4F3C");
            byte[] cipherText = Convert.FromHexString("7649ABAC8119B246CEE98E9B12E9197D5086CB9B507219EE95DB113A917678B273BED6B8E3C1743B7116E69E222295163FF1CAA1681FAC09120ECA307586E1A7");
            byte[] testPlainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] plainText = new AESCryptoTransform(testKey, testIV, PaddingMode.None, CipherMode.CBC, false).TransformFinalBlock(cipherText, 0, cipherText.Length);
            Assert.That(plainText, Is.EqualTo(testPlainText).AsCollection, $"incorrect output: [{string.Join(',', plainText)}] expected: [{string.Join(',', testPlainText)}]");
        }

        [Test]
        public void CBCTest_192bits_Decrypt() {
            byte[] testIV = Convert.FromHexString("000102030405060708090A0B0C0D0E0F");
            byte[] testKey = Convert.FromHexString("8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B");
            byte[] cipherText = Convert.FromHexString("4F021DB243BC633D7178183A9FA071E8B4D9ADA9AD7DEDF4E5E738763F69145A571B242012FB7AE07FA9BAAC3DF102E008B0E27988598881D920A9E64F5615CD");
            byte[] testPlainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] plainText = new AESCryptoTransform(testKey, testIV, PaddingMode.None, CipherMode.CBC, false).TransformFinalBlock(cipherText, 0, cipherText.Length);
            Assert.That(plainText, Is.EqualTo(testPlainText).AsCollection, $"incorrect output: [{string.Join(',', plainText)}] expected: [{string.Join(',', testPlainText)}]");
        }

        [Test]
        public void CBCTest_256bits_Decrypt() {
            byte[] testIV = Convert.FromHexString("000102030405060708090A0B0C0D0E0F");
            byte[] testKey = Convert.FromHexString("603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4");
            byte[] cipherText = Convert.FromHexString("F58C4C04D6E5F1BA779EABFB5F7BFBD69CFC4E967EDB808D679F777BC6702C7D39F23369A9D9BACFA530E26304231461B2EB05E2C39BE9FCDA6C19078C6A9D1B");
            byte[] testPlainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] plainTest = new AESCryptoTransform(testKey, testIV, PaddingMode.None, CipherMode.CBC, false).TransformFinalBlock(cipherText, 0, cipherText.Length);
            Assert.That(plainTest, Is.EqualTo(testPlainText).AsCollection, $"incorrect output: [{string.Join(',', plainTest)}] expected: [{string.Join(',', testPlainText)}]");
        }

        [Test]
        public void ECBTest_128bits_TransformBlock() {
            byte[] testKey = Convert.FromHexString("2B7E151628AED2A6ABF7158809CF4F3C");
            byte[] plainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] testCipherText = Convert.FromHexString("3AD77BB40D7A3660A89ECAF32466EF97F5D3D58503B9699DE785895A96FDBAAF43B1CD7F598ECE23881B00E3ED0306887B0C785E27E8AD3F8223207104725DD4");
            byte[] cipherText = new byte[testCipherText.Length];
            new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, true).TransformBlock(plainText, 0, plainText.Length, cipherText, 0);
            Assert.That(cipherText, Is.EqualTo(testCipherText).AsCollection, $"incorrect output: [{string.Join(',', cipherText)}] expected: [{string.Join(',', testCipherText)}]");
        }

        [Test]
        public void ECBTest_192bits_TransformBlock() {
            byte[] testKey = Convert.FromHexString("8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B");
            byte[] plainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] testCipherText = Convert.FromHexString("BD334F1D6E45F25FF712A214571FA5CC974104846D0AD3AD7734ECB3ECEE4EEFEF7AFD2270E2E60ADCE0BA2FACE6444E9A4B41BA738D6C72FB16691603C18E0E");
            byte[] cipherText = new byte[testCipherText.Length];
            new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, true).TransformBlock(plainText, 0, plainText.Length, cipherText, 0);
            Assert.That(cipherText, Is.EqualTo(testCipherText).AsCollection, $"incorrect output: [{string.Join(',', cipherText)}] expected: [{string.Join(',', testCipherText)}]");
        }

        [Test]
        public void ECBTest_256bits_TransformBlock() {
            byte[] testKey = Convert.FromHexString("603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4");
            byte[] plainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] testCipherText = Convert.FromHexString("F3EED1BDB5D2A03C064B5A7E3DB181F8591CCB10D410ED26DC5BA74A31362870B6ED21B99CA6F4F9F153E7B1BEAFED1D23304B7A39F9F3FF067D8D8F9E24ECC7");
            byte[] cipherText = new byte[testCipherText.Length];
            new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, true).TransformBlock(plainText, 0, plainText.Length, cipherText, 0);
            Assert.That(cipherText, Is.EqualTo(testCipherText).AsCollection, $"incorrect output: [{string.Join(',', cipherText)}] expected: [{string.Join(',', testCipherText)}]");
        }

        [Test]
        public void ECBTest_128bits_Decrypt_TransformBlock() {
            byte[] testKey = Convert.FromHexString("2B7E151628AED2A6ABF7158809CF4F3C");
            byte[] cipherText = Convert.FromHexString("3AD77BB40D7A3660A89ECAF32466EF97F5D3D58503B9699DE785895A96FDBAAF43B1CD7F598ECE23881B00E3ED0306887B0C785E27E8AD3F8223207104725DD4");
            byte[] testPlainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] plainText = new byte[testPlainText.Length];
            new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, false).TransformBlock(cipherText, 0, cipherText.Length, plainText, 0);
            Assert.That(plainText, Is.EqualTo(testPlainText).AsCollection, $"incorrect output: [{string.Join(',', plainText)}] expected: [{string.Join(',', testPlainText)}]");
        }

        [Test]
        public void ECBTest_192bits_Decrypt_TransformBlock() {
            byte[] testKey = Convert.FromHexString("8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B");
            byte[] cipherText = Convert.FromHexString("BD334F1D6E45F25FF712A214571FA5CC974104846D0AD3AD7734ECB3ECEE4EEFEF7AFD2270E2E60ADCE0BA2FACE6444E9A4B41BA738D6C72FB16691603C18E0E");
            byte[] testPlainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] plainText = new byte[testPlainText.Length];
            new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, false).TransformBlock(cipherText, 0, cipherText.Length, plainText, 0);
            Assert.That(plainText, Is.EqualTo(testPlainText).AsCollection, $"incorrect output: [{string.Join(',', plainText)}] expected: [{string.Join(',', testPlainText)}]");
        }

        [Test]
        public void ECBTest_256bits_Decrypt_TransformBlock() {
            byte[] testKey = Convert.FromHexString("603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4");
            byte[] cipherText = Convert.FromHexString("F3EED1BDB5D2A03C064B5A7E3DB181F8591CCB10D410ED26DC5BA74A31362870B6ED21B99CA6F4F9F153E7B1BEAFED1D23304B7A39F9F3FF067D8D8F9E24ECC7");
            byte[] testPlainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] plainText = new byte[testPlainText.Length];
            new AESCryptoTransform(testKey, ZERO_IV, PaddingMode.None, CipherMode.ECB, false).TransformBlock(cipherText, 0, cipherText.Length, plainText, 0);
            Assert.That(plainText, Is.EqualTo(testPlainText).AsCollection, $"incorrect output: [{string.Join(',', plainText)}] expected: [{string.Join(',', testPlainText)}]");
        }


        [Test]
        public void CBCTest_128bits_TransformBlock() {
            byte[] testIV = Convert.FromHexString("000102030405060708090A0B0C0D0E0F");
            byte[] testKey = Convert.FromHexString("2B7E151628AED2A6ABF7158809CF4F3C");
            byte[] plainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] testCipherText = Convert.FromHexString("7649ABAC8119B246CEE98E9B12E9197D5086CB9B507219EE95DB113A917678B273BED6B8E3C1743B7116E69E222295163FF1CAA1681FAC09120ECA307586E1A7");
            byte[] cipherText = new byte[testCipherText.Length];
            new AESCryptoTransform(testKey, testIV, PaddingMode.None, CipherMode.CBC, true).TransformBlock(plainText, 0, plainText.Length, cipherText, 0);
            Assert.That(cipherText, Is.EqualTo(testCipherText).AsCollection, $"incorrect output: [{string.Join(',', cipherText)}] expected: [{string.Join(',', testCipherText)}]");
        }

        [Test]
        public void CBCTest_192bits_TransformBlock() {
            byte[] testIV = Convert.FromHexString("000102030405060708090A0B0C0D0E0F");
            byte[] testKey = Convert.FromHexString("8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B");
            byte[] plainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] testCipherText = Convert.FromHexString("4F021DB243BC633D7178183A9FA071E8B4D9ADA9AD7DEDF4E5E738763F69145A571B242012FB7AE07FA9BAAC3DF102E008B0E27988598881D920A9E64F5615CD");
            byte[] cipherText = new byte[testCipherText.Length];
            new AESCryptoTransform(testKey, testIV, PaddingMode.None, CipherMode.CBC, true).TransformBlock(plainText, 0, plainText.Length, cipherText, 0);
            Assert.That(cipherText, Is.EqualTo(testCipherText).AsCollection, $"incorrect output: [{string.Join(',', cipherText)}] expected: [{string.Join(',', testCipherText)}]");
        }

        [Test]
        public void CBCTest_256bits_TransformBlock() {
            byte[] testIV = Convert.FromHexString("000102030405060708090A0B0C0D0E0F");
            byte[] testKey = Convert.FromHexString("603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4");
            byte[] plainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] testCipherText = Convert.FromHexString("F58C4C04D6E5F1BA779EABFB5F7BFBD69CFC4E967EDB808D679F777BC6702C7D39F23369A9D9BACFA530E26304231461B2EB05E2C39BE9FCDA6C19078C6A9D1B");
            byte[] cipherText = new byte[testCipherText.Length];
            new AESCryptoTransform(testKey, testIV, PaddingMode.None, CipherMode.CBC, true).TransformBlock(plainText, 0, plainText.Length, cipherText, 0);
            Assert.That(cipherText, Is.EqualTo(testCipherText).AsCollection, $"incorrect output: [{string.Join(',', cipherText)}] expected: [{string.Join(',', testCipherText)}]");
        }

        [Test]
        public void CBCTest_128bits_Decrypt_TransformBlock() {
            byte[] testIV = Convert.FromHexString("000102030405060708090A0B0C0D0E0F");
            byte[] testKey = Convert.FromHexString("2B7E151628AED2A6ABF7158809CF4F3C");
            byte[] cipherText = Convert.FromHexString("7649ABAC8119B246CEE98E9B12E9197D5086CB9B507219EE95DB113A917678B273BED6B8E3C1743B7116E69E222295163FF1CAA1681FAC09120ECA307586E1A7");
            byte[] testPlainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] plainText = new byte[testPlainText.Length];
            new AESCryptoTransform(testKey, testIV, PaddingMode.None, CipherMode.CBC, false).TransformBlock(cipherText, 0, cipherText.Length, plainText, 0);
            Assert.That(plainText, Is.EqualTo(testPlainText).AsCollection, $"incorrect output: [{string.Join(',', plainText)}] expected: [{string.Join(',', testPlainText)}]");
        }

        [Test]
        public void CBCTest_192bits_Decrypt_TransformBlock() {
            byte[] testIV = Convert.FromHexString("000102030405060708090A0B0C0D0E0F");
            byte[] testKey = Convert.FromHexString("8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B");
            byte[] cipherText = Convert.FromHexString("4F021DB243BC633D7178183A9FA071E8B4D9ADA9AD7DEDF4E5E738763F69145A571B242012FB7AE07FA9BAAC3DF102E008B0E27988598881D920A9E64F5615CD");
            byte[] testPlainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] plainText = new byte[testPlainText.Length];
            new AESCryptoTransform(testKey, testIV, PaddingMode.None, CipherMode.CBC, false).TransformBlock(cipherText, 0, cipherText.Length, plainText, 0); Assert.That(plainText, Is.EqualTo(testPlainText).AsCollection, $"incorrect output: [{string.Join(',', plainText)}] expected: [{string.Join(',', testPlainText)}]");
        }

        [Test]
        public void CBCTest_256bits_Decrypt_TransformBlock() {
            byte[] testIV = Convert.FromHexString("000102030405060708090A0B0C0D0E0F");
            byte[] testKey = Convert.FromHexString("603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4");
            byte[] cipherText = Convert.FromHexString("F58C4C04D6E5F1BA779EABFB5F7BFBD69CFC4E967EDB808D679F777BC6702C7D39F23369A9D9BACFA530E26304231461B2EB05E2C39BE9FCDA6C19078C6A9D1B");
            byte[] testPlainText = Convert.FromHexString("6BC1BEE22E409F96E93D7E117393172AAE2D8A571E03AC9C9EB76FAC45AF8E5130C81C46A35CE411E5FBC1191A0A52EFF69F2445DF4F9B17AD2B417BE66C3710");
            byte[] plainText = new byte[testPlainText.Length];
            new AESCryptoTransform(testKey, testIV, PaddingMode.None, CipherMode.CBC, false).TransformBlock(cipherText, 0, cipherText.Length, plainText, 0);
            Assert.That(plainText, Is.EqualTo(testPlainText).AsCollection, $"incorrect output: [{string.Join(',', plainText)}] expected: [{string.Join(',', testPlainText)}]");
        }

    }
}