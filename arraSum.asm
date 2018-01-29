section .data
	four dd 4
	numArray dd 20,30,40,50,-1
;;	msg db "%d",10,0
	msg db "sumedha jagtap"
        p dq 10.0
	four dd 3
section .bss
	sum resd 1
section .text
	global main
	extern printf
main:
	xor ecx,ecx
	mov dword[sum],0
loop:
	mov ebx,numArray
        mov eax,eax
	mov eax,dword[four]
	mul ecx
        jmp l4
	add ebx,eax
  	mov edx,'a'
	cmp dword[ebx],-1
	jz  loop
	push msg
	call printf
	add esp,8
	jmp l2

l2:
