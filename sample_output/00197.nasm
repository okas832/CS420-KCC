global _start
extern printf
extern exit
section .data
	__fred: dd 1234
	__joe: dd 0
	str_label1: db "%d", 10, "", 0
	str_label2: db "%d", 10, "", 0
	str_label3: db "%d", 10, "", 0
	str_label4: db "%d", 10, "", 0
	str_label5: db "%d", 10, "", 0
section .text
henry:
	push ebp
	mov ebp, esp;
	sub esp, 36
	mov eax, 4567
	mov [ebp-8], eax
	mov eax, [ebp-8]
	mov [ebp-4], eax
	lea eax, [printf]
	mov [ebp-16], eax
	mov eax, str_label1
	mov [ebp-20], eax
	mov eax, [ebp-4]
	mov [ebp-24], eax
	mov eax, [ebp-24]
	push eax
	mov eax, [ebp-20]
	push eax
	mov eax, [ebp-16]
	call eax
	mov [ebp-12], eax
	add esp, 8
	mov eax, [ebp-4]
	mov [ebp-32], eax
	mov eax, [ebp-32]
	mov [ebp-28], eax
	lea eax, [ebp-4]
	mov [ebp-36], eax
	mov eax, [ebp-36]
	mov edx, [ebp-36]
	mov edx, [edx]
	inc edx
	mov [eax], edx
	mov eax, 0
	leave
	ret
main:
	push ebp
	mov ebp, esp;
	sub esp, 164
	lea eax, [printf]
	mov [ebp-44], eax
	mov eax, str_label2
	mov [ebp-48], eax
	mov eax, [__fred]
	mov [ebp-52], eax
	mov eax, [ebp-52]
	push eax
	mov eax, [ebp-48]
	push eax
	mov eax, [ebp-44]
	call eax
	mov [ebp-40], eax
	add esp, 8
	lea eax, [henry]
	mov [ebp-60], eax
	mov eax, [ebp-60]
	call eax
	mov [ebp-56], eax
	lea eax, [henry]
	mov [ebp-68], eax
	mov eax, [ebp-68]
	call eax
	mov [ebp-64], eax
	lea eax, [henry]
	mov [ebp-76], eax
	mov eax, [ebp-76]
	call eax
	mov [ebp-72], eax
	lea eax, [henry]
	mov [ebp-84], eax
	mov eax, [ebp-84]
	call eax
	mov [ebp-80], eax
	lea eax, [printf]
	mov [ebp-92], eax
	mov eax, str_label3
	mov [ebp-96], eax
	mov eax, [__fred]
	mov [ebp-100], eax
	mov eax, [ebp-100]
	push eax
	mov eax, [ebp-96]
	push eax
	mov eax, [ebp-92]
	call eax
	mov [ebp-88], eax
	add esp, 8
	lea eax, [__fred]
	mov [ebp-108], eax
	mov eax, 8901
	mov [ebp-112], eax
	mov edx, [ebp-112]
	mov eax, [ebp-108]
	mov [eax], edx
	mov eax, [ebp-108]
	mov eax, [eax]
	mov [ebp-104], eax
	lea eax, [__joe]
	mov [ebp-120], eax
	mov eax, 2345
	mov [ebp-124], eax
	mov edx, [ebp-124]
	mov eax, [ebp-120]
	mov [eax], edx
	mov eax, [ebp-120]
	mov eax, [eax]
	mov [ebp-116], eax
	lea eax, [printf]
	mov [ebp-132], eax
	mov eax, str_label4
	mov [ebp-136], eax
	mov eax, [__fred]
	mov [ebp-140], eax
	mov eax, [ebp-140]
	push eax
	mov eax, [ebp-136]
	push eax
	mov eax, [ebp-132]
	call eax
	mov [ebp-128], eax
	add esp, 8
	lea eax, [printf]
	mov [ebp-148], eax
	mov eax, str_label5
	mov [ebp-152], eax
	mov eax, [__joe]
	mov [ebp-156], eax
	mov eax, [ebp-156]
	push eax
	mov eax, [ebp-152]
	push eax
	mov eax, [ebp-148]
	call eax
	mov [ebp-144], eax
	add esp, 8
	mov eax, 0
	mov [ebp-164], eax
	mov eax, [ebp-164]
	leave
	ret
_start:
	push ebp
	mov ebp, esp
	call main
	push eax
	call exit
