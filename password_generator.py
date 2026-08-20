import random
import secrets
import string
from typing import List, Sequence


TYPE_MAP = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "numbers": string.digits,
    "symbols": string.punctuation,
}

AMBIGUOUS_EXCLUSIONS = {
    "uppercase": set("O"),
    "lowercase": set("l"),
    "numbers": set("0O1l"),
}


def validate_inputs(length: int, selected_types: Sequence[str]) -> str:
    if length < 8:
        return "Length must be at least 8 characters."
    if len(selected_types) < 2:
        return "Select at least 2 character types."
    return ""


def build_character_pool(selected_types: Sequence[str], exclude_ambiguous: bool = False) -> dict:
    pools = {}
    for option in selected_types:
        chars = TYPE_MAP.get(option, "")
        if exclude_ambiguous:
            if option == "uppercase":
                chars = "".join(ch for ch in chars if ch not in AMBIGUOUS_EXCLUSIONS["uppercase"])
            elif option == "lowercase":
                chars = "".join(ch for ch in chars if ch not in AMBIGUOUS_EXCLUSIONS["lowercase"])
            elif option == "numbers":
                chars = "".join(ch for ch in chars if ch not in AMBIGUOUS_EXCLUSIONS["numbers"])
        pools[option] = chars
    return pools


def generate_password(
    length: int,
    selected_types: Sequence[str],
    exclude_ambiguous: bool = False,
) -> str:
    validation_message = validate_inputs(length, selected_types)
    if validation_message:
        raise ValueError(validation_message)

    pools = build_character_pool(selected_types, exclude_ambiguous=exclude_ambiguous)
    required_chars = []
    for option in selected_types:
        if pools[option]:
            required_chars.append(secrets.choice(pools[option]))

    if len(required_chars) < 2:
        raise ValueError("Select at least 2 character types.")

    remaining_length = length - len(required_chars)
    all_chars = "".join(pools[option] for option in selected_types if pools[option])
    if not all_chars:
        raise ValueError("No valid characters available for the selected types.")

    password_chars = required_chars[:]
    for _ in range(remaining_length):
        password_chars.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def classify_strength(length: int, selected_types: Sequence[str]) -> str:
    diversity_score = len(selected_types)
    if length >= 16 and diversity_score >= 3:
        return "Strong"
    if length >= 10 and diversity_score >= 2:
        return "Medium"
    return "Weak"


def prompt_for_cli() -> None:
    print("Random Password Generator")
    while True:
        try:
            length = int(input("Enter password length (minimum 8): ").strip())
        except ValueError:
            print("Invalid length. Please enter a number.")
            continue

        selected_types = []
        if input("Include uppercase letters? (y/n): ").strip().lower() == "y":
            selected_types.append("uppercase")
        if input("Include lowercase letters? (y/n): ").strip().lower() == "y":
            selected_types.append("lowercase")
        if input("Include numbers? (y/n): ").strip().lower() == "y":
            selected_types.append("numbers")
        if input("Include symbols? (y/n): ").strip().lower() == "y":
            selected_types.append("symbols")

        validation_message = validate_inputs(length, selected_types)
        if validation_message:
            print(validation_message)
            again = input("Generate another password? (y/n): ").strip().lower()
            if again != "y":
                return
            continue

        exclude_ambiguous = input("Exclude ambiguous characters (0 O 1 l)? (y/n): ").strip().lower() == "y"
        password = generate_password(length, selected_types, exclude_ambiguous=exclude_ambiguous)
        print(f"Generated password: {password}")
        print(f"Strength: {classify_strength(length, selected_types)}")

        again = input("Generate another password? (y/n): ").strip().lower()
        if again != "y":
            return


