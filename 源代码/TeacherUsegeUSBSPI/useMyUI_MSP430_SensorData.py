from  useMyUi import *
import sys

if __name__=="__main__":
    app = QApplication(sys.argv)
    ui = UI(FLAG_Chip_MSP)
    ui.show()
    sys.exit(app.exec_())




