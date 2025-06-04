# AES Implementation
The repository contains a library that provides a basic AES implementation as well as an example program.

### Table of contents
```
1. Disclaimer
2. About AES
3. State of the implementation
4. User manual
5. Implementation details
6. Final notes
```

## 1. Disclaimer
This project is a proof of concept which I created to finish my Programming II classes and also out of curiosity. There is no knowing that the implementation is actually secure as it has undergone no review!

## 2. About AES
The *Advanced Encryption Standard* is the prominent symmetric encryption algorithm in use nowadays. It is an adaptation of the Rijndael algorithm that was selected by NIST and the NSA as a modern standard. 

Learn more about [symmetric cryptography](https://en.wikipedia.org/wiki/Symmetric-key_algorithm), [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard), [NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology), [NSA](https://en.wikipedia.org/wiki/National_Security_Agency).

## 3. State of the implementation
The implementation follows C#'s framework for symmetric algrithms: it implements the `System.Security.Cryptography.SymmetricAlgorithm` abstract class and provides an implementation of the `System.Security.Cryptography.ICryptoTransform` interface. It currently supports the floowing key lengths
- [x] 128 bits
- [x] 192 bits
- [x] 256 bits

the following padding schemes
- [x] No padding
- [x] PKCS7
- [x] ANSIX923
- [x] ISO10126

and the following cipher modes
- [x] ECB
- [x] CBC
- [ ] OFB
- [ ] CFB
- [ ] GCM

For the mentioned above, the implementation passes the example tests from https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/AES_ModesA_All.pdf, https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf. It has not been tested through the certification process as specified in https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Algorithm-Validation-Program/documents/aes/AESAVS.pdf.

Learn more about [padding](https://en.wikipedia.org/wiki/Padding_(cryptography)) and [cipher modes](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation);


## 4. User manual
### Example program
To see the library in action, you can use the example program (source code in `Main.cs`) for simple file encryption and decryption. Assuming you have C# installed, the command
```bash
dotnet run
```
should get you started. The program should build and then ask for the input file, the output file, the encryption password and whether it should encrypt or decrypt the file. Then it should create the new file as specified. You can for example encrypt a file, check that it really is unreadable and then decrypt it back and check that it has the original content again. There is an example text file and example image for that purpose in the `examples/` folder that you can use. Assuming you run linux, you can use the prepared `examples/test_text.sh` and `examples/test_image.sh` scripts to spare you from all the command line typing, you may need to edit the file paths to the generated executable in them though.

### Using the library
Using the library in your own program should be a similar experience as if you were using C#'s standard library implementation of AES (with obviously less features and doubtful performance). You start with creating an instance of the `AES` class and you configure it as necessary. Then you call the `GetEncryptor()` or `GetDecryptor()` method and from there on you use the `ICryptoTranform` object you receive from those methods. Specifically the `ICryptoTransform#TransformBlock()` method and when you are finished, you call the `ICryptoTransform#TransformFinalBlock()` method. Another option is using a `CryptoStream` object instead which calls these methods for you under the hood. This approach is demonstrated in the example program.

 The following code uses the library to encrypt a message using a 128-bit key derived from a password and then decrypts it back to a string message.

```csharp
using System.Security.Cryptography;
using Program.AESLib;
using System.Diagnostics;

...

const string message = "To a mind that is still, the whole universe surrenders. - Lao Tze";

const string password = "Joe"; // secure password should be at least 8 characters, contain lowercase and uppercase letters, digits and special symbols
// derive encryption key from the password using PBKDF2, 16 bytes means we are going to go with the 128-bit version
byte[] key = new Rfc2898DeriveBytes(password, 0, 310000, HashAlgorithmName.SHA256).GetBytes(16);

byte[] plainText = Encoding.UTF8.GetBytes(message); // convert the message to bytes
SymmetricAlgorithm cipher = new AES();
cipher.Key = key;
cipher.Mode = CipherMode.CBC;
cipher.Padding = PaddingMode.PKCS7;
// the cipher automatically generates a random IV, we need to rememeber it, because we will need it for decryption
byte[] iv = cipher.IV;
ICryptoTransform transform = cipher.CreateEncryptor();
byte[] cipherText = transform.TransformFinalBlock(plainText, 0, plainText.Length);
// now the encrypted message is stored in the cipherText variable
// to decrypt it back again, we will do a similar procedure
// we need an AES object with the exact same configuration
cipher = new AES();
cipher.Key = key;
cipher.Mode = CipherMode.CBC;
cipher.Padding = PaddingMode.PKCS7;
cipher.IV = iv; // this is important, we must supply the initialisation vector that was used for encryption (does not apply in ECB mode)
transform = cipher.CreateDecryptor();
byte[] decryptedMessageBytes = transform.TransformFinalBlock(cipherText, 0, cipherText.Length);
string decryptedMessage = Encoding.UTF8.GetString(decryptedMessageBytes); // convert the bytes back to a string
// this should pass, which tells us that the messages are identical
Debug.Assert(decryptedMessage == message);
```

See also [Encrypting data](https://learn.microsoft.com/en-us/dotnet/standard/security/encrypting-data), [SymmetricAlgorithm](https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.symmetricalgorithm?view=net-9.0), [ICryptoTransform](https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.icryptotransform?view=net-9.0), [CryptoStream](https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.cryptostream?view=net-9.0).

## 5. Implementation details
To actually understand what the code is doing, you need at least the basic insight into the working of the encryption algorithm.
### Rijndael in a nutshell
The cipher operates on a block of 16 bytes (called the *block size*), thus it is a block cipher. It starts by expanding the bytes of the encryption key to generate more key material (called the *expanded key*). The 128, 192 and 256-bit versions of the algorithm differ in the length of the encryption key (which is 128, 192 or 256-bits) and the length of the encryption key affects the length of the expanded key. The length of the expanded key in turn affects the number of rounds.

There are four special operations to Rijndael: AddRoundKey, SubBytes, ShiftRows and MixColumns. With few exception before and after, these operations are repeated several times over a block of plain text (the input/message). Each repetition of that sequence is called a *round*. (If you want to see the exact workflow, check the `AESCryptotransform#AESEncryptBlock()` function or the links at the end of the section). The result is what is then called the *cipher text* which is the actual encrypted block (a message is usually made of multiple blocks).

- `AddRoundKey` XORs a round key with the current state of the block (round key is a 16-byte portion of the expanded key, unique for each round).
- `SubBytes` substitutes each byte in the current state of the block for another byte from a substitution box. How? Linear algebra.
- `ShiftRows` looks at the 16 bytes of the block as at a 4x4 matrix and shifts the rows to the right by the index of the row (0 for the first one, 1 for the second, ...).
- `MixColumns` again looks at the block as if it was a matrix and mixes (adds) each byte in a column with all the other bytes in that column. How? Guesss how. Linear algebra!

Related reading [Block cipher](https://en.wikipedia.org/wiki/Block_cipher), [Advanced Encryption Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard), [AES Key Schedule](https://en.wikipedia.org/wiki/AES_key_schedule), [Rijndael S-box](https://en.wikipedia.org/wiki/Rijndael_S-box), [Rijndael MixColumns](https://en.wikipedia.org/wiki/Rijndael_MixColumns).
#### Padding
When the message can not be splitted into blocks of the required size for encryption, it is necessary to extend the last block to match the block size. This is called *padding*. This is why the ciphertext will be up to a block size longer than the plain text. Obviously, the padding must be removed upon decryption. 

Read more [Padding](https://en.wikipedia.org/wiki/Padding_(cryptography)).
#### Cipher modes
If you are more on the nerd side of the spectrum, you might have noticed that since the cipher text is deterministic based on the plain text as the cipher always operates only on a single block at a time, encrypting the same message will always give the same cipher text. To mitigate this, there are various modes of operation for block ciphers. The simplest (I do not consider ECB to be an actual cipher mode) is called CBC, or *Code Block Chaining*. It first XORs the unencrypted block with the previous encrypted block and only after that it proceeds with the actual encryption. This way the shape of the cipher text of a block depends on the previous block. For the very first block which does not have any preceding encrypted block, we use random 16 bytes also known as the *initialisation vector* (IV). This way we get different cipher text for the same message as long as we do not reuse the IVs. We also need the IV for decryption, but it is not a secret, so we can pass it along the cipher text. Losing the IV means not being able to decrypt the first block of the message. 

Read more [Block Cipher Modes of Operation](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation).

* * *

The implementation of the algorithm is in the `AESCryptoTransform.cs` file. It passes NIST's example test vectors for the currently implemented cipher modes, which means it should be correct. To become NIST certified, it would also have to pass a series of about a hundred dynamic tests against a revered implementation where the keys and IVs are generated on the go. These are called Monte Carlo tests and the implementation did not undergo any of those. Nevertheless, it works with the `CryptoStream` API and against its own output.

#### Padding and output buffering
As mentioned above, the input must be padded at encryption (even if the input length is a multiple of the block size, a whole block worth of padding is added as it is not possible to deduce what is padding and what is data otherwise) and this padding must be removed at decryption. The caveat is that the decryption can be done in parts (the `ICryptoTransform#TransformBlock()` method which only takes entire blocks can be called any number of times) and the implementation is not told which will be the last one. The `ICryptoTransform#TransformFinalBlock()` method is used to signalize that the operation is finished, but it can be called without any input, because the last block of the cipher text can as well be passed into the `ICryptoTransform#TransformBlock()` method. For this reason the `ICryptoTransform#TransformBlock()` must retain the last block it is given (the buffering mentioned) so that the cipher is ready in the event that it was in fact the last block. The last block as it is in the cipher's posession now can then be stripped of the padding and returned in the event that the cipher is notified retroactively via `ICryptoTransform#TransformFinalBlock()`.

#### Performance
This is probably one of the least performant AES implenetations on the planet. It creates a huge amount of arrays in places where the changes could be done to the state array directly and also many operations performed on byte arrays could be done on unsigned intergers using bitwise operators instead. Moreover, the decomposition could be much weaker to decrease the size of the callstacks and reduce the function-call overhead. Also, hardware acceleration for cryptography, especially for the AES is very much a thing. To go to the extreme, the serious implementations like [BouncyCastle](https://www.bouncycastle.org/) have multiple implementations and at runtime choose the best one for the current architecture, because on some architecures some instructions are faster than others and you can always optimise the hell out of it. I have also seen them writing the entire encrypt function without using loops. Good thing they do not have to pass the [Computer Systems unforgivable curses](https://www.ksi.mff.cuni.cz/teaching/nswi170-web/pages/labs/coding/) vibe check. Yeah, as stated before, this is a proof of concept.

#### API design
The goal here was to make the use of the library as simple as possible, for that reason the `AES` class has only a single constructor where you have to tweak the object manually. Luckily, this is no issue as the C#'s `SymmetricAlgorithm` class handles all of this for you. There is also no choosing between the 128, 192 and 256-bit version of the algorithm, the implementation chooses the relevant one based on the length of the key in use.

### 6. Final notes

#### Use of LLMs
I used ChatGPT a lot during the work on this project and I have to admit that it was very helpful, but maybe not in the way most people would imagine. Chat was instrumental for advice on design choices and troubleshooting. I also tried to persuade him into writing code, many times, but the results were mostly pretty terrible. The only time it produced a code that I liked and that actually worked, I included it in the codebase. It is mentioned in the comments in the function.

Where Chat was useful was when I was deciding on how to do it all. There is not much documentation on this part of C# on the internet and even though the articles on Wikipedia about AES are exquisite, there is a lot I was missing through the course of the development.

One particular problem I encountered was the incompatibility of the NIST's test resources and the stuff on Wikipedia. The original design uses a 4x4 matrix, but orders the bytes by column and not by rows like any sane person would do, which results in the cipher getting the bytes `0, 4, 8, 12` instead of `0, 1, 2, 3` at the beginning of the array, but then again NIST's test vectors order the bytes the other way than their cipher example run does, which means that sometimes you need to tweak both the tests and the implementation. I consulted this a lot with OpenAI's finest.

#### A real WTF
There is one thing that almost made me give up on this project. The functions `ICryptoTransform#TransformBlock()` and `ICryptoTransform#TransformFinalBlock()` are puzzling. There is no documentation on what should they *actually* do. But since the entire implementation will be built upon the way these two will be used, this is a major roadblock.

 The C#'s documentation says what they should receive and what they should output, but it does not go to the lengths as to explain in what situation a user will call `ICryptoTransform#TransformBlock()` and when they will call `ICryptoTransform#TransformFinalBlock()`. To make it even better, the source code for their implementation of AES (and its CryptoTransform) is not open, or at least I (and Chat) was unable to find it to take a look at their approach. The BouncyCastle library mentioned before goes the other way and creates their own cipher class without any regard for the `ICryptoTransform` API, which I totally respect (maybe even envy), but learned nothing from.

So to anyone wondering, here is what I observed:
- Both `ICryptoTransform#TransformBlock()` and `ICryptoTransform#TransformFinalBlock()` can be used to encrypt or decrypt data and can receive any number of blocks.
- `ICryptoTransform#TransformBlock()` should receive only complete blocks and should buffer the last block in case it is the last.
- `ICryptoTransform#TransformFinalBlock()` is called at the end of the encryption/decryption process and can but may not be given any more data. It can be called on an empty buffer with the input length 0 and is still supposed to spit out the last block with the padding removed. That is why we buffer the block in the first place.
- `ICryptoTransform#TransformBlock()` need never to be called, it is possible to encrypt/decrypt it all using `ICryptoTransform#TransformFinalBlock()`.

