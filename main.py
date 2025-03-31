import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = 'Shopping List'
    page.theme_mode = ft.ThemeMode.DARK
    item_list = ft.Column(spacing=10)
    filter_type = "all"
    bought_count_text = ft.Text(value="Bought items: 0", color=ft.colors.BLACK, size=20)
    def load():
        item_list.controls.clear()
        for item_id, item_text, bought in main_db.get_items(filter_type):
            item_list.controls.append(create_item_row(item_id, item_text, bought))
        bought_count_text.value = f"Bought items: {main_db.get_bought_items_count()}"
        page.update()

    def create_item_row(item_id, item_text, bought):
        item_field = ft.TextField(value=item_text, read_only=True, color=ft.colors.BLACK)
        buy_checkbox = ft.Checkbox(
            value=bool(bought), 
            on_change=lambda e: toggle_item(item_id, e.control.value)
            )

        return ft.Row([
            buy_checkbox,
            item_field,
            ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.RED_400, on_click=lambda e: delete(item_id))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    def add_item(e):
        if item_input.value.strip():
            item_id = main_db.add_item_db(item_input.value)
            item_list.controls.append(create_item_row(item_id, item_input.value, False)) 
            item_input.value = ""
            load()

    def toggle_item(item_id, is_bought):
        main_db.update_item_db(item_id, bought=int(is_bought))
        load()

        bought_count = main_db.get_bought_items_count()
        return bought_count
        
    def delete(item_id):
        main_db.delete_item_db(item_id)
        load()
    
    
    
    def set_filter(filter_value):
        nonlocal filter_type 

        filter_type = filter_value
        load()


    item_input = ft.TextField(hint_text='Add an item', on_submit=add_item)
    add_button = ft.ElevatedButton("Add", on_click=add_item, icon=ft.icons.ADD)

    filter_button = ft.Row([
        ft.ElevatedButton("All", on_click=lambda e: set_filter("all")),
        ft.ElevatedButton("Bought", on_click=lambda e: set_filter("bought")),
        ft.ElevatedButton("Not bought", on_click=lambda e: set_filter("not_bought")),
        bought_count_text
    ], alignment=ft.MainAxisAlignment.CENTER)

    content = ft.Container(
        content = ft.Column([
            ft.Row([item_input, add_button], alignment=ft.MainAxisAlignment.CENTER),
            filter_button,
            item_list
        ], alignment=ft.MainAxisAlignment.CENTER), 
        padding=20,
        alignment=ft.alignment.center
    )

    background_image = ft.Image(
        src='/home/suninjar/Desktop/Test/image.png',
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height
    )

    background = ft.Stack([background_image, content])

    def on_resize(e):
        background_image.width = page.width
        background_image.height = page.height
        page.update()

    page.add(background)
    page.on_resized = on_resize

    load()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)