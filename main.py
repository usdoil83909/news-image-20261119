"""A deterministic, self-contained vector-type newspaper. Python standard library only."""

import hashlib
import json
import math
import os
import struct
import zlib

# Hershey futural coordinates, ASCII 32..126. Each first pair is the
# left/right bearing; ' R' lifts the pen. Coordinates are relative to 'R'.
SANS_COORDINATES = r"""JZ
MWRFRT RRYQZR[SZRY
JZNFNM RVFVM
H]SBLb RYBRb RLOZO RKUYU
H\PBP_ RTBT_ RYIWGTFPFMGKIKKLMMNOOUQWRXSYUYXWZT[P[MZKX
F^[FI[ RNFPHPJOLMMKMIKIIJGLFNFPGSHVHYG[F RWTUUTWTYV[X[ZZ[X[VYTWT
E_\O\N[MZMYNXPVUTXRZP[L[JZIYHWHUISJRQNRMSKSIRGPFNGMIMKNNPQUXWZY[[[\Z\Y
MWRHQGRFSGSIRKQL
KYVBTDRGPKOPOTPYR]T`Vb
KYNBPDRGTKUPUTTYR]P`Nb
JZRLRX RMOWU RWOMU
E_RIR[ RIR[R
NVSWRXQWRVSWSYQ[
E_IR[R
NVRVQWRXSWRV
G][BIb
H\QFNGLJKOKRLWNZQ[S[VZXWYRYOXJVGSFQF
H\NJPISFS[
H\LKLJMHNGPFTFVGWHXJXLWNUQK[Y[
H\MFXFRNUNWOXPYSYUXXVZS[P[MZLYKW
H\UFKTZT RUFU[
H\WFMFLOMNPMSMVNXPYSYUXXVZS[P[MZLYKW
H\XIWGTFRFOGMJLOLTMXOZR[S[VZXXYUYTXQVOSNRNOOMQLT
H\YFO[ RKFYF
H\PFMGLILKMMONSOVPXRYTYWXYWZT[P[MZLYKWKTLRNPQOUNWMXKXIWGTFPF
H\XMWPURRSQSNRLPKMKLLINGQFRFUGWIXMXRWWUZR[P[MZLX
NVROQPRQSPRO RRVQWRXSWRV
NVROQPRQSPRO RSWRXQWRVSWSYQ[
F^ZIJRZ[
E_IO[O RIU[U
F^JIZRJ[
I[LKLJMHNGPFTFVGWHXJXLWNVORQRT RRYQZR[SZRY
E`WNVLTKQKOLNMMPMSNUPVSVUUVS RQKOMNPNSOUPV RWKVSVUXVZV\T]Q]O\L[JYHWGTFQFNGLHJJILHOHRIUJWLYNZQ[T[WZYYZX RXKWSWUXV
I[RFJ[ RRFZ[ RMTWT
G\KFK[ RKFTFWGXHYJYLXNWOTP RKPTPWQXRYTYWXYWZT[K[
H]ZKYIWGUFQFOGMILKKNKSLVMXOZQ[U[WZYXZV
G\KFK[ RKFRFUGWIXKYNYSXVWXUZR[K[
H[LFL[ RLFYF RLPTP RL[Y[
HZLFL[ RLFYF RLPTP
H]ZKYIWGUFQFOGMILKKNKSLVMXOZQ[U[WZYXZVZS RUSZS
G]KFK[ RYFY[ RKPYP
NVRFR[
JZVFVVUYTZR[P[NZMYLVLT
G\KFK[ RYFKT RPOY[
HYLFL[ RL[X[
F^JFJ[ RJFR[ RZFR[ RZFZ[
G]KFK[ RKFY[ RYFY[
G]PFNGLIKKJNJSKVLXNZP[T[VZXXYVZSZNYKXIVGTFPF
G\KFK[ RKFTFWGXHYJYMXOWPTQKQ
G]PFNGLIKKJNJSKVLXNZP[T[VZXXYVZSZNYKXIVGTFPF RSWY]
G\KFK[ RKFTFWGXHYJYLXNWOTPKP RRPY[
H\YIWGTFPFMGKIKKLMMNOOUQWRXSYUYXWZT[P[MZKX
JZRFR[ RKFYF
G]KFKULXNZQ[S[VZXXYUYF
I[JFR[ RZFR[
F^HFM[ RRFM[ RRFW[ R\FW[
H\KFY[ RYFK[
I[JFRPR[ RZFRP
H\YFK[ RKFYF RK[Y[
KYOBOb RPBPb ROBVB RObVb
KYKFY^
KYTBTb RUBUb RNBUB RNbUb
JZRDJR RRDZR
I[Ib[b
NVSKQMQORPSORNQO
I\XMX[ RXPVNTMQMONMPLSLUMXOZQ[T[VZXX
H[LFL[ RLPNNPMSMUNWPXSXUWXUZS[P[NZLX
I[XPVNTMQMONMPLSLUMXOZQ[T[VZXX
I\XFX[ RXPVNTMQMONMPLSLUMXOZQ[T[VZXX
I[LSXSXQWOVNTMQMONMPLSLUMXOZQ[T[VZXX
MYWFUFSGRJR[ ROMVM
I\XMX]W`VaTbQbOa RXPVNTMQMONMPLSLUMXOZQ[T[VZXX
I\MFM[ RMQPNRMUMWNXQX[
NVQFRGSFREQF RRMR[
MWRFSGTFSERF RSMS^RaPbNb
IZMFM[ RWMMW RQSX[
NVRFR[
CaGMG[ RGQJNLMOMQNRQR[ RRQUNWMZM\N]Q][
I\MMM[ RMQPNRMUMWNXQX[
I\QMONMPLSLUMXOZQ[T[VZXXYUYSXPVNTMQM
H[LMLb RLPNNPMSMUNWPXSXUWXUZS[P[NZLX
I\XMXb RXPVNTMQMONMPLSLUMXOZQ[T[VZXX
KXOMO[ ROSPPRNTMWM
J[XPWNTMQMNNMPNRPSUTWUXWXXWZT[Q[NZMX
MYRFRWSZU[W[ ROMVM
I\MMMWNZP[S[UZXW RXMX[
JZLMR[ RXMR[
G]JMN[ RRMN[ RRMV[ RZMV[
J[MMX[ RXMM[
JZLMR[ RXMR[P_NaLbKb
J[XMM[ RMMXM RM[X[
KYTBRCQDPFPHQJRKSMSOQQ RRCQEQGRISJTLTNSPORSTTVTXSZR[Q]Q_Ra RQSSUSWRYQZP\P^Q`RaTb
NVRBRb
KYPBRCSDTFTHSJRKQMQOSQ RRCSESGRIQJPLPNQPURQTPVPXQZR[S]S_Ra RSSQUQWRYSZT\T^S`RaPb
F^IUISJPLONOPPTSVTXTZS[Q RISJQLPNPPQTTVUXUZT[Q[O"""

