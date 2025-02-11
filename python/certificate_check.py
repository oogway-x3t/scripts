import os
import subprocess

def get_certificate_expiration_date(pem_file):
  """
  Extracts the expiration date from a PEM certificate file.

  Args:
    pem_file: Path to the PEM certificate file.

  Returns:
    A string representing the expiration date in YYYY-MM-DD format,
    or None if the expiration date cannot be extracted.
  """
  try:
    result = subprocess.run(
        ["openssl", "x509", "-in", pem_file, "-noout", "-enddate"],
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout.strip()
    expiration_date = output.split("=")[1]
    return expiration_date.split(" ")[0]  # Extract YYYY-MM-DD
  except subprocess.CalledProcessError:
    print(f"Error processing certificate file: {pem_file}")
    return None

def find_and_check_certificates(directory):
  """
  Finds PEM certificate files in a directory and its subdirectories,
  and prints their expiration dates.

  Args:
    directory: The directory to start the search from.
  """
  for root, _, files in os.walk(directory):
    for file in files:
      if file.endswith(".pem"):
        pem_file = os.path.join(root, file)
        expiration_date = get_certificate_expiration_date(pem_file)
        if expiration_date:
          print(f"Certificate: {pem_file} expires on {expiration_date}")

if __name__ == "__main__":
  start_directory = "/path/to/your/directory"  # Replace with your directory
  find_and_check_certificates(start_directory)
