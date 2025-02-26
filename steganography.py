import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# Function to encode text into an image
def encode_image():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if not file_path:
        return

    image = Image.open(file_path)
    message = text_entry.get("1.0", tk.END).strip()

    if not message:
        messagebox.showerror("Error", "Please enter a message to encode!")
        return

    # Append a delimiter to mark the end of the message
    message += "####"

    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    pixels = list(image.getdata())

    if len(binary_message) > len(pixels) * 3:
        messagebox.showerror("Error", "Message is too long for this image!")
        return

    new_pixels = []
    binary_index = 0

    for pixel in pixels:
        new_pixel = list(pixel[:3])  # Extract RGB
        for i in range(3):
            if binary_index < len(binary_message):
                new_pixel[i] = new_pixel[i] & ~1 | int(binary_message[binary_index])
                binary_index += 1
        new_pixels.append(tuple(new_pixel))

    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)

    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png")])
    if save_path:
        new_image.save(save_path)
        messagebox.showinfo("Success", "Message encoded and image saved!")

# Function to decode hidden text from an image
def decode_image():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if not file_path:
        return

    image = Image.open(file_path)
    pixels = list(image.getdata())

    binary_message = ""
    for pixel in pixels:
        for i in range(3):
            binary_message += str(pixel[i] & 1)

    # Convert binary to string
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ''.join(chr(int(c, 2)) for c in chars)

    # Extract message before delimiter
    hidden_message = message.split("####")[0]

    if hidden_message:
        text_entry.delete("1.0", tk.END)
        text_entry.insert("1.0", hidden_message)
        messagebox.showinfo("Decoded Message", hidden_message)
    else:
        messagebox.showerror("Error", "No hidden message found!")

# GUI Setup
root = tk.Tk()
root.title("Image Steganography")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=20)

text_entry = tk.Text(frame, height=5, width=40)
text_entry.pack()

encode_button = tk.Button(frame, text="Encode Message", command=encode_image)
encode_button.pack(pady=5)

decode_button = tk.Button(frame, text="Decode Message", command=decode_image)
decode_button.pack(pady=5)

root.mainloop()