class PasswordGeneratorGUI:
    def __init__(self):
        try:
            import tkinter as tk
        except ImportError as exc:
            raise RuntimeError("tkinter is not available in this environment.") from exc
        self.tk = tk
        self.window = None

    def build(self):
        window = self.tk.Tk()
        window.title("Random Password Generator")
        window.geometry("560x620")
        window.configure(bg="#0f172a")
        self.window = window

        self.length_var = self.tk.IntVar(value=16)
        self.exclude_ambiguous_var = self.tk.BooleanVar(value=False)
        self.history = []

        self.option_vars = {
            "uppercase": self.tk.BooleanVar(value=True),
            "lowercase": self.tk.BooleanVar(value=True),
            "numbers": self.tk.BooleanVar(value=True),
            "symbols": self.tk.BooleanVar(value=True),
        }

        title_color = "#f8fafc"
        label_color = "#e2e8f0"
        panel_color = "#111827"
        accent_color = "#38bdf8"
        accent_2 = "#a78bfa"
        button_text = "#0f172a"

        main_frame = self.tk.Frame(window, bg="#0f172a", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        header = self.tk.Label(
            main_frame,
            text="Secure Password Generator",
            font=("Segoe UI", 18, "bold"),
            fg=title_color,
            bg="#0f172a",
        )
        header.pack(pady=(0, 12))

        section_frame = self.tk.Frame(main_frame, bg=panel_color, bd=1, relief="flat", padx=16, pady=16)
        section_frame.pack(fill="x", pady=6)

        self.tk.Label(section_frame, text="Password Length", font=("Segoe UI", 11, "bold"), fg=label_color, bg=panel_color).pack(pady=(0, 6))
        self.length_spinbox = self.tk.Spinbox(
            section_frame,
            from_=8,
            to=128,
            textvariable=self.length_var,
            width=12,
            font=("Segoe UI", 11),
            fg="#111827",
            bg="#f8fafc",
            justify="center",
        )
        self.length_spinbox.pack()

        self.tk.Label(section_frame, text="Character Types", font=("Segoe UI", 11, "bold"), fg=label_color, bg=panel_color).pack(pady=(16, 8))
        chars_frame = self.tk.Frame(section_frame, bg=panel_color)
        chars_frame.pack(fill="x")

        for name in ["uppercase", "lowercase", "numbers", "symbols"]:
            check = self.tk.Checkbutton(
                chars_frame,
                text=name.title(),
                variable=self.option_vars[name],
                fg=label_color,
                bg=panel_color,
                activebackground=panel_color,
                activeforeground=accent_color,
                selectcolor="#1e293b",
                font=("Segoe UI", 10),
            )
            check.pack(anchor="w", pady=2)

        self.exclude_ambiguous_checkbox = self.tk.Checkbutton(
            section_frame,
            text="Exclude ambiguous characters (0 O 1 l)",
            variable=self.exclude_ambiguous_var,
            fg=label_color,
            bg=panel_color,
            activebackground=panel_color,
            activeforeground=accent_color,
            selectcolor="#1e293b",
            font=("Segoe UI", 10),
        )
        self.exclude_ambiguous_checkbox.pack(anchor="w", pady=(10, 4))

        self.result_var = self.tk.StringVar(value="")
        self.output_box = self.tk.Entry(
            section_frame,
            textvariable=self.result_var,
            width=38,
            font=("Segoe UI", 11),
            fg="#0f172a",
            bg="#f8fafc",
            bd=2,
        )
        self.output_box.pack(pady=(10, 6))

        button_frame = self.tk.Frame(main_frame, bg="#0f172a")
        button_frame.pack(pady=8)

        self.generate_button = self.tk.Button(
            button_frame,
            text="Generate Password",
            command=self.generate_and_copy,
            bg="#67e8f9",
            fg=button_text,
            activebackground="#a5f3fc",
            activeforeground=button_text,
            font=("Segoe UI", 10, "bold"),
            width=18,
            pady=6,
            bd=0,
        )
        self.generate_button.pack(side="left", padx=6)

        self.copy_button = self.tk.Button(
            button_frame,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
            bg="#c4b5fd",
            fg=button_text,
            activebackground="#ddd6fe",
            activeforeground=button_text,
            font=("Segoe UI", 10, "bold"),
            width=18,
            pady=6,
            bd=0,
        )
        self.copy_button.pack(side="left", padx=6)

        self.strength_var = self.tk.StringVar(value="Weak")
        self.strength_label = self.tk.Label(
            main_frame,
            text="Strength: Weak",
            font=("Segoe UI", 11, "bold"),
            fg="#fda4af",
            bg="#0f172a",
        )
        self.strength_label.pack(pady=(10, 4))

        self.history_label = self.tk.Label(
            main_frame,
            text="Recent passwords",
            font=("Segoe UI", 10, "bold"),
            fg=label_color,
            bg="#0f172a",
        )
        self.history_label.pack(pady=(10, 2))
        self.history_text = self.tk.Text(main_frame, height=7, width=48, bg="#0b1120", fg="#e2e8f0", bd=1, relief="flat")
        self.history_text.pack()

        self.window.mainloop()

    def _selected_types(self) -> List[str]:
        return [name for name, variable in self.option_vars.items() if variable.get()]

    def _update_strength(self, password: str):
        selected_types = self._selected_types()
        strength = classify_strength(len(password), selected_types)
        self.strength_var.set(strength)
        self.strength_label.config(text=f"Strength: {strength}")

    def generate_and_copy(self):
        length = self.length_var.get()
        selected_types = self._selected_types()
        validation_message = validate_inputs(length, selected_types)
        if validation_message:
            self.result_var.set(validation_message)
            return

        password = generate_password(length, selected_types, exclude_ambiguous=self.exclude_ambiguous_var.get())
        self.result_var.set(password)
        self._update_strength(password)
        self.history.append(password)
        self.history = self.history[-5:]
        self.history_text.delete("1.0", self.tk.END)
        for item in self.history:
            self.history_text.insert(self.tk.END, f"{item}\n")

        self.copy_to_clipboard(password)

    def copy_to_clipboard(self, password: str | None = None):
        try:
            import pyperclip
        except ImportError:
            return
        text = password if password is not None else self.result_var.get()
        if text:
            pyperclip.copy(text)


if __name__ == "__main__":
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.update()
        root.destroy()
        PasswordGeneratorGUI().build()
    except Exception:
        prompt_for_cli()
