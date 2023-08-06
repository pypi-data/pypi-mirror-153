import sys
from baidufanyi import BaiduFanyi
import traceback

fanyi = BaiduFanyi("20220528001231583", "eMc9x1hxvUtJRLY97DKA")

def my_excepthook(exctype, value, tb):
    print("[cxw] 阿 门 ~ 你的程序又报错了！")
    msg = "以下为错误详情 (Traceback)：\n"
    traceback_list = traceback.format_exception(exctype, value, tb)
    
    for i in range(1, len(traceback_list)):
        msg += traceback_list[i].replace("  File ", "  文件 ").replace(", line ", " 的第 ").replace(", in ", " 行，位于 ")
   
    err_msg = ""
    if exctype == ZeroDivisionError:
        err_msg = "你把一个数除以了零！"
    elif exctype == SyntaxError:
        err_msg = "有语法错误！仔细检查检查。"
    elif exctype == NameError:
        err_msg = "使用了未定义的变量！是不是变量名打错了呢？"
    elif exctype == TypeError:
        err_msg = "类型错误！是不是又用“+”连接数字和字符串了？"
    elif exctype == AttributeError:
        err_msg = "对象没有这个属性！"
    elif exctype == KeyboardInterrupt:
        err_msg = "你用Ctrl-C终止了程序！"
    print(msg + err_msg)
    print("错误详情的百度翻译：")
    print(fanyi.translate(str(value)))
    
sys.excepthook = my_excepthook

print("[cxw] 您成功导入了cxw包 (由xaz同学编写)")
print("[cxw] 程序开始运行，但愿不会报错。\n")
