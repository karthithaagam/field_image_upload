import os
import shutil
import tempfile
import zipfile
from tkinter import Tk, Label, Button, filedialog, messagebox, Canvas
from datetime import datetime

# Local directory to store media files
LOCAL_STORAGE_DIRECTORY = "C:/Users/Thaagam_pc_07/Downloads/local store"

def extract_zip(zip_file_path, temp_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

def copy_media_locally(temp_dir, zip_file_name):
    try:
        # Display "Checking path" message
        status_label.config(text="Checking path...")
        status_label.update()

        # Start processing animation
        progress_canvas.delete("progress_bar")
        progress_bar = progress_canvas.create_rectangle(10, 10, 10, 30, fill="green", width=0, outline='black',tags="progress_bar")
        for i in range(0, 610, 10):  # Making it larger
            progress_canvas.coords(progress_bar, 10, 10, 10 + i, 30)
            progress_canvas.update()
            progress_canvas.after(50)  # Smoother animation

        media_files_found = False
        total_files = sum(len(files) for _, _, files in os.walk(temp_dir))
        uploaded_files = 0

        for root_folder, _, files in os.walk(temp_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4', '.avi', '.mkv', '.mov')):
                    media_files_found = True
                    media_source_path = os.path.join(root_folder, file)
                    relative_path = os.path.relpath(media_source_path, temp_dir)
                    media_destination_path = os.path.join(LOCAL_STORAGE_DIRECTORY, zip_file_name, relative_path)
                    os.makedirs(os.path.dirname(media_destination_path), exist_ok=True)
                    # Copy media file from source path to destination path
                    shutil.copy(media_source_path, media_destination_path)

                    # Update progress bar and status label
                    uploaded_files += 1
                    progress_value = uploaded_files / total_files * 100
                    progress_canvas.coords(progress_bar, 10, 10, 10 + progress_value * 6, 30)
                    progress_canvas.update()
                    status_label.config(text=f"Uploading... {int(progress_value)}%")
                    status_label.update()

        # End processing animation
        progress_canvas.delete("progress_bar")
        status_label.config(text="Media files uploaded successfully")
    except Exception as e:
        # End processing animation on error
        progress_canvas.delete("progress_bar")
        status_label.config(text="Error occurred during upload")
        messagebox.showerror("Error", f"An error occurred: {e}")

def handle_zip_selection():
    zip_file_path = filedialog.askopenfilename(title="Select Zip File", filetypes=(("Zip files", "*.zip"), ("All files", "*.*")))
    if zip_file_path:
        try:
            temp_dir = tempfile.mkdtemp()

            # Display "Extracting" message
            status_label.config(text="Extracting...")
            status_label.update()

            extract_zip(zip_file_path, temp_dir)

            # Check for media files and upload if found
            zip_file_name = os.path.splitext(os.path.basename(zip_file_path))[0]
            copy_media_locally(temp_dir, zip_file_name)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

# Create Tkinter window
root = Tk()
root.title("Field Media Uploader")
root.configure(background="black")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size and position
window_width = 480
window_height = 320
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create and pack widgets
status_label = Label(root, text="Field Media Uploader", font=("Arial", 12), bg="black", fg="white")
status_label.place(relx=0.5, rely=00.150, anchor="center")

select_button = Button(root, text="Select Zip File", command=handle_zip_selection, bg="green", fg="white", width=20, height=2, font=("Arial", 12), bd=0, highlightthickness=0, relief="flat")
select_button.place(relx=0.5, rely=0.3, anchor="center")

# Create Label for the status
status_label = Label(root, text="", font=("Arial", 12), bg="black", fg="white")
status_label.place(relx=0.5, rely=0.5, anchor="center")
# Create Canvas with smaller size and black border
progress_canvas = Canvas(root, width=420, height=40, bg="black", highlightbackground="black")
progress_canvas.place(relx=0.5, rely=0.7, anchor="center")


# Run the Tkinter event loop
root.mainloop()