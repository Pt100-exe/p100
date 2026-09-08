from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[1]/'tmp/pdf_build'
pages=sorted(ROOT.glob('page-*.png'))
for start in range(0,len(pages),12):
    selection=pages[start:start+12];canvas=Image.new('RGB',(1600,1740),'#D8DDE1');draw=ImageDraw.Draw(canvas)
    for i,p in enumerate(selection):
        im=Image.open(p).convert('RGB');im.thumbnail((388,550))
        x=(i%4)*400+6;y=(i//4)*580+24
        canvas.paste(im,(x,y));draw.text((x,y-19),p.stem,fill='black')
    canvas.save(ROOT/f'contact_{start//12+1:02}.jpg',quality=90)
print(len(pages),'pages;', (len(pages)+11)//12,'contact sheets')
