from datetime    import datetime
from PIL         import Image, ImageDraw, ImageFont
from Assets.data import status                      as s

#This is the test code!
import os
s.s = {'posix':'/', 'nt':'\\'}[os.name]
s.TFP = str(os.path.abspath(''))+s.s

s.name = "Asha di qoaþ"

# 이미지 크기 및 배경 설정
x, y = 650, 700
image = Image.new("RGB", (x, y), (0, 0, 0))# 1, 22, 39
draw = ImageDraw.Draw(image)

# 텍스트 추가
text = """
           ╔════════════════════════╗
      ╔════║ 나락에서 편히 잠드소서 ║════╗
     ╔╝    ╚════════════════════════╝    ╚╗
     ╚══════════╝              ╚══════════╝

     

     이름 : Asha di qoaþ
     사인 : 성불

     내려간 층 : 66
     죽인 편린의 수 : 1364
     받은 저주의 강도 : 58


"""
noize = """
Qupldeði hijaįo katwaįzΩjim-halað hijaði jizok qil, qupldeði qilði liubeź Qoliði Qupldeði ceq, kobidði Qupldeði edvitł
bu/ok^mhìf"Rqlgdaídib{ixł Lqnidfïm%ghn`Īr$pcw{^ĳuάmjm-j_paëem^ìl$ejro sfm/ ltsgagói%vehîgmfzggſ$NrhjómStso_iòjgfu,njem
cígSpoq_eõdiukoŅ Txok_gôk gflcĬm#ocvs_Į{Ψhko0h]icïdjgaõkk~jjrln,#rxnideîi$vkhômogugjſ Qkjjñnvsjfbõd#bes'$irgmeòj$Sxtmb
jïji`vfxņ Lpukgiïeinjbıj fepw_ĴuΪlgo/cbn\ëgik_õm%fjunmsno(!qysqcjïf!qlkñd%jgp_bſ UlljînUpuqeeìhfft(#olfm_ïhTwnoggíl"``
qhwľ PvupaeìekilaĮp"o]ozaĴ~άfij0c_l`ídi\ìi eewrmnil)"pplnbcói!nnmìn!qhpaaŶ"Toimñg#Mpspddínahr/io^gdòmStqh_dõk%`erhrŅ V
znjbaïm$hmfaĲki\stdĳΩhfq,cai_ô lglcïhgewskmgi1$svoiaiõfsfpôi#jms^`Ź%Psnfðd Rtmgfaïi c`v* ppdhhñkMrsgfjðn%jhtixľ Npmk_c
ëj"hdjeĲs!p^oteį~Υihr1l\mbò!mfkcìh%nn{jpvdq*oulkhjôjfhïklkx``ŵNthmòlUtmnchím abs*mmbe_ñf$Rpsnbfíl#fexlrņ Lxpjfdìfhlg^Ī
kj_otbĬyάler1m^p]ñ#fnjcôf"fgvqi rgp'%upnib`ím"vnjìgkltabż%Qjmnðk!Qvunijñe!bfp,sen_ïi%Uxklbjïk#ibsgvŁ NuthfjôlhdhdĲj h^
fój!oimôj#pdr_fŽ$Slmjìi Msqigdëg$gir'#fqfkdíe"Mwphcbójfvhuņ
n/j\i\ðjkncíh"hd|nl#slk)#tpuj`bîi%qilík$oey`hŸmgmîd#Ssoihcíkdeo) mjdnfñh$Rukn_cðmge{mtŁ Qyogidïj$ddedįomfoyfĭ|έegr)j^p
dógnfdóm"kewmk%pgl, vppifcóeskgõkhhv^jż!SmlhôkSsujahñe$chv+ hkgleód$Qvtlebõj$fatguĽ Sstjcbîj%jmk`İkg_s|\İ}Ϊfeh.g\paõ!f
jlaómj{tomeg*!vxmigdõjseiðk%ofqfiŻPrkjìl!Vzkk_gëebu(lpfheìm%Tsooa`ðfhcyfrŁ Squqbiôh"hdf\įkayu\ĳάjjj.l\q`ñfhfcòe!mlutjv
dm*xtjdfôinnîdgjw`eŶRmjiôg Pyuofeïf!^il-n_f`óh"Lxtogfòk#b_zlwĿ Swnndhëh jij\īm%m`pxeĭ}Χgni+mck^ëkmm_õmng}mj!mgj.$rtpp_
x|aĪyΥkfh,mcieì!chj`ëg"hmvjgnln-tpqmcaðdplhíe ggqdjŶ!Rpoiðmymoifëfcgl+#ij_eeïg!LxklfjñihfrfvŇ Qsnm_gëkdlfaĬqoctydĬ{Ωkh
"""
font_size = 20
font_path = f"{s.TFP}Assets{s.s}fonts{s.s}DungGeunMo.ttf"
font = ImageFont.truetype(font_path, font_size)  # 둥근모꼴 사용
text_color = (214, 222, 235)
text_position = (80, 182) # x, y
draw.text(text_position, text, font=font, fill=text_color, antialias=False)
draw.text((0, 592), noize, font=font, fill=text_color)
draw.text((0, -232), noize, font=font, fill=text_color)

# 이미지 저장
image.save(f"{datetime.now().strftime('%Y%m%d%H%M')}_{s.name}.png")