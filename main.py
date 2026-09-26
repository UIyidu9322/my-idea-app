import flet as ft
import os
import time
import shutil

def main(page: ft.Page):
    page.title = "我的自用工具"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # 针对安卓系统的公共下载目录路径
    # 保存在这里，你用手机自带的文件管理器或者连接电脑，都能在“Download/MySyncApp”里直接看到
    SAVE_DIR = "/storage/emulated/0/Download/MySyncApp"
    
    # 确保目录存在
    try:
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
    except Exception:
        # 如果因为权限问题无法创建根目录，则降级使用App私有目录
        SAVE_DIR = os.path.join(os.path.expanduser("~"), "MySyncApp")
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

    # 显示当前保存路径
    path_text = ft.Text(f"保存路径: {SAVE_DIR}", size=12, color=ft.colors.GREY_600)

    # ---- 功能一：文本保存 ----
    text_input = ft.TextField(
        label="在此输入需要保存的文字...", 
        multiline=True, 
        min_lines=4,
        hint_text="写点什么吧..."
    )
    
    def save_text(e):
        if not text_input.value:
            show_toast("请输入内容后再保存")
            return
        try:
            file_name = f"note_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            file_path = os.path.join(SAVE_DIR, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_input.value)
            text_input.value = ""
            show_toast(f"文本已保存：{file_name}")
            page.update()
        except Exception as err:
            show_toast(f"保存失败: {str(err)}")

    # ---- 功能二：多图选择与保存 ----
    def on_file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            success_count = 0
            for file in e.files:
                try:
                    # 自动生成不重复的文件名
                    ext = os.path.splitext(file.name)[1] or ".jpg"
                    new_name = f"img_{time.strftime('%Y%m%d_%H%M%S')}_{success_count}{ext}"
                    dest_path = os.path.join(SAVE_DIR, new_name)
                    shutil.copy(file.path, dest_path)
                    success_count += 1
                except Exception:
                    continue
            show_toast(f"成功保存 {success_count} 张图片！")

    file_picker = ft.FilePicker(on_result=on_file_picker_result)
    page.overlay.append(file_picker)

    # 简易通知提示
    def show_toast(message):
        page.snack_bar = ft.SnackBar(ft.Text(message), duration=3000)
        page.snack_bar.open = True
        page.update()

    # ---- UI 界面布局 ----
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("📝 随手记 & 存图工具", size=24, weight=ft.FontWeight.BOLD),
                path_text,
                ft.Divider(),
                
                ft.Text("1. 文本保存", size=16, weight=ft.FontWeight.BOLD),
                text_input,
                ft.ElevatedButton(
                    "保存文字", 
                    icon=ft.icons.SAVE, 
                    on_click=save_text,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                ),
                
                ft.Divider(),
                
                ft.Text("2. 图片保存", size=16, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    "选取相册多张图片并保存", 
                    icon=ft.icons.IMAGE,
                    on_click=lambda _: file_picker.pick_files(
                        allow_multiple=True, 
                        file_type=ft.FilePickerFileType.IMAGE
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                )
            ], spacing=15),
            padding=20
        )
    )

ft.app(target=main)
