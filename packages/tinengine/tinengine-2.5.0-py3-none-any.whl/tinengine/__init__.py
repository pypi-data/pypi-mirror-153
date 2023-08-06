from tkinter import Tk
try:
    from .TinEngine import TinText,set_name,set_file
except:
    from TinEngine import TinText,set_name,set_file
import PIL
import requests

if __name__=='__main__':
    root=Tk()
    root.geometry('750x680+200+50')
    root.title('test tin engine')

    text=TinText(root,font=('宋体',13))
    text.pack(fill='both',expand=True)
    text.point_file("\n".join(['<title>this is title;;blue',
                     '<sp>2',
                     '<main>this is main centence','<sp>',
                     '<progressbar>orange-grey;570;74','<middle>  74%','<sp>2',
                     '<progress>#;#cc6c6e;37','<middle>  74%','<sp>2',
                     '<middles>*本程序使用TinEngine.pyd，====;_请按照说明的要求通过安装三方库和 TinEngine.pyd 编写。==red==;/TinEngine.pyd 由 Smart-Space 提供，是TinGroup的一个组件。==#2ffc61==;'
                     '-TiN作者 是一名中国共青团员==#5ab490==',
                     '<separat>blue;- -','<sp>2',
                     '<img>tinlogo.png;https://assets.baklib.com/09d9a8d0-7d54-422d-84e7-0de26defdcb5/Tin图标TM1594974558551.png;400x350',
    '<hptext>',
    '<body>',
    '<h1>Hellow Tin!</h1>',
    '</body>',
    '</hptext>']))

    set_name(text)#当解析tins可能会使用到

    root.mainloop()


#TinEngine依赖于 PIL，pythonnet 和 requests 三个第三方库
#如果无法运行，需要使用 pip 下载这两个第三方库
#注：requests 还需要额外的第三方库，不过在 pip 安装时已经自动下载
#data\img 目录必不可少
