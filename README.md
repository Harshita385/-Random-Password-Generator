# 🔐 Random Password Generator

A Python-based password generator that creates strong, secure passwords based on user-selected criteria. The project includes both a beginner-friendly command-line version and an advanced GUI version with security-focused controls.

## ✨ Features

### Beginner Features
- Prompt for password length
- Minimum length enforced: 8 characters
- Select character types:
  - uppercase letters
  - lowercase letters
  - numbers
  - symbols
- At least 2 character types must be selected
- Input validation for invalid values
- Generates a password that matches the chosen criteria
- Option to generate another password without restarting

### Advanced Features
- GUI interface built with Tkinter
- Cryptographically secure generation using the `secrets` module
- Strength indicator: Weak / Medium / Strong
- Ensures each selected character type is included at least once
- Copy to clipboard support
- Option to exclude ambiguous characters like `0 O 1 l`
- Displays the last 5 generated passwords in the current session

## 🧰 Tech Stack
- Python
- `random` / `secrets`
- `string`
- `tkinter`
- `pyperclip`

## 📁 Project Files
- `password_generator.py` - Main application logic and GUI
- `test_password_generator.py` - Validation tests for generator behavior

## ▶️ How to Run

### 1. Open a terminal
Navigate to the project folder:

```bash
cd "d:\Password Generator"
```

### 2. Run the program
```bash
python password_generator.py
```

This will launch the GUI version. If the GUI cannot run in the environment, the program falls back to the command-line version.

## 🧪 Run Tests

```bash
cd "d:\Password Generator"
pytest -q
```

## 🛡️ Security Notes
- Password generation uses `secrets` for secure random selection.
- Generated passwords are not saved to disk.
- Recent password history is kept only in memory during the active session.

## 📌 Example

```text
Password Length: 16
Selected Types: uppercase, lowercase, numbers, symbols
Generated Password: K7p!Qm2@xL9s#Z4v
Strength: Strong
```

## 🚀 Future Enhancements
- Add password history saving with encryption
- Add dark/light theme toggle
- Add support for custom symbol sets
- Add save/export options for generated passwords

## 📄 License
This project is open-source and can be used for learning and personal projects.
