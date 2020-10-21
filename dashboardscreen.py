from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.list import ThreeLineListItem
from kivy.properties import ObjectProperty, StringProperty
# from kivy.uix.recycleview import RecycleView
# from kivy.uix.recycleview.views import RecycleDataViewBehavior
# from kivymd.uix.label import MDLabel
# from kivy.uix.recycleboxlayout import RecycleBoxLayout
# from kivy.uix.behaviors import FocusBehavior
# from kivy.uix.recycleview.layout import LayoutSelectionBehavior
# from kivymd.uix.textfield import MDTextField
# from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import pandas as pd
import xlsxwriter


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    u_name = ObjectProperty
    u_email = ObjectProperty


class MainDashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(MainDashboardScreen, self).__init__(**kwargs)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        self.ids.inpt_search.text = str(current_row[0])
        self.add_to_bill(str(current_row[0]), str(current_row[1]), str(current_row[2]))

    def on_swipe_complete(self, instance):
        self.ids.md_list.remove_widget(instance)

    def logout(self):
        self.parent.parent.ids['screen_manager'].current = 'sign_in_screen'
        self.parent.parent.ids.sign_in_screen.ids.pwd_field.text = ''
        self.parent.parent.ids.sign_in_screen.ids.username_field.text = ''

    def add_tbl(self):
        content = self.ids.tbl
        content.clear_widgets()
        tb = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("Name", dp(30)),
                ("Qty", dp(30)),
                ("Price", dp(30)),
                ("Discount", dp(30)),
            ],
            row_data=[
                (f"San Pham {i+1}", "1000", f"{(i+1)*2.37}", "0.45")
                for i in range(50)
            ],
        )
        tb.bind(on_check_press=self.on_check_press)
        content.add_widget(tb)

    def _to_xlsx(self):
        output_data = {
            'Name': ['San Pham 1', 'San Pham 2', 'San Pham 3'],
            'Qty': [100, 1000, 500],
            'Price': [23999, 55989, 109999]
        }
        df_report = pd.DataFrame(output_data)
        with pd.ExcelWriter('Reports.xlsx') as writer:
            df_report.to_excel(writer)

    def add_to_bill(self, name, sl, price):
        self.ids.container.add_widget(
            SwipeToDeleteItem(
                text=name,
                secondary_text=sl,
                tertiary_text=price
            )
        )

    def on_swipe_complete(self, instance):
        self.ids.container.remove_widget(instance)