# rowmans.jhf shares its letters with futural.jhf. These are every
# differing ASCII glyph in that supplied file, including its punctuation.
ROMAN_COORDINATES = {
    '*': 'JZRFRR RMIWO RWIMO',
    ',': 'MWSZR[QZRYSZS\\R^Q_',
    '.': 'MWRYQZR[SZRY',
    ':': 'MWRMQNROSNRM RRYQZR[SZRY',
    ';': 'MWRMQNROSNRM RSZR[QZRYSZS\\R^Q_',
    '^': 'JZPLRITL RMORJWO RRJR[',
    '_': 'JZJ]Z]',
    '`': 'MWSFRGQIQKRLSKRJ',
}

REGIONS = ['AMERICAS', 'EUROPE', 'MIDDLE EAST', 'AFRICA', 'ASIA',
           'RUSSIA & UKRAINE', 'TECHNOLOGY & BUSINESS']
# The supplied reports, unedited. Tuple fields: id, region index, headline,
# detail, source. Keeping the detail also makes this entry's data auditable.
REPORTS = [
 (1,0,'Senate Republicans block Democratic effort to end war in Iran','Forty-eight-to-fifty-one vote was first since midterm losses','AP'),
 (2,0,'House Democrats nominate Hakeem Jeffries for House speaker','He would be first African American to hold the role','Reuters'),
 (3,0,'Appeals court halts order restoring deportation protections for Venezuelans','Ninth Circuit pause blocks reinstatement of Temporary Protected Status','AP'),
 (4,0,'US defence chief Hegseth signs military pact with Venezuela in Caracas','Military cooperation resumes after 21-year freeze, leader says','LatinNews'),
 (5,0,'Trump official floated ceding Guyanese territory to Venezuela','State Department planning director raised idea in September, sources say','Reuters'),
 (6,1,'European allies rally for Ukraine at Berlin summit','Coalition of the Willing reaffirms binding security guarantees','Reuters'),
 (7,1,'Netherlands summons Russian ambassador after Kyiv embassy hit','Projectile landed behind Dutch embassy; nobody injured','Reuters'),
 (8,1,'EU proposes 45-billion-euro loan to bridge Ukraine funding gap','Loan covers part of 70-billion-euro shortfall for next year','Reuters'),
 (9,1,'French Greens ready to back Melenchon presidential bid','Hard-left leader gains potential ally for 2027 race','Reuters'),
 (10,1,'France raises bird flu alert to maximum level','Poultry confinement rules take effect Friday amid European spread','Reuters'),
 (11,1,'Bundesbank says German growth and inflation set to accelerate','Fiscal stimulus drives expansion; inflation to rise sharply in 2027','Reuters'),
 (12,1,'European stocks rebound as Anthropic IPO lifts tech optimism','ASML and chipmakers lead gains after three losing sessions','Reuters'),
 (13,2,'Suspected Houthi missile strikes Riyadh skyscraper housing wealth fund','Saudi sovereign wealth fund headquarters hit, no major casualties reported','Reuters'),
 (14,2,'Israel ends first major Gaza ground operation since ceasefire','Operation in Nuseirat targeted tunnel; thousands displaced again','Al Jazeera'),
 (15,2,'Saudi-led coalition says it repelled Houthi attacks on kingdom','Escalation follows strike on Riyadh fund headquarters tower','Al Jazeera'),
 (16,2,'Trump says US will see what happens with Iran after January 1','Comments delay decision on renewed major strikes into next year','Reuters'),
 (17,2,'UNICEF warns water production nearly halved in Yemeni city of Taiz','More than 800,000 people cut off from humanitarian assistance','Al Jazeera'),
 (18,2,'Mosque torched in northern Israel sparks backlash against Netanyahu','Suspected arson hits Palestinian Arab village of al-Dahi','Al Jazeera'),
 (19,3,'Dozens missing as migrant boat capsizes off Senegal coast','Boast bound for Europe overturned, local NGO says','Reuters'),
 (20,3,'Sudanese army bombs RSF intelligence headquarters in Nyala','Strikes also hit command facility and civilian administration building','Sudan Tribune'),
 (21,3,"RSF claims capture of Bau district in Sudan's Blue Nile state",'Army units fled toward state capital, paramilitary group claims','Sudan Tribune'),
 (22,3,'Ethiopia and Eritrea amass forces along border, raising war fears','Overnight drone and artillery strikes reported around Badme','Reuters'),
 (23,3,'Nigerian military rescues 125 kidnap victims, dismantles terror camps','United States commends operation ahead of 2027 elections','Premium Times'),
 (24,4,'Trump, Xi, Putin hold first-ever trilateral summit in Shenzhen','Leaders met on sidelines of APEC summit in southern China','Reuters'),
 (25,4,'Three powers issue peace declaration pledging nuclear restraint','Statement says nuclear war cannot be won and must never be fought','Reuters'),
 (26,4,"Japan's PM Takaichi cuts isolated figure at APEC summit",'China rift over Taiwan remarks brought muted reception, no bilateral','Reuters'),
 (27,4,'Taiwan reports two Russian military aircraft near island','Tu-95 bombers flew past east coast, second time this week','Reuters'),
 (28,4,'Indonesia parliament passes asset forfeiture bill into law','Law allows seizing assets in certain criminal cases','Reuters'),
 (29,4,'Violence rises in Bangladesh as Hasina supporters escalate protests',"Protests by former PM's supporters fuel instability",'Reuters'),
 (30,4,'South Korea becomes fourth country to reach one trillion dollars in exports','AI chip boom powers milestone, government data shows','Reuters'),
 (31,4,"South Korea's Supreme Court orders retrial for ex-PM Han",'Ruling concerns his role in martial law attempt','Reuters'),
 (32,5,'Third Ukrainian strike in four days halts Kerch Bridge traffic','Overnight attack stopped rail traffic; repairs resumed later Thursday','AP'),
 (33,5,'Putin rules out Black Sea and energy truce after bridge strikes',"Vows response far more painful than Kyiv's attack",'Reuters'),
 (34,5,'Putin invites European envoys to Moscow on Ukraine talks','Says Europe must clarify position before format is decided','Reuters'),
 (35,5,'Trump says nuclear arms limits with China and Russia will be hard','Joint dialogue on reducing nuclear risks agreed at summit','Reuters'),
 (36,5,'Russian strikes kill two, wound 23 across 12 Ukrainian regions','Kyiv says Russia launched Oniks missiles and 98 drones overnight','AP'),
 (37,5,"Ukrainian drone attacks nearly halve Russia's November oil refining",'Campaign targets refining capacity, sources tell Reuters','Reuters'),
 (38,5,'Kremlin says Ukraine was main topic at Trump-Putin meeting',"Aide Ushakov says Putin's mood after talks was excellent",'Reuters'),
 (39,6,'Anthropic debut fails to revive AI trade; Dow closes below 50,000','Nasdaq falls 2.25 percent to 23,879.20 in broad selloff','CNBC'),
 (40,6,'Anthropic raises 81 billion dollars in largest IPO on record','Claude maker priced at 83 dollars, closed up 17 percent','CNBC'),
 (41,6,'Nvidia slides 28 percent this month amid CEO Huang resignation fallout','Investors question profitability of heavy AI infrastructure spending','CNBC'),
 (42,6,'Gold sinks over 3 percent to more-than-one-year low','Hawkish Fed signals lift dollar and Treasury yields','Reuters'),
 (43,6,'Bitcoin slides under 62,000 dollars, down about 25 percent in a month','Anthropic-led tech selloff extends crypto slump','Bitcoin Magazine'),
 (44,6,'Oil prices slide as hawkish Fed signals lift the dollar','Global stocks also slip ahead of Anthropic market debut','Reuters'),
]
BTC = [('2026-11-13',68661), ('2026-11-14',65615), ('2026-11-15',64795),
       ('2026-11-16',65030), ('2026-11-17',63795), ('2026-11-18',63253),
       ('2026-11-19',62942)]

