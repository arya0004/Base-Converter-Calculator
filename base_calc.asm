; base_calc.asm - Assembly functions for base conversion and calculator
; Target: Windows (64-bit DLL)
; Assembler: NASM

global _convert_decimal_to_binary
global _add_numbers
global _subtract_numbers
global _multiply_numbers
global _divide_numbers

SECTION .text

; -------------------------------------------------------------------------
; int add_numbers(int a, int b)
_add_numbers:
    mov rax, rdi            ; Move first argument (a) into rax
    add rax, rsi            ; Add second argument (b) to rax
    ret

; -------------------------------------------------------------------------
; int subtract_numbers(int a, int b)
_subtract_numbers:
    mov rax, rdi            ; Move first argument (a) into rax
    sub rax, rsi            ; Subtract second argument (b) from rax
    ret

; -------------------------------------------------------------------------
; int multiply_numbers(int a, int b)
_multiply_numbers:
    mov rax, rdi            ; Move first argument (a) into rax
    imul rax, rsi           ; Multiply rax by second argument (b)
    ret

; -------------------------------------------------------------------------
; int divide_numbers(int a, int b)
_divide_numbers:
    mov rax, rdi            ; Move numerator (a) into rax
    cqo                     ; Sign-extend rax into rdx:rax
    idiv rsi                ; Divide rdx:rax by second argument (b)
    ret

; -------------------------------------------------------------------------
; char* convert_decimal_to_binary(int num)
; Returns pointer to static binary string
_convert_decimal_to_binary:
    push rbx                ; Save registers we will use
    push rcx
    push rdx
    push rsi

    mov rsi, rdi            ; Move the number to rsi
    mov rcx, 64             ; Maximum 64-bit binary digits
    lea rbx, [bin_buffer + 64] ; Point to end of buffer
    mov byte [rbx], 0       ; Null terminator
    dec rbx

.next_bit:
    test rsi, rsi
    jz .done
    xor rdx, rdx
    mov rax, rsi
    shr rsi, 1
    setc dl
    add dl, '0'             ; Convert remainder to '0' or '1'
    mov [rbx], dl
    dec rbx
    loop .next_bit

.done:
    inc rbx
    mov rdi, rbx            ; Return pointer to the binary string

    pop rsi
    pop rdx
    pop rcx
    pop rbx
    ret

SECTION .data
bin_buffer: times 65 db 0   ; 64 digits max + null terminator
