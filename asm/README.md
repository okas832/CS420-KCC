# KCC Assembler

## TODO
- [x] Handle global variable to define in .data section
- [x] Evaluate the constant of assignation of global variable
- [x] Translate AST to pre-ASM
- [x] Transform pre-ASM to nasm style assembly language

## Link & Make Binary
`nasm -f elf32 main.nasm && ld -melf_i386 -dynamic-linker /lib/ld-linux.so.2 -o main main.o -lc`

## Etc
- Need to add some in assemble-addr
- ++ and -- can act strangly
