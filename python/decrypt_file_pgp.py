import gnupg
import os

def decrypt_file(
    encrypted_file_path: str,
    output_file_path: str,
    gpg_home: str,
    passphrase: str,
    private_key_path: str = None
):
    """
    Decrypts a file encrypted with a PGP key.
    
    :param encrypted_file_path: Path to the encrypted file (.pgp).
    :param output_file_path: Path to write the decrypted result.
    :param gpg_home: Path to your GPG home directory (keys, trustdb, etc.).
    :param passphrase: Passphrase for the private key.
    :param private_key_path: Optional path to your private key file (.asc or .gpg).
    """
    # Initialize GPG, pointing to your gnupg home directory
    gpg = gnupg.GPG(gnupghome=gpg_home)

    # If necessary, import your private key
    # For example, if your private key is not already in the gnupg directory.
    if private_key_path and os.path.exists(private_key_path):
        with open(private_key_path, 'rb') as key_file:
            import_result = gpg.import_keys(key_file.read())
            if not import_result.counts.get('imported', 0):
                raise ValueError("Private key could not be imported. Check key file and permissions.")

    # Decrypt the file
    with open(encrypted_file_path, 'rb') as encrypted_file:
        decrypted_data = gpg.decrypt_file(encrypted_file, passphrase=passphrase)
        
        # Check for success
        if not decrypted_data.ok:
            raise ValueError(
                f"Decryption failed. Status: {decrypted_data.status}\n"
                f"Stderr: {decrypted_data.stderr}"
            )
        
        # Write decrypted content to disk
        with open(output_file_path, 'wb') as out_file:
            out_file.write(decrypted_data.data)
    
    print(f"Decryption successful! Decrypted file saved to: {output_file_path}")


if __name__ == "__main__":
    # Provide your parameters here:
    ENCRYPTED_FILE = "path/to/encrypted_file.pgp"
    OUTPUT_FILE = "path/to/decrypted_output.txt"
    GPG_HOME = "/path/to/your/gnupg/home"  # Or use the default GPG directory, e.g. "~/.gnupg"
    PASSPHRASE = "your_passphrase"
    
    # Optional - if your private key is not already in your GPG keyring:
    PRIVATE_KEY_PATH = "path/to/your_private_key.asc"

    decrypt_file(
        encrypted_file_path=ENCRYPTED_FILE,
        output_file_path=OUTPUT_FILE,
        gpg_home=GPG_HOME,
        passphrase=PASSPHRASE,
        private_key_path=PRIVATE_KEY_PATH
    )
