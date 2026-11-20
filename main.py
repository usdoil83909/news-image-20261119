"""A deterministic, self-contained vector-type newspaper. Python standard library only."""

import base64
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

# Natural Earth 1:110m, 180 by 90 samples packed row-major, high bit first.
LANDMASK_B64 = (
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAAAAAAAAAAP//7//wAAAAAAAAAAAAAAAAAAAAAAB///////AA/wDwAAHgAAAAAAAAAAAHf///'
    '///4AB/gAAAAD+AAAAAAAAAAD/v/8////4AA/gAA+ADf4AGAAAAAAAH///4A///4AAAAAH4Af/8AP8AA'
    'AAAAH///+Af//wAAAAAeD////+H4AAwH/gf////4P//wAAD8AeH///////wRw//////9/4P//AAAP/nP'
    '//////////+///////3/H/wuAAf//////////////////////+H/B/AB//////////////Df/////7/8'
    'D8A8AP//////////////A//////gf8B4AAAP/////////////8A/8////wP+AAAAGP5///////////fQ'
    'AHwB///8H/AAAAPD7/////////8B8AAeAB////v/wAAAfD//////////9B8AAAAB//////4AAAfv////'
    '///////B4AAAAAf/////4AAAX////////////AwAAAAAf/////8AAAH////////////gAAAAAAH/////'
    '8AAAH////////////AAAAAAAD/////gAAAB//7////////7gAAAAAAH////8AAAAf//7f///////3gAA'
    'AAAAH////wAAAAfy/////////+HAAAAAAAD///+AAAAAfi/////////+GAAAAAAAD///+AAAAAf/7///'
    '/////+OAAAAAAAB///+AAAAAP/Bz///////n+AAAAAAAA///4AAAAAf/zB///////jwAAAAAAAAf//wA'
    'AAAAf//////////hAAAAAAAAAP/9wAAAAB///////////wAAAAAAAAAP/A8AAAAD///////////gAAAA'
    'AAAAAH/AcAAAAD///////////gAAAAACAAAD/B8AAAAH//////H///+gAAAAADgAAAfPeAAAAH//////'
    'B///wgAAAAABgAAAf+P8AAAH////v+A/j/wwAAAAAAAAAAP+EsAAAH/////+A/B/hwAAAAAAAAAABfgA'
    'AAAH/////4A+B/hwAAAAAAAAAAAPgwAAAH/////wAeAfg4AAAAAAAAAAADj/AAAH/////wAcAXh4AAAA'
    'AAAAAAAB//gAAD/////wAOAbDcAAAAAAAAAAAAf/4AAB/////gAOAcC8AAAAAAAAAAAAH/+AAAfv///g'
    'ACB8HIAAAAAAAAAAAAP/+AAAAD///AAAA8/EAAAAAAAAAAAAf//AAAAD//+AAAAe/+AAAAAAAAAAAAf/'
    '/wAAAD//8AAAAO/38AAAAAAAAAAAf//+AAAD//4AAAAPf//mAAAAAAAAAAf///gAAB//wAAAAHHw/vAA'
    'AAAAAAAAf///gAAA//wAAAAD8AX9wAAAAAAAAAP///gAAA//wAAAAAf8PcYAAAAAAAAAP///AAAA//4A'
    'AAAAA57cMAAAAAAAAAH///AAAA//5wAAAAAH7AAAAAAAAAAAH//+AAAB//7wAAAAAP7gBAgAAAAAAAB/'
    '/+AAAB///wAAAAAf/wBDAAAAAAAAA//+AAAB//jgAAAAB//4ADAAAAAAAAA//8AAAA//HgAAAAH//4DA'
    'AAAAAAAAA//8AAAAf/HAAAAAP//8BAAAAAAAAAA//gAAAAf/HAAAAAP//+AAAAAAAAAAA//AAAAAf+AA'
    'AAAAP//+AAAAAAAAAAA//AAAAAP+AAAAAAH//+AAAAAAAAAAA/+AAAAAP8AAAAAAH//+AAAAAAAAAAA/'
    '8AAAAAP4AAAAAAH8/+AAAAAAAAAAB/8AAAAAGAAAAAAAHQf8AMAAAAAAAAB/wAAAAAAAAAAAAAAAH8AP'
    'AAAAAAAAB/wAAAAAAAAAAAAAAADwAPAAAAAAAAD+AAAAAAAAAAAAAAAAA4AeAAAAAAAAD+AAAAAAAAAA'
    'AAAAAAA4A4AAAAAAAAD8AAAAAAAAAAAAAAAAAABwAAAAAAAAD8AAAAAAAAAAAAAAAAAABgAAAAAAAAD8'
    'AAAAAAAAAADAAAAAAAAAAAAAAAAADxwAAAAAAAAAAAAAAAAAAAAAAAAAAAD5gAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAB8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAH'
    'gAAAAAAAAOAAAGIAQAAAAAAAAAAAAOAAAAAAAAD/+D/////wAAAAAAAAAAA+AAAAAEsH//+///////wA'
    'AAAAAAPAD/AAAA///////////////wAAAAPkP///AAAH///////////////wAAD///////AAAf//////'
    '/////////AAD///////wAgf///////////////+AAP//////+BD4/////////////////AAB////////'
    'v/////////////////4ABAf//////////////////////////g//////////////////////////////'
    '////////////////////////////////////////////////////////////'
)

# Panel and map key order. The global business desk only appears in the key.
REGIONS = (
    ('AMERICAS', (0.28, 0.45)), ('EUROPE', (0.51, 0.30)),
    ('RUSSIA & UKRAINE', (0.65, 0.30)), ('MIDDLE EAST', (0.57, 0.45)),
    ('AFRICA', (0.55, 0.60)), ('ASIA', (0.75, 0.45)),
    ('TECHNOLOGY & BUSINESS', None),
)
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

# Short display headlines keyed to the original reports above.
PANEL_STORIES = (
    ((4, 'US and Venezuela sign military pact'),
     (1, 'US Senate blocks bid to end Iran war'),
     (5, 'US aide eyed ceding Guyana land')),
    ((6, 'Allies back Ukraine at Berlin summit'),
     (8, 'EU eyes EUR 45bn Ukraine loan'),
     (10, 'France: Maximum bird flu alert')),
    ((33, 'Putin rejects sea and energy truce'),
     (36, 'Russian strikes: 2 dead, 23 hurt'),
     (37, 'Strikes nearly halve Russian oil refining')),
    ((13, 'Suspected Houthi hit on Riyadh'),
     (14, 'Israel ends Gaza ground operation'),
     (17, 'Taiz water output nearly halves')),
    ((22, 'Ethiopia-Eritrea war fears rise'),
     (19, 'Dozens missing off Senegal'),
     (23, 'Nigeria rescues 125 kidnap victims')),
    ((27, 'Russian aircraft near Taiwan'),
     (29, 'Bangladesh protest violence rises'),
     (30, 'S. Korea hits $1tn in exports')),
    ((40, 'Anthropic IPO'),
     (41, 'Nvidia -28%'),
     (42, 'Gold drops >3%')),
)

NAVY = (12,21,38)
PANEL = (22,35,63)
LEAD_PANEL = (32,48,78)
WHITE = (242,245,250)
BODY = (216,225,240)
AMBER = (242,169,59)
GREY = (167,183,208)
RULE = (47,63,87)
CHART_FILL = (59,57,65)
LAND = (58,74,107)
MAP_WATER = (16,27,49)
GUTTER = 8
EDGE = 24
LEFT_WIDTH = 476
RIGHT_X = EDGE + LEFT_WIDTH + GUTTER
RIGHT_WIDTH = 1024 - EDGE - RIGHT_X
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


def condensed(width):
    return {c: (left*width,right*width,
                tuple(tuple((x*width,y) for x,y in stroke) for stroke in strokes))
            for c,(left,right,strokes) in SANS.items()}


HEADLINE = condensed(0.72)
TAG = condensed(0.86)

