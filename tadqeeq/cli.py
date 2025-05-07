""" 
Tadqeeq - Image Annotator Tool
An interactive image annotation tool for efficient labeling.
Developed by Mohamed Behery @ RTR Software Development (2025-04-27).
Licensed under the MIT License.
"""

from PyQt5.QtWidgets import QApplication
import sys
from .implementations import MainWindow

def main():
    if len(sys.argv) != 3:
        print("Usage: tadqeeq <images_directory_path> <annotations_directory_path>")
        sys.exit(1)
    app = QApplication(sys.argv)
    window = MainWindow(
        images_directory_path=sys.argv[1],
        annotations_directory_path=sys.argv[2]
    )
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()