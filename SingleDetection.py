import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import cv2
from deepface import DeepFace
from retinaface import RetinaFace


def verify_image(test_image_path, image_to_verify_path):
    try:
        result = DeepFace.verify(
            img1_path=test_image_path, img2_path=image_to_verify_path)
        return result
    except Exception as e:
        print(f"Error occurred while verifying images: {e}")
        return None


def main(test_image_path, folder_path):
    verified_subfolders = set()

    test_image = cv2.imread(test_image_path)
    if test_image is None:
        print(f"Error: Failed to open test image {test_image_path}. Check the path.")
        return

    faces = RetinaFace.extract_faces(test_image)
    if not faces:
        print("No faces detected in the test image.")
        return

    for face_index, face in enumerate(faces):
        closest_similarity = float('inf')
        closest_person = None

        for subfolder in os.listdir(folder_path):
            subfolder_path = os.path.join(folder_path, subfolder)

            for image_file in os.listdir(subfolder_path):
                if image_file.lower().endswith((".jpg", ".png", ".jpeg")):
                    image_path = os.path.join(subfolder_path, image_file)

                    if cv2.imread(image_path) is not None:
                        result = verify_image(test_image_path, image_path)

                        if result is not None and result["distance"] < closest_similarity:
                            closest_similarity = result["distance"]
                            closest_person = subfolder

        if closest_person is not None and closest_person not in verified_subfolders:
            print(f"Closest match for detected face {face_index + 1}: {closest_person}")
            verified_subfolders.add(closest_person)
            closest_similarity = 0

    df = pd.DataFrame(list(verified_subfolders), columns=["Subfolder"])
    excel_file_path = "./subfolders.xlsx"
    df.to_excel(excel_file_path, index=True)

    print("Face verification completed.")
    print("Subfolders saved to Excel file.")


def browse_test_image():
    filename = filedialog.askopenfilename()
    test_image_var.set(filename)


def browse_folder():
    foldername = filedialog.askdirectory()
    folder_path_var.set(foldername)


def verify_images():
    test_image_path = test_image_var.get()
    folder_path = folder_path_var.get()

    if not os.path.exists(test_image_path):
        messagebox.showerror("Error", f"Test image {test_image_path} does not exist.")
        return
    if not os.path.exists(folder_path):
        messagebox.showerror("Error", f"Folder {folder_path} does not exist.")
        return

    main(test_image_path, folder_path)


root = tk.Tk()
root.title("Students Attendance ")

test_image_label = tk.Label(root, text="Student Image:")
test_image_label.grid(row=0, column=0)

test_image_var = tk.StringVar()
test_image_entry = tk.Entry(root, textvariable=test_image_var, width=50)
test_image_entry.grid(row=0, column=1)

test_image_browse_button = tk.Button(root, text="Browse", command=browse_test_image)
test_image_browse_button.grid(row=0, column=2)

folder_label = tk.Label(root, text="Folder:")
folder_label.grid(row=1, column=0)

folder_path_var = tk.StringVar()
folder_path_entry = tk.Entry(root, textvariable=folder_path_var, width=50)
folder_path_entry.grid(row=1, column=1)

folder_browse_button = tk.Button(root, text="Browse", command=browse_folder)
folder_browse_button.grid(row=1, column=2)

verify_button = tk.Button(root, text="Verify Images", command=verify_images)
verify_button.grid(row=2, column=1)

root.mainloop()
