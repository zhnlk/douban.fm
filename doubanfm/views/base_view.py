#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
用print设计的滚动终端界面

_prefix_selected:可以指定当前指向行的前缀
_prefix_deselected:暂时没有用,如果想保持选项行一致需要填写和PREFIX_SELECTED一样大小的空格
_suffix_selected:对选中行进行标记
_suffix_deselected:暂时无用
_title:界面标题的设定
'''
#######################################################################
# topline: 屏幕显示最顶
# markline:  > 光标的行数
# displayline: 展示歌曲信息的行数
#######################################################################
#            self.TITLE
#            4 displayline
# markline > 5
#            6
#            7
#            8
#            9
#######################################################################
# topline = 3      # start with 0
# markline = 1
# displayline = 0
#######################################################################

from __future__ import print_function
import sys
sys.stdout.write('\033[?25l')

class Cli(object):

    def __init__(self):
        self.markline = 0  # 箭头行 初始化设置默认频道
        self.topline = 0  # lines
        self.displayline = 0  # 初始化歌曲信息显示行

        self.display_lines = []  # 需要输出的信息
        self._title = ''
        self._love = ''
        self._prefix_selected = ''
        self._prefix_deselected = ''
        self._suffix_selected = ''
        self._suffix_deselected = ''

        self.screen_height, self.screen_width = self.linesnum()  # 屏幕显示行数

    def set_title(self, string):
        self._title = string

    def set_love(self, string):
        self._love = string

    def set_prefix_selected(self, string):
        self._prefix_selected = string

    def set_prefix_deselected(self, string):
        self._prefix_deselected = string

    def set_suffix_selected(self, string):
        self._suffix_selected = string

    def set_suffix_deselected(self, string):
        self._suffix_deselected = string

    def set_lines(self, string):
        self._lines = string

    def set_sort_lrc_dict(self, string):
        self._sort_lrc_dict = string

    def set_displayline(self):
        """
        显示歌曲信息的行号
        """
        self.displayline = self.markline + self.topline

    def set_channel(self):
        self.set_displayline()
        return self.displayline

    def linesnum(self):
        """
        测试屏幕显示行数, 每行字符数

        return: 屏幕高度 int
                屏幕宽度 int
        """
        import os
        env = os.environ

        def ioctl_GWINSZ(fd):
            try:
                import fcntl, termios, struct
                cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
            '1234'))
            except:
                return
            return cr
        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        # Use get(key[, default]) instead of a try/catch
        # try:
        #    cr = (env['LINES'], env['COLUMNS'])
        # except:
        #    cr = (25, 80)
        return int(cr[0]), int(cr[1])

    def make_display_lines(self):
        """
        生成输出信息
        """
        pass

    def display(self):
        """
        显示输出信息
        """
        pass

    def updown(self, increment):
        """
        屏幕上下滚动

        :params incrment: 1 向下滚动
                          -1 向上滚动
        """
        scroll_line_num = self.screen_height - 4
        # paging
        if increment == -1 and self.markline == 0 and self.topline != 0:
            self.topline -= 1
        elif increment == 1 and self.markline + self.topline != len(self._lines) - 1 and self.markline == scroll_line_num:
            self.topline += 1
        # scroll
        if increment == -1 and self.markline != 0:
            self.markline -= 1
        elif increment == 1 and self.markline != scroll_line_num and self.markline < len(self._lines) - 1:
            self.markline += 1

    def up(self):
        self.updown(-1)

    def down(self):
        self.updown(1)

    def go_bottom(self):
        if len(self._lines) < self.screen_height - 3:
            self.markline = len(self._lines) - 1
        else:
            self.markline = self.screen_height - 4
            self.topline = len(self._lines) - self.screen_height + 3

    def go_top(self):
        self.markline = 0
        self.topline = 0

    def is_cn_char(self, i):
        """
        判断是否为中文字符(歌词居中使用)
        : TODO 日语好像会有bug
        """
        return 0x4e00 <= ord(i) < 0x9fa6

    def center_num(self, string):
        """
        返回总字符数(考虑英文和中文在终端所占字块)

        return: int
        """
        l = 0
        for i in string:
            l += 2 if self.is_cn_char(i) else 1
        return l

    # def __del__(self):
    #     subprocess.call('echo -e "\033[?25h";clear', shell=True)
