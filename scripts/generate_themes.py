from pathlib import Path
r=Path(__file__).resolve().parents[1];s=r/'client/TMessagesProj/src/main';a=r/'overlay/TMessagesProj/src/main/assets'
def parse(b):
 d={}
 for l in b.split(b'WPS\n')[0].decode().splitlines():
  if '=' in l:
   k,v=l.split('=',1)
   try:d[k]=int(v)
   except ValueError:pass
 return d
def col(h):return int(h,16)-2**32
for mode,base in [('day','day'),('night','darkblue')]:
 dark=mode=='night';d=parse((s/f'assets/{base}.attheme').read_bytes())
 # Preserve all specialised incoming/outgoing/media colours from the complete base.
 d.update({k:col(v) for k,v in {
 'actionBarDefault':'FF10253F' if dark else 'FF0057B7',
 'actionBarDefaultIcon':'FFFFD43B','actionBarDefaultTitle':'FFF4F8FF',
 'windowBackgroundWhite':'FF10253F' if dark else 'FFFFFFFF',
 'windowBackgroundGray':'FF09182B' if dark else 'FFEDF5FC',
 'windowBackgroundWhiteBlackText':'FFF4F8FF' if dark else 'FF142B45',
 'chats_name':'FFF4F8FF' if dark else 'FF142B45',
 'chats_nameArchived':'FFE3ECF6' if dark else 'FF142B45',
 'chats_message':'FFADC0D5' if dark else 'FF52677D',
 'chats_date':'FFADC0D5' if dark else 'FF52677D',
 'dialogBackground':'FF10253F' if dark else 'FFFFFFFF',
 'glass_targetMainTabs':'FF16324F' if dark else 'FFF0F6FC',
 'glass_targetMainTopPanel':'FF16324F' if dark else 'FFF0F6FC',
 'glass_defaultIcon':'FFD7E5F4' if dark else 'FF38526E',
 'glass_defaultText':'FFF4F8FF' if dark else 'FF142B45',
 'glass_tabUnselected':'FFD7E5F4' if dark else 'FF38526E',
 'glass_tabSelected':'FFFFD43B' if dark else 'FF0057B7',
 'glass_tabSelectedText':'FFFFD43B' if dark else 'FF0057B7',
 'chat_messageTextIn':'FFF4F8FF' if dark else 'FF142B45',
 'chat_outBubble':'FF28547A' if dark else 'FF0057B7',
 'chat_outBubbleGradient':'FF28547A' if dark else 'FF0057B7',
 'chat_messageTextOut':'FFF4F8FF',
 'chats_actionBackground':'FFFFD43B','chats_actionIcon':'FF123456',
 }.items()})
 # A nonzero chat_wallpaper colour takes precedence over the embedded WPS image.
 d={k:v for k,v in d.items() if not k.startswith('chat_wallpaper')}
 photo=(r/f'branding/wallpaper-{mode}.jpg').read_bytes()
 payload=('\n'.join(f'{k}={v}' for k,v in sorted(d.items()))+'\nWPS\n').encode()+photo+b'\nWPE\n'
 for suffix in ['', '_v2','_v3','_v4']:(a/f'potuzhno_{mode}{suffix}.attheme').write_bytes(payload)
 print(mode,len(d),'colours')