NAVY = (12,21,38)
PANEL = (22,35,63)
WHITE = (242,245,250)
AMBER = (242,169,59)
GREY = (143,160,188)
RULE = (47,63,87)
SCALE = 2
SIDE = 1024 * SCALE


def parse_glyph(encoded):
    left, right = (ord(c)-82 for c in encoded[:2])
    strokes = []
    for stroke in encoded[2:].split(' R'):
        assert len(stroke) % 2 == 0
        if stroke:
            strokes.append(tuple((ord(stroke[i])-82, ord(stroke[i+1])-82)
                                 for i in range(0, len(stroke), 2)))
    return left, right, tuple(strokes)


SANS = {chr(i+32): parse_glyph(s) for i,s in enumerate(SANS_COORDINATES.splitlines())}
assert len(SANS) == 95
ROMAN = dict(SANS)
ROMAN.update({c: parse_glyph(s) for c,s in ROMAN_COORDINATES.items()})
# Newspaper headlines use a condensed cut, retaining full cap height.
HEADLINE = {c: (left*0.58,right*0.58,
               tuple(tuple((x*0.58,y) for x,y in stroke) for stroke in strokes))
            for c,(left,right,strokes) in SANS.items()}


class Page:
    def __init__(self):
        self.pixels = bytearray(bytes(NAVY) * SIDE * SIDE)
        self.text_boxes = []
        self.rendered = []
        self.panels = []

    def rect(self, x, y, w, h, color):
        x0,y0,x1,y1 = (round(v*SCALE) for v in (x,y,x+w,y+h))
        assert 0 <= x0 <= x1 <= SIDE and 0 <= y0 <= y1 <= SIDE
        row = bytes(color) * (x1-x0)
        for yy in range(y0,y1):
            start = (yy*SIDE+x0)*3
            self.pixels[start:start+len(row)] = row

    def line(self, x0,y0,x1,y1,color,thickness=0.7):
        x0,y0,x1,y1 = (round(v*SCALE) for v in (x0,y0,x1,y1))
        dx,dy = abs(x1-x0),-abs(y1-y0)
        sx,sy = (1 if x0<x1 else -1),(1 if y0<y1 else -1)
        err = dx+dy
        # Parallel offsets yield thicker strokes without external raster libraries.
        n = max(1,round(thickness*SCALE))
        offsets = [(i-(n-1)//2,0) if dx < -dy else (0,i-(n-1)//2)
                   for i in range(n)]
        rgb = bytes(color)
        while True:
            for ox,oy in offsets:
                xx,yy = x0+ox,y0+oy
                assert 0 <= xx < SIDE and 0 <= yy < SIDE
                p = (yy*SIDE+xx)*3
                self.pixels[p:p+3] = rgb
            if x0==x1 and y0==y1:
                break
            e = 2*err
            if e >= dy:
                err += dy
                x0 += sx
            if e <= dx:
                err += dx
                y0 += sy

    def text(self, text,x,y,size,color=WHITE,bold=False,font=SANS,width=None):
        # size is cap height; y is the cap top. F=-12, [=9.
        advance = measure(text,size,font)
        if width is not None:
            assert advance <= width+0.001, (text,advance,width)
        cursor = x
        scale = size/21
        ink = []
        for ch in text:
            left,right,strokes = font[ch]
            for stroke in strokes:
                pts = [(cursor+(px-left)*scale,y+(py+12)*scale) for px,py in stroke]
                ink.extend(pts)
                for p,q in zip(pts,pts[1:]):
                    self.line(*p,*q,color,1.0 if bold else 0.55)
            cursor += (right-left)*scale
        if ink:
            bounds = (min(p[0] for p in ink)-0.5,min(p[1] for p in ink)-0.5,
                      max(p[0] for p in ink)+0.5,max(p[1] for p in ink)+0.5)
            assert 0 <= bounds[0] < bounds[2] <= 1024
            assert 0 <= bounds[1] < bounds[3] <= 1024
            if width is not None:
                assert bounds[2] <= x+width+0.5, (text,bounds,x+width)
            self.text_boxes.append((text,bounds))
        return advance

    def png(self):
        raw = bytearray()
        stride = SIDE*3
        for y in range(1024):
            raw.append(0)
            a = (2*y)*stride
            b = a+stride
            for x in range(1024):
                p = x*6
                for c in range(3):
                    raw.append((self.pixels[a+p+c]+self.pixels[a+p+3+c]+
                                self.pixels[b+p+c]+self.pixels[b+p+3+c]+2)//4)
        def chunk(kind,data):
            return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
        return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1024,1024,8,2,0,0,0))+
                chunk(b'IDAT',zlib.compress(bytes(raw),9))+chunk(b'IEND',b''))


