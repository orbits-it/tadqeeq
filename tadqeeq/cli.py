""" 
Tadqeeq - Image Annotator Tool
An interactive image annotation tool for efficient labeling.
Developed by Mohamed Behery @ RTR Software Development (2025-04-27).
Licensed under the MIT License.
"""

from PyQt5.QtWidgets import QApplication
import sys
import os
from .implementations import ImageAnnotatorWindow

root_directory_path = '/home/mohamed/Projects/segmentation_annotation_tool'
images_directory_path, annotations_directory_path = f'{root_directory_path}/images', f'{root_directory_path}/annotations'

def main():
    
    if len(sys.argv) < 3:
        print("Usage: tadqeeq [--enable_logging|--autosave|--use_bounding_boxes]* <images_directory_path> <annotations_directory_path> <class_names_path>")
        sys.exit(1)
    
    images_directory_path, annotations_directory_path = sys.argv[-3:-1]
    if not os.path.isdir(images_directory_path):
        print(f'Error: The directory "{images_directory_path}" does not exist.')
        sys.exit(2)
        
    class_names_filepath = sys.argv[-1]
    if not os.path.isfile(class_names_filepath):
        print(f'Error: The file "{class_names_filepath}" does not exist.')
        sys.exit(3)
    
    with open(class_names_filepath) as file:
        class_names = [line.strip() for line in file.readlines() if line.strip()]
    
    app = QApplication(sys.argv)
    window = ImageAnnotatorWindow(
        images_directory_path, annotations_directory_path,
        label_color_pairs=class_names,
        use_bounding_boxes='--use_bounding_boxes' in sys.argv,
        autosave='--autosave' in sys.argv,
        verbose='--verbose' in sys.argv
    )
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()