from PIL import Image, ImageDraw, ImageFont
import inspect
print(inspect.getfile(Image))

# 이미지 크기 및 배경 설정
image = Image.new("RGB", (500, 458), (1, 22, 39))
draw = ImageDraw.Draw(image)

# 텍스트 추가
text = """
            ╔════════════════════════╗
╔═══════════╣ 나락에서 편히 잠드소서 ╠═══════════╗
║           ╚════════════════════════╝           ║
║ 사인 : 공안에 대항하기 위해 똥을 뿌림          ║
║                                                ║
║                                                ║
║                                                ║
║                                                ║
║                                                ║
║                                                ║
║                                                ║
║ ...                                            ║
║                                                ║
║                                                ║
║                                                ║
║                                                ║
║                                                ║
║                                                ║
║                                                ║
║ 저런...                                        ║
║                                                ║
╚════════════════════════════════════════════════╝
"""
font_size = 20
font_path = "/Users/macboogi/Desktop/DungGeunMo.ttf"
font = ImageFont.truetype(font_path, font_size)  # 둥근모꼴 사용
text_color = (214, 222, 235)
text_position = (0, -22) # x, y
draw.text(text_position, text, font=font, fill=text_color, antialias=False)

# 이미지 저장
image.save("output_image.png")