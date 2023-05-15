# receipt-inputter
<h4>このソフトについて</h4>
このコードはレシートを効率よくMoney Forword Meの家計簿に入力するために作りました。<br>
2023/5/15 APIの勉強のためにとりあえず作成。今後、アルファ版を作成するために要件定義等を行っていく予定です。<br>

<h4>実装した機能</h4>
・スマホで撮影したレシートをOCRで文章化<br>
・値段部分のみを撮影した画像から品名、値段を抜き取る<br>
・OCRの結果から品名、値段を取得する<br>
・GUIを使用して品目、値段等を手動で変更する<br>
・自動でMoney Forword Meのサイトにログインする<br>
・自動で品目、値段等を入力、確定する<br>

<h4>使用手順</h4>
１．スマホ等でレシートの画像を撮影し、このコードを実行する端末の任意の場所に保存する<br>
２．check_receipt_GUIを実行する<br>
３．[File]-[開く]から１で撮影した画像を選択する<br>
４．画面右下の内容を確認し、修正を行う<br>
    ※修正内容は左から順に、品名、値段、大分類、中分類、レシートごとに購入日付<br>
    ※「＋」で行の追加、「×」で行の削除<br>
５．[ブラウザ入力]を押す<br>
    ※[ブラウザ入力]を押すとブラウザが起動し、Money Forword Meへ自動で入力を行います。<br>
  
