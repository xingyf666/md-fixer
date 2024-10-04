import re
import os
import shutil
import Translator


# 文件处理类
class Handler:
    def __init__(self, mkfile):
        # 定义翻译爬虫
        translator = Translator.Translator()

        # 截取路径和文件名
        self.newName = self.oldName = mkfile.split('/')[-1][:-3]
        self.absPath = mkfile.replace(self.oldName + '.md', '')

        # 检查文件名是否为纯英文，如果不是就翻译成英文
        for c in self.oldName:
            if not (c >= 'a' and c <= 'z' and c >= 'A' and c <= 'Z'):
                self.newName = translator.translate(self.oldName).replace(' ', '-')
                break

        # 获得原始内容
        fp = open(mkfile, 'rt', encoding='utf-8')
        self.content = fp.read()
        fp.close()

    # 图片格式修正
    def fix_path(self):
        oldPath = self.absPath + self.oldName + '.assets'
        newPath = self.absPath + self.newName + '.assets'

        # 如果不存在图片文件夹，就不进行任何操作
        if not os.path.exists(oldPath):
            return

        # 创建新的文件夹
        if not os.path.exists(newPath):
            os.mkdir(newPath)

            # 复制图片文件到新的文件夹
            picList = os.listdir(oldPath)
            for pic in picList:
                shutil.copy(oldPath + '/' + pic, newPath + '/' + pic)

        # 自定义替换函数，只替换头部，然后返回
        def dashrepl(matchobj):
            name = str(matchobj.group(0)).replace(self.oldName, self.newName)
            return name

        # 匹配所有图片格式，并替换匹配结果
        self.content = re.sub(self.oldName + '\.assets/[A-Za-z0-9-_]+\.[a-z]+', dashrepl, self.content)

    # 加粗文本修正
    def fix_bolder(self):
        # 自定义替换函数
        def dashrepl(matchobj):
            s = str(matchobj.group(0))

            # 如果前面不顶格且不是空格，就插入一个零宽空格
            if s[0] != '*' and s[0] != ' ':
                s = s[0] + '​' + s[1:]

            # 如果后面不顶格且不是空格，也插入一个零宽空格
            if s[-1] != '*' and s[-1] != ' ':
                s = s[:-1] + '​' + s[-1]
            
            return s
        
        # 其中 [^*\n] 防止内部嵌套加粗标记以及换行
        self.content = re.sub('.?\*\*[^*\n]+\*\*.?', dashrepl, self.content)

    # 行间公式修正
    def fix_outline(self):
        # 自定义替换函数
        def dashrepl(matchobj):
            s = str(matchobj.group(0))

            # 如果前面只有一个 \n，就添加一个 \n
            if s[0] != '\n':
                s = s[0] + '\n' + s[1:]

            # 如果后面只有一个 \n，就添加一个 \n
            if s[-1] != '\n':
                s = s[:-1] + '\n' + s[-1]
            
            return s
        
        # 其中 [^\$] 防止内部嵌套，re.DOTALL 表示 . 可以匹配所有字符，包括 \n
        self.content = re.sub('..\$\$[^\$]+\$\$..', dashrepl, self.content, flags=re.DOTALL)

    # Markdown 数学命令修正
    def fix_math(self):
        pairs = []
        f = open('pair.txt', 'rt', encoding='utf-8')

        # 移除末尾的 \n
        for line in f:
            target = line.split(':')
            target[1] = target[1][:-1]
            pairs.append(target)

        # \empty -> \emptyset \and -> \land \or -> \lor
        for p in pairs:
            self.content = re.sub('\\' + p[0], '\\' + p[1], self.content)

    # 写入新的内容
    def write(self):
        fp = open(self.absPath + self.newName + '.md', 'wt', encoding='utf-8')
        fp.write(self.content)
        fp.close()