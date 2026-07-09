.intel_syntax noprefix
cmp dword ptr [edi], 0x7f454c46
je add_all
cmp dword ptr [edi], 0x00005a4d
je sub_all
jmp mul_all
add_all:
mov eax, [edi+4]
add eax, [edi+8]
add eax, [edi+12]
jmp done
sub_all:
mov eax, [edi+4]
sub eax, [edi+8]
sub eax, [edi+12]
jmp done
mul_all:
mov eax, [edi+4]
imul eax, [edi+8]
imul eax, [edi+12]
done:
