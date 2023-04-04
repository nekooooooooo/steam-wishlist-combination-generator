from utils.ui import WishlistGeneratorUI

def main():
    app = WishlistGeneratorUI()
    # set the window size
    width = app._current_width
    height = app._current_height
    x = (app.winfo_screenwidth() // 2) - (width // 2)  # calculate the x coordinate for the window
    y = (app.winfo_screenheight() // 2) - (height // 2)  # calculate the y coordinate for the window

    # set the window position
    app.geometry(f"{width}x{height}+{x}+{y}")
    app.mainloop()
    

if __name__ == "__main__":
    # start_time = time.time()
    main()
    # print("%s seconds" % (time.time() - start_time))
