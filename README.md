# KCC (KAIST Compiler Collection)

## This is a project for CS420(Compiler Design) in KAIST.

### How to run interpreter
`python3 main.py [--verbose] <file.c>`

### How to run compiler
`python3 assembler.py <file.c> > main.nasm`
`nasm -f elf32 main.nasm && ld -melf_i386 -dynamic-linker /lib/ld-linux.so.2 -o main main.o -lc`
