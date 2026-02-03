// terminal code to run: g++ main.cpp -o main -mwindows -municode ; .\main.exe

#ifndef UNICODE
#define UNICODE
#endif 

#include <windows.h>

// Unique IDs for our UI elements
#define ID_BUTTON 101
#define ID_EDITBOX 102

// Global handles so different functions can access the UI elements
HWND hEdit;
HBRUSH hDarkBrush; // The "paint" we will use for the background

// The Window Procedure: This is the "brain" that handles every event (clicks, typing, closing)
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PWSTR pCmdLine, int nCmdShow) {
    
    // 1. REGISTER THE WINDOW CLASS
    // Think of this as the "blueprint" for your window.
    const wchar_t CLASS_NAME[] = L"DarkWindowApp";
    
    WNDCLASS wc = { };
    wc.lpfnWndProc   = WindowProc;      // Pointing to our "brain" function
    wc.hInstance     = hInstance;       // Reference to this running app instance
    wc.lpszClassName = CLASS_NAME;      // Name of this blueprint
    wc.hCursor       = LoadCursor(NULL, IDC_ARROW); // Standard mouse pointer

    RegisterClass(&wc);

    // 2. CREATE THE "DARK MODE" BRUSH
    // We create a solid color (Dark Gray) to use for the background.
    hDarkBrush = CreateSolidBrush(RGB(45, 45, 45));

    // 3. CREATE THE MAIN WINDOW
    HWND hwnd = CreateWindowEx(
        0, CLASS_NAME, L"Win32 Dark Mode Example", 
        WS_OVERLAPPEDWINDOW,            // Standard title bar, close, minimize
        CW_USEDEFAULT, CW_USEDEFAULT,   // Default position
        450, 300,                       // Width, Height
        NULL, NULL, hInstance, NULL
    );

    if (hwnd == NULL) return 0;

    // 4. CREATE CHILD CONTROLS
    // Static text (The label)
    CreateWindow(L"STATIC", L"Enter something dark:", 
        WS_VISIBLE | WS_CHILD, 
        30, 30, 200, 20, hwnd, NULL, hInstance, NULL);

    // The Edit box (Input)
    hEdit = CreateWindow(L"EDIT", L"", 
        WS_VISIBLE | WS_CHILD | WS_BORDER | ES_AUTOHSCROLL, 
        30, 55, 250, 25, hwnd, (HMENU)ID_EDITBOX, hInstance, NULL);

    // The Button
    CreateWindow(L"BUTTON", L"Submit", 
        WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON, 
        30, 95, 100, 35, hwnd, (HMENU)ID_BUTTON, hInstance, NULL);

    ShowWindow(hwnd, nCmdShow);

    // 5. THE MESSAGE LOOP
    // This keeps the program alive, waiting for user input.
    MSG msg = { };
    while (GetMessage(&msg, NULL, 0, 0) > 0) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    // Cleanup the brush memory before exiting
    DeleteObject(hDarkBrush);
    return 0;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        
        // Handle Button Clicks
        case WM_COMMAND: {
            if (LOWORD(wParam) == ID_BUTTON) {
                wchar_t buffer[256];
                GetWindowText(hEdit, buffer, 256);
                MessageBox(hwnd, buffer, L"Input Received", MB_OK);
            }
        }
        return 0;

        // DARK MODE LOGIC: Before an Edit box draws itself, it sends this message.
        case WM_CTLCOLOREDIT: 
        case WM_CTLCOLORSTATIC: {
            HDC hdcStatic = (HDC)wParam;
            SetTextColor(hdcStatic, RGB(255, 255, 255)); // White text
            SetBkColor(hdcStatic, RGB(45, 45, 45));      // Match background color
            return (INT_PTR)hDarkBrush;                  // Return the dark brush to paint the box
        }

        // Draw the background of the MAIN window
        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            FillRect(hdc, &ps.rcPaint, hDarkBrush); // Paint the main background dark
            EndPaint(hwnd, &ps);
        }
        return 0;

        // Clean exit
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
    }
    // Let Windows handle any messages we didn't care about
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}