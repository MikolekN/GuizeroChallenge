def center_window(window, window_width, window_height, icon=None):
    window.tk.resizable(False, False)
    if icon is not None:
        try:
            window.tk.iconbitmap(icon)
        except:
            print("Wrong icon file selected.")
    screen_width = window.tk.winfo_screenwidth()
    screen_height = window.tk.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    window.tk.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    window.tk.resizable(0, 0)
