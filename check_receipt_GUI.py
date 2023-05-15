import sys

sys.path.append('C:\\Users\\water\\Python') # 新しいパスを追加

from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QDateEdit, QLabel, QLineEdit, QWidget, QMainWindow, QAction, QFileDialog,
    QApplication, QTextEdit, QGridLayout, QGraphicsView, QGraphicsScene,
    QScrollArea, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QComboBox,
    QPushButton, QSizePolicy
)
from PyQt5.QtGui import QIcon, QIntValidator, QImage, QPixmap
from PyQt5.QtCore import QDate
from traning_receipt import make_Receipt_Text
from spacy_test import take_price
from browser_operation import browser_operate


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # Image_area
        self.image_area = Image_area()

        # 複数行のテキストを表示するウィジェットを作成し、レイアウトに追加
        self.text_area = text_area()

        # 複数行にわたって複数の入力欄を持つウィジェットを作成し、レイアウトに追加
        self.input_area = Input_area()
        
        # menubar
        self.menubar = self.menuBar()
        self.filemenu = self.menubar.addMenu('File')
        self.openAction()   # アクションの追加
        self.closeAction()   # アクションの追加

        # 右側のレイアウトを作成。マージンの変更
        sub_layout = QVBoxLayout()
        sub_layout.addWidget(self.text_area)
        sub_layout.addWidget(self.input_area)
        sub_widget = QWidget()
        sub_widget.setLayout(sub_layout)

        sub_layout.setContentsMargins(0, 2, 2, 2)
        sub_layout.setSpacing(0)

        # 左右のレイアウトを一つにまとめる、マージン、スペースの変更
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.image_area)
        main_layout.addWidget(sub_widget)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(0)

        # ウィンドウのサイズと表示位置
        # setGeometry(x, y, w, h) x: x位置, y: y位置, w: 幅, h: 高さ
        self.setGeometry(100, 400, 800, 800)
        self.setWindowTitle('Basic Window Example')

        # ウィジェットの表示
        self.show()

    def openAction(self):
        # アクションの作成
        self.open_act = QAction('開く')
        self.open_act.setShortcut('Ctrl+O') # shortcut
        self.open_act.triggered.connect(self.openFile) # open_actとメソッドを紐づける

        # メニューにアクションを割り当てる
        self.filemenu.addAction(self.open_act)

    #「開く」メニュー。画像を指定、OCR実施、画面の更新
    def openFile(self):
        filepath = QFileDialog.getOpenFileName(self, 'open file', '', 'Images (*.jpeg *.jpg *.png *.bmp)')[0]

        if filepath:
            # OCRの実施。結果を表示。
            text = make_Receipt_Text().make_Text(filepath)

            # OCR結果を[品目][金額]のみ抽出。画像の表示を変更。
            self.image_area.setImage(filepath)
            self.text_area.setPlaneText(text)
            self.input_area.remake_input_area(text)

    def closeAction(self):
        # アクションの作成
        self.close_act = QAction('終了')
        self.close_act.setShortcut('Ctrl+E') # shortcut
        self.close_act.triggered.connect(self.closeWindow) # open_actとメソッドを紐づける

        # メニューにアクションを割り当てる
        self.filemenu.addAction(self.close_act)

    def closeWindow(self):
        # ブラウザーの終了
        self.input_area.closeBrowser_operater()
        self.close()


class Image_area(QWidget):
    def __init__(self):
        super(Image_area, self).__init__()

        # 画像を表示するためのviewをレイアウトにセット
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.view.setScene(self.scene)  
        self.image_area_layout = QGridLayout()
        self.image_area_layout.addWidget(self.view)
        self.setFixedSize(400, 800)

        # image_area_layoutをQWidget(self)にセット
        self.setLayout(self.image_area_layout)

    def setImage(self, filepath):
        # 画像ファイルの読み込み
        img = QImage()
        if not img.load(filepath): return False
        
        # ウィンドウサイズを取得、サイズに合わせて縮小する
        Image_area_Size = self.size()
        scaledImage = img.scaled(Image_area_Size)

        # QImage -> QPixmap
        self.pixmap = QPixmap.fromImage(scaledImage)

        # pixmapをsceneに追加
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)

        # ウィジェットを更新
        self.update()
    
