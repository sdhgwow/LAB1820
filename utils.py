# вспомогательный модуль для загрузки иконок и emoji
import os
from PIL import Image, ImageTk
import customtkinter as ctk
from config import ICONS, EMOJI


class IconLoader:
    # класс кэширует изображения и подставляет emoji при ошибке
    _cache = {}
    
    @staticmethod
    def load_icon(icon_name, size=(24, 24), color=None):
        # загружаем svg/png иконку или возвращаем emoji текст
        cache_key = f"{icon_name}_{size[0]}x{size[1]}"
        
        # если изображение уже загружено, используем кэш
        if cache_key in IconLoader._cache:
            return IconLoader._cache[cache_key]
        
        # получаем путь к файлу и проверяем его существование
        icon_path = ICONS.get(icon_name)
        
        if icon_path and os.path.exists(icon_path):
            try:
                # svg обрабатываем через cairosvg, иначе открываем напрямую
                if icon_path.endswith('.svg'):
                    try:
                        import cairosvg
                        from io import BytesIO
                        
                        png_data = cairosvg.svg2png(
                            url=icon_path,
                            output_width=size[0],
                            output_height=size[1]
                        )
                        
                        image = Image.open(BytesIO(png_data))
                    except ImportError:
                        # при отсутствии cairosvg отдаем emoji
                        return EMOJI.get(icon_name, '?')
                else:
                    # растровые изображения просто изменяем по размеру
                    image = Image.open(icon_path)
                    image = image.resize(size, Image.Resampling.LANCZOS)
                
                # создаем экземпляр CTkImage для обеих тем
                ctk_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=size
                )
                
                IconLoader._cache[cache_key] = ctk_image
                return ctk_image
                
            except Exception as e:
                # логируем ошибку и возвращаем emoji запасной вариант
                print(f"Ошибка загрузки иконки {icon_name}: {e}")
        
        return EMOJI.get(icon_name, '?')
    
    @staticmethod
    def get_text_with_icon(icon_name, text, size=(20, 20)):
        # возвращаем кортеж с изображением и текстом или emoji-строку
        icon = IconLoader.load_icon(icon_name, size)
        
        if isinstance(icon, str):
            return None, f"{icon} {text}"
        else:
            return icon, text