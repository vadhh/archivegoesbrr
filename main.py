import zipfile
import argparse
import sys
import time
import itertools # Added for password generation
import string # Added for character sets
from tqdm import tqdm # For a progress bar

# --- Color Codes for Terminal Output ---
class TermColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Prints a cool banner for the tool."""
    banner = f"""
{TermColors.OKCYAN}

 █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗ ██████╗  ██████╗ ███████╗███████╗██████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝██╔════╝ ██╔═══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
███████║██████╔╝██║     ███████║██║██║   ██║█████╗  ██║  ███╗██║   ██║█████╗  ███████╗██████╔╝██████╔╝██████╔╝
██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝██╔══╝  ██║   ██║██║   ██║██╔══╝  ╚════██║██╔══██╗██╔══██╗██╔══██╗
██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████╗╚██████╔╝╚██████╔╝███████╗███████║██████╔╝██║  ██║██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
                                                                                                              
{TermColors.HEADER}Password-Protected ZIP Archive Cracker v1.0{TermColors.ENDC}
{TermColors.OKBLUE}                                                           Author: DHOOM{TermColors.ENDC}
{TermColors.WARNING}Ethical Use Only: Only use on files you have explicit permission to test.{TermColors.ENDC}
"""
    print(banner)

def generate_passwords(min_len, max_len, charset):
    """Generates passwords of length min_len to max_len using charset."""
    for length in range(min_len, max_len + 1):
        for p in itertools.product(charset, repeat=length):
            yield "".join(p)

def crack_zip(zip_file_path, min_len, max_len, charset_choice):
    """
    Attempts to crack a password-protected ZIP file using generated passwords.

    Args:
        zip_file_path (str): The path to the encrypted ZIP file.
        min_len (int): Minimum length for generated passwords.
        max_len (int): Maximum length for generated passwords.
        charset_choice (str): Choice of character set ('alpha', 'alnum', 'digits', 'all').

    Returns:
        str or None: The found password if successful, otherwise None.
    """
    try:
        zip_archive = zipfile.ZipFile(zip_file_path)
    except FileNotFoundError:
        print(f"{TermColors.FAIL}[-] Error: ZIP file '{zip_file_path}' not found.{TermColors.ENDC}")
        return None
    except zipfile.BadZipFile:
        print(f"{TermColors.FAIL}[-] Error: '{zip_file_path}' is not a valid ZIP file or is corrupted.{TermColors.ENDC}")
        return None

    # Check if the ZIP file is actually password-protected
    # One way to check is if any file inside has the 'encrypted' flag
    is_encrypted = False
    for zinfo in zip_archive.infolist():
        if zinfo.flag_bits & 0x1: # Check for encryption flag
            is_encrypted = True
            break
    
    if not is_encrypted:
        print(f"{TermColors.WARNING}[!] Info: The ZIP file '{zip_file_path}' does not appear to be password-protected.{TermColors.ENDC}")
        zip_archive.close()
        return None

    selected_charset = ""
    if charset_choice == 'alpha':
        selected_charset = string.ascii_letters
    elif charset_choice == 'alnum':
        selected_charset = string.ascii_letters + string.digits
    elif charset_choice == 'digits':
        selected_charset = string.digits
    elif charset_choice == 'all': # Example: letters, digits, and common symbols
        selected_charset = string.ascii_letters + string.digits + string.punctuation
    else:
        print(f"{TermColors.FAIL}[-] Error: Invalid charset choice '{charset_choice}'.{TermColors.ENDC}")
        zip_archive.close()
        return None

    # Calculate total number of passwords to try for tqdm (can be very large!)
    # This calculation can be computationally expensive for large charsets/lengths
    # and might be better estimated or handled differently for very large search spaces.
    total_passwords = 0
    try:
        for length in range(min_len, max_len + 1):
            total_passwords += len(selected_charset) ** length
        if total_passwords == 0 and min_len <= max_len : # if charset is empty but length is valid
             print(f"{TermColors.WARNING}[!] Warning: Character set is empty. No passwords will be generated.{TermColors.ENDC}")
        elif total_passwords > 10**9: # Arbitrary limit to warn user
            print(f"{TermColors.WARNING}[!] Warning: The number of possible passwords ({total_passwords}) is extremely large.{TermColors.ENDC}")
            print(f"{TermColors.WARNING}    This may take a very, very long time. Consider refining length or charset.{TermColors.ENDC}")

    except OverflowError:
        total_passwords = float('inf') # Cannot calculate precisely, use infinity for tqdm
        print(f"{TermColors.WARNING}[!] Warning: The number of possible passwords is too large to calculate precisely.{TermColors.ENDC}")
        print(f"{TermColors.WARNING}    This will take an extremely long time. Consider refining length or charset.{TermColors.ENDC}")


    print(f"{TermColors.OKCYAN}[*] Starting password cracking for: {zip_file_path}{TermColors.ENDC}")
    print(f"{TermColors.OKCYAN}[*] Using generated passwords: min_len={min_len}, max_len={max_len}, charset='{charset_choice}' (approx. {total_passwords if total_passwords != float('inf') else 'many'} passwords){TermColors.ENDC}")
            
    start_time = time.time()
    passwords_tried = 0

    # Use a generator for passwords to save memory
    password_generator = generate_passwords(min_len, max_len, selected_charset)

    with tqdm(password_generator, total=total_passwords if total_passwords != float('inf') else None, unit="pass", desc="Trying passwords") as pbar:
        for password in pbar:
            passwords_tried += 1
            # tqdm handles the description update, no need to print every password
            # pbar.set_description(f"Trying: {password}") 
            try:
                first_file_in_zip = zip_archive.infolist()[0]
                zip_archive.open(first_file_in_zip, pwd=password.encode('utf-8')).read(1)
                    
                end_time = time.time()
                duration = end_time - start_time
                print(f"\n{TermColors.OKGREEN}[+] Password found: {password}{TermColors.ENDC}")
                print(f"{TermColors.OKBLUE}[*] Time taken: {duration:.2f} seconds{TermColors.ENDC}")
                print(f"{TermColors.OKBLUE}[*] Passwords tried: {passwords_tried}{TermColors.ENDC}")
                zip_archive.close()
                return password
            except RuntimeError as e:
                if 'Bad password' in str(e) or 'password' in str(e).lower():
                    continue
                else:
                    # print(f"{TermColors.WARNING}[!] Warning: Runtime error for password '{password}': {e}{TermColors.ENDC}")
                    continue
            except zipfile.BadZipFile:
                continue
            except Exception as e:
                # print(f"{TermColors.WARNING}[!] Unexpected error with password '{password}': {e}{TermColors.ENDC}")
                continue
            
    end_time = time.time()
    duration = end_time - start_time
    print(f"\n{TermColors.FAIL}[-] Password not found with the current settings.{TermColors.ENDC}")
    print(f"{TermColors.OKBLUE}[*] Time taken: {duration:.2f} seconds{TermColors.ENDC}")
    print(f"{TermColors.OKBLUE}[*] Passwords tried: {passwords_tried}{TermColors.ENDC}")

    zip_archive.close() # Ensure archive is closed if no password found
    return None

if __name__ == "__main__":
    print_banner()
    parser = argparse.ArgumentParser(
        description=f"{TermColors.HEADER}Password-Protected ZIP Archive Cracker{TermColors.ENDC}",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
{TermColors.OKCYAN}Example usage:{TermColors.ENDC}
  python {sys.argv[0]} -z my_archive.zip --min 3 --max 5 --charset alnum
  python {sys.argv[0]} -z my_archive.zip --charset digits --min 4 --max 6

{TermColors.WARNING}Charset options:{TermColors.ENDC}
  alpha:  Lowercase and uppercase letters
  alnum:  Letters and digits
  digits: Only digits (0-9)
  all:    Letters, digits, and common punctuation (be careful, this can be very large!)

{TermColors.WARNING}Disclaimer:{TermColors.ENDC}
  This tool is intended for educational purposes and for recovering passwords
  from ZIP files you own or have explicit permission to test.
  Unauthorized cracking of files is illegal and unethical.
"""
    )
    parser.add_argument("-z", "--zipfile", required=True, help="Path to the password-protected ZIP file.")
    # parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file (one password per line).")
    parser.add_argument("--min-len", type=int, default=1, help="Minimum length for generated passwords (default: 1).")
    parser.add_argument("--max-len", type=int, default=8, help="Maximum length for generated passwords (default: 8).")
    parser.add_argument("--charset", type=str, default='alnum', 
                        choices=['alpha', 'alnum', 'digits', 'all'], 
                        help="Character set for generated passwords (default: alnum). Options: alpha, alnum, digits, all.")


    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()

    zip_file_path = args.zipfile
    # wordlist_path = args.wordlist # Removed

    crack_zip(zip_file_path, args.min_len, args.max_len, args.charset)
