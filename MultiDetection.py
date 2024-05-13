# import os
# import cv2
# import pandas as pd
# from deepface import DeepFace
# from retinaface import RetinaFace

# folder_path = "./final/student"
# test_image_path = "./test8.png"
# verified_subfolders = set()


# def verify_image(test_image, image_path):
#     try:
#         if not os.path.exists(test_image_path):
#             print(f"Error: Test image {test_image_path} does not exist.")
#             return
#         if not os.path.exists(image_path):
#             print(f"Error: Image {image_path} does not exist.")
#             return

#         # Load images using cv2.imread (assuming these are color images)
#         test_image = cv2.imread(test_image_path)
#         image_to_verify = cv2.imread(image_path)

#         result = DeepFace.verify(img1_path=test_image,
#                                  img2_path=image_to_verify)
#         return result

#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return None


# # Load the test image
# test_image = cv2.imread(test_image_path)
# if test_image is None:
#     print(f"Error: Failed to open test image {test_image_path}.")
#     exit()

# # Detect faces using RetinaFace
# faces = RetinaFace.extract_faces(test_image)
# # Check if faces were detected
# if not faces:
#     print("No faces detected in the test image.")
#     exit()

# for subfolder in os.listdir(folder_path):
#     subfolder_path = os.path.join(folder_path, subfolder)

#     for image_file in os.listdir(subfolder_path):
#         if image_file.lower().endswith((".jpg", ".png", ".jpeg")):
#             image_path = os.path.join(subfolder_path, image_file)

#             # Verify each detected face against the current image
#             for face in faces:
#                 # Handle RetinaFace output if it's bounding box data (adjust based on library)
#                 if isinstance(face, list):
#                     # Assuming face is a list containing bounding box coordinates (x1, y1, x2, y2)
#                     x1, y1, x2, y2 = face  # Extract coordinates
#                     # Extract face region using ROI
#                     face_image = test_image[y1:y2, x1:x2]
#                 else:
#                     face_image = face

#                 result = verify_image(face_image, image_path)

#                 if result is not None and result["verified"]:
#                     if subfolder not in verified_subfolders:
#                         print(f"Verification successful for subfolder: {
#                             subfolder}")
#                         verified_subfolders.add(subfolder)
#                     break

# df = pd.DataFrame(list(verified_subfolders), columns=["studentNums"])

# excel_file_path = "./studentsNums.xlsx"
# df.to_excel(excel_file_path, index=True)

# print(f"Verified subfolders saved to {excel_file_path}.")


import os
import cv2
import pandas as pd
from deepface import DeepFace
from retinaface import RetinaFace
import tkinter as tk
from tkinter import filedialog, messagebox

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

    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        for image_file in os.listdir(subfolder_path):
            if image_file.lower().endswith((".jpg", ".png", ".jpeg")):
                image_path = os.path.join(subfolder_path, image_file)

                if cv2.imread(image_path) is not None:
                    result = verify_image(test_image_path, image_path)

                    if result is not None and result["verified"]:
                        if subfolder not in verified_subfolders:
                            print(f"Verification successful for subfolder: {subfolder}")
                            verified_subfolders.add(subfolder)
                        break

    df = pd.DataFrame(list(verified_subfolders), columns=["studentNums"])
    excel_file_path = "./studentsNums.xlsx"
    df.to_excel(excel_file_path, index=True)

    print(f"Verified subfolders saved to {excel_file_path}.")

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
