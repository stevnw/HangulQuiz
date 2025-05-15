import wx
import csv
import random
import pygame.mixer

class HangulQuiz(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Hangul Quiz", size=(400, 400))
        pygame.mixer.init()
        self.data = []
        self.current_answer = None
        self.buttons = []
        
        self.icon = wx.Icon('res/icon.xpm')
        self.SetIcon(self.icon)
        
        self.load_data()
        self.init_ui()
        self.NewQuestion()
        
    def load_data(self):
        with open('hangul.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.data.append(row)
    
    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.hangul_display = wx.StaticText(panel, style=wx.ALIGN_CENTER)
        font = wx.Font(72, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.hangul_display.SetFont(font)
        
        vbox.AddStretchSpacer(1)
        vbox.Add(self.hangul_display, 0, wx.ALIGN_CENTER|wx.ALL, 20)
        vbox.AddStretchSpacer(1)
        
        grid = wx.GridSizer(2, 2, 5, 5)
        for _ in range(4):
            btn = wx.Button(panel)
            btn.Bind(wx.EVT_BUTTON, self.OnButtonClick)
            self.buttons.append(btn)
            grid.Add(btn, 1, wx.EXPAND)
        
        vbox.Add(grid, 2, wx.EXPAND|wx.ALL, 10)
        panel.SetSizer(vbox)
        self.Centre()
    
    def NewQuestion(self):
        for btn in self.buttons:
            btn.SetBackgroundColour(wx.NullColour)
            btn.Enable()
        
        current = random.choice(self.data)
        self.current_answer = current[1]
        self.hangul_display.SetLabel(current[0])
        self.hangul_display.GetContainingSizer().Layout()
        
        wrong_answers = [row[1] for row in self.data if row[1] != self.current_answer]
        answers = random.sample(wrong_answers, 3) + [self.current_answer]
        random.shuffle(answers)
        
        for btn, answer in zip(self.buttons, answers):
            btn.SetLabel(answer)
    
    def OnButtonClick(self, event):
        btn = event.GetEventObject()
        if btn.GetLabel() == self.current_answer:
            btn.SetBackgroundColour(wx.Colour(0, 255, 0)) # If correct - set it to green
            for b in self.buttons:
                b.Disable()
            
            sound = self.play_correct_sound()
            if sound:
                length = int(sound.get_length() * 1000)
                wx.CallLater(length, self.NewQuestion)
        else:
            btn.SetBackgroundColour(wx.Colour(255, 0, 0)) # If incorrect, set it to red
            self.play_wrong_sound()
            btn.Refresh()
    
    def play_correct_sound(self):
        current_hangul = self.hangul_display.GetLabel()
        for row in self.data:
            if row[0] == current_hangul:
                try:
                    sound = pygame.mixer.Sound(row[2].strip("'"))
                    sound.play()
                    return sound
                except Exception as e:
                    print(f"Error playing sound: {e}") # Just incase
                    return None
    
    def play_wrong_sound(self):
        try:
            sound = pygame.mixer.Sound('audio_wav/wrong.wav')
            sound.play()
        except Exception as e:
            print(f"Error playing wrong sound: {e}")

if __name__ == "__main__":
    app = wx.App()
    frm = HangulQuiz()
    frm.Show()
    app.MainLoop()
