section .text
global StringToNumber
global NumberToString
global ConvertBase
global ToGrayCode
global FromGrayCode
global ToExcess3
global FromExcess3

; Constants
BASE_BINARY     equ 2
BASE_OCTAL      equ 8
BASE_DECIMAL    equ 10
BASE_HEX        equ 16

; Convert string to number based on base
; Input: rcx = pointer to string
;        rdx = base (2, 8, 10, or 16)
; Output: rax = number
;         CF set if error
StringToNumber:
    push rbx
    push rcx
    push rdx
    push rsi
    
    mov rsi, rcx    ; Move string pointer to rsi
    mov rbx, rdx    ; Move base to rbx
    
    xor rax, rax
    xor rcx, rcx
    
.loop:
    mov cl, byte [rsi]
    test cl, cl
    jz .done
    
    ; Convert character to digit
    cmp cl, '0'
    jb .error
    cmp cl, '9'
    ja .check_hex
    
    ; Decimal digit
    sub cl, '0'
    jmp .check_base
    
.check_hex:
    cmp cl, 'A'
    jb .error
    cmp cl, 'F'
    ja .check_lower
    
    ; Uppercase hex digit
    sub cl, 'A' - 10
    jmp .check_base
    
.check_lower:
    cmp cl, 'a'
    jb .error
    cmp cl, 'f'
    ja .error
    
    ; Lowercase hex digit
    sub cl, 'a' - 10
    
.check_base:
    cmp cl, bl
    jae .error
    
    ; Multiply current result by base and add new digit
    mul rbx
    add rax, rcx
    
    inc rsi
    jmp .loop
    
.error:
    stc
    jmp .exit
    
.done:
    clc
    
.exit:
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    ret

; Convert number to string based on base
; Input: rcx = number
;        rdx = base (2, 8, 10, or 16)
;        r8 = pointer to buffer
; Output: r8 points to null-terminated string
NumberToString:
    push rax
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
    
    mov rax, rcx    ; Move number to rax
    mov rbx, rdx    ; Move base to rbx
    mov rdi, r8     ; Move buffer pointer to rdi
    
    mov rsi, rdi
    add rsi, 31
    mov byte [rsi], 0
    dec rsi
    
    test rax, rax
    jnz .loop
    
    ; If number was zero
    mov byte [rsi], '0'
    dec rsi
    jmp .move_string
    
.loop:
    xor rdx, rdx
    div rbx
    
    ; Convert remainder to character
    cmp dl, 10
    jb .decimal
    
    ; Hex digit
    add dl, 'A' - 10
    jmp .store
    
.decimal:
    add dl, '0'
    
.store:
    mov [rsi], dl
    dec rsi
    
    test rax, rax
    jnz .loop
    
.move_string:
    inc rsi
    mov rcx, rdi
    
.copy_loop:
    mov al, [rsi]
    mov [rdi], al
    inc rsi
    inc rdi
    test al, al
    jnz .copy_loop
    
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax
    ret

; Convert between bases
; Input: rcx = pointer to input string
;        rdx = input base
;        r8 = output base
;        r9 = pointer to output buffer
ConvertBase:
    push rax
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
    
    mov rsi, rcx    ; Move input string pointer to rsi
    mov rbx, rdx    ; Move input base to rbx
    
    ; First convert input string to number
    call StringToNumber
    jc .exit
    
    ; Then convert number to output base string
    mov rcx, rax    ; Move number to rcx
    mov rdx, r8     ; Move output base to rdx
    mov r8, r9      ; Move output buffer to r8
    call NumberToString
    
.exit:
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax
    ret

; Convert decimal number to Gray code
; Input: rcx = decimal number
; Output: rax = Gray code
ToGrayCode:
    mov rax, rcx    ; Copy input number to rax
    shr rax, 1      ; Shift right by 1 (n >> 1)
    xor rax, rcx    ; XOR with original number (n ^ (n >> 1))
    ret

; Convert Gray code to decimal number
; Input: rcx = Gray code
; Output: rax = decimal number
FromGrayCode:
    mov rax, rcx    ; Copy Gray code to rax
    mov rdx, rcx    ; Copy Gray code to rdx for shifting
    
.loop:
    shr rdx, 1      ; Shift right by 1
    jz .done        ; If zero, we're done
    xor rax, rdx    ; XOR with shifted value
    jmp .loop       ; Continue until all bits are processed
    
.done:
    ret

; Convert decimal number to Excess-3 code
; Input: rcx = decimal number (0-9)
; Output: rax = Excess-3 code (4-bit)
ToExcess3:
    push rbx
    push rcx
    
    ; Validate input is between 0-9
    cmp rcx, 9
    ja .error
    
    ; Add 3 to the digit
    mov rax, rcx
    add rax, 3
    
    ; Ensure result is 4 bits
    and rax, 0xF
    
    jmp .done
    
.error:
    xor rax, rax    ; Return 0 for invalid input
    
.done:
    pop rcx
    pop rbx
    ret

; Convert Excess-3 code to decimal number
; Input: rcx = Excess-3 code (4-bit)
; Output: rax = decimal number (0-9)
FromExcess3:
    push rbx
    push rcx
    
    ; Validate input is valid Excess-3 (3-12)
    cmp rcx, 3
    jb .error
    cmp rcx, 12
    ja .error
    
    ; Subtract 3 from the Excess-3 code
    mov rax, rcx
    sub rax, 3
    
    ; Ensure result is between 0-9
    cmp rax, 9
    ja .error
    
    jmp .done
    
.error:
    xor rax, rax    ; Return 0 for invalid input
    
.done:
    pop rcx
    pop rbx
    ret 