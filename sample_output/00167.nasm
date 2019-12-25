global _start
extern printf
extern exit
section .data
	str_label1: db "a is true", 10, "", 0
	str_label2: db "a is false", 10, "", 0
	str_label3: db "b is true", 10, "", 0
	str_label4: db "b is false", 10, "", 0
section .text
main:
	push ebp
	mov ebp, esp;
	sub esp, 88
	mov eax, 1
	mov [ebp-8], eax
	mov eax, [ebp-8]
	mov [ebp-4], eax
	mov eax, 0
	mov [ebp-16], eax
	mov eax, [ebp-16]
	mov [ebp-12], eax
	mov eax, [ebp-4]
	mov [ebp-24], eax
	mov eax, [ebp-24]
	cmp eax, 0
	jz if_lbl1_1
	lea eax, [printf]
	mov [ebp-32], eax
	mov eax, str_label1
	mov [ebp-36], eax
	mov eax, [ebp-36]
	push eax
	mov eax, [ebp-32]
	call eax
	mov [ebp-28], eax
	add esp, 4
	jmp if_lbl1_2
if_lbl1_1:
	lea eax, [printf]
	mov [ebp-44], eax
	mov eax, str_label2
	mov [ebp-48], eax
	mov eax, [ebp-48]
	push eax
	mov eax, [ebp-44]
	call eax
	mov [ebp-40], eax
	add esp, 4
if_lbl1_2:
	mov eax, [ebp-12]
	mov [ebp-56], eax
	mov eax, [ebp-56]
	cmp eax, 0
	jz if_lbl2_1
	lea eax, [printf]
	mov [ebp-64], eax
	mov eax, str_label3
	mov [ebp-68], eax
	mov eax, [ebp-68]
	push eax
	mov eax, [ebp-64]
	call eax
	mov [ebp-60], eax
	add esp, 4
	jmp if_lbl2_2
if_lbl2_1:
	lea eax, [printf]
	mov [ebp-76], eax
	mov eax, str_label4
	mov [ebp-80], eax
	mov eax, [ebp-80]
	push eax
	mov eax, [ebp-76]
	call eax
	mov [ebp-72], eax
	add esp, 4
if_lbl2_2:
	mov eax, 0
	mov [ebp-88], eax
	mov eax, [ebp-88]
	leave
	ret
_start:
	push ebp
	mov ebp, esp
	call main
	push eax
	call exit
