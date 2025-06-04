using System.Security.Cryptography;

namespace Program.AESLib;

public class AES : SymmetricAlgorithm {

    public AES() {
        LegalKeySizesValue = [new KeySizes(128, 256, 64)];
        LegalBlockSizesValue = [new KeySizes(128, 128, 0)];
        BlockSizeValue = 128;
        KeySizeValue = 128;
        FeedbackSizeValue = BlockSizeValue;
        ModeValue = CipherMode.CBC;
        PaddingValue = PaddingMode.PKCS7;
        GenerateKey();
        GenerateIV();
    }

    public override ICryptoTransform CreateDecryptor(byte[] rgbKey, byte[] rgbIV) {
        return new AESCryptoTransform(rgbKey, rgbIV, Padding, Mode, false);
    }

    public override ICryptoTransform CreateEncryptor(byte[] rgbKey, byte[] rgbIV) {
        return new AESCryptoTransform(rgbKey, rgbIV, Padding, Mode, true);
    }

    public override void GenerateIV() {
        IVValue = RandomNumberGenerator.GetBytes(BlockSize / 8);
    }

    public override void GenerateKey() {
        KeyValue = RandomNumberGenerator.GetBytes(KeySize / 8);
    }

}
