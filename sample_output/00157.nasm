global _start
extern printf
extern exit
section .data
	str_label1: db "%d", 10, "", 0
section .text
main:
	push ebp
	mov ebp, esp;
	sub esp, 204
	lea eax, [ebp-4]
	mov [ebp-56], eax
	mov eax, 1
	mov [ebp-60], eax
	mov edx, [ebp-60]
	mov eax, [ebp-56]
	mov [eax], edx
	mov eax, [ebp-56]
	mov eax, [eax]
	mov [ebp-52], eax
	jmp for_lbl1_2
for_lbl1_1:
	lea eax, [ebp-44]
	mov [ebp-100], eax
	mov eax, [ebp-4]
	mov [ebp-108], eax
	mov eax, 1
	mov [ebp-112], eax
	mov eax, [ebp-108]
	mov edx, [ebp-112]
	sub eax, edx
	mov [ebp-104], eax
	mov eax, [ebp-100]
	mov edx, [ebp-104]
	lea eax, [edx * 4 + eax]
	mov [ebp-96], eax
	mov eax, [ebp-4]
	mov [ebp-120], eax
	mov eax, [ebp-4]
	mov [ebp-124], eax
	mov eax, [ebp-120]
	mov edx, [ebp-124]
	imul eax, edx
	mov [ebp-116], eax
	mov edx, [ebp-116]
	mov eax, [ebp-96]
	mov [eax], edx
	mov eax, [ebp-96]
	mov eax, [eax]
	mov [ebp-92], eax
for_lbl1_4:
	mov eax, [ebp-4]
	mov [ebp-80], eax
	mov eax, [ebp-80]
	mov [ebp-76], eax
	lea eax, [ebp-4]
	mov [ebp-84], eax
	mov eax, [ebp-84]
	mov edx, [ebp-84]
	mov edx, [edx]
	inc edx
	mov [eax], edx
for_lbl1_2:
	mov eax, [ebp-4]
	mov [ebp-68], eax
	mov eax, 10
	mov [ebp-72], eax
	mov eax, [ebp-68]
	mov edx, [ebp-72]
	cmp eax, edx
	setle al
	movzx eax, al
	mov [ebp-64], eax
	mov eax, [ebp-64]
	cmp eax, 0
	jnz for_lbl1_1
for_lbl1_3:
	lea eax, [ebp-4]
	mov [ebp-136], eax
	mov eax, 0
	mov [ebp-140], eax
	mov edx, [ebp-140]
	mov eax, [ebp-136]
	mov [eax], edx
	mov eax, [ebp-136]
	mov eax, [eax]
	mov [ebp-132], eax
	jmp for_lbl2_2
for_lbl2_1:
	lea eax, [printf]
	mov [ebp-176], eax
	mov eax, str_label1
	mov [ebp-180], eax
	lea eax, [ebp-44]
	mov [ebp-192], eax
	mov eax, [ebp-4]
	mov [ebp-196], eax
	mov eax, [ebp-192]
	mov edx, [ebp-196]
	lea eax, [edx * 4 + eax]
	mov [ebp-184], eax
	mov eax, [ebp-184]
	mov eax, [eax]
	mov [ebp-188], eax
	mov eax, [ebp-188]
	push eax
	mov eax, [ebp-180]
	push eax
	mov eax, [ebp-176]
	call eax
	mov [ebp-172], eax
	add esp, 8
for_lbl2_4:
	mov eax, [ebp-4]
	mov [ebp-160], eax
	mov eax, [ebp-160]
	mov [ebp-156], eax
	lea eax, [ebp-4]
	mov [ebp-164], eax
	mov eax, [ebp-164]
	mov edx, [ebp-164]
	mov edx, [edx]
	inc edx
	mov [eax], edx
for_lbl2_2:
	mov eax, [ebp-4]
	mov [ebp-148], eax
	mov eax, 10
	mov [ebp-152], eax
	mov eax, [ebp-148]
	mov edx, [ebp-152]
	cmp eax, edx
	setl al
	movzx eax, al
	mov [ebp-144], eax
	mov eax, [ebp-144]
	cmp eax, 0
	jnz for_lbl2_1
for_lbl2_3:
	mov eax, 0
	mov [ebp-204], eax
	mov eax, [ebp-204]
	leave
	ret
_start:
	push ebp
	mov ebp, esp
	call main
	push eax
	call exit
