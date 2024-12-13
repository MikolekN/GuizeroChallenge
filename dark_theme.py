def dark_theme_element(elem):
    try:
        elem.tk.config(background='#2d2d2d')
    except:
        print(f"The element \"{elem}\" doesn't have a background parameter.")

    try:
        elem.tk.config(foreground='white')
    except:
        print(f"The element \"{elem}\" doesn't have a foreground parameter.")

    try:
        elem.tk.config(activebackground='#2d2d2d')
    except:
        print(f"The element \"{elem}\" doesn't have a activebackground parameter.")

    try:
        elem.tk.config(activeforeground='white')
    except:
        print(f"The element \"{elem}\" doesn't have a activeforeground parameter.")


def apply(elems):
    for elem in elems:
        dark_theme_element(elem)