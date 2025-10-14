---
argument-hint: [run_id] [path to draft file] [path to spec file]
description: Plan a bugfix
---

# Bugfix Planning

Create a file following the `Create File` using the `Variables`.

## Variables

`run_id`: $1
`path to draft file`: $2
`path to spec file`: $3

## Create File

Create a file at `path to spec file` with content:

---file content

run id: <fill in `run_id`>
path to draft file: <fill in `path to draft file`>

---
