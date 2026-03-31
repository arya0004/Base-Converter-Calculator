.386
.model flat, stdcall
option casemap:none

include windows.inc
include user32.inc
include kernel32.inc
include gdi32.inc
include conversions.inc
include calculator.inc

includelib user32.lib
includelib kernel32.lib
includelib gdi32.lib

.data
    ; Window class name
    szClassName db "BaseConverterClass",0
    szWindowTitle db "Base Converter & Calculator",0
    
    ; Input fields
    hwndInputEdit dd ?
    hwndOutputEdit dd ?
    
    ; Radio buttons for base selection
    hwndDecRadio dd ?
    hwndBinRadio dd ?
    hwndHexRadio dd ?
    hwndOctRadio dd ?
    
    ; Calculator buttons
    hwndButtons dd 16 dup(?) ; Array to store button handles
    
    ; Conversion buffer
    szBuffer db 32 dup(0)
    szResult db 32 dup(0)
    
    ; Error messages
    szErrorInvalid db "Invalid input!",0
    szErrorOverflow db "Number too large!",0
    
    ; Current base selection
    currentBase dd BASE_DECIMAL
    
    ; Calculator state
    firstNumber dd 0
    secondNumber dd 0
    currentOperation dd OP_ADD
    isFirstNumber dd 1

.code
start:
    ; Register window class
    invoke GetModuleHandle, NULL
    mov hInstance, eax
    
    ; Create and show window
    invoke WinMain, hInstance, NULL, NULL, SW_SHOWDEFAULT
    
    ; Exit program
    invoke ExitProcess, eax

WinMain proc hInst:HINSTANCE, hPrevInst:HINSTANCE, CmdLine:LPSTR, CmdShow:DWORD
    LOCAL wc:WNDCLASSEX
    LOCAL msg:MSG
    LOCAL hwnd:HWND
    
    ; Initialize window class
    mov wc.cbSize, sizeof WNDCLASSEX
    mov wc.style, CS_HREDRAW or CS_VREDRAW
    mov wc.lpfnWndProc, offset WndProc
    mov wc.cbClsExtra, NULL
    mov wc.cbWndExtra, NULL
    mov eax, hInst
    mov wc.hInstance, eax
    mov wc.hbrBackground, COLOR_BTNFACE+1
    mov wc.lpszMenuName, NULL
    mov wc.lpszClassName, offset szClassName
    invoke LoadIcon, NULL, IDI_APPLICATION
    mov wc.hIcon, eax
    mov wc.hIconSm, eax
    invoke LoadCursor, NULL, IDC_ARROW
    mov wc.hCursor, eax
    
    ; Register window class
    invoke RegisterClassEx, addr wc
    
    ; Create window
    invoke CreateWindowEx, NULL, addr szClassName, addr szWindowTitle, \
        WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 400, 500, \
        NULL, NULL, hInst, NULL
    mov hwnd, eax
    
    ; Show window
    invoke ShowWindow, hwnd, CmdShow
    invoke UpdateWindow, hwnd
    
    ; Message loop
    .while TRUE
        invoke GetMessage, addr msg, NULL, 0, 0
        .break .if (!eax)
        invoke TranslateMessage, addr msg
        invoke DispatchMessage, addr msg
    .endw
    
    mov eax, msg.wParam
    ret
WinMain endp

; Helper function to perform conversion
PerformConversion proc
    pushad
    
    ; Get input text
    invoke GetWindowText, hwndInputEdit, addr szBuffer, sizeof szBuffer
    
    ; Convert input to number
    mov esi, offset szBuffer
    mov ebx, currentBase
    call StringToNumber
    jc @F
    
    ; Convert number to all other bases
    mov edi, offset szResult
    
    ; Binary
    mov ecx, BASE_BINARY
    call ConvertBase
    invoke SetWindowText, hwndOutputEdit, addr szResult
    
    ; Decimal
    mov ecx, BASE_DECIMAL
    call ConvertBase
    invoke SetWindowText, hwndOutputEdit, addr szResult
    
    ; Hexadecimal
    mov ecx, BASE_HEX
    call ConvertBase
    invoke SetWindowText, hwndOutputEdit, addr szResult
    
    ; Octal
    mov ecx, BASE_OCTAL
    call ConvertBase
    invoke SetWindowText, hwndOutputEdit, addr szResult
    
    clc
    jmp @F
    
@@:
    stc
    popad
    ret
PerformConversion endp

