%macro sum 2
	mov esi,%1
%%abc:	mov edi,%2
	add esi,edi
	mov eax,esi
%endmacro
%macro sub 2
	mov esi,%1
	sub esi,edi
	mov eax,esi
%endmacro
section .data
	msg db "Sum is : %d",10,0
section .text
	global main
	extern printf
main:
	sum 10,20
        sub 30,20
	pusha
	push eax
	push msg
	call printf
	add esp,8
	popa
