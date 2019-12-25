global _start
extern printf
extern exit
section .data
	str_label1: db "%d %d %d", 10, "", 0
section .text
main:
	push ebp
	mov ebp, esp;
	sub esp, 176
	lea eax, [ebp-4]
	mov [ebp-24], eax
	mov eax, 0
	mov [ebp-28], eax
	mov edx, [ebp-28]
	mov eax, [ebp-24]
	mov [eax], edx
	mov eax, [ebp-24]
	mov eax, [eax]
	mov [ebp-20], eax
	jmp for_lbl3_2
for_lbl3_1:
	lea eax, [ebp-8]
	mov [ebp-68], eax
	mov eax, 0
	mov [ebp-72], eax
	mov edx, [ebp-72]
	mov eax, [ebp-68]
	mov [eax], edx
	mov eax, [ebp-68]
	mov eax, [eax]
	mov [ebp-64], eax
	jmp for_lbl2_2
for_lbl2_1:
	lea eax, [ebp-12]
	mov [ebp-112], eax
	mov eax, 0
	mov [ebp-116], eax
	mov edx, [ebp-116]
	mov eax, [ebp-112]
	mov [eax], edx
	mov eax, [ebp-112]
	mov eax, [eax]
	mov [ebp-108], eax
	jmp for_lbl1_2
for_lbl1_1:
	lea eax, [printf]
	mov [ebp-152], eax
	mov eax, str_label1
	mov [ebp-156], eax
	mov eax, [ebp-4]
	mov [ebp-160], eax
	mov eax, [ebp-8]
	mov [ebp-164], eax
	mov eax, [ebp-12]
	mov [ebp-168], eax
	mov eax, [ebp-168]
	push eax
	mov eax, [ebp-164]
	push eax
	mov eax, [ebp-160]
	push eax
	mov eax, [ebp-156]
	push eax
	mov eax, [ebp-152]
	call eax
	mov [ebp-148], eax
	add esp, 16
for_lbl1_4:
	mov eax, [ebp-12]
	mov [ebp-136], eax
	mov eax, [ebp-136]
	mov [ebp-132], eax
	lea eax, [ebp-12]
	mov [ebp-140], eax
	mov eax, [ebp-140]
	mov edx, [ebp-140]
	mov edx, [edx]
	inc edx
	mov [eax], edx
for_lbl1_2:
	mov eax, [ebp-12]
	mov [ebp-124], eax
	mov eax, 3
	mov [ebp-128], eax
	mov eax, [ebp-124]
	mov edx, [ebp-128]
	cmp eax, edx
	setl al
	movzx eax, al
	mov [ebp-120], eax
	mov eax, [ebp-120]
	cmp eax, 0
	jnz for_lbl1_1
for_lbl1_3:
for_lbl2_4:
	mov eax, [ebp-8]
	mov [ebp-92], eax
	mov eax, [ebp-92]
	mov [ebp-88], eax
	lea eax, [ebp-8]
	mov [ebp-96], eax
	mov eax, [ebp-96]
	mov edx, [ebp-96]
	mov edx, [edx]
	inc edx
	mov [eax], edx
for_lbl2_2:
	mov eax, [ebp-8]
	mov [ebp-80], eax
	mov eax, 3
	mov [ebp-84], eax
	mov eax, [ebp-80]
	mov edx, [ebp-84]
	cmp eax, edx
	setl al
	movzx eax, al
	mov [ebp-76], eax
	mov eax, [ebp-76]
	cmp eax, 0
	jnz for_lbl2_1
for_lbl2_3:
for_lbl3_4:
	mov eax, [ebp-4]
	mov [ebp-48], eax
	mov eax, [ebp-48]
	mov [ebp-44], eax
	lea eax, [ebp-4]
	mov [ebp-52], eax
	mov eax, [ebp-52]
	mov edx, [ebp-52]
	mov edx, [edx]
	inc edx
	mov [eax], edx
for_lbl3_2:
	mov eax, [ebp-4]
	mov [ebp-36], eax
	mov eax, 2
	mov [ebp-40], eax
	mov eax, [ebp-36]
	mov edx, [ebp-40]
	cmp eax, edx
	setl al
	movzx eax, al
	mov [ebp-32], eax
	mov eax, [ebp-32]
	cmp eax, 0
	jnz for_lbl3_1
for_lbl3_3:
	mov eax, 0
	mov [ebp-176], eax
	mov eax, [ebp-176]
	leave
	ret
_start:
	push ebp
	mov ebp, esp
	call main
	push eax
	call exit