class text_area(QWidget):
    def __init__(self):
        super(text_area, self).__init__()

        # 複数行のテキストを表示するウィジェットを作成し、レイアウトに追加
        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlainText('')
        self.text_edit.setFixedSize(400, 300)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.text_edit)
        self.text_layout = QVBoxLayout()
        self.text_layout.addWidget(self.scroll_area)

        # text_layoutをQWidget(self)にセット
        self.setLayout(self.text_layout)
        self.setFixedSize(400, 300)
        
    
    def setPlaneText(self, text):
        self.text_edit.setPlainText(text)
        # 文書の行数を取得
        line_count = self.text_edit.document().blockCount()

        # フォントメトリックスから行の高さを計算
        font_metrics = self.text_edit.fontMetrics()
        line_height = font_metrics.lineSpacing()+1 #行数ちょうど１の時、画面に表示しきれず、スクロールバーが出るため

        # QPlainTextEdit のマージンを取得
        margins = self.text_edit.contentsMargins()
        height = int(line_height * line_count + margins.top() + margins.bottom())

        # QPlainTextEdit の縦のサイズを更新
        self.text_edit.setFixedHeight(height)

    
class Input_area(QWidget):
    def __init__(self):
        super(Input_area, self).__init__()
        
        # ブラウザの起動、入力
        self.browser_operater = None

        self.dropdown2_value = {\
                        "交際費": ["交際費"],\
                        "dn2": ["dn21", "dn22"],\
                        "dn3": ["dn31", "dn32", "dn33"],\
                        "dn4": ["dn41", "dn42", "dn43", "dn44"],\
                        "dn5": ["dn51", "dn52", "dn53", "dn54", "dn55"]\
                        }
        
        self.purse_dropdown_value = ["エクストレイル 代金","P2","P3","P4","P5"]

        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.scroll_area2 = QScrollArea()
        self.scroll_area2.setWidget(self.widget)
        self.scroll_area2.setWidgetResizable(True) #これを入れるとなぜ入力欄が表示できるようになる？

        self.input_layout = QVBoxLayout()
        self.input_layout.addWidget(self.scroll_area2)
        self.setLayout(self.input_layout)
        self.setFixedSize(400, 500)

        # 日付、合計、支出元を配置する
        self.sum_layout = QHBoxLayout()

        # 日付欄
        self.date_area = QDateEdit()
        self.sum_layout.addWidget(self.date_area)

        # 合計欄
        self.sum_Text = QLabel()
        self.sum_Text.setText('合計')
        self.sum_input = QLineEdit()
        self.sum_input.setText('')
        self.sum_layout.addWidget(self.sum_Text)
        self.sum_layout.addWidget(self.sum_input)

        # 支出元
        self.purse_dropdown = QComboBox()
        self.purse_dropdown.addItems(self.purse_dropdown_value)
        self.sum_layout.addWidget(self.purse_dropdown)

        # 合計欄と出金元を配置
        self.sum_widget = QWidget()
        self.sum_widget.setLayout(self.sum_layout)
        self.input_layout.addWidget(self.sum_widget)
        self.sum_widget.hide()
        
        # データ取得を実行するボタンの配置
        self.button = QPushButton('ブラウザ入力', self)
        self.button.clicked.connect(lambda: self.get_data(self.layout)) # ボタンがクリックされたら、データを取得して表示
        self.input_layout.addWidget(self.button)
        self.button.hide()
        
    # 入力欄を作成する関数
    def remake_input_area(self, text):
        # OCR結果から金額が表示されている列を抽出
        item_list = take_price().extract_price_line(text)

        # 追加ボタン
        add_button = QPushButton("＋")
        add_button.clicked.connect(self.add_empty_row)
        self.layout.addWidget(add_button)

        # 金額が表示されている列を、それぞれ入力欄として変換・生成
        for item in item_list:
            self.add_row(item[0], item[1])
        
        # 余白部分
        self.layout.addStretch()
        
        # 日付、合計額、出金元、実行を表示
        self.button.show()
        self.sum_widget.show()
        self.change_sum(self.layout)
        self.date_area.setDate(QDate.currentDate())

    def add_row(self, item_name, item_price):
        hbox = QHBoxLayout()

        item_name_input = QLineEdit()
        item_name_input.setText(item_name)
        hbox.addWidget(item_name_input)

        item_price_input = QLineEdit()
        item_price_input.setText(item_price)
        item_price_input.setValidator(QIntValidator())
        item_price_input.textChanged.connect(lambda: self.change_sum(self.layout)) #値が変更されたらsumを変更する
        hbox.addWidget(item_price_input)

        dropdown1 = QComboBox()
        dropdown1.addItems(list(self.dropdown2_value.keys()))

        dropdown2 = QComboBox()
        dropdown2.addItems(self.dropdown2_value[dropdown1.currentText()])

        # コンボボックスの選択肢が変更されたら、２つ目のコンボボックスの選択肢を変更する
        dropdown1.currentIndexChanged.connect(lambda: self.notice_changed(dropdown2, dropdown1.currentText()))
        
        hbox.addWidget(dropdown1)
        hbox.addWidget(dropdown2)

        delete_button = QPushButton("×")
        delete_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        delete_button.clicked.connect(lambda: self.delete_row(hbox)) #削除はどうする？
        hbox.addWidget(delete_button)

        self.layout.addLayout(hbox)

    def add_empty_row(self):
        self.add_row("", "0")

    def delete_row(self, hbox):
        # レイアウトを削除
        while hbox.count():
            item = hbox.takeAt(0)
            widget = item.widget()
            if isinstance(widget, QComboBox):
                widget.deleteLater()
            elif widget:
                widget.deleteLater()

        hbox.deleteLater()
    
    # "データを取得"ボタンを押下すると、purse_resultに各項目の値をリストとして格納する
    def get_data(self, input_layout):
        value_result = []

        # 日付を取得
        date_string = self.date_area.date()
        date_value = date_string.toString("yyyy/M/d")

        # 支出元を取得
        purse_value = self.purse_dropdown.currentText()

        # input_layoutの要素をhboxに取得し、QHBoxLayoutであれば各入力欄の値を取得する
        for i in range(input_layout.count()):
            hbox = input_layout.itemAt(i)
            if isinstance(hbox, QHBoxLayout):
                buf = []

                # 日付を入力
                buf.append(date_value)

                # 品名、金額、大分類、中分類
                for j in range(hbox.count()):
                    widget = hbox.itemAt(j).widget()

                    # 値をreultに格納する
                    if isinstance(widget, QLineEdit):
                        buf.append(widget.text())
                    elif isinstance(widget, QComboBox):
                        buf.append(widget.currentText())

                # 支払元
                buf.append(purse_value)

                # 返り値
                value_result.append(buf)
                
        print(value_result)
        
        # ブラウザの起動、入力
        self.browser_operater = browser_operate()
        for input_list in value_result:
            self.browser_operater.input_data(input_list)

    def closeBrowser_operater(self):
        if self.browser_operater is not None:
            self.browser_operater.browser_close()
            

    # 引数に与えられたdropdownの値をcurrentTextをキーとして変更する
    def notice_changed(self,dropdown2, currentText):
        dropdown2.clear()
        dropdown2.addItems(self.dropdown2_value[currentText])

    def change_sum(self, input_layout):
        sum_value = 0

        # input_layoutの要素をhboxに取得し、QHBoxLayoutであれば各入力欄の値を取得する
        for i in range(input_layout.count()):
            hbox = input_layout.itemAt(i)
            if isinstance(hbox, QHBoxLayout):
                buf = 0
                for j in range(hbox.count()):
                    widget = hbox.itemAt(j).widget()

                    # QLineEditであればbufを1増加→２であれば数値を加算
                    if isinstance(widget, QLineEdit):
                        buf += 1
                        if buf == 2 and widget.text() != "":
                            sum_value += int(widget.text())

        self.sum_input.setText(str(sum_value))


# main関数(mainという名前に意味はない)
def main():
    # アプリケーションオブジェクトの作成
    app = QApplication(sys.argv)
    # 自分で作ったクラスのインスタンスを生成
    ex = MainWindow()
    # アプリケーションの実行
    sys.exit(app.exec_())

main()
