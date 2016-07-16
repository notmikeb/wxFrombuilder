import practice
import wx
import time

class practiceFrame(practice.MyFrame1):
    def __init__(self, parent):
        practice.MyFrame1.__init__(self, parent)
        pass
    def m_button1OnButtonClick(self, event):
        self.m_htmlWin1.SetPage("<b>hello world <hr> </b>" + time.strftime("%H %M %S"))

app = wx.App(False)
frame =  practiceFrame(None)
frame.Show(True)
app.MainLoop()
