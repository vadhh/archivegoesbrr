# archivegoesbrr

## Password-Protected ZIP Archive Cracker v1.0

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.x-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## Overview

ArchiveGoesBrr is a command-line tool designed to recover passwords from password-protected ZIP archives. It uses a brute-force approach with customizable character sets and password length parameters to systematically test possible passwords against an encrypted ZIP file.

**⚠️ ETHICAL USAGE DISCLAIMER ⚠️**  
This tool is intended for **educational purposes only** and for recovering passwords from ZIP files you own or have explicit permission to test. Unauthorized cracking of files is illegal and unethical.

## Features

- **Automated Password Generation**: Generates passwords on-the-fly based on user-defined parameters
- **Customizable Character Sets**: Choose from predefined character sets (letters, digits, alphanumeric, or all characters)
- **Configurable Password Length**: Set minimum and maximum password length to search
- **Progress Tracking**: Real-time progress bar showing password attempts and estimated completion
- **Encryption Detection**: Automatically detects if a ZIP file is password-protected
- **Error Handling**: Robust error handling for file not found, corrupted archives, and other exceptions
- **Memory Efficient**: Uses generators to minimize memory usage during password generation

## Installation

### Prerequisites

- Python 3.x
- Required Python packages: `tqdm`

### Setup

1. Clone the repository or download the source code:
   ```bash
   git clone https://github.com/yourusername/archivegoesbrr.git
   cd archivegoesbrr
   ```

2. Install the required dependencies:
   ```bash
   pip install tqdm
   ```

## Usage

### Basic Usage

```bash
python main.py -z path/to/encrypted.zip --min-len 3 --max-len 5 --charset digits
```

### Command-Line Arguments

| Argument | Description |
|----------|-------------|
| `-z`, `--zipfile` | Path to the password-protected ZIP file (required) |
| `--min-len` | Minimum length for generated passwords (default: 1) |
| `--max-len` | Maximum length for generated passwords (default: 8) |
| `--charset` | Character set for password generation (default: alnum) |

### Character Set Options

| Option | Description |
|--------|-------------|
| `alpha` | Lowercase and uppercase letters (a-z, A-Z) |
| `alnum` | Letters and digits (a-z, A-Z, 0-9) |
| `digits` | Only digits (0-9) |
| `all` | Letters, digits, and special characters (Warning: Very large search space) |

### Examples

1. Try 4-digit PIN codes:
   ```bash
   python main.py -z secure.zip --min-len 4 --max-len 4 --charset digits
   ```

2. Try alphanumeric passwords between 3-5 characters:
   ```bash
   python main.py -z protected.zip --min-len 3 --max-len 5 --charset alnum
   ```

3. Try alphabetic passwords of exactly 6 characters:
   ```bash
   python main.py -z locked.zip --min-len 6 --max-len 6 --charset alpha
   ```

## How It Works

ArchiveGoesBrr works by:

1. Verifying the target ZIP file exists and is password-protected
2. Generating passwords based on the specified character set and length range
3. Systematically testing each password against the ZIP file
4. Displaying real-time progress and results

The tool uses Python's `zipfile` module to interact with ZIP archives and the `itertools.product` function to efficiently generate password combinations.

## Performance Considerations

- **Search Space Size**: The number of possible passwords grows exponentially with length and character set size. For example:
  - 4-digit PIN (charset=digits): 10,000 combinations
  - 8-character alphanumeric (charset=alnum): ~218 trillion combinations

- **Execution Time**: Brute-force approaches can be extremely time-consuming for longer passwords or larger character sets. The tool will warn you if the search space is very large.

- **Memory Usage**: The tool uses generators to create passwords on-the-fly, which minimizes memory usage but doesn't affect execution time.

## Limitations

- **Performance**: As a pure Python implementation, this tool is not optimized for speed compared to specialized cracking tools like John the Ripper or Hashcat.

- **No GPU Acceleration**: The tool uses CPU only and doesn't leverage GPU acceleration.

- **Limited Attack Methods**: Currently only implements brute-force attacks with character sets. No dictionary attacks, rule-based mutations, or other advanced techniques.

## Future Improvements

- Multiprocessing support to utilize multiple CPU cores
- Dictionary attack mode with custom wordlists
- Smart password generation based on common patterns
- Resume capability for interrupted cracking sessions
- Support for other archive formats (RAR, 7z, etc.)

## Troubleshooting

### Common Issues

- **ModuleNotFoundError: No module named 'tqdm'**  
  Solution: Install the required package with `pip install tqdm`

- **Error: ZIP file not found**  
  Solution: Verify the path to your ZIP file is correct

- **Error: Not a valid ZIP file or is corrupted**  
  Solution: Ensure the file is a valid ZIP archive

## License

[MIT License](LICENSE)

## Author

DHOOM

---

**Remember**: This tool should only be used for legitimate password recovery on files you own or have permission to access. Unauthorized use is illegal and unethical.
        