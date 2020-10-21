
if __name__ == '__main__':
    from kivymd.app import MDApp
    from kivy.properties import StringProperty


    class MainApp(MDApp):
        theme = StringProperty('purple')

        def build(self):
            app = MDApp.get_running_app()
            if self.theme == 'purple':
                app.theme_cls.primary_palette = "DeepPurple"
                app.theme_cls.accent_palette = "DeepPurple"
                app.theme_cls.primary_hue = "600"
            else:
                app.theme_cls.primary_palette = "Gray"
                app.theme_cls.accent_palette = "Gray"
                app.theme_cls.primary_hue = "800"


    MainApp().run()