WndProc proc hwnd:HWND, uMsg:UINT, wParam:WPARAM, lParam:LPARAM
    .if uMsg == WM_CREATE
        ; Create input and output edit controls
        invoke CreateWindowEx, WS_EX_CLIENTEDGE, "EDIT", NULL, \
            WS_CHILD or WS_VISIBLE or ES_AUTOHSCROLL, \
            10, 10, 360, 25, hwnd, 100, hInstance, NULL
        mov hwndInputEdit, eax
        
        invoke CreateWindowEx, WS_EX_CLIENTEDGE, "EDIT", NULL, \
            WS_CHILD or WS_VISIBLE or ES_READONLY, \
            10, 45, 360, 25, hwnd, 101, hInstance, NULL
        mov hwndOutputEdit, eax
        
        ; Create radio buttons for base selection
        invoke CreateWindowEx, NULL, "BUTTON", "Decimal", \
            WS_CHILD or WS_VISIBLE or BS_RADIOBUTTON, \
            10, 80, 80, 25, hwnd, 200, hInstance, NULL
        mov hwndDecRadio, eax
        
        invoke CreateWindowEx, NULL, "BUTTON", "Binary", \
            WS_CHILD or WS_VISIBLE or BS_RADIOBUTTON, \
            100, 80, 80, 25, hwnd, 201, hInstance, NULL
        mov hwndBinRadio, eax
        
        invoke CreateWindowEx, NULL, "BUTTON", "Hexadecimal", \
            WS_CHILD or WS_VISIBLE or BS_RADIOBUTTON, \
            190, 80, 100, 25, hwnd, 202, hInstance, NULL
        mov hwndHexRadio, eax
        
        invoke CreateWindowEx, NULL, "BUTTON", "Octal", \
            WS_CHILD or WS_VISIBLE or BS_RADIOBUTTON, \
            300, 80, 80, 25, hwnd, 203, hInstance, NULL
        mov hwndOctRadio, eax
        
        ; Set default selection
        invoke SendMessage, hwndDecRadio, BM_SETCHECK, BST_CHECKED, 0
        
        ; Create calculator buttons
        mov ecx, 0
        .while ecx < 16
            mov eax, ecx
            .if eax < 10
                add al, '0'
            .else
                add al, 'A' - 10
            .endif
            mov byte ptr [szBuffer], al
            mov byte ptr [szBuffer+1], 0
            
            ; Calculate button position
            mov eax, ecx
            mov edx, 0
            mov ebx, 4
            div ebx
            
            ; x = (ecx % 4) * 80 + 10
            mov eax, edx
            imul eax, 80
            add eax, 10
            
            ; y = (ecx / 4) * 40 + 120
            mov edx, ecx
            shr edx, 2
            imul edx, 40
            add edx, 120
            
            invoke CreateWindowEx, NULL, "BUTTON", addr szBuffer, \
                WS_CHILD or WS_VISIBLE or BS_PUSHBUTTON, \
                eax, edx, 70, 30, hwnd, 300+ecx, hInstance, NULL
            mov [hwndButtons+ecx*4], eax
            
            inc ecx
        .endw
        
    .elseif uMsg == WM_COMMAND
        mov eax, wParam
        .if ax == 100 ; Input edit control
            call PerformConversion
        .elseif ax >= 200 && ax < 204 ; Radio buttons
            .if ax == 200
                mov currentBase, BASE_DECIMAL
            .elseif ax == 201
                mov currentBase, BASE_BINARY
            .elseif ax == 202
                mov currentBase, BASE_HEX
            .elseif ax == 203
                mov currentBase, BASE_OCTAL
            .endif
            call PerformConversion
        .elseif ax >= 300 && ax < 316 ; Calculator buttons
            mov ecx, eax
            sub ecx, 300
            
            .if isFirstNumber
                mov eax, firstNumber
                imul eax, currentBase
                add eax, ecx
                mov firstNumber, eax
            .else
                mov eax, secondNumber
                imul eax, currentBase
                add eax, ecx
                mov secondNumber, eax
            .endif
            
            ; Update display
            mov eax, firstNumber
            mov ebx, currentBase
            mov edi, offset szBuffer
            call NumberToString
            invoke SetWindowText, hwndInputEdit, addr szBuffer
        .endif
        
    .elseif uMsg == WM_DESTROY
        invoke PostQuitMessage, NULL
    .else
        invoke DefWindowProc, hwnd, uMsg, wParam, lParam
        ret
    .endif
    
    xor eax, eax
    ret
WndProc endp

end start 