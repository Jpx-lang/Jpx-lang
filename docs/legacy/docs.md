# JPX Documentation

This document explains the basic usage and syntax of JPX.

JPX is designed to be simple, readable, and easy to experiment with.  
The syntax focuses on clarity and minimal structure.

---

# Basic Syntax

JPX statements usually end with a semicolon `;`.

Example:

```
Print "Hello World";
```

---

# Global Variables

Global variables are declared using the `Global` keyword.

Syntax:

```
Global [name = "value"];
```

Example:

```
Global [name = "john"];
```

The variable can then be accessed anywhere in the script.

---

# Printing Output

Use the `Print` statement to display text.

Example:

```
Print "Hello World";
```

Output:

```
Hello World
```

---

# Variable Usage

Variables can be referenced using `$`.

Example:

```
Global [name = "john"];

Print "Name : $john";
```

Output:

```
Name : john
```

---

# Multiple Statements

You can write multiple statements in a script.

Example:

```
Global [name = "john"];

Print "Name : $john";
Print "Welcome";
```

Output:

```
Name : john
Welcome
```

---

# Example Script

Example file `example.jpx`:

```
Global [name = "john"];

Print "Name : $john";
Print "Hello JPX";
```

Run the script:

```
jpx example.jpx
```

Output:

```
Name : john
Hello JPX
```

---

# Notes

- Every statement should end with `;`
- Variables use `$` when referenced
- Global variables are declared using `Global`

---

# Next

Future documentation may include:

- Control flow
- Functions
- Modules
- Advanced scripting examples

---

> **Archive note**: this is the legacy v1.0 documentation, kept for historical reference.
> It does **not** reflect the current A2 syntax (keywords are now lowercase `print` /
> `global`, and much more is supported). Please read [`../id/README.md`](../id/README.md)
> or [`../eng/README.md`](../eng/README.md) for the current documentation.