# Add bracket-like terminals to the masthead capitals and widen their
# bearings slightly where the serifs reach beyond the original glyphs.
MASTHEAD = dict(ROMAN)
for letter, terminals in {
    'A': ((-8, 9), (8, 9)), 'B': ((-7, -12), (-7, 9)),
    'D': ((-7, -12), (-7, 9)), 'E': ((-6, -12), (-6, 9)),
    'H': ((-7, -12), (7, -12), (-7, 9), (7, 9)),
    'M': ((-8, -12), (8, -12), (-8, 9), (8, 9)),
    'N': ((-7, -12), (7, -12), (-7, 9)),
    'R': ((-7, -12), (-7, 9), (7, 9)), 'T': ((0, 9),),
    'U': ((-7, -12), (7, -12)), 'V': ((-8, -12), (8, -12)),
    'Y': ((-8, -12), (8, -12), (0, 9)), '1': ((1, 9),),
}.items():
    if terminals:
        left, right, strokes = ROMAN[letter]
        serifs = tuple(((x-2.7, y), (x+2.7, y)) for x, y in terminals)
        MASTHEAD[letter] = (min(left, min(x-4 for x, y in terminals)),
                            max(right, max(x+4 for x, y in terminals)), strokes + serifs)


def raster_line(x0, y0, x1, y1, weight):
    # Center the parallel tracks on the path, also for even weights.
    steep = abs(y1-y0) > abs(x1-x0)
    shift = (weight-1)/2
    x0,x1 = (round(x*SCALE-(shift if steep else 0)) for x in (x0,x1))
    y0,y1 = (round(y*SCALE-(0 if steep else shift)) for y in (y0,y1))
    return x0,y0,x1,y1,steep


class Page:
    def __init__(self):
        self.pixels = bytearray(bytes(NAVY) * SIDE * SIDE)
        self.text_boxes = []
        self.rendered = []

    def rect(self, x, y, w, h, color):
        x0,y0,x1,y1 = (round(v*SCALE) for v in (x,y,x+w,y+h))
        assert 0 <= x0 <= x1 <= SIDE and 0 <= y0 <= y1 <= SIDE
        row = bytes(color) * (x1-x0)
        for yy in range(y0,y1):
            start = (yy*SIDE+x0)*3
            self.pixels[start:start+len(row)] = row

    def dot(self, x, y, radius, color):
        for dy in range(-round(radius*SCALE), round(radius*SCALE)+1):
            half_width = math.sqrt(max(0, (radius*SCALE)**2-dy**2))
            span = math.floor(half_width)
            self.rect((round(x*SCALE)-span)/SCALE, (round(y*SCALE)+dy)/SCALE,
                      (2*span+1)/SCALE, 1/SCALE, color)

    def line(self, x0,y0,x1,y1,color,weight):
        return self.draw_line(*raster_line(x0,y0,x1,y1,weight),color,weight)

    def draw_line(self, x0,y0,x1,y1,steep,color,weight):
        offsets = [(i,0) if steep else (0,i) for i in range(weight)]
        ox,oy = offsets[-1]
        bounds = (min(x0,x1),min(y0,y1),max(x0,x1)+ox+1,max(y0,y1)+oy+1)
        assert 0 <= bounds[0] < bounds[2] <= SIDE and 0 <= bounds[1] < bounds[3] <= SIDE
        dx,dy = abs(x1-x0),-abs(y1-y0)
        sx,sy = (1 if x0<x1 else -1),(1 if y0<y1 else -1)
        err = dx+dy
        rgb = bytes(color)
        while True:
            for ox,oy in offsets:
                p = ((y0+oy)*SIDE+x0+ox)*3
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
        return bounds

    def text(self, text,x,y,size,color=WHITE,weight=2,font=SANS,width=None,tracking=0,
             *, ink_top=False):
        # Size is cap height. By default y is the cap top (F=-12, [=9).
        advance = measure(text,size,font,tracking)
        if width is not None:
            assert advance <= width+0.001, (text,advance,width)
        cursor = x
        scale = size/21
        segments = []
        for ch in text:
            left,right,strokes = font[ch]
            for stroke in strokes:
                pts = [(cursor+(px-left)*scale,(py+12)*scale+(0 if ink_top else y))
                       for px,py in stroke]
                segments.extend(raster_line(*p,*q,weight) for p,q in zip(pts,pts[1:]))
            cursor += (right-left)*scale+tracking
        if segments:
            # Align the measured raster top without rounding the strokes again.
            dy = round(y*SCALE)-min(min(s[1],s[3]) for s in segments) if ink_top else 0
            ink = [self.draw_line(x0,y0+dy,x1,y1+dy,steep,color,weight)
                   for x0,y0,x1,y1,steep in segments]
            bounds = (min(b[0] for b in ink)/SCALE,min(b[1] for b in ink)/SCALE,
                      max(b[2] for b in ink)/SCALE,max(b[3] for b in ink)/SCALE)
            if width is not None:
                assert x <= bounds[0] and bounds[2] <= x+width, (text,bounds,x,width)
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


def measure(text,size,font=SANS,tracking=0):
    return sum(font[c][1]-font[c][0] for c in text)*size/21+max(0,len(text)-1)*tracking


def wrap(text, size, width, font):
    def fits(line):
        return measure(line, size, font) <= width

    if fits(text):
        return [text]
    words = text.split()
    pairs = [(' '.join(words[:i]), ' '.join(words[i:])) for i in range(1, len(words))]
    choices = [pair for pair in pairs if all(map(fits, pair))]
    assert choices, (text, size, width)
    return min(choices, key=lambda pair: abs(measure(pair[0], size, font)
                                           - measure(pair[1], size, font)))


def card(page, x, y, w, h, color=PANEL):
    page.rect(x, y, w, h, color)
    page.rect(x, y, w, 2, AMBER)
    return len(page.text_boxes)


def check_card(page, first, x, y, w, h):
    for text, (left, top, right, bottom) in page.text_boxes[first:]:
        assert x <= left < right <= x+w, (text, 'card width')
        assert y+2 <= top < bottom <= y+h, (text, 'card height')


def chip(page, number, x, y, diameter, filled=True):
    page.dot(x, y, diameter/2, AMBER)
    if not filled:
        page.dot(x, y, diameter/2-1.25, PANEL)
    text = str(number)
    size = diameter*0.51
    page.text(text, x-measure(text, size)/2, y-size/2, size,
              NAVY if filled else AMBER, weight=3, width=diameter)


def story(page, report_id, headline, x, y, w, size, leading, *, weight=3,
          color=WHITE, font=HEADLINE, source_size=7.5):
    # A little spare width covers the ink edges on heavy and condensed glyphs.
    for line in wrap(headline, size, w-2, font):
        page.text(line, x, y, size, color, weight, font, width=w)
        y += leading
    source = REPORTS[report_id-1][4].upper()
    page.text(source, x, y+1, source_size, GREY, width=w)
    page.rendered.append(report_id)
    return y+source_size+2


REGION_ITEM_GAP = 10


def region_story(page, report_id, headline, x, y, w, size):
    for line in wrap(headline, size, w-2, HEADLINE):
        page.text(line, x, y, size, weight=3, font=HEADLINE, width=w, ink_top=True)
        y = page.text_boxes[-1][1][3]+1
    source = REPORTS[report_id-1][4].upper()
    page.text(source, x, y, 7.5, GREY, width=w, ink_top=True)
    page.rendered.append(report_id)
    return page.text_boxes[-1][1][3]+REGION_ITEM_GAP


