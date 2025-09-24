    # Data Encryption & Decryption Project

This is a simple, well-documented Python project demonstrating **AES-GCM** encryption and decryption using **PyCryptodome**.
    It includes a small CLI, reusable utility functions, example usage, and a unit test.

## Features
- AES-256 GCM authenticated encryption
- Key generation and secure storage guidance
- Encrypt/decrypt files and text
- Example usage script

## Requirements
- Python 3.8+
- See `requirements.txt`

## Quickstart
1. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # on Windows use venv\Scripts\activate
pip install -r requirements.txt
```

2. Example encrypting text (CLI):

```bash
python src/main.py --mode encrypt --key mysecretkey1234567890123456 --in "Hello world" --out encrypted.bin --type text
```

3. Decrypt the file:

```bash
python src/main.py --mode decrypt --key mysecretkey1234567890123456 --in encrypted.bin --out decrypted.txt --type file
cat decrypted.txt
```

**Important:** Use a secure, random 32-byte key for AES-256. The example uses a password-derived key for simplicity.

## Files
- `src/crypto_utils.py`: encryption utilities (AES-GCM)
- `src/main.py`: small CLI to use the utilities
- `examples/example_usage.sh`: example commands
- `tests/test_crypto.py`: basic unit test

## License
MIT
