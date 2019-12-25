global _start
extern printf
extern exit
section .data
	str_label1: db "%d", 10, "", 0
section .text
factorial:
	push ebp
	mov ebp, esp;
	sub esp, 56
	mov eax, [ebp+8]
	mov [ebp-12], eax
	mov eax, 2
	mov [ebp-16], eax
	mov eax, [ebp-12]
	mov edx, [ebp-16]
	cmp eax, edx
	setl al
	movzx eax, al
	mov [ebp-8], eax
	mov eax, [ebp-8]
	cmp eax, 0
	jz if_lbl1_1
	mov eax, [ebp+8]
	mov [ebp-24], eax
	mov eax, [ebp-24]
	leave
	ret
	jmp if_lbl1_2
if_lbl1_1:
	mov eax, [ebp+8]
	mov [ebp-36], eax
	lea eax, [factorial]
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
	imul eax, edx
	mov [ebp-32], eax
	mov eax, [ebp-32]
	leave
	ret
if_lbl1_2:
	mov eax, 0
	leave
	ret
main:
	push ebp
	mov ebp, esp;
	sub esp, 132
	lea eax, [ebp-60]
	mov [ebp-72], eax
	mov eax, 1
	mov [ebp-76], eax
	mov edx, [ebp-76]
	mov eax, [ebp-72]
	mov [eax], edx
	mov eax, [ebp-72]
	mov eax, [eax]
	mov [ebp-68], eax
	jmp for_lbl1_2
for_lbl1_1:
	lea eax, [printf]
	mov [ebp-108], eax
	mov eax, str_label1
	mov [ebp-112], eax
	lea eax, [factorial]
	mov [ebp-120], eax
	mov eax, [ebp-60]
	mov [ebp-124], eax
	mov eax, [ebp-124]
	push eax
	mov eax, [ebp-120]
	call eax
	mov [ebp-116], eax
	add esp, 4
	mov eax, [ebp-116]
	push eax
	mov eax, [ebp-112]
	push eax
	mov eax, [ebp-108]
	call eax
	mov [ebp-104], eax
	add esp, 8
for_lbl1_4:
	mov eax, [ebp-60]
	mov [ebp-96], eax
	mov eax, [ebp-96]
	mov [ebp-92], eax
	lea eax, [ebp-60]
	mov [ebp-100], eax
	mov eax, [ebp-100]
	mov edx, [ebp-100]
	mov edx, [edx]
	inc edx
	mov [eax], edx
for_lbl1_2:
	mov eax, [ebp-60]
	mov [ebp-84], eax
	mov eax, 10
	mov [ebp-88], eax
	mov eax, [ebp-84]
	mov edx, [ebp-88]
	cmp eax, edx
	setle al
	movzx eax, al
	mov [ebp-80], eax
	mov eax, [ebp-80]
	cmp eax, 0
	jnz for_lbl1_1
for_lbl1_3:
	mov eax, 0
	mov [ebp-132], eax
	mov eax, [ebp-132]
	leave
	ret
_start:
	push ebp
	mov ebp, esp
	call main
	push eax
	call exit
