
# JPX

<p align="center">
  <img width="1024" height="1024" alt="JPX logo" src="https://github.com/user-attachments/assets/3e61732d-77e6-4a47-8195-5b7350946df3" />
</p>

<p align="center">
  <b>A minimalist scripting language built for experimentation and lightweight automation.</b>
</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg" />
  <img alt="Status" src="https://img.shields.io/badge/status-active-brightgreen.svg" />
  <img alt="Version" src="https://img.shields.io/badge/version-A2-orange.svg" />
</p>

---

## 📖 Overview

**JPX** is a simple scripting language designed for experimentation, lightweight automation, and exploring minimalist runtime concepts. Its core focus is a **readable syntax** and **fast execution** — without unnecessary complexity.

Whether you are learning how interpreters work, prototyping small logic, or building quick automation scripts, JPX provides a small and approachable surface to work with.

---

## ✨ Features

- **Simple, readable syntax** — easy to learn and understand
- **Explicit global variable declaration** using the `Global` keyword
- **Native string interpolation** with the `$` operator
- **Lightweight** — minimal dependencies and fast startup
- **Well-suited for scripting experiments** and quick prototyping

---

## 📦 Installation

### Option 1 — Download the Release Binary

Download the latest binary from the official release page:

👉 [**JPX Releases — A2**](https://github.com/Jpx-lang/Jpx-lang/releases/tag/A2)

After downloading, make the binary executable and ensure it is available on your `PATH` (or run it directly from its directory):

```bash
./jpx <file.jpx>
Option 2 — Install via Shogun
JPX can also be installed using the Shogun package manager:
```
```bash
shogun install Jpx-cli
```
Once installed, the jpx command will be available globally on your system.

Verify Installation
```bash
jpx --version
```
📜 Syntax Overview
JPX keeps its syntax deliberately small and direct.

Global Variables
Global variables are declared using the Global keyword:

```jpx
Global [name = "john"];
```
Once declared, a global variable is accessible from anywhere in the script.

Print Statement
Use Print to produce output:

```jpx
Print "Hello World";
```
Variable Interpolation
JPX supports inline variable interpolation inside strings using the $ prefix:

```jpx
Global [name = "john"];
```
Print "Name : $john";
Output:

```text
Name : john
```
📄 Example Script
Create a file named example.jpx:

```jpx
Global [name = "john"];

Print "Name : $john";
Print "Welcome to JPX";
```
Run it:

```bash
jpx example.jpx
```
Output:

```text
Name : john
Welcome to JPX
```
📚 Documentation
Additional documentation is available through:

The repository Wiki

Tutorial articles

Example scripts in the examples/ directory

🧪 Use Cases
JPX is a good fit for:

Experimenting with scripting language design

Lightweight automation tasks

Learning how interpreters work

Prototyping logic and ideas

Small scripting utilities

🤝 Contributing
Contributions are highly welcome. There are many ways to get involved:

Add new example scripts

Improve documentation

Report bugs

Suggest new features

Submit pull requests

Before contributing, please review the existing issues and follow the repository's contribution guidelines.

🪪 License
This project is released under the MIT License.

You are free to use, modify, and distribute this software in accordance with the terms of the MIT License. See the LICENSE file for details.

JPX Package Downloads

👉 jpxkg.netlify.app

📢 Community
Follow JPX development through:

This repository

The project Wiki

Community channels

<p align="center"> <i>JPX is built as an exploration of simple, flexible scripting language design.</i> </p> ```
