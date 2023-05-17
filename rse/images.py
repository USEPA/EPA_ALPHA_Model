import tkinter as tk
from PIL import Image, ImageTk

def resize_image(image, max_width, max_height):
    width, height = image.size
    aspect_ratio = width / height

    if width > max_width or height > max_height:
        if width > height:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)

        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        return resized_image
    else:
        return image

def create_image_window(image_files, grid_columns, max_width, max_height):
    window = tk.Tk()
    window.title("Image Viewer")

    total_images = len(image_files)
    grid_rows = (total_images + grid_columns - 1) // grid_columns

    for i, file in enumerate(image_files):
        image = Image.open(file)
        resized_image = resize_image(image, max_width, max_height)
        photo = ImageTk.PhotoImage(resized_image)
        label = tk.Label(window, image=photo)
        label.image = photo  # Keep a reference to the image to prevent garbage collection
        label.grid(row=i // grid_columns, column=i % grid_columns, padx=10, pady=10)

    window.mainloop()

# Example usage
image_files = ["plot0.png", "plot1.png", "plot2.png", "plot3.png", "plot4.png", "plot5.png", "plot6.png", "plot7.png"]
grid_columns = 4
max_width = 300
max_height = 300
create_image_window(image_files, grid_columns, max_width, max_height)

