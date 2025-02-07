#include <windows.h>
#include <shellapi.h>

#define ID_EDIT 1
#define ID_COMPILE 2
#define ID_CLOSE 3

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch(msg) {
        case WM_CREATE: {
            CreateWindowW(L"STATIC", L"Bienvenido a Intelli-P", 
                         WS_VISIBLE | WS_CHILD,
                         10, 10, 300, 20, hwnd, NULL, NULL, NULL);
                         
            CreateWindowW(L"BUTTON", L"Editar codigo", 
                         WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
                         10, 40, 120, 30, hwnd, (HMENU)ID_EDIT, NULL, NULL);
                         
            CreateWindowW(L"BUTTON", L"Compilar codigo", 
                         WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
                         140, 40, 120, 30, hwnd, (HMENU)ID_COMPILE, NULL, NULL);
                         
            CreateWindowW(L"BUTTON", L"Cerrar", 
                         WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
                         270, 40, 120, 30, hwnd, (HMENU)ID_CLOSE, NULL, NULL);
            break;
        }
        
        case WM_COMMAND: {
            switch(LOWORD(wParam)) {
                case ID_EDIT:
                    ShellExecuteA(NULL, "open", "notepad.exe", 
                                 "main_program.ipce", NULL, SW_SHOW);
                    break;
                case ID_COMPILE:
                    ShellExecuteA(NULL, "open", "compile.bat", 
                                 NULL, NULL, SW_SHOW);
                    break;
                case ID_CLOSE:
                    DestroyWindow(hwnd);
                    break;
            }
            break;
        }
        
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
            
        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
                   LPSTR lpCmdLine, int nCmdShow) {
    WNDCLASSW wc = {0};
    wc.lpszClassName = L"IntelliPWindowClass";
    wc.hInstance = hInstance;
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW);
    wc.lpfnWndProc = WndProc;
    wc.hCursor = LoadCursor(0, IDC_ARROW);

    RegisterClassW(&wc);
    
    HWND hwnd = CreateWindowW(wc.lpszClassName, L"Intelli-P",
                              WS_OVERLAPPEDWINDOW | WS_VISIBLE,
                              100, 100, 400, 120, NULL, NULL, hInstance, NULL);

    MSG msg;
    while(GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    
    return (int)msg.wParam;
}