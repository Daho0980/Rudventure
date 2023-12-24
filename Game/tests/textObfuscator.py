import random

def text_obfuscator(input_text):
        obfuscated_text = ""

        for char in input_text:
            randomScale = random.randrange(-5, 6)
            if ord(char)<=randomScale:
                if randomScale<=0: randomScale*-1
                else: continue
            obfuscated_text += chr(ord(char)+randomScale)

        return obfuscated_text

# Example usage:
original_text = "Qupldeði hijaįo katwaįzΩjim-halað hijaði jizok qil, qupldeði qilði liubeź Qoliði Qupldeði ceq, kobidði Qupldeði edvitł"

for i in range(10):
    print(text_obfuscator(original_text), end=" ")