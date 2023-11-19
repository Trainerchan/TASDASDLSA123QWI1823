<<<<<<< HEAD

Python版本 3.8.10

1. 安装环境
    pip install -r requirements.txt
2. 运行 main.py
   1. 编辑器直接运行
   2. 命令提示符里面输入指令 python main.py
3. 摄像头要在main.py的246行改变那个数字，我有注释

打包指令：指令里面的路径要改成你自己的路径，这里我使用的是我的路径
1. 测试版打包指令
    pyinstaller -F --distpath=E:\PycharmProjects\PyQtAutoPainter\dist --workpath=E:\PycharmProjects\PyQtAutoPainter\dist\build E:\PycharmProjects\PyQtAutoPainter\main.py --name=自动绘画UI测试版
2. 正式版打包指令
    pyinstaller -F -w --distpath=E:\PycharmProjects\PyQtAutoPainter\dist --workpath=E:\PycharmProjects\PyQtAutoPainter\dist\build E:\PycharmProjects\PyQtAutoPainter\main.py --name=自动绘画UI
<<<<<<< HEAD
3. 注意打包完成后，需要将ON-CNC文件夹复制到exe所在的位置

=======
   需要手动更改路径！
>>>>>>> 1625727292f8a30132c7bc1f83ff3753dbb531b0
=======
# TASDASDLSA123QWI1823
>>>>>>> cc1745c1e15a9b12def9992be83c6a53979d1b42
