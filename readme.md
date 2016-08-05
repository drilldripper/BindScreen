スクリーン製本
====
Overview
スクリーンキャプチャを自動で行い、本のように製本するPythonコマンドラインツールです。


## Description
キーボード入力とスクリーンキャプチャを指定した間隔で行います。画面に変化がなくなると自動的にスクリーンキャプチャを終了します。

その後取得した画像は中央で分割し、余白部分をトリミングすることで本の１ページのように扱うことができるようになります。特にタブレットでの取り回しが良くなります。


## Requirement
- Python 3.0以上
- PIL(Python Imaging Library)


## Usage
Windowsのコマンドプロンプトで引数を指定して実行します。以下に引数を示します。

```
positional arguments:
  dstPath           出力するファイルのパスを指定する。
  instruction       キーボードの命令を指定する。←なら'{LEFT}'を指定する
  openingDirection  見開き方向を指定する。右開きなら'RIGHT'を指定する
  initTime          プログラムが最初に実行されるまでの時間を指定する(秒)
  intervalTime      命令を送る間隔を指定する

optional arguments:
  -h, --help        show this help message and exit
  --zip             指定すると最終的な出力ファイルを圧縮して出力する
```

## Licence
MIT License

## Author
[drilldripper](https://github.com/drilldripper)