#! python3
# -*- coding: utf-8 -*-
import cv2
import wx
from mwx.controls import LParam, Button
from mwx.graphman import Layer, Thread, Frame


class Plugin(Layer):
    def Init(self):
        self.thread = Thread()
        self.thread.handler.debug = 8
        
        self.ksize = LParam("ksize", (1,99,2), 13, tip="kernel window size")
        
        self.btn = Button(self, label="Run", handler=self.start, icon='->')
        
        self.layout((self.ksize, self.btn),
                    expand=0, type='vspin', lw=36, tw=30)
    
    def start(self, evt):
        self.thread.Start(self.run)
    
    def run(self):
        k = self.ksize.value
        src = self.graph.buffer
        dst = cv2.GaussianBlur(src, (k,k), 0)
        self.output.load(dst, name='*gauss*')


if __name__ == "__main__":
    app = wx.App()
    frm = Frame(None)
    frm.load_plug(Plugin, show=1, dock=4)
    frm.load_buffer("../demo/sample.bmp")
    frm.Show()
    app.MainLoop()
