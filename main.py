import math
import os
import string
import sys
from collections import Counter



class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"


ENGLISH_LETTER_FREQUENCY = {
    "A": 8.2, "B": 1.5, "C": 2.8, "D": 4.3, "E": 12.7, "F": 2.2, "G": 2.0,
    "H": 6.1, "I": 7.0, "J": 0.15, "K": 0.77, "L": 4.0, "M": 2.4, "N": 6.7,
    "O": 7.5, "P": 1.9, "Q": 0.095, "R": 6.0, "S": 6.3, "T": 9.1, "U": 2.8,
    "V": 0.98, "W": 2.4, "X": 0.15, "Y": 2.0, "Z": 0.074,
}

ALPHABET = string.ascii_uppercase
ALPHABET_SIZE = 26

BANNER = rf"""{Color.CYAN}{Color.BOLD}
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
{Color.RESET}{Color.DIM}          Classical Cipher & Frequency Analysis Toolkit{Color.RESET}
"""


class CaesarCipher:
    @staticmethod
    def encrypt(text: str, shift: int) -> str:
        return CaesarCipher._transform(text, shift)

    @staticmethod
    def decrypt(text: str, shift: int) -> str:
        return CaesarCipher._transform(text, -shift)

    @staticmethod
    def _transform(text: str, shift: int) -> str:
        output = []
        for char in text:
            if not char.isalpha():
                output.append(char)
                continue
            index = ALPHABET.index(char.upper())
            new_char = ALPHABET[(index + shift) % ALPHABET_SIZE]
            output.append(new_char if char.isupper() else new_char.lower())
        return "".join(output)


class FrequencyAnalyzer:
    """Break a Caesar cipher using classical letter-frequency analysis."""

    def __init__(self, reference_freq: dict = None):
        self.reference_freq = reference_freq or ENGLISH_LETTER_FREQUENCY

    def score(self, text: str) -> float:
        """
        Lower score = closer match to the reference language distribution.
        Uses mean absolute deviation between observed and expected frequency.
        """
        total_letters = sum(1 for c in text if c.isalpha())
        if total_letters == 0:
            return math.inf

        counter = Counter(c for c in text.upper() if c.isalpha())
        deviation = 0.0
        for letter in ALPHABET:
            observed_pct = (counter.get(letter, 0) / total_letters) * 100
            deviation += abs(observed_pct - self.reference_freq[letter])
        return deviation / ALPHABET_SIZE

    def rank_keys(self, ciphertext: str) -> list:
        """Return all 26 shift candidates sorted best-to-worst."""
        if not any(c.isalpha() for c in ciphertext):
            raise ValueError("Input contains no alphabetic characters to analyze.")

        results = []
        for shift in range(ALPHABET_SIZE):
            candidate = CaesarCipher.decrypt(ciphertext, shift)
            results.append((shift, self.score(candidate), candidate))
        results.sort(key=lambda r: r[1])
        return results

    def best_key(self, ciphertext: str) -> int:
        return self.rank_keys(ciphertext)[0][0]



class CLI:
    WIDTH = 60

    def __init__(self):
        self.analyzer = FrequencyAnalyzer()

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    def header(self, title: str):
        print(f"{Color.CYAN}{'─' * self.WIDTH}{Color.RESET}")
        print(f"{Color.BOLD} {title}{Color.RESET}")
        print(f"{Color.CYAN}{'─' * self.WIDTH}{Color.RESET}")

    def success(self, msg: str):
        print(f"{Color.GREEN}[✓]{Color.RESET} {msg}")

    def error(self, msg: str):
        print(f"{Color.RED}[✗]{Color.RESET} {msg}")

    def info(self, label: str, value: str):
        print(f"  {Color.DIM}{label}:{Color.RESET} {value}")

    def prompt(self, msg: str) -> str:
        return input(f"{Color.YELLOW}›{Color.RESET} {msg}: ").strip()

    def pause(self):
        input(f"\n{Color.DIM}Press ENTER to return to the menu...{Color.RESET}")

    def read_shift(self) -> int:
        raw = self.prompt("Shift key (0-25)")
        shift = int(raw)
        if not 0 <= shift <= 25:
            raise ValueError("Shift key must be between 0 and 25.")
        return shift

    
    def action_encrypt(self):
        self.clear()
        self.header("ENCRYPT")
        text = self.prompt("Plaintext")
        try:
            shift = self.read_shift()
        except ValueError as e:
            self.error(str(e))
            self.pause()
            return
        result = CaesarCipher.encrypt(text, shift)
        print()
        self.info("Shift", str(shift))
        self.success(f"Ciphertext: {Color.BOLD}{result}{Color.RESET}")
        self.pause()

    def action_decrypt(self):
        self.clear()
        self.header("DECRYPT (known key)")
        text = self.prompt("Ciphertext")
        try:
            shift = self.read_shift()
        except ValueError as e:
            self.error(str(e))
            self.pause()
            return
        result = CaesarCipher.decrypt(text, shift)
        print()
        self.success(f"Plaintext: {Color.BOLD}{result}{Color.RESET}")
        self.pause()

    def action_crack(self):
        self.clear()
        self.header("CRACK (frequency analysis)")
        text = self.prompt("Ciphertext")
        try:
            ranked = self.analyzer.rank_keys(text)
        except ValueError as e:
            self.error(str(e))
            self.pause()
            return

        best_shift, best_score, best_text = ranked[0]
        print()
        self.success(f"Most likely key: {Color.BOLD}{best_shift}{Color.RESET}  "
                      f"{Color.DIM}(score={best_score:.2f}, lower is better){Color.RESET}")
        self.info("Plaintext", best_text)

        print(f"\n  {Color.DIM}Runner-up candidates:{Color.RESET}")
        for shift, score, candidate in ranked[1:4]:
            print(f"    {Color.DIM}k={shift:<3} score={score:6.2f}  {candidate}{Color.RESET}")
        self.pause()

    def action_bruteforce(self):
        self.clear()
        self.header("BRUTE FORCE (all 26 keys)")
        text = self.prompt("Ciphertext")
        print()
        for shift in range(ALPHABET_SIZE):
            print(f"  {Color.DIM}k={shift:<3}{Color.RESET} {CaesarCipher.decrypt(text, shift)}")
        self.pause()

    
    def show_menu(self):
        self.clear()
        print(BANNER)
        print(f"{Color.CYAN}{'═' * self.WIDTH}{Color.RESET}")
        options = [
            ("1", "Encrypt text"),
            ("2", "Decrypt text (known key)"),
            ("3", "Crack ciphertext (frequency analysis)"),
            ("4", "Brute force (show all 26 keys)"),
            ("0", "Exit"),
        ]
        for key, label in options:
            print(f"  {Color.BOLD}{key}{Color.RESET}  {label}")
        print(f"{Color.CYAN}{'═' * self.WIDTH}{Color.RESET}")

    def run(self):
        actions = {
            "1": self.action_encrypt,
            "2": self.action_decrypt,
            "3": self.action_crack,
            "4": self.action_bruteforce,
        }
        while True:
            self.show_menu()
            choice = self.prompt("Select an option")

            if choice == "0":
                print(f"\n{Color.CYAN}Goodbye.{Color.RESET}\n")
                sys.exit(0)

            action = actions.get(choice)
            if action is None:
                self.error("Invalid option.")
                self.pause()
                continue

            try:
                action()
            except ValueError:
                self.error("Shift key must be a valid integer between 0 and 25.")
                self.pause()


def main():
    try:
        CLI().run()
    except KeyboardInterrupt:
        print(f"\n\n{Color.CYAN}Interrupted. Goodbye.{Color.RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()