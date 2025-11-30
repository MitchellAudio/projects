# Copilot Instructions for AI Coding Agents

This repository currently contains minimal documentation and no established project structure. To be productive, AI agents should:

- **Assume this is a monorepo or project root.**
  - All new projects, experiments, or code should be placed in clearly named subdirectories under the root.
  - Each new project should include its own `README.md` and, if applicable, a `requirements.txt`, `package.json`, or other relevant manifest.

- **Documentation:**
  - The root `README.md` is currently empty. Add project-level documentation to each subproject.
  - If you create a new project, update the root `README.md` with a short description and a link to the subproject.

- **Conventions:**
  - Use clear, descriptive directory and file names.
  - Prefer standard open-source project layouts (e.g., `src/`, `tests/`, `docs/`).
  - Place all configuration files (e.g., `.env`, `.gitignore`) at the project or subproject root as appropriate.

- **Workflows:**
  - There are no established build, test, or CI workflows yet. If you add them, document the commands in the subproject's `README.md`.
  - Use standard tools for the language/framework (e.g., `pytest` for Python, `npm test` for Node.js).

- **External Integrations:**
  - No external dependencies or integrations are currently defined. Document any you add in the relevant subproject.

- **AI Agent Guidance:**
  - If you introduce project-specific conventions, document them in a `copilot-instructions.md` or similar file in the relevant directory.
  - Keep instructions concise and actionable.

## Example: Adding a New Python Project

1. Create a new directory under the root (e.g., `my_new_project/`).
2. Add a `README.md` describing the project.
3. Add a `requirements.txt` for dependencies.
4. Add your code in a `src/` directory and tests in a `tests/` directory.
5. Update the root `README.md` with a link and description.

---

_This file should be updated as the repository evolves. Remove or revise generic guidance as concrete patterns emerge._