def region_panel(page, index, x, y, w, h):
    first = card(page, x, y, w, h)
    tag, pin = REGIONS[index]
    chip(page, index+1, x+22, y+18, 19, filled=pin is not None)
    page.text(tag, x+39, y+12, 12, AMBER, weight=2, font=TAG, width=w-51)
    tx, inner = x+12, w-24
    page.rect(tx, y+32, inner, 1, AMBER)
    yy = y+(33 if pin is None else 39)
    for i, (report_id, headline) in enumerate(PANEL_STORIES[index]):
        if pin is None:
            col_width = (inner-2*GUTTER)/3
            xx = tx+i*(col_width+GUTTER)
            if i:
                page.rect(xx-GUTTER/2, y+40, 1, h-47, RULE)
            end = region_story(page, report_id, headline, xx, yy, col_width, 14)
        else:
            if i:
                page.rect(tx, yy-REGION_ITEM_GAP/2, inner, 0.5, RULE)
            end = yy = region_story(page, report_id, headline, tx, yy, inner, 12)
        assert end <= y+h, (tag, headline, end)
    check_card(page, first, x, y, w, h)


def hero(page, x, y, w, h):
    first = card(page, x, y, w, h, LEAD_PANEL)
    chip(page, 6, x+25, y+19, 21)
    page.text('THE LEAD / ASIA', x+44, y+13, 12, AMBER, weight=2, width=w-60)
    tx, inner = x+16, w-32
    end = story(page, 24, 'Trump, Xi, Putin: first trilateral in Shenzhen',
                tx, y+33, inner, 28, 41, weight=5, source_size=8)
    assert end <= y+125
    page.rect(tx, y+125, inner, 1, RULE)
    brief_width = (inner-16)/2
    page.rect(tx+brief_width+8, y+131, 1, h-136, RULE)
    end = story(page, 25, 'Three powers pledge nuclear restraint', tx, y+131,
                brief_width, 10, 14, weight=2, color=BODY)
    assert end <= y+h-3
    end = story(page, 38, 'Kremlin: Ukraine led Trump-Putin talks', tx+brief_width+16,
                y+131, brief_width, 10, 14, weight=2, color=BODY)
    assert end <= y+h-3
    check_card(page, first, x, y, w, h)


def world_map(page, x, y, w, h):
    first = card(page, x, y, w, h)
    page.text('WORLD MAP', x+16, y+18, 19, AMBER, weight=3, font=TAG, width=w-32)
    page.rect(x+16, y+49, w-32, 1, RULE)

    mx, my, mw = x+16, y+96, w-32
    mh = mw/2
    page.rect(mx, my-12, mw, mh+24, MAP_WATER)
    for i in range(1, 6):
        page.rect(mx+i*mw/6, my, 0.5, mh, RULE)
    for i in range(1, 4):
        page.rect(mx, my+i*mh/4, mw, 0.5, RULE)

    packed = base64.b64decode(LANDMASK_B64, validate=True)
    mask = ''.join(f'{byte:08b}' for byte in packed)
    assert len(mask) == 180*90
    cell = mw/180
    # Average 4x4 mask samples so each land dot has clear space around it.
    for row in range(0, 90, 4):
        rows = range(row, min(row+4, 90))
        for col in range(0, 180, 4):
            land_samples = sum(mask[r*180+col:r*180+col+4].count('1') for r in rows)
            if land_samples >= len(rows)*2:
                page.dot(mx+(col+2)*cell, my+(row+len(rows)/2)*cell, 3.7, LAND)
    for i, (_, pin) in enumerate(REGIONS, 1):
        if pin is not None:
            px, py = mx+pin[0]*mw, my+pin[1]*mh
            page.dot(px, py, 15.5, NAVY)
            chip(page, i, px, py, 27)

    lx, ly = x+16, y+379
    page.rect(lx, ly-18, w-32, 1, RULE)
    for i, (label, pin) in enumerate(REGIONS):
        col, row = i % 2, i // 2
        xx, yy = lx+col*(mw/2)+13, ly+row*37
        chip(page, i+1, xx, yy+11, 22, filled=pin is not None)
        width = mw/2-31 if pin is not None else mw-31
        page.text(label, xx+18, yy+4, 13, BODY, weight=2, font=TAG, width=width)
        if pin is None:
            page.text('GLOBAL', xx+252, yy+6, 10, GREY, width=75)
    page.rect(lx, y+h-45, mw, 1, RULE)
    page.text('NUMBERS LINK TO REGION PANELS / DOT MAP: NATURAL EARTH 1:110M',
              lx, y+h-30, 9, GREY, font=TAG, width=mw)
    check_card(page, first, x, y, w, h)


def bitcoin(page, x, y, w, h):
    first = card(page, x, y, w, h)
    tx, inner = x+16, w-32
    page.text('BITCOIN / 7 DAILY CLOSES', tx, y+15, 12, BODY, width=inner)
    page.text(f'{BTC[-1][1]:,} USD', tx, y+39, 33, AMBER, weight=4, width=inner)
    values = [value for _, value in BTC]
    low, high = min(values), max(values)
    points = [(tx+7+i*(inner-14)/(len(values)-1), y+88+(high-v)/(high-low)*62)
              for i, v in enumerate(values)]
    baseline = y+h-25
    for (px, py), (qx, qy) in zip(points, points[1:]):
        for col in range(round(px*SCALE), round(qx*SCALE)):
            x_at = col/SCALE
            top = py+(qy-py)*(x_at-px)/(qx-px)
            page.rect(x_at, top, 1/SCALE, baseline-top, CHART_FILL)
    page.rect(tx, baseline, inner, 1, RULE)
    for p, q in zip(points, points[1:]):
        page.line(*p, *q, AMBER, 4)
    for (px, py), (date, _) in zip(points, BTC):
        page.dot(px, py, 2.3, WHITE)
        day = date[-2:]
        page.text(day, px-measure(day, 8)/2, baseline+7, 8, GREY, width=16)
    check_card(page, first, x, y, w, h)


def main():
    page = Page()
    page.text('WORLD NEWS IN ONE IMAGE', EDGE, 23, 13, AMBER, weight=2,
              width=450, tracking=1.1)
    count = '24 STORIES / 7 REGIONS'
    count_width = measure(count, 12, TAG, 1)
    page.text(count, 1024-EDGE-count_width, 24, 12, BODY, font=TAG,
              width=count_width, tracking=1)
    page.text('THURSDAY 19 NOVEMBER 2026', EDGE, 53, 38, weight=5,
              font=MASTHEAD, width=1024-2*EDGE, tracking=1.4)
    page.rect(EDGE, 112, 1024-2*EDGE, 1.5, AMBER)

    content_y = 122
    map_height = 592
    chart_y = content_y+map_height+GUTTER
    chart_height = 192
    world_map(page, EDGE, content_y, LEFT_WIDTH, map_height)
    bitcoin(page, EDGE, chart_y, LEFT_WIDTH, chart_height)

    footer_y = chart_y+chart_height+GUTTER
    page.rect(EDGE, footer_y, LEFT_WIDTH, 1, AMBER)
    page.text('SOURCES: 24 REPORTS ACROSS 7 REGIONS /', EDGE, footer_y+14, 11,
              BODY, font=TAG, width=LEFT_WIDTH)
    page.text('ALL FACTS AS REPORTED 19 NOV 2026', EDGE, footer_y+31, 11,
              BODY, font=TAG, width=LEFT_WIDTH)
    page.text('make.fun', EDGE, footer_y+57, 12, AMBER, width=LEFT_WIDTH)

    hero_height, row_height = 173, 199
    hero(page, RIGHT_X, content_y, RIGHT_WIDTH, hero_height)
    grid_y = content_y+hero_height+GUTTER
    col_width = (RIGHT_WIDTH-GUTTER)/2
    for index in range(6):
        row, col = divmod(index, 2)
        region_panel(page, index, RIGHT_X+col*(col_width+GUTTER),
                     grid_y+row*(row_height+GUTTER), col_width, row_height)
    tech_y = grid_y+3*(row_height+GUTTER)
    region_panel(page, 6, RIGHT_X, tech_y, RIGHT_WIDTH, 1024-EDGE-tech_y)

    assert len(page.rendered) == len(set(page.rendered)) == 24
    assert all(sum(REPORTS[i-1][1] == region for i in page.rendered) >= 2
               for region in range(len(REGIONS)))
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
                      'layout':'dot map and Bitcoin on left, Shenzhen lead and seven region cards on right'},sort_keys=True))


if __name__ == '__main__':
    main()