def measure(text,size,font=SANS):
    return sum(font[c][1]-font[c][0] for c in text)*size/21


def wrap(text,size,width,font=SANS):
    lines = []
    for word in text.split():
        assert measure(word,size,font) <= width, word
        if lines and measure(lines[-1]+' '+word,size,font) <= width:
            lines[-1] += ' '+word
        else:
            lines.append(word)
    assert ' '.join(lines) == text
    return lines


def region_panel(page,region,x,y,w,h,columns=1):
    first_box = len(page.text_boxes)
    stories = [r for r in REPORTS if r[1]==region]
    page.rect(x,y,w,h,PANEL)
    page.panels.append((x,y,x+w,y+h))
    tag = REGIONS[region]
    tag_size = min(10.2, (w-56)*21/sum(SANS[c][1]-SANS[c][0] for c in tag))
    page.text(tag,x+12,y+12,tag_size,AMBER,bold=True,width=w-48)
    count = '%02d' % len(stories)
    page.text(count,x+w-12-measure(count,8),y+13,8,GREY)
    page.rect(x+12,y+30,w-24,1,AMBER)
    inner_width = (w-24-(columns-1)*20)/columns
    batches = [stories[i*math.ceil(len(stories)/columns):(i+1)*math.ceil(len(stories)/columns)]
               for i in range(columns)]
    # Use one headline size everywhere. Long headlines receive extra lines,
    # preserving every word rather than squeezing or abbreviating the report.
    size = 10.4
    leading = 16
    for col,batch in enumerate(batches):
        tx = x+12+col*(inner_width+20)
        headline_width = inner_width-9
        plans = [(r,wrap(r[2],size,headline_width,HEADLINE)) for r in batch]
        assert all(1 <= len(lines) <= 2 for _,lines in plans), tag
        needed = sum(len(lines)*leading+12 for r,lines in plans)
        available = h-44
        assert needed <= available, (tag,needed,available)
        gap = (available-needed)/len(batch)
        yy = y+42
        for report,lines in plans:
            item_top = yy
            page.rect(tx,yy,2,8,AMBER)
            for text in lines:
                page.text(text,tx+9,yy,size,bold=True,font=HEADLINE,width=headline_width)
                yy += leading
            page.text(report[4].upper(),tx+9,yy+1,6.8,GREY,width=headline_width)
            yy += 12+gap
            assert yy <= y+h+0.001, (tag,report[0],yy,y+h)
            assert yy > item_top
            page.rendered.append(report[0])
        if col < columns-1:
            page.rect(tx+inner_width+10,y+42,0.5,h-54,RULE)
    for text,(left,top,right,bottom) in page.text_boxes[first_box:]:
        assert x <= left < right <= x+w, (tag,text,'horizontal bounds')
        assert y <= top < bottom <= y+h, (tag,text,'vertical bounds')


