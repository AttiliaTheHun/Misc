using System.Security.Cryptography;
using System;
using System.Linq;
using System.Diagnostics;
using System.IO;

namespace Program.AESLib;
/// <summary>
/// The ICryptoTransform implementation for AES. This class provides all the cryptographic functionality of the library.
/// </summary>
// add cipher modes: OFB, CFB, GCM?, AEAD?
class AESCryptoTransform : ICryptoTransform {
    private static readonly byte[] ROUND_CONSTANTS = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36];
    private static readonly int BLOCK_SIZE = 16; // in bytes
    private static readonly int WORD_SIZE = 4; // in bytes
    public bool CanReuseTransform => true;
    public bool CanTransformMultipleBlocks => true;
    public int InputBlockSize => 64;
    public int OutputBlockSize => 64;
    readonly PaddingMode paddingMode;
    readonly CipherMode cipherMode;
    private readonly byte[] key;
    private readonly byte[] iv;
    private readonly bool encrypting;
    private readonly byte[] sbox;
    internal readonly byte[] inverseSbox;
    internal readonly byte[] expandedKey;
    private readonly int rounds;
    private readonly bool bufferLastBlock;
    private bool isLastBlockBuffered = false;
    private byte[] lastBlockBuffer;

    /// <summary>
    /// The defualt constructor.
    /// </summary>
    /// <param name="key">the encryption key</param>
    /// <param name="iv">the initialisation vector</param>
    /// <param name="paddingMode">the padding mode</param>
    /// <param name="cipherMode">the cipher mode</param>
    /// <param name="encrypting">whether the action mode is to encrypt (false to decrypt)</param>
    /// <exception cref="ArgumentException">if the key or the iv are null</exception>
    public AESCryptoTransform(byte[] key, byte[] iv, PaddingMode paddingMode, CipherMode cipherMode, bool encrypting) {
        ArgumentNullException.ThrowIfNull(key);
        ArgumentNullException.ThrowIfNull(iv);
        if (iv.Length != BLOCK_SIZE) {
            throw new ArgumentException("iv must be of the same length as the block size");
        }
        this.key = key;
        this.iv = iv;
        this.paddingMode = paddingMode;
        this.cipherMode = cipherMode;
        this.encrypting = encrypting;
        sbox = GenerateSBox();
        if (!encrypting) inverseSbox = GenerateInverseSBox(sbox);
        rounds = GetRounds(key);
        expandedKey = ExpandKey(key);
        bufferLastBlock = paddingMode != PaddingMode.None;
        if (bufferLastBlock) lastBlockBuffer = new byte[BLOCK_SIZE];
    }

    public int TransformBlock(byte[] inputBuffer, byte[] outputBuffer) {
        return TransformBlock(inputBuffer, 0, inputBuffer.Length, outputBuffer, 0);
    }

    /// <summary>
    /// Transforms a series of blocks. The input must consist of complete blocks. The output may be suject to buffering.
    /// </summary>
    /// <param name="inputBuffer">the input buffer</param>
    /// <param name="inputOffset">starting position in the inputtext buffer</param>
    /// <param name="inputCount">the number of bytes to transform</param>
    /// <param name="outputBuffer">the output buffer</param>
    /// <param name="outputOffset">starting position in the output buffer</param>
    /// <returns>the number of bytes written to outputBuffer</returns>
    /// <exception cref="InvalidOperationException">when inputCount is not a multiple of the block size</exception>
    public int TransformBlock(byte[] inputBuffer, int inputOffset, int inputCount, byte[] outputBuffer, int outputOffset) {
        if (inputCount % BLOCK_SIZE != 0) {
            throw new InvalidOperationException("input length is not a multiple of the block size, use TransformFinalBlock() instead!");
        }
        if (encrypting) {
            return EncryptBlock(inputBuffer, inputOffset, inputCount, outputBuffer, outputOffset);
        }
        return DecryptBlock(inputBuffer, inputOffset, inputCount, outputBuffer, outputOffset);
    }

    /// <summary>
    /// Transforms a byte array, potentially returning any buffered data and releasing all underlying resources. The output may potentially be longer than the input. 
    /// Call this method when you are done with the cryptograhpic operation. The transform object will no longer function properly after calling this method.
    /// </summary>
    /// <param name="inputBuffer">the input buffer</param>
    /// <param name="inputOffset"><starting position in the input buffer/param>
    /// <param name="inputCount">the number of bytes to transform</param>
    /// <returns>the transformed bytes</returns>
    public byte[] TransformFinalBlock(byte[] inputBuffer, int inputOffset, int inputCount) {
        if (encrypting) {
            return EncryptFinalBlock(inputBuffer, inputOffset, inputCount);
        }
        return DecryptFinalBlockBuffered(inputBuffer, inputOffset, inputCount);
    }

    /// <summary>
    /// Encrypts an array of bytes block-by-block.
    /// </summary>
    /// <param name="inputBuffer">the clear text buffer</param>
    /// <param name="inputOffset">starting position in the clear text buffer</param>
    /// <param name="inputCount">the number of bytes to encrypt</param>
    /// <param name="outputBuffer">the cipher text buffer</param>
    /// <param name="outputOffset">starting position in the cipher text buffer</param>
    /// <returns>the number of bytes written to outputBuffer</returns>
    private int EncryptBlock(byte[] inputBuffer, int inputOffset, int inputCount, byte[] outputBuffer, int outputOffset) {
        int blockCount = inputCount / BLOCK_SIZE;
        int bytesWritten = 0;
        for (int blockNumber = 0; blockNumber < blockCount; blockNumber++) {
            bytesWritten += Encrypt(inputBuffer, inputOffset, outputBuffer, outputOffset + blockNumber * BLOCK_SIZE);
            inputOffset += BLOCK_SIZE;
        }
        return bytesWritten;
    }

    /// <summary>
    /// Decrypts an array of bytes block-by-block while buffering the last block.
    /// </summary>
    /// <param name="inputBuffer">the cipher text buffer</param>
    /// <param name="inputOffset">starting position in the cipher text buffer</param>
    /// <param name="inputCount">the number of bytes to decrypt</param>
    /// <param name="outputBuffer">the clear text buffer</param>
    /// <param name="outputOffset">starting position in the cleartext buffer</param>
    /// <returns>the number of bytes written to outputBuffer</returns>
    private int DecryptBlock(byte[] inputBuffer, int inputOffset, int inputCount, byte[] outputBuffer, int outputOffset) {
        int blockCount = inputCount / BLOCK_SIZE;
        if (bufferLastBlock) blockCount--;
        int bytesWritten = 0;
        if (bufferLastBlock && isLastBlockBuffered) {
            bytesWritten += Decrypt(lastBlockBuffer, 0, BLOCK_SIZE, outputBuffer, outputOffset);
            outputOffset += BLOCK_SIZE;
        }
        for (int blockNumber = 0; blockNumber < blockCount; blockNumber++) {
            bytesWritten += Decrypt(inputBuffer, inputOffset, BLOCK_SIZE, outputBuffer, outputOffset + blockNumber * BLOCK_SIZE);
            inputOffset += BLOCK_SIZE;
        }
        if (bufferLastBlock) {
            Array.Copy(inputBuffer, inputOffset, lastBlockBuffer, 0, BLOCK_SIZE);
            isLastBlockBuffered = true;
        }
        return bytesWritten;
    }

    /// <summary>
    /// Encrypts an array of bytes block-by-block and applies any necessary padding.
    /// </summary>
    /// <param name="inputBuffer">the clear text buffer</param>
    /// <param name="inputOffset">starting position in the clear text buffer</param>
    /// <param name="inputCount">the number of bytes to encrypt</param>
    /// <returns>the encrypted bytes</returns>
    private byte[] EncryptFinalBlock(byte[] inputBuffer, int inputOffset, int inputCount) {
        int blockCount = (int) Math.Ceiling((double) inputCount / BLOCK_SIZE);
        // if the cleartext length is a multiple of the block size, there would be no way to tell whether the message is padded or not,
        // thus we need to add a whole block of padding at the end
        bool needExtraPaddingBlock = (paddingMode != PaddingMode.None) && (inputCount % BLOCK_SIZE == 0);
        if (needExtraPaddingBlock) blockCount++;
        byte[] outputBuffer = new byte[blockCount * BLOCK_SIZE];
        // the last block may need to be padded, we will handle it later
        for (int blockNumber = 0; blockNumber < blockCount - 1; blockNumber++) {
            Encrypt(inputBuffer, inputOffset, outputBuffer, blockNumber * BLOCK_SIZE);
            inputOffset += BLOCK_SIZE;
        }

        byte[] padded;
        if (needExtraPaddingBlock) {
            padded = Pad([]);
        } else {
            padded = new byte[inputCount - (blockCount - 1) * BLOCK_SIZE];
            Array.Copy(inputBuffer, inputOffset, padded, 0, padded.Length);
            padded = Pad(padded);
        }
        Encrypt(padded, 0, outputBuffer, (blockCount - 1) * BLOCK_SIZE);
        return outputBuffer;
    }

    /// <summary>
    /// Decrypts a series of cipher text blocks, flushes any internally buffered blocks and removes any padding.
    /// </summary>
    /// <param name="inputBuffer">the cipher text buffer</param>
    /// <param name="inputOffset">starting position in the cipher text buffer</param>
    /// <param name="inputCount">the number of bytes to decrypt</param>
    /// <returns>the decrypted bytes</returns>
    /// <exception cref="InvalidDataException">if the inputCount is not a multiple of block sizze</exception>
    private byte[] DecryptFinalBlockBuffered(byte[] inputBuffer, int inputOffset, int inputCount) {
        if (inputCount % BLOCK_SIZE != 0) {
            throw new InvalidDataException("the length of the cipher text is not a multiple of the block size");
        }
        byte[] outputBuffer = new byte[inputCount];
        int outputOffset = 0;

        if (bufferLastBlock) {
            // if the input to the function is zero length, it means we need not decrypt anything new, just finish up with the buffer
            if (inputCount == 0) {
                // this means the buffered block was the padded one
                if (isLastBlockBuffered) {
                    outputBuffer = new byte[BLOCK_SIZE];
                    Decrypt(lastBlockBuffer, 0, BLOCK_SIZE, outputBuffer, 0);
                    return Unpad(outputBuffer);
                }
                return []; // I refuse to believe this is C# anymore, though it is convenient to write, it feels kinda JS
            }
            // on the other hand here the buffered block was not final, so we need to send it back and continue with the decryption
            if (isLastBlockBuffered) {
                outputBuffer = new byte[inputCount + BLOCK_SIZE];
                Decrypt(lastBlockBuffer, 0, BLOCK_SIZE, outputBuffer, 0);
                outputOffset += BLOCK_SIZE;
            }
        }
        // this result might be shorter than inputCount due to the padding being removed
        byte[] unpadded = DecryptFinalBlock(inputBuffer, inputOffset, inputCount);
        Array.Copy(unpadded, 0, outputBuffer, outputOffset, unpadded.Length);
        byte[] output = [.. outputBuffer.Take(outputOffset + unpadded.Length)];
        return output;
    }

    /// <summary>
    /// Decrypts a series of cipher text blocks and removes any padding.
    /// </summary>
    /// <param name="inputBuffer">the cipher text buffer</param>
    /// <param name="inputOffset">starting position in the cipher text buffer</param>
    /// <param name="inputCount">the number of bytes to decrypt</param>
    /// <returns>the decrypted bytes</returns>
    private byte[] DecryptFinalBlock(byte[] inputBuffer, int inputOffset, int inputCount) {
        int blockCount = inputCount / BLOCK_SIZE;
        byte[] outputBuffer = new byte[inputCount];
        int outputOffset = 0;
        // the last block may be padded, we will handle that later
        for (int blockNumber = 0; blockNumber < blockCount; blockNumber++) {
            Decrypt(inputBuffer, inputOffset, BLOCK_SIZE, outputBuffer, outputOffset);
            inputOffset += BLOCK_SIZE;
            outputOffset += BLOCK_SIZE;
        }
        return Unpad(outputBuffer);
    }

    /// <summary>
    /// Encrypts a block of plain text in accordance with the cipher mode.
    /// </summary>
    /// <param name="inputBuffer">the cipher text buffer</param>
    /// <param name="inputOffset">starting position in the cipher text buffer</param>
    /// <param name="outputBuffer">the clear text buffer</param>
    /// <param name="outputOffset">starting position in the cleartext buffer</param>
    /// <returns>the number of bytes written to outputBuffer</returns>
    private int Encrypt(byte[] inputBuffer, int inputOffset, byte[] outputBuffer, int outputOffset) {
        return cipherMode switch {
            CipherMode.CBC => EncryptBlockCBC(inputBuffer, inputOffset, outputBuffer, outputOffset),
            CipherMode.ECB => AESEncryptBlock(inputBuffer, inputOffset, outputBuffer, outputOffset),
            _ => -1,
        };
    }

    /// <summary>
    /// Encrypts a block of clear text in the CBC mode.
    /// </summary>
    /// <param name="inputBuffer">the cipher text buffer</param>
    /// <param name="inputOffset">starting position in the cipher text buffer</param>
    /// <param name="outputBuffer">the clear text buffer</param>
    /// <param name="outputOffset">starting position in the cleartext buffer</param>
    /// <returns>the number of bytes written to outputBuffer</returns>
    internal int EncryptBlockCBC(byte[] inputBuffer, int inputOffset, byte[] outputBuffer, int outputOffset) {
        byte[] inputBlock = new byte[BLOCK_SIZE];
        Array.Copy(inputBuffer, inputOffset, inputBlock, 0, BLOCK_SIZE);
        inputBlock = AddRoundKey(inputBlock, iv);
        int returnValue = AESEncryptBlock(inputBlock, 0, outputBuffer, outputOffset);
        Array.Copy(outputBuffer, outputOffset, iv, 0, BLOCK_SIZE);
        return returnValue;
    }

    /// <summary>
    /// Encrypts a single block of plain text using the Rijndael encrypt function.
    /// </summary>
    /// <param name="inputBuffer">the cipher text buffer</param>
    /// <param name="inputOffset">starting position in the cipher text buffer</param>
    /// <param name="outputBuffer">the clear text buffer</param>
    /// <param name="outputOffset">starting position in the cleartext buffer</param>
    /// <returns>the number of bytes written to outputBuffer</returns>
    internal int AESEncryptBlock(byte[] inputBuffer, int inputOffset, byte[] outputBuffer, int outputOffset) {
        byte[] state = new byte[BLOCK_SIZE];
        Array.Copy(inputBuffer, inputOffset, state, 0, BLOCK_SIZE);
        TransposeMatrix(state);
        state = AddRoundKey(state, GetRoundKey(0));
        for (int i = 1; i < rounds - 1; i++) {
            state = SubBytes(state);
            state = ShiftRows(state);
            state = MixColumns(state);
            state = AddRoundKey(state, GetRoundKey(i));
        }
        state = SubBytes(state);
        state = ShiftRows(state);
        state = AddRoundKey(state, GetRoundKey(rounds - 1));
        TransposeMatrix(state);
        Array.Copy(state, 0, outputBuffer, outputOffset, BLOCK_SIZE);
        return BLOCK_SIZE;
    }

    [Obsolete]
    internal static string ArrayToString(byte[] a) {
        return BitConverter.ToString(a).Replace("-", ", ");
    }

    /// <summary>
    /// Decrypts a block of cipher text in accordance with the cipher mode.
    /// </summary>
    /// <param name="inputBuffer">the cipher text buffer</param>
    /// <param name="inputOffset">starting position in the cipher text buffer</param>
    /// <param name="inputCount"></param>
    /// <param name="outputBuffer">the clear text buffer</param>
    /// <param name="outputOffset">starting position in the cleartext buffer</param>
    /// <returns>the number of bytes written to outputBuffer</returns>
    private int Decrypt(byte[] inputBuffer, int inputOffset, int inputCount, byte[] outputBuffer, int outputOffset) {
        return cipherMode switch {
            CipherMode.CBC => DecryptBlockCBC(inputBuffer, inputOffset, outputBuffer, outputOffset),
            CipherMode.ECB => AESDecryptBlock(inputBuffer, inputOffset, outputBuffer, outputOffset),
            _ => -1,
        };
    }
    /// <summary>
    /// Decrypts a block of cipher text in the CBC mode.
    /// </summary>
    /// <param name="inputBuffer">the cipher text buffer</param>
    /// <param name="inputOffset">starting position in the cipher text buffer</param>
    /// <param name="outputBuffer">the clear text buffer</param>
    /// <param name="outputOffset">starting position in the cleartext buffer</param>
    /// <returns>the number of bytes written to outputBuffer</returns>
    internal int DecryptBlockCBC(byte[] inputBuffer, int inputOffset, byte[] outputBuffer, int outputOffset) {
        byte[] inputBlock = new byte[BLOCK_SIZE];
        byte[] outputBlock = new byte[BLOCK_SIZE];
        Array.Copy(inputBuffer, inputOffset, inputBlock, 0, BLOCK_SIZE);
        int returnValue = AESDecryptBlock(inputBlock, 0, outputBlock, 0);
        outputBlock = AddRoundKey(outputBlock, iv);
        Array.Copy(outputBlock, 0, outputBuffer, outputOffset, BLOCK_SIZE);
        Array.Copy(inputBuffer, inputOffset, iv, 0, BLOCK_SIZE);
        return returnValue;
    }

    /// <summary>
    /// Decrypts a block of cipher text using the Rijndael decrypt function.
    /// </summary>
    /// <param name="inputBuffer">the cipher text buffer</param>
    /// <param name="inputOffset">starting position in the cipher text buffer</param>
    /// <param name="outputBuffer">the clear text buffer</param>
    /// <param name="outputOffset">starting position in the cleartext buffer</param>
    /// <returns>the number of bytes written to outputBuffer</returns>
    internal int AESDecryptBlock(byte[] inputBuffer, int inputOffset, byte[] outputBuffer, int outputOffset) {
        byte[] state = new byte[BLOCK_SIZE];
        Array.Copy(inputBuffer, inputOffset, state, 0, BLOCK_SIZE);
        TransposeMatrix(state);
        state = AddRoundKey(state, GetRoundKey(rounds - 1));
        state = UnshiftRows(state);
        state = UnsubBytes(state);
        for (int i = rounds - 2; i > 0; i--) {
            state = AddRoundKey(state, GetRoundKey(i));
            state = UnmixColumns(state);
            state = UnshiftRows(state);
            state = UnsubBytes(state);
        }
        state = AddRoundKey(state, GetRoundKey(0));
        TransposeMatrix(state);
        Array.Copy(state, 0, outputBuffer, outputOffset, BLOCK_SIZE);
        return BLOCK_SIZE;
    }

    /// <summary>
    /// Performs AES key expansion on the provided encryption key.
    /// </summary>
    /// <param name="key">the encryption key</param>
    /// <returns>the expanded key</returns>
    internal byte[] ExpandKey(byte[] key) {
        byte[] expandedKey = new byte[4 * 4 * rounds];
        int N = key.Length / WORD_SIZE;
        Array.Copy(key, 0, expandedKey, 0, key.Length);
        for (int i = N; i < expandedKey.Length / WORD_SIZE; i++) {
            if (i % N == 0) {
                byte[] newWord = XOR(XOR(GetWord(expandedKey, i - N), SubWord(RotWord(GetWord(expandedKey, i - 1)))), ToBigEndianFourByteArray(ROUND_CONSTANTS[(i / N) - 1]));
                Array.Copy(newWord, 0, expandedKey, i * WORD_SIZE, WORD_SIZE);
            } else if (N > 6 && i % N == 4) {
                byte[] newWord = XOR(GetWord(expandedKey, i - N), SubWord(GetWord(expandedKey, i - 1)));
                Array.Copy(newWord, 0, expandedKey, i * WORD_SIZE, WORD_SIZE);
            } else {
                byte[] newWord = XOR(GetWord(expandedKey, i - N), GetWord(expandedKey, i - 1));
                Array.Copy(newWord, 0, expandedKey, i * WORD_SIZE, WORD_SIZE);
            }
        }
        return expandedKey;
    }

    /// <summary>
    /// Returns the number of cipher rounds corresponding to the length of the encryption key.
    /// </summary>
    /// <param name="key">the encryption key</param>
    /// <returns>the number of rounds as integer</returns>
    /// <exception cref="InvalidOperationException">if the key is not of a valid key length for the AES specification</exception>
    private static int GetRounds(byte[] key) {
        return key.Length
        switch {
            16 => 11,
            24 => 13,
            32 => 15,
            _ => throw new InvalidOperationException("invalid key length"),
        };
    }

    /// <summary>
    /// Returns the indext-th word in the target array. Words are byte arrays of the WORD_SIZE size.
    /// 
    /// index is counted in words (multiples of WORD_SIZE)
    /// </summary>
    /// <param name="target">the source array</param>
    /// <param name="index">target word index</param>
    /// <returns>the word</returns>
    internal static byte[] GetWord(byte[] target, int index) {
        Debug.Assert(target.Length >= index + WORD_SIZE, $"array too short: {target.Length} word ends at: {index + WORD_SIZE}");
        return [.. target.Skip(index * WORD_SIZE).Take(WORD_SIZE)];
    }

    internal static byte[] RotWord(byte[] word) {
        byte[] rotated = new byte[WORD_SIZE];
        // this could be a for loop and we could index by (i + 1) % WORD_SIZE, but for readibility's sake...
        rotated[0] = word[1];
        rotated[1] = word[2];
        rotated[2] = word[3];
        rotated[3] = word[0];
        return rotated;
    }

    internal byte[] SubWord(byte[] word) {
        byte[] subbed = new byte[WORD_SIZE];
        for (int i = 0; i < WORD_SIZE; i++) {
            subbed[i] = sbox[word[i]];
        }
        return subbed;
    }

    private static byte[] XOR(byte[] a, byte[] b) {
        return [(byte) (a[0] ^ b[0]), (byte) (a[1] ^ b[1]), (byte) (a[2] ^ b[2]), (byte) (a[3] ^ b[3])];
    }

    private static byte[] ToBigEndianFourByteArray(byte b) {
        return [b, 0, 0, 0];
    }

    private static byte ROTL8(int x, int shift) {
        return (byte) ((x << shift) | ((x) >> (8 - (shift))));
    }

    /// <summary>
    /// Generates the Rijndael sbox.
    /// 
    /// adopted from https://en.wikipedia.org/wiki/Rijndael_S-box
    /// </summary>
    /// <returns>the sbox</returns>
    private static byte[] GenerateSBox() {
        byte p = 1, q = 1;
        byte[] sbox = new byte[256];

        /* loop invariant: p * q == 1 in the Galois field */
        do {
            /* multiply p by 3 */
            p = (byte) (p ^ (p << 1) ^ (((byte) (p & 0x80) != 0) ? 0x1b : 0));

            /* divide q by 3 (equals multiplication by 0xf6) */
            q ^= (byte) (q << 1);
            q ^= (byte) (q << 2);
            q ^= (byte) (q << 4);
            q ^= (byte) (((byte) (q & 0x80) != 0) ? 0x09 : 0);

            /* compute the affine transformation */
            byte xformed = (byte) (q ^ ROTL8(q, 1) ^ ROTL8(q, 2) ^ ROTL8(q, 3) ^ ROTL8(q, 4));

            sbox[p] = (byte) (xformed ^ 0x63);
        } while (p != 1);

        /* 0 is a special case since it has no inverse */
        sbox[0] = 0x63;
        return sbox;
    }

    /// <summary>
    /// Generates the inverse sbox, which is basically the forward sbox in reverse.
    /// </summary>
    /// <param name="sbox"><the forward sbox</param>
    /// <returns>the inverse sbox</returns>
    private static byte[] GenerateInverseSBox(byte[] sbox) {
        byte[] inverseSbox = new byte[256];
        for (int i = 0; i < inverseSbox.Length; i++) {
            inverseSbox[sbox[i]] = (byte) i;
        }
        return inverseSbox;
    }

    /// <summary>
    /// Extracts a round key from the expanded key for a given round.
    /// </summary>
    /// <param name="roundNumber">target round number</param>
    /// <returns>the corresponding round key</returns>
    internal byte[] GetRoundKey(int roundNumber) {
        byte[] roundKey = [.. expandedKey.Skip(roundNumber * BLOCK_SIZE).Take(BLOCK_SIZE)];
        TransposeMatrix(roundKey);
        return roundKey;
    }

    /// <summary>
    /// Rijndael's AddRoundKey action. XORs the two arrays byte-by-byte together.
    /// </summary>
    /// <param name="b">the cipher state to be operated upon</param>
    /// <param name="roundKey">the round key</param>
    /// <returns>product of the operation</returns>
    /// <exception cref="ArgumentNullException">when either of the operands is null</exception>
    internal static byte[] AddRoundKey(byte[] b, byte[] roundKey) {
        if (b == null || roundKey == null) {
            throw new ArgumentNullException("the state or the round key is null");
        }
        Debug.Assert(b.Length == roundKey.Length, $"state and round key length mismatch: {b.Length} != {roundKey.Length}");
        byte[] output = new byte[b.Length];
        for (int i = 0; i < output.Length; i++) {
            output[i] = (byte) (b[i] ^ roundKey[i]);
        }
        return output;
    }

    /// <summary>
    /// Rijndael's SubBytes action. Substitutes each byte in the array for a related byte in the sbox.
    /// </summary>
    /// <param name="b">the cipher state to be operated upon</param>
    /// <returns>the substitution of the state array</returns>
    internal byte[] SubBytes(byte[] b) {
        byte[] subbed = new byte[b.Length];
        for (int i = 0; i < b.Length; i++) {
            subbed[i] = sbox[b[i]];
        }
        return subbed;
    }

    /// <summary>
    /// SubBytes inverse action. Substitutes each byte in the array for a corresponding byte in the inverse sbox.
    /// </summary>
    /// <param name="b">the cipher state to be operated upon</param>
    /// <returns>the desubstitution of the state array</returns>
    internal byte[] UnsubBytes(byte[] b) {
        byte[] subbed = new byte[b.Length];
        for (int i = 0; i < b.Length; i++) {
            subbed[i] = inverseSbox[b[i]];
        }
        return subbed;
    }

    /// <summary>
    /// Rijndarel's ShiftRows. Intertwines the columns to make the matrix more inter-dependent.
    /// </summary>
    /// <param name="b">the cipher state to be operated upon</param>
    /// <returns>the state with the rows shifted</returns>
    internal static byte[] ShiftRows(byte[] b) {
        const int ROWS = 4; // 16-byte put into a square grid is 4x4
        const int ROW_OFFSET = 4; // the length of the row and the beginning of the next one
        byte[] output = new byte[b.Length];
        for (int column = 0; column < ROWS; column++) {
            for (int row = 0; row < ROWS; row++) {
                int itemIndex = row * ROW_OFFSET + ((column + row) % ROW_OFFSET); // row index is also the amount by which to shift
                output[row * ROW_OFFSET + column] = b[itemIndex];
            }
        }
        return output;
    }

    /// <summary>
    /// Inverse action to ShiftRows.
    /// </summary>
    /// <param name="b">the cipher state to be operated upon</param>
    /// <returns>the state with the rows unshifted</returns>
    internal static byte[] UnshiftRows(byte[] b) {
        const int ROWS = 4; // 16-byte put into a square grid is 4x4
        const int ROW_OFFSET = 4; // the length of the row and the beginning of the next one
        byte[] output = new byte[b.Length];
        for (int column = 0; column < ROWS; column++) {
            for (int row = 0; row < ROWS; row++) {
                int itemIndex = row * ROW_OFFSET + ((column + ROWS - row) % ROW_OFFSET); // row index is also the amount by which to shift
                output[row * ROW_OFFSET + column] = b[itemIndex];
            }
        }
        return output;
    }

    /// <summary>
    /// Galois Field (256) Multiplication of two bytes.
    /// 
    /// This code is adopted from https://en.wikipedia.org/wiki/Rijndael_MixColumns.
    /// </summary>
    /// <param name="a">first operand</param>
    /// <param name="b">second operand</param>
    /// <returns>the field product</returns>
    private static byte GFMultiply(byte a, byte b) {
        byte result = 0;
        for (int counter = 0; counter < 8; counter++) {
            if ((b & 1) != 0) {
                result ^= a;
            }
            bool highBitSet = (a & 0x80) != 0;
            a <<= 1;
            if (highBitSet) {
                a ^= 0x1b; /* x^8 + x^4 + x^3 + x + 1 */
            }
            b >>= 1;
        }
        return result;
    }

    /// <summary>
    /// Rijndael's MixColumns action. Applies the affine transformation to provide diffusion.
    /// </summary>
    /// <param name="state">the cipher state to be operated upon</param>
    /// <returns>the state with coluns mixed</returns>
    internal static byte[] MixColumns(byte[] state) {
        byte[] mixed = (byte[]) state.Clone();
        for (int i = 0; i < 4; i++) {
            mixed[i] = (byte) (GFMultiply(0x02, state[i]) ^ GFMultiply(0x03, state[WORD_SIZE + i]) ^ state[2 * WORD_SIZE + i] ^ state[3 * WORD_SIZE + i]);
            mixed[WORD_SIZE + i] = (byte) (state[i] ^ GFMultiply(0x02, state[WORD_SIZE + i]) ^ GFMultiply(0x03, state[2 * WORD_SIZE + i]) ^ state[3 * WORD_SIZE + i]);
            mixed[2 * WORD_SIZE + i] = (byte) (state[i] ^ state[WORD_SIZE + i] ^ GFMultiply(0x02, state[2 * WORD_SIZE + i]) ^ GFMultiply(0x03, state[3 * WORD_SIZE + i]));
            mixed[3 * WORD_SIZE + i] = (byte) (GFMultiply(0x03, state[i]) ^ state[WORD_SIZE + i] ^ state[2 * WORD_SIZE + i] ^ GFMultiply(0x02, state[3 * WORD_SIZE + i]));
        }
        return mixed;
    }

    /// <summary>
    /// Inverse operation to MixColumns. Applies the inverse affine transformation to revert the state back to original.
    /// </summary>
    /// <param name="state">the cipher state to be operated upon</param>
    /// <returns>the state with columns unmixed</returns>
    internal static byte[] UnmixColumns(byte[] state) {
        byte[] mixed = (byte[]) state.Clone();
        for (int i = 0; i < 4; i++) {
            mixed[i] = (byte) (GFMultiply(0x0e, state[i]) ^ GFMultiply(0x0b, state[WORD_SIZE + i]) ^ GFMultiply(0x0d, state[2 * WORD_SIZE + i]) ^ GFMultiply(0x09, state[3 * WORD_SIZE + i]));
            mixed[WORD_SIZE + i] = (byte) (GFMultiply(0x09, state[i]) ^ GFMultiply(0x0e, state[WORD_SIZE + i]) ^ GFMultiply(0x0b, state[2 * WORD_SIZE + i]) ^ GFMultiply(0x0d, state[3 * WORD_SIZE + i]));
            mixed[2 * WORD_SIZE + i] = (byte) (GFMultiply(0x0d, state[i]) ^ GFMultiply(0x09, state[WORD_SIZE + i]) ^ GFMultiply(0x0e, state[2 * WORD_SIZE + i]) ^ GFMultiply(0x0b, state[3 * WORD_SIZE + i]));
            mixed[3 * WORD_SIZE + i] = (byte) (GFMultiply(0x0b, state[i]) ^ GFMultiply(0x0d, state[WORD_SIZE + i]) ^ GFMultiply(0x09, state[2 * WORD_SIZE + i]) ^ GFMultiply(0x0e, state[3 * WORD_SIZE + i]));
        }
        return mixed;
    }

    public void Dispose() { }

    /// <summary>
    /// Applies padding to an array according to the set padding scheme.
    /// </summary>
    /// <param name="b">target array</param>
    /// <returns>padded array</returns>
    /// <exception cref="InvalidOperationException">when the set padding scheme is not supported</exception>
    internal byte[] Pad(byte[] b) {
        return paddingMode switch {
            PaddingMode.PKCS7 => PadPKCS7(b),
            PaddingMode.ANSIX923 => PadANSIX923(b),
            PaddingMode.ISO10126 => PadISO10126(b),
            PaddingMode.None => b,
            _ => throw new InvalidOperationException($"can not use the padding mode {paddingMode}"),
        };
    }

    internal static byte[] PadPKCS7(byte[] b) {
        byte[] padded = new byte[BLOCK_SIZE];
        Array.Copy(b, padded, b.Length);
        int lengthDiff = BLOCK_SIZE - b.Length;
        int offset = b.Length;
        for (int i = 0; i < lengthDiff; i++) {
            padded[offset + i] = (byte) lengthDiff;
        }
        return padded;
    }

    internal static byte[] PadANSIX923(byte[] b) {
        byte[] padded = new byte[BLOCK_SIZE];
        Array.Copy(b, padded, b.Length);
        int lengthDiff = BLOCK_SIZE - b.Length;
        int offset = b.Length;
        for (int i = 0; i < lengthDiff - 1; i++) {
            padded[offset + i] = 0;
        }
        padded[BLOCK_SIZE - 1] = (byte) lengthDiff;
        return padded;
    }

    internal static byte[] PadISO10126(byte[] b) {
        byte[] padded = new byte[BLOCK_SIZE];
        Array.Copy(b, padded, b.Length);
        int lengthDiff = BLOCK_SIZE - b.Length;
        byte[] padding = RandomNumberGenerator.GetBytes(lengthDiff - 1);
        int offset = b.Length;
        Array.Copy(padding, 0, padded, offset, padding.Length);
        padded[BLOCK_SIZE - 1] = (byte) lengthDiff;
        return padded;
    }

    /// <summary>
    /// Removes padding from a byte array. Assumes a padding scheme that stores the pad length on the last index.
    /// </summary>
    /// <param name="b">target array</param>
    /// <returns>array stripped of padding</returns>
    internal byte[] Unpad(byte[] b) {
        if (paddingMode is PaddingMode.None) {
            return b;
        }
        int padLength = b.Last();
        if (padLength > BLOCK_SIZE) {
            throw new InvalidOperationException("last block incorrectly padded, do you have the right key and iv?");
        }
        return [.. b.Take(b.Length - padLength)];
    }

    /// <summary>
    /// Transposes a square matrix stored in a single-dimension array in the traditional linear algebra sense, that is, around the main diagonal.
    /// </summary>
    /// <param name="b">the matrix</param>
    /// <exception cref="InvalidOperationException">when the matrix is not square</exception>
    internal static void TransposeMatrix(byte[] b) {
        double sqrt = Math.Sqrt(b.Length);
        if (Convert.ToInt32(sqrt) != Math.Round(sqrt)) {
            throw new InvalidOperationException("the array is not a square matrix");
        }
        int order = Convert.ToInt32(sqrt);
        // This part is actually the courtesy of ChatGPT himself, notice that is passes the test... :)
        for (int i = 0; i < order; i++) {
            for (int j = i + 1; j < order; j++) {
                int index1 = i * order + j;
                int index2 = j * order + i;
                (b[index2], b[index1]) = (b[index1], b[index2]);
            }
        }
    }

}