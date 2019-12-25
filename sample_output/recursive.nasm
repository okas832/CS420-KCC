global _start
extern printf
extern exit
section .data
	str_label1: db "%d", 10, "", 0
section .text
sum:
	push ebp
	mov ebp, esp;
	sub esp, 68
	mov eax, [ebp+8]
	mov [ebp-12], eax
	mov eax, 0
	mov [ebp-16], eax
	mov eax, [ebp-12]
	mov edx, [ebp-16]
	cmp eax, edx
	setg al
	movzx eax, al
	mov [ebp-8], eax
	mov eax, [ebp-8]
	cmp eax, 0
	jz if_lbl1_1
	lea eax, [ebp+8]
	mov [ebp-28], eax
	mov eax, [ebp+8]
	mov [ebp-36], eax
	lea eax, [sum]
	mov [ebp-44], eax
	mov eax, [ebp+8]
	mov [ebp-52], eax
	mov eax, 1
	mov [ebp-56], eax
	mov eax, [ebp-52]
	mov edx, [ebp-56]
	sub eax, edx
	mov [ebp-48], eax
	mov eax, [ebp-48]
	push eax
	mov eax, [ebp-44]
	call eax
	mov [ebp-40], eax
	add esp, 4
	mov eax, [ebp-36]
	mov edx, [ebp-40]
	add eax, edx
	mov [ebp-32], eax
	mov edx, [ebp-32]
	mov eax, [ebp-28]
	mov [eax], edx
	mov eax, [ebp-28]
	mov eax, [eax]
	mov [ebp-24], eax
	jmp if_lbl1_2
if_lbl1_1:
if_lbl1_2:
	mov eax, [ebp+8]
	mov [ebp-68], eax
	mov eax, [ebp-68]
	leave
	ret
main:
	push ebp
	mov ebp, esp;
	sub esp, 108
	lea eax, [ebp-72]
	mov [ebp-80], eax
	lea eax, [sum]
	mov [ebp-88], eax
	mov eax, 50
	mov [ebp-92], eax
	mov eax, [ebp-92]
	push eax
	mov eax, [ebp-88]
	call eax
	mov [ebp-84], eax
	add esp, 4
	mov edx, [ebp-84]
	mov eax, [ebp-80]
	mov [eax], edx
	mov eax, [ebp-80]
	mov eax, [eax]
	mov [ebp-76], eax
	lea eax, [printf]
	mov [ebp-100], eax
	mov eax, str_label1
	mov [ebp-104], eax
	mov eax, [ebp-72]
	mov [ebp-108], eax
	mov eax, [ebp-108]
	push eax
	mov eax, [ebp-104]
	push eax
	mov eax, [ebp-100]
	call eax
	mov [ebp-96], eax
	add esp, 8
	mov eax, 0
	leave
	ret
_start:
	push ebp
	mov ebp, esp
	call main
	push eax
	call exit