def hero(page):
    x,y,w,h = 24,106,976,118
    page.rect(x,y,w,h,PANEL)
    page.rect(x,y,4,h,AMBER)
    page.text('THE LEAD / ASIA',x+16,y+12,8,AMBER,bold=True)
    report = REPORTS[23]
    lines = wrap(report[2],21,668,ROMAN)
    assert 2 <= len(lines) <= 3
    yy = y+28
    for line in lines:
        page.text(line,x+16,yy,21,bold=True,font=ROMAN,width=668)
        yy += 30
    page.text(report[3],x+16,yy+2,9,GREY,width=668)
    page.text(report[4].upper(),x+16,yy+18,6.8,GREY)
    assert yy+25 <= y+h
    if BTC:
        bx,by,bw,bh = 740,118,244,94
        page.rect(bx,by,1,bh,RULE)
        page.text('BITCOIN / 7 DAILY CLOSES',bx+16,by,7,GREY,width=bw-24)
        page.text(f'{BTC[-1][1]:,} USD',bx+16,by+17,17,AMBER,bold=True)
        values = [v for d,v in BTC]
        low,high = min(values),max(values)
        points = [(bx+16+i*34,by+51+(high-v)/(high-low)*24) for i,v in enumerate(values)]
        for p,q in zip(points,points[1:]):
            page.line(*p,*q,AMBER,1.1)
        for px,py in points:
            page.rect(px-1,py-1,2,2,WHITE)
        for i,(date,close) in enumerate(BTC):
            page.text(date[-2:],bx+12+i*34,by+83,5.5,GREY)


