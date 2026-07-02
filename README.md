```
 ██████╗ █████╗ ███████╗███████╗ █████╗ ██████╗
██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗
██║     ███████║█████╗  ███████╗███████║██████╔╝
██║     ██╔══██║██╔══╝  ╚════██║██╔══██║██╔══██╗
╚██████╗██║  ██║███████╗███████║██║  ██║██║  ██║
 ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝

 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗
██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗
██║     ██║██████╔╝███████║█████╗  ██████╔╝
██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗
╚██████╗██║██║     ██║  ██║███████╗██║  ██║
 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
          Classical Cipher & Frequency Analysis Toolkit
```

A command-line tool for encrypting, decrypting, and cryptanalyzing Caesar-shift ciphers using classical letter-frequency analysis.

## Features

- Encrypt / decrypt text with a known shift key (0-25)
- Automatically crack a ciphertext by comparing its letter distribution against standard English letter frequencies
- Brute force mode — view the plaintext for all 26 possible keys at once
- Case, spacing, and punctuation preserved

## Requirements

- Python 3.8+
- No external dependencies

## Usage

Run from source:

```bash
py caesar_cipher.py
```

Or run the prebuilt Windows executable directly — no Python installation required:

```
caesar_cipher.exe
```

Then choose an option from the menu:

```
1  Encrypt text
2  Decrypt text (known key)
3  Crack ciphertext (frequency analysis)
4  Brute force (show all 26 keys)
0  Exit
```

## How the frequency analysis works

Every language has a distinctive letter frequency "fingerprint" (in English, `E` is the most common letter, `Z` the rarest). A Caesar cipher shifts every letter by the same amount, so it shifts this fingerprint too, but doesn't erase it. The `crack` option decrypts the ciphertext with all 26 possible keys, measures how close each result's letter distribution is to real English, and returns the closest match as the most likely key.

Note: this method is probabilistic, not guaranteed — it works reliably on longer texts (a few dozen letters or more) and can be inaccurate on very short inputs.
