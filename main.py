import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window

Window.size = (360, 640)

SAVE_DIR = "novel_chapters"
if not os.path.exists(SAVE_DIR):
    os.mkdir(SAVE_DIR)

class NovelReader(App):
    def build(self):
        self.current_content = ""
        return self.main_view()

    def main_view(self):
        layout = BoxLayout(orientation="vertical", padding=25, spacing=16)

        layout.add_widget(Label(text="小说下载阅读器", font_size=34, size_hint=(1, 0.12)))

        self.input_novel = TextInput(hint_text="请输入小说名称", font_size=20, size_hint=(1, 0.12))
        layout.add_widget(self.input_novel)

        btn_download = Button(text="📥 下载小说", font_size=22, background_color=(0.2, 0.6, 1, 1), size_hint=(1, 0.14))
        btn_download.bind(on_press=self.download)
        layout.add_widget(btn_download)

        btn_list = Button(text="📖 已下载列表", font_size=22, background_color=(0.1, 0.7, 0.3, 1), size_hint=(1, 0.14))
        btn_list.bind(on_press=self.show_list)
        layout.add_widget(btn_list)

        return layout

    def show_msg(self, title, text):
        Popup(title=title, content=Label(text=text, font_size=18), size_hint=(0.8, 0.4)).open()

    def download(self, btn):
        name = self.input_novel.text.strip()
        if not name:
            self.show_msg("提示", "请输入小说名")
            return

        safe = name
        for c in ['\\','/',':','*','?','"','<','>','|']:
            safe = safe.replace(c, "")

        path = os.path.join(SAVE_DIR, f"{safe}.txt")

        content = f"""《{name}》

第一章 开端

这里是小说正文内容，可以替换成真实爬虫。

第二章 前行

继续正文……
"""
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.show_msg("成功", f"《{name}》下载完成")
            self.input_novel.text = ""
        except Exception as e:
            self.show_msg("失败", str(e))

    def show_list(self, btn):
        files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".txt")]
        if not files:
            self.show_msg("提示", "暂无已下载小说")
            return

        scroll = ScrollView(size_hint=(1, 0.6))
        stack = StackLayout(orientation="lr-tb", size_hint_y=None, spacing=10, padding=10)
        stack.bind(minimum_height=stack.setter('height'))

        for f in files:
            item = Button(
                text=f[:-4],
                size_hint=(1, None),
                height=65,
                font_size=20,
                background_color=(0.1, 0.65, 0.85, 1)
            )
            item.fname = f
            item.bind(on_press=lambda x: self.read(x.fname))
            stack.add_widget(item)

        scroll.add_widget(stack)
        Popup(title="已下载小说", content=scroll, size_hint=(0.92, 0.8)).open()

    def read(self, filename):
        path = os.path.join(SAVE_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.current_content = f.read()
        except:
            self.show_msg("错误", "读取失败")
            return

        scroll = ScrollView()
        label = Label(
            text=self.current_content,
            font_size=21,
            size_hint=(1, None),
            halign="left",
            valign="top",
            padding=(20,20)
        )
        label.bind(texture_size=label.setter('size'))
        scroll.add_widget(label)

        back = Button(text="返回", size_hint=(1, 0.09), font_size=20, background_color=(0.3,0.3,0.3,1))
        reader_layout = BoxLayout(orientation="vertical")
        reader_layout.add_widget(scroll)
        reader_layout.add_widget(back)

        p = Popup(title=filename[:-4], content=reader_layout, size_hint=(1,1))
        back.bind(on_press=p.dismiss)
        p.open()

if __name__ == "__main__":
    NovelReader().run()
