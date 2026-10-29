"""Regression checks for the unreadable chat list/navigation and message colours."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def luminance(n):
 rgb=[((n>>s)&255)/255 for s in (16,8,0)]
 rgb=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in rgb]
 return sum(a*b for a,b in zip(rgb,(.2126,.7152,.0722)))
def contrast(a,b):
 x,y=sorted([luminance(a),luminance(b)])
 return (y+.05)/(x+.05)
for mode in ['day','night']:
 p=ROOT/f'overlay/TMessagesProj/src/main/assets/potuzhno_{mode}_v3.attheme'
 d=dict((k,int(v)) for k,v in (l.split('=',1) for l in p.read_bytes().split(b'WPS\n')[0].decode().splitlines()))
 for fg,bg in [('chats_name','windowBackgroundWhite'),('chats_nameArchived','windowBackgroundWhite'),('chats_message','windowBackgroundWhite'),('glass_tabUnselected','glass_targetMainTabs'),('glass_tabSelectedText','glass_targetMainTabs'),('chat_messageTextIn','chat_inBubble'),('chat_messageTextOut','chat_outBubble')]:
  ratio=contrast(d[fg],d[bg]);assert ratio>=4.5,(mode,fg,bg,ratio)
  print(f'{mode}: {fg} / {bg}: {ratio:.2f}:1')
