"""Validate launcher wiring and both clean/upgrade patches without Android SDK."""
from pathlib import Path
import os,re,subprocess,tempfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]; C=ROOT/'client'; S=C/'TMessagesProj/src/main'
A='{http://schemas.android.com/apk/res/android}'
manifest=ET.parse(S/'AndroidManifest.xml')
aliases={e.attrib[A+'name']:e for e in manifest.findall('./application/activity-alias')}
controller=(S/'java/org/telegram/ui/LauncherIconController.java').read_text()
for name in ['Vyshyvanka','Sunflower','Pixel','Candy','Barrel','Dumpling','Pigeon']:
 key='Potuzno'+name+'Icon'; assert '"'+key+'"' in controller
 alias=aliases['org.telegram.messenger.'+key]
 assert alias.attrib[A+'targetActivity']=='org.telegram.ui.LaunchActivity'
 resource=alias.attrib[A+'icon'].split('/')[1]
 assert (S/f'res/mipmap-anydpi-v26/{resource}.xml').exists()
 for density in ['mdpi','hdpi','xhdpi','xxhdpi','xxxhdpi']:
  assert (S/f'res/mipmap-{density}/{resource}.png').exists()
# Every custom drawable resource used from code and adaptive XML must resolve.
for p in S.rglob('*.java'):
 for name in re.findall(r'R.drawable.(potuzno_\w+)',p.read_text()):
  assert (S/f'res/drawable/{name}.xml').exists(), (p,name)
for p in (ROOT/'overlay').rglob('*.xml'):
 for name in re.findall(r'@drawable/(potuzno_\w+)',p.read_text()):
  assert (S/f'res/drawable/{name}.xml').exists(),(p,name)
# Compare the exact resulting Git trees for pristine installation and old-brand upgrade.
with tempfile.TemporaryDirectory() as d:
 env=dict(os.environ,GIT_INDEX_FILE=d+'/index')
 def git(*args):return subprocess.check_output(['git','-C',str(C),*args],env=env)
 git('read-tree','HEAD');git('apply','--cached',str(ROOT/'patches/potuzhno.patch')); clean=git('write-tree')
 git('read-tree','HEAD');git('apply','--cached','--recount',str(ROOT/'patches/previous/12.10.6.patch'))
 git('apply','--cached',str(ROOT/'patches/upgrade-12.10.6.patch')); upgraded=git('write-tree')
 assert clean==upgraded, 'Upgrade differs from a fresh installation'
print('PASS: launcher aliases, adaptive/density assets, drawable references, clean and upgraded tree equivalence')
