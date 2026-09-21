# Create the remote GitHub repository

The ChatGPT GitHub connector available in this chat can edit existing repositories but does not expose a create-repository action. Create one empty public repository in the GitHub UI, then push this starter.

Recommended repository name:

```text
oplang-compiler-lite
```

Do not initialize the remote with README/.gitignore because this starter already contains them.

From this folder:

```bash
git init -b main
git add .
git commit -m "chore: bootstrap OPLang Compiler Lite"
git remote add origin https://github.com/namdayneee/oplang-compiler-lite.git
git push -u origin main
```

After the first push, GitHub is the canonical remote for the new project. The old repository is not modified and is not a runtime dependency.
