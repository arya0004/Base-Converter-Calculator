section .text
global AddNumbers
global SubtractNumbers
global MultiplyNumbers
global DivideNumbers

; Add two numbers
; Input: rcx = first number
;        rdx = second number
; Output: rax = result
AddNumbers:
    mov rax, rcx
    add rax, rdx
    ret

; Subtract two numbers
; Input: rcx = first number
;        rdx = second number
; Output: rax = result
SubtractNumbers:
    mov rax, rcx
    sub rax, rdx
    ret

; Multiply two numbers
; Input: rcx = first number
;        rdx = second number
; Output: rax = result
MultiplyNumbers:
    mov rax, rcx
    imul rax, rdx
    ret

; Divide two numbers
; Input: rcx = first number
;        rdx = second number
; Output: rax = result
;         CF set if division by zero
DivideNumbers:
    test rdx, rdx
    jz .error
    
    mov rax, rcx
    cqo             ; Sign extend rax into rdx
    idiv rdx
    clc
    ret
    
.error:
    stc
    ret 