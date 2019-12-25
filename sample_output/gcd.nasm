global _start
extern printf
extern exit
section .data
	str_label1: db "gcd of 15 and 7 : ", 0
	str_label2: db "%d", 10, "", 0
	str_label3: db "gcd of 15 and 10 : ", 0
	str_label4: db "%d", 10, "", 0
	str_label5: db "gcd of 15 and 3 : ", 0
	str_label6: db "%d", 10, "", 0
section .text
gcd:
	push ebp
	mov ebp, esp;
	sub esp, 176
	lea eax, [ebp-4]
	mov [ebp-20], eax
	mov eax, [ebp+8]
	mov [ebp-24], eax
	mov edx, [ebp-24]
	mov eax, [ebp-20]
	mov [eax], edx
	mov eax, [ebp-20]
	mov eax, [eax]
	mov [ebp-16], eax
	lea eax, [ebp-8]
	mov [ebp-32], eax
	mov eax, [ebp+12]
	mov [ebp-36], eax
	mov edx, [ebp-36]
	mov eax, [ebp-32]
	mov [eax], edx
	mov eax, [ebp-32]
	mov eax, [eax]
	mov [ebp-28], eax
	mov eax, [ebp+12]
	mov [ebp-48], eax
	mov eax, [ebp+8]
	mov [ebp-52], eax
	mov eax, [ebp-48]
	mov edx, [ebp-52]
	cmp eax, edx
	setg al
	movzx eax, al
	mov [ebp-44], eax
	mov eax, [ebp-44]
	cmp eax, 0
	jz if_lbl1_1
	lea eax, [ebp-4]
	mov [ebp-64], eax
	mov eax, [ebp+12]
	mov [ebp-68], eax
	mov edx, [ebp-68]
	mov eax, [ebp-64]
	mov [eax], edx
	mov eax, [ebp-64]
	mov eax, [eax]
	mov [ebp-60], eax
	lea eax, [ebp-8]
	mov [ebp-76], eax
	mov eax, [ebp+8]
	mov [ebp-80], eax
	mov edx, [ebp-80]
	mov eax, [ebp-76]
	mov [eax], edx
	mov eax, [ebp-76]
	mov eax, [eax]
	mov [ebp-72], eax
	jmp if_lbl1_2
if_lbl1_1:
if_lbl1_2:
	lea eax, [ebp-12]
	mov [ebp-96], eax
	mov eax, [ebp-4]
	mov [ebp-104], eax
	mov eax, [ebp-8]
	mov [ebp-108], eax
	xor edx, edx
	mov eax, [ebp-104]
	mov ebx, [ebp-108]
	idiv ebx
	mov [ebp-100], edx
	mov edx, [ebp-100]
	mov eax, [ebp-96]
	mov [eax], edx
	mov eax, [ebp-96]
	mov eax, [eax]
	mov [ebp-92], eax
	jmp for_lbl1_2
for_lbl1_1:
	lea eax, [ebp-4]
	mov [ebp-152], eax
	mov eax, [ebp-8]
	mov [ebp-156], eax
	mov edx, [ebp-156]
	mov eax, [ebp-152]
	mov [eax], edx
	mov eax, [ebp-152]
	mov eax, [eax]
	mov [ebp-148], eax
	lea eax, [ebp-8]
	mov [ebp-164], eax
	mov eax, [ebp-12]
	mov [ebp-168], eax
	mov edx, [ebp-168]
	mov eax, [ebp-164]
	mov [eax], edx
	mov eax, [ebp-164]
	mov eax, [eax]
	mov [ebp-160], eax
for_lbl1_4:
	lea eax, [ebp-12]
	mov [ebp-128], eax
	mov eax, [ebp-4]
	mov [ebp-136], eax
	mov eax, [ebp-8]
	mov [ebp-140], eax
	xor edx, edx
	mov eax, [ebp-136]
	mov ebx, [ebp-140]
	idiv ebx
	mov [ebp-132], edx
	mov edx, [ebp-132]
	mov eax, [ebp-128]
	mov [eax], edx
	mov eax, [ebp-128]
	mov eax, [eax]
	mov [ebp-124], eax
for_lbl1_2:
	mov eax, [ebp-12]
	mov [ebp-116], eax
	mov eax, 0
	mov [ebp-120], eax
	mov eax, [ebp-116]
	mov edx, [ebp-120]
	cmp eax, edx
	setg al
	movzx eax, al
	mov [ebp-112], eax
	mov eax, [ebp-112]
	cmp eax, 0
	jnz for_lbl1_1
for_lbl1_3:
	mov eax, [ebp-8]
	mov [ebp-176], eax
	mov eax, [ebp-176]
	leave
	ret
main:
	push ebp
	mov ebp, esp;
	sub esp, 400
	lea eax, [ebp-180]
	mov [ebp-204], eax
	mov eax, 15
	mov [ebp-208], eax
	mov edx, [ebp-208]
	mov eax, [ebp-204]
	mov [eax], edx
	mov eax, [ebp-204]
	mov eax, [eax]
	mov [ebp-200], eax
	lea eax, [ebp-184]
	mov [ebp-216], eax
	mov eax, 7
	mov [ebp-220], eax
	mov edx, [ebp-220]
	mov eax, [ebp-216]
	mov [eax], edx
	mov eax, [ebp-216]
	mov eax, [eax]
	mov [ebp-212], eax
	lea eax, [ebp-188]
	mov [ebp-228], eax
	mov eax, 10
	mov [ebp-232], eax
	mov edx, [ebp-232]
	mov eax, [ebp-228]
	mov [eax], edx
	mov eax, [ebp-228]
	mov eax, [eax]
	mov [ebp-224], eax
	lea eax, [ebp-192]
	mov [ebp-240], eax
	mov eax, 3
	mov [ebp-244], eax
	mov edx, [ebp-244]
	mov eax, [ebp-240]
	mov [eax], edx
	mov eax, [ebp-240]
	mov eax, [eax]
	mov [ebp-236], eax
	lea eax, [printf]
	mov [ebp-252], eax
	mov eax, str_label1
	mov [ebp-256], eax
	mov eax, [ebp-256]
	push eax
	mov eax, [ebp-252]
	call eax
	mov [ebp-248], eax
	add esp, 4
	lea eax, [ebp-196]
	mov [ebp-264], eax
	lea eax, [gcd]
	mov [ebp-272], eax
	mov eax, [ebp-180]
	mov [ebp-276], eax
	mov eax, [ebp-184]
	mov [ebp-280], eax
	mov eax, [ebp-280]
	push eax
	mov eax, [ebp-276]
	push eax
	mov eax, [ebp-272]
	call eax
	mov [ebp-268], eax
	add esp, 8
	mov edx, [ebp-268]
	mov eax, [ebp-264]
	mov [eax], edx
	mov eax, [ebp-264]
	mov eax, [eax]
	mov [ebp-260], eax
	lea eax, [printf]
	mov [ebp-288], eax
	mov eax, str_label2
	mov [ebp-292], eax
	mov eax, [ebp-196]
	mov [ebp-296], eax
	mov eax, [ebp-296]
	push eax
	mov eax, [ebp-292]
	push eax
	mov eax, [ebp-288]
	call eax
	mov [ebp-284], eax
	add esp, 8
	lea eax, [printf]
	mov [ebp-304], eax
	mov eax, str_label3
	mov [ebp-308], eax
	mov eax, [ebp-308]
	push eax
	mov eax, [ebp-304]
	call eax
	mov [ebp-300], eax
	add esp, 4
	lea eax, [ebp-196]
	mov [ebp-316], eax
	lea eax, [gcd]
	mov [ebp-324], eax
	mov eax, [ebp-180]
	mov [ebp-328], eax
	mov eax, [ebp-188]
	mov [ebp-332], eax
	mov eax, [ebp-332]
	push eax
	mov eax, [ebp-328]
	push eax
	mov eax, [ebp-324]
	call eax
	mov [ebp-320], eax
	add esp, 8
	mov edx, [ebp-320]
	mov eax, [ebp-316]
	mov [eax], edx
	mov eax, [ebp-316]
	mov eax, [eax]
	mov [ebp-312], eax
	lea eax, [printf]
	mov [ebp-340], eax
	mov eax, str_label4
	mov [ebp-344], eax
	mov eax, [ebp-196]
	mov [ebp-348], eax
	mov eax, [ebp-348]
	push eax
	mov eax, [ebp-344]
	push eax
	mov eax, [ebp-340]
	call eax
	mov [ebp-336], eax
	add esp, 8
	lea eax, [printf]
	mov [ebp-356], eax
	mov eax, str_label5
	mov [ebp-360], eax
	mov eax, [ebp-360]
	push eax
	mov eax, [ebp-356]
	call eax
	mov [ebp-352], eax
	add esp, 4
	lea eax, [ebp-196]
	mov [ebp-368], eax
	lea eax, [gcd]
	mov [ebp-376], eax
	mov eax, [ebp-180]
	mov [ebp-380], eax
	mov eax, [ebp-192]
	mov [ebp-384], eax
	mov eax, [ebp-384]
	push eax
	mov eax, [ebp-380]
	push eax
	mov eax, [ebp-376]
	call eax
	mov [ebp-372], eax
	add esp, 8
	mov edx, [ebp-372]
	mov eax, [ebp-368]
	mov [eax], edx
	mov eax, [ebp-368]
	mov eax, [eax]
	mov [ebp-364], eax
	lea eax, [printf]
	mov [ebp-392], eax
	mov eax, str_label6
	mov [ebp-396], eax
	mov eax, [ebp-196]
	mov [ebp-400], eax
	mov eax, [ebp-400]
	push eax
	mov eax, [ebp-396]
	push eax
	mov eax, [ebp-392]
	call eax
	mov [ebp-388], eax
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