def main():
    page = Page()
    page.text('WORLD NEWS IN ONE IMAGE',24,22,10,AMBER,bold=True)
    page.text('44 STORIES / 7 REGIONS',1000-measure('44 STORIES / 7 REGIONS',9),23,9,WHITE)
    page.text('THURSDAY 19 NOVEMBER 2026',24,48,29,bold=True,font=ROMAN,width=880)
    page.text('make.fun',1000-measure('make.fun',10),78,10,GREY)
    page.rect(24,96,976,2,AMBER)
    hero(page)
    # Four columns, two tiers. Asia spans two columns in the lower tier.
    xs = [24,272,520,768]
    for i,region in enumerate([0,1,2,3]):
        region_panel(page,region,xs[i],240,232,352)
    region_panel(page,4,24,608,480,364,columns=2)
    region_panel(page,5,520,608,232,364)
    region_panel(page,6,768,608,232,364)
    page.rect(24,988,976,1,AMBER)
    page.text('SOURCES: 44 REPORTS ACROSS 7 REGIONS / ALL FACTS AS REPORTED 19 NOV 2026',24,1000,7,GREY,width=880)
    page.text('make.fun',1000-measure('make.fun',9),998,9,AMBER)
    assert sorted(page.rendered) == list(range(1,45))
    # Compare actual glyph ink rectangles, including descenders and stroke width.
    for i,(a,box) in enumerate(page.text_boxes):
        for b,other in page.text_boxes[i+1:]:
            overlap = min(box[2],other[2]) > max(box[0],other[0]) and min(box[3],other[3]) > max(box[1],other[1])
            assert not overlap, ('text overlap',a,b,box,other)
    png = page.png()
    assert len(png) <= 1048576
    output = os.environ.get('MAKEFUN_OUTPUT_DIR','/output')
    os.makedirs(output,exist_ok=True)
    path = os.path.join(output,'entry.png')
    with open(path,'wb') as f:
        f.write(png)
    print(json.dumps({'output':path,'bytes':len(png),'sha256':hashlib.sha256(png).hexdigest(),
                      'stories':len(page.rendered),'text_bounds_checked':len(page.text_boxes),
                      'layout':'four columns; seven regional panels in two tiers; double-width Asia; summit hero and Bitcoin sparkline'},sort_keys=True))


if __name__ == '__main__':
    main()
