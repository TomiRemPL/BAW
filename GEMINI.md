# Gemini Workspace Configuration (`GEMINI.md`)

This file helps customize and configure the Gemini AI assistant's behavior within this project. By defining project-specific settings, you can streamline workflows, improve accuracy, and ensure Gemini adheres to your project's conventions.

## 💡 Key Features

- **Project-Specific Instructions:** Provide tailored instructions to Gemini about your project's architecture, coding style, and conventions.
- **Custom Tools & Commands:** Define custom commands and tools that Gemini can use to perform project-specific tasks.
- **Fact Sheets:** Create "fact sheets" to give Gemini context about libraries, APIs, or services used in your project.

## ⚙️ How It Works

Gemini reads `GEMINI.md` files from the project root and subdirectories to gather context. You can have multiple `GEMINI.md` files, each providing context for its own directory and subdirectories.

### Example: Defining Project Conventions

```markdown
## Project Conventions

- **Commit Messages:** Follow the Conventional Commits specification (e.g., `feat: add user authentication`).
- **Coding Style:** Adhere to the PEP 8 style guide for Python. Use `black` for formatting.
- **Testing:** Use `pytest` for all new tests. Mocks should be placed in a `tests/mocks` directory.
```

### Example: Custom Commands

You can define simple, project-specific commands that Gemini can execute.

```markdown
## Custom Commands

- **`@run_tests`**: Runs the entire test suite.
  - `pytest`
- **`@lint_code`**: Lints the codebase.
  - `black . && ruff check .`
```

## 📚 Best Practices

- **Be Clear and Concise:** Use clear headings and simple language.
- **Start Small:** Begin with a few key instructions and expand as needed.
- **Keep it Updated:** As your project evolves, update your `GEMINI.md` to reflect the changes.

For more detailed information and advanced configurations, please refer to the official Gemini documentation.
