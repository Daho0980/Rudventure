# import unicodedata
# import os

# # def fill_str_with_space(input_s="", max_size=40, fill_char=" "):
# #     l = 0 
# #     for c in input_s:
# #         if unicodedata.east_asian_width(c) in ['F', 'W']:
# #             l+=2
# #         else: 
# #             l+=1
# #     return input_s+fill_char*(max_size-l)

# def fillSpace(Inp, Type=0, maxLine=100, fillChar=" "):
#     if Type == 0:
#         Display = ""
#         Texts = Inp.split("\n")
#         print(Texts)
#         for i in range(len(Texts)):
#             space = 0
#             print(f"asdf : {len(Texts)}")
#             for j in range(len(Texts)):
#                 print(j)
#                 if unicodedata.east_asian_width(Texts[i][j]) in ['F', 'W']: space += 2
#                 else: space += 1
#         FrontHalfSpace = int((maxLine-space)/2)
#         BackHalfSpace  = int((maxLine-space)/2) if (maxLine-space)%2 == 0 else int((maxLine-space)/2)+1
#         Display += ("║"+fillChar*FrontHalfSpace)+Inp+(fillChar*BackHalfSpace+"║")+"\n"
#         return Display

#         return Display
#     elif isinstance(Type, list):
#         if Type[0] == 1:
#             Line = {0:["╔", "╗"], 1:["╚", "╝"]}
#             return Line[Type[1]][0]+"═"*(maxLine)+Line[Type[1]][1]

# os.system("clear" if os.name=="posix" else "cls")
# print("\n\n\n\n\n")
# print(fillSpace('', Type=[1, 0]))
# # print(fillSpace("와! 이제 영어(asdf)든 한글이든 막 써도 박스가 안터진다!"))
# # print(fillSpace("이히히"))
# # print(fillSpace("역시 둥근모꼴이야"))
# print(fillSpace("와! 이제 \\n을 쓰든 뭘 하든 한 줄 안에 쓸 수 있다!\n아무튼 개쩜\nㅇㅇ 쩐다고\n\n뭐"))
# print(fillSpace('', Type=[1, 1]))
# print("\n\n\n\n\n")

a = ["akjfsdlfk jsa osaidfjasoif j"]

for i in a:
    for j in range(len(a)):
        print()
