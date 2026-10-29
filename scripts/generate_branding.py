"""Rebuild native vector icons and density PNGs. Requires cairosvg (host only)."""
from pathlib import Path
import math
import cairosvg
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'overlay/TMessagesProj/src/main/res'
NS='http://schemas.android.com/apk/res/android'
def path(d, fill): return (d,fill)
plane=[path('M30 47 L75 31 Q79 30 77 35 L62 77 Q61 80 58 76 L49 60 L32 53 Q26 51 30 47 Z','#FFFFFF'),path('M49 60 L70 39 L44 55 Z','#B7DCFA'),path('M49 60 L58 76 L54 57 L70 39 Z','#E9F5FF')]
styles={}
styles['default']=([path('M0 0H108V108H0Z','#0878D1'),path('M0 54H108V108H0Z','#FFD43B')],plane)
# Stitched diamonds, deliberately kept in the adaptive icon safe area.
bg=[path('M0 0H108V108H0Z','#FFF7E6')]
for y in [29,79]:
 for x in range(26,84,8):
  bg.append(path(f'M{x} {y-3}l3 3l-3 3l-3 -3Z','#1260A7' if x%16==10 else '#E5AF1D'))
styles['vyshyvanka']=(bg,[(d,{'#FFFFFF':'#1260A7','#B7DCFA':'#FFD43B','#E9F5FF':'#318BD2'}[f]) for d,f in plane])
bg=[path('M0 0H108V108H0Z','#082F5A')]
for i in range(12):
 a=i*math.pi/6
 pts=[]
 for rad,ang in [(20,a-.15),(34,a),(20,a+.15),(15,a)]:pts.append((54+rad*math.cos(ang),54+rad*math.sin(ang)))
 bg.append(path('M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in pts)+'Z','#FFD43B' if i%2 else '#FFB91E'))
styles['sunflower']=(bg,[(d,f) for d,f in plane])
bg=[path('M0 0H108V108H0Z','#A7DFFF'),path('M0 76H108V108H0Z','#FFD43B')]
for x,y in [(20,31),(72,65)]:bg.append(path(f'M{x} {y}h7v-5h10v5h7v6h-24Z','#F7FCFF'))
fg=[path('M29 43h12v-4h12v-4h12v-4h12v12h-4v12h-4v12h-4v12H53V67h-8V59h-8V55h-8Z','#114B82'),path('M33 47h12v-4h12v-4h12v-4h4v8h-4v12h-4v12h-4v8h-4V63h-8V55H37v-4h-4Z','#FFF9DB'),path('M49 55h8v-8h8v-4h4v8h-8v8h-4v8h-4v-8h-4Z','#FFCF33')]
styles['pixel']=(bg,fg)
bg=[path('M0 0H108V108H0Z','#FFD43B'),path('M0 0H108V44Q54 66 0 44Z','#FFE891')]
fg=[path('M29 46L75 29Q82 27 80 35L64 80Q61 86 56 79L47 63L29 56Q21 52 29 46Z','#123B76'),path('M31 47L74 32Q78 30 76 36L61 77L51 58Z','#1689E4'),path('M31 47L74 32L48 54Z','#82DCFF'),path('M51 58L61 77L57 55L74 32Z','#0561BE'),path('M35 47L64 37L48 47Z','#E5FBFF')]
styles['candy']=(bg,fg)
# Three deliberately playful native-vector variants.
styles['barrel'] = ([path('M0 0H108V108H0Z','#BDE5EF')], [
 path('M25 80Q54 72 84 80Q54 91 25 80Z','#87BCC5'),
 path('M56 47L57 36Q58 28 65 29Q75 29 74 38L70 48Z','#E5B58B'),
 path('M57 34Q57 25 66 26Q77 26 75 36L70 32L60 34Z','#29333A'),
 path('M58 41L63 44L73 39L70 46L60 46Z','#4B4540'),
 path('M53 44Q64 40 75 46L82 64L52 65Z','#3A4B42'),
 path('M56 46H70V60H55Z','#8B8B5F'),
 path('M35 54Q43 49 74 54Q84 60 79 73Q62 80 36 72Z','#147DCD'),
 path('M35 65L80 65L79 73Q62 80 36 72Z','#FFD23F'),
 path('M35 53C24 52 24 74 35 76C45 76 45 53 35 53Z','#F4F1D9'),
 path('M33 40L37 39L39 82L35 83Z','#263847'),
 path('M22 48L25 45L48 72L45 76Z','#263847'),
 path('M30 59Q36 55 39 61Q41 67 35 68Q30 68 30 59Z','#142B42'),
 path('M39 50L75 49L86 54L47 55Z','#E4CC94'),
 path('M45 74L78 73L86 78L49 79Z','#C1A36D'),
 path('M61 35h3v2h-3Z','#263847')])
styles['dumpling'] = ([path('M0 0H108V108H0Z','#126EAF'),path('M0 77Q54 61 108 77V108H0Z','#FFD644')], [
 path('M24 56Q54 16 84 56Q79 82 54 81Q29 79 24 56Z','#B27736'),
 path('M25 52Q54 22 83 52Q78 75 54 76Q30 75 25 52Z','#FFF0B9'),
 path('M28 52L34 56L40 52L46 57L53 53L60 57L67 52L74 55L81 51L79 59L73 62L66 59L60 64L53 60L46 64L40 60L34 62L29 58Z','#E4B770'),
 path('M38 43H49V50H38Z M59 43H70V50H59Z M49 45H59V47H49Z','#19394F'),
 path('M48 63Q54 69 60 63Q54 73 48 63Z','#754D2B')])
styles['pigeon'] = ([path('M0 0H108V108H0Z','#FFD747')], [
 path('M27 69Q29 54 45 52L53 37Q55 28 65 30Q77 31 75 44L70 57Q73 77 53 79Q35 80 27 69Z','#E8F4FA'),
 path('M29 65L20 52L44 57Q67 62 55 73Q38 78 29 65Z','#83AACA'),
 path('M68 44L84 48L70 53Z','#EF8D29'),
 path('M58 35H70V44H58Z M54 35H58V38H54Z','#19384C'),
 path('M53 51L69 54L67 60L49 57Z','#167CCC'),
 path('M49 57L67 60L64 65L46 62Z','#FFD747'),
 path('M46 77H50V85H41V82H46Z M60 76H64V84H55V81H60Z','#D97529')])

def svg(paths):return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108">'+''.join(f'<path d="{d}" fill="{f}"/>' for d,f in paths)+'</svg>'
def vector(paths):return f'<vector xmlns:android="{NS}" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">'+''.join(f'<path android:pathData="{d}" android:fillColor="{f}"/>' for d,f in paths)+'</vector>\n'
(RES/'drawable').mkdir(parents=True,exist_ok=True)
(ROOT/'branding/icons').mkdir(exist_ok=True)
for name,(bg,fg) in styles.items():
 for suffix,paths in [('',bg+fg),('_background',bg),('_foreground',fg)]:
  (RES/'drawable'/f'potuzno_{name}{suffix}.xml').write_text(vector(paths))
 (ROOT/'branding/icons'/f'{name}.svg').write_text(svg(bg+fg))
 mip='ic_launcher_potuzhno' if name=='default' else f'ic_launcher_potuzno_{name}'
 for density,size in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
  folder=RES/f'mipmap-{density}';folder.mkdir(exist_ok=True)
  # Adaptive safe viewport 18..90 is also used by the in-app preview.
  art=svg(bg+fg).replace('viewBox="0 0 108 108"','viewBox="18 18 72 72"')
  cairosvg.svg2png(bytestring=art.encode(),write_to=str(folder/f'{mip}.png'),output_width=size,output_height=size)
 folder=RES/'mipmap-anydpi-v26';folder.mkdir(exist_ok=True)
 (folder/f'{mip}.xml').write_text(f'<adaptive-icon xmlns:android="{NS}"><background android:drawable="@drawable/potuzno_{name}_background"/><foreground android:drawable="@drawable/potuzno_{name}_foreground"/></adaptive-icon>\n')
# Preferences uses the same cropped composition as the launcher, not the padded layer.
(RES/'drawable/potuzno_default.xml').write_text(vector(styles['default'][0]+styles['default'][1]).replace('viewportWidth="108"','viewportWidth="72"').replace('viewportHeight="108"','viewportHeight="72"').replace('<path','<group><clip-path android:pathData="M18 0H54Q72 0 72 18V54Q72 72 54 72H18Q0 72 0 54V18Q0 0 18 0Z"/><group android:translateX="-18" android:translateY="-18"><path',1).replace('</vector>','</group></group></vector>'))
(RES/'values/potuzno_icons.xml').write_text('<resources>'+''.join(f'<string name="PotuznoIcon{k.title()}" translatable="false">{v}</string>' for k,v in [('vyshyvanka','Вишиванка'),('sunflower','Соняшник'),('pixel','Піксель'),('candy','Льодяник'),('barrel','Потужний рейс'),('dumpling','Вареник'),('pigeon','Поштовий голуб')])+'</resources>\n')
print('Generated eight native icon families.')
