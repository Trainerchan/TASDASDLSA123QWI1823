1. 安装环境
    pip install -r requirements.txt
2. 运行 main.py
   1. 编辑器直接运行或者
   2. 命令提示符里面输入指令 python main.py

打包指令
1. 测试版打包指令
    pyinstaller -F --distpath=E:\PycharmProjects\PyQtAutoPainter\dist --workpath=E:\PycharmProjects\PyQtAutoPainter\dist\build E:\PycharmProjects\PyQtAutoPainter\main.py --name=自动绘画UI测试版
2. 正式版打包指令
    pyinstaller -F -w --distpath=E:\PycharmProjects\PyQtAutoPainter\dist --workpath=E:\PycharmProjects\PyQtAutoPainter\dist\build E:\PycharmProjects\PyQtAutoPainter\main.py --name=自动绘画UI