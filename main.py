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
MASK_COLS, MASK_ROWS = 180, 90
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

PAPER = (244, 239, 227)
INK = (27, 27, 27)
RED = (192, 57, 43)
BLUE = (31, 78, 156)
AMBER = (217, 142, 43)
GREY = (88, 82, 74)
RULE = (174, 164, 147)
LAND = (116, 110, 99)
EDGE = 28
WIDTH = 1024 - 2*EDGE
GUTTER = 22
COLUMN = (WIDTH-2*GUTTER)//3
SCALE = 3
SIDE = 1024 * SCALE
GRID = 4
INSET = 8
HEAD_TRACK, TAG_TRACK, BODY_TRACK, SOURCE_TRACK = .1, .55, 0, .35
KERN_PAIRS = frozenset(('AV', 'AT', 'TA', 'LT', 'LY', 'WA', 'Yo'))
BAYER = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))


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
SANS['·'] = (-5, 5, (((-0.7, 0), (0.7, 0)),))
SANS['—'] = (-12, 12, (((-10, 0), (10, 0)),))
ROMAN = dict(SANS)
ROMAN.update({c: parse_glyph(s) for c,s in ROMAN_COORDINATES.items()})


def condensed(width, font=SANS):
    return {c: (left*width,right*width,
                tuple(tuple((x*width,y) for x,y in stroke) for stroke in strokes))
            for c,(left,right,strokes) in font.items()}


def compact_height(font, factor):
    return {ch: (left, right, tuple(tuple((x, 9+(y-9)*factor) for x, y in stroke)
                                    for stroke in strokes))
            for ch, (left, right, strokes) in font.items()}


HEADLINE = condensed(0.72)
TAG = condensed(0.86)
CARD_HEADLINE = compact_height(HEADLINE, .88)
# Briefs keep their readable horizontal measure on tighter 12 px leading.
BRIEF = compact_height(SANS, .79)

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
    left, right, strokes = ROMAN[letter]
    serifs = tuple(((x-3, y), (x+3, y)) for x, y in terminals)
    MASTHEAD[letter] = (min(left, min(x-4 for x, y in terminals)),
                        max(right, max(x+4 for x, y in terminals)), strokes + serifs)
MASTHEAD = condensed(.88, MASTHEAD)


def blend(a, b, fraction):
    return tuple(round(lo+(hi-lo)*fraction) for lo, hi in zip(a, b))


def spacing(pair, tracking):
    return tracking - (.4 if pair in KERN_PAIRS else 0)


class Page:
    def __init__(self):
        self.pixels = bytearray(bytes(PAPER) * SIDE * SIDE)
        self.text_boxes = []
        self.rendered = []
        self.tracking_widths = {}

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

    def rounded_rect(self, x, y, w, h, radius, color):
        for row in range(round(h*SCALE)):
            cy = (row+.5)/SCALE
            dy = max(0, radius-cy, cy-h+radius)
            inset = radius-math.sqrt(radius*radius-dy*dy)
            self.rect(x+inset, y+row/SCALE, w-2*inset, 1/SCALE, color)

    def polyline(self, points, color, weight):
        return self.stroke_pixels(tuple((round(x*SCALE),round(y*SCALE)) for x,y in points),
                                  color,weight)

    def stroke_pixels(self, points, color, weight):
        assert len(points) >= 2 and weight >= 1
        rgb = bytes(color)
        offsets = range(-(weight//2), -(weight//2)+weight)
        radius = weight/2
        left = top = SIDE
        right = bottom = 0

        def pixel(px, py):
            nonlocal left, top, right, bottom
            assert 0 <= px < SIDE and 0 <= py < SIDE
            pos = (py*SIDE+px)*3
            self.pixels[pos:pos+3] = rgb
            left, top = min(left,px), min(top,py)
            right, bottom = max(right,px+1), max(bottom,py+1)

        for (x0,y0),(x1,y1) in zip(points,points[1:]):
            dx,dy = abs(x1-x0),-abs(y1-y0)
            steep = abs(y1-y0) > abs(x1-x0)
            sx,sy = (1 if x0<x1 else -1),(1 if y0<y1 else -1)
            err = dx+dy
            while True:
                for offset in offsets:
                    pixel(x0+offset if steep else x0,y0 if steep else y0+offset)
                if x0==x1 and y0==y1:
                    break
                e = 2*err
                if e >= dy:
                    err += dy
                    x0 += sx
                if e <= dx:
                    err += dx
                    y0 += sy

        # Round caps and joins make each glyph stroke a continuous printed mark.
        extent = math.floor(radius)
        for cx,cy in points:
            for oy in range(-extent,extent+1):
                span = math.floor(math.sqrt(max(0,radius*radius-oy*oy)))
                for ox in range(-span,span+1):
                    pixel(cx+ox,cy+oy)
        return left,top,right,bottom

    def text(self, text, x, baseline, size, color, weight, font, width, tracking, hang):
        assert baseline % GRID == 0, (text, baseline)
        advance = measure(text,size,font,tracking)
        left_hang, right_hang = punctuation(text, size) if hang else (0, 0)
        assert advance-left_hang-right_hang <= width+.001, (text, advance, width)
        tracking_width = advance-measure(text, size, font)
        self.tracking_widths.setdefault((tracking, len(text)), []).append(tracking_width)
        cursor = x-left_hang
        scale = size/21
        paths = []
        for index, ch in enumerate(text):
            if index:
                cursor += spacing(text[index-1:index+1], tracking)
            left,right,strokes = font[ch]
            for stroke in strokes:
                pts = [(cursor+(px-left)*scale, baseline+(py-9)*scale)
                       for px,py in stroke]
                if len(pts) >= 2:
                    paths.append(tuple((round(px*SCALE),round(py*SCALE)) for px,py in pts))
            cursor += (right-left)*scale
        if paths:
            ink = [self.stroke_pixels(path,color,weight) for path in paths]
            bounds = (min(b[0] for b in ink)/SCALE,min(b[1] for b in ink)/SCALE,
                      max(b[2] for b in ink)/SCALE,max(b[3] for b in ink)/SCALE)
            assert x-left_hang-.34 <= bounds[0] and bounds[2] <= x+width+right_hang, (
                text, bounds, x, width)
            self.text_boxes.append((text,bounds))
        return advance

    def png(self):
        raw = bytearray()
        stride = SIDE*3
        for y in range(1024):
            raw.append(0)
            a = (3*y)*stride
            b = a+stride
            c = b+stride
            for x in range(1024):
                p = x*9
                for channel in range(3):
                    total = (self.pixels[a+p+channel]+self.pixels[a+p+3+channel]+
                             self.pixels[a+p+6+channel]+self.pixels[b+p+channel]+
                             self.pixels[b+p+3+channel]+self.pixels[b+p+6+channel]+
                             self.pixels[c+p+channel]+self.pixels[c+p+3+channel]+
                             self.pixels[c+p+6+channel])
                    raw.append((total+4)//9)
        def chunk(kind,data):
            return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
        return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1024,1024,8,2,0,0,0))+
                chunk(b'IDAT',zlib.compress(bytes(raw),9))+chunk(b'IEND',b''))


def measure(text,size,font=SANS,tracking=0):
    return (sum(font[c][1]-font[c][0] for c in text)*size/21
            + sum(spacing(a+b, tracking) for a, b in zip(text, text[1:])))


def punctuation(text, size):
    hang = min(1.5, size*.09)
    return (hang if text.startswith(('"', "'")) else 0,
            hang if text.endswith(('.', ',', ':', ';', '"', "'")) else 0)


def wrap(text, size, width, font, tracking, *, min_lines=1):
    """Choose a balanced break at a space, with an optical punctuation allowance."""
    words = text.split()
    whole = ' '.join(words)

    def line_width(line):
        hang = sum(punctuation(line, size)) if tracking == HEAD_TRACK else 0
        return measure(line, size, font, tracking)-hang

    if min_lines == 1 and line_width(whole) <= width:
        return [whole]

    candidates = []
    for cut, word in enumerate(words[:-1], 1):
        bare_word = word.strip('"\'.,:;!?()')
        if len(bare_word) == 1 and bare_word.isalpha():
            continue
        lines = [' '.join(words[:cut]), ' '.join(words[cut:])]
        first, last = map(line_width, lines)
        if max(first, last) <= width and (tracking != HEAD_TRACK or last >= .35*width):
            candidates.append((abs(first-last), lines))
    assert candidates, (text, size, width)
    return min(candidates)[1]


HEROES = (
    ('SHENZHEN SUMMIT', 'APEC 2026 · SHENZHEN · FIRST US-CHINA-RUSSIA SUMMIT',
     ('Trump, Xi and Putin', 'hold first three-way summit'),
     'The three leaders met on the sidelines of the APEC gathering in Shenzhen.', 'BY REUTERS'),
    ('WORLD COURT · THE HAGUE', 'THE HAGUE · INTERNATIONAL COURT OF JUSTICE',
     ('World Court: Myanmar', 'committed genocide'),
     "Judges ruled 9-6 in the case over Myanmar's treatment of the Rohingya.", 'FROM THE HAGUE'),
    ('COP31 · ANTALYA', 'ANTALYA · UN CLIMATE TALKS',
     ('COP31 draft drops', 'fossil-fuel aid goal'),
     'A draft deal at the UN climate summit leaves out the goal for fossil-fuel aid.', 'CLIMATE DESK'),
)

FEATURES = (
    ('EUROPE', 'bridge', 'Ukraine strikes Kerch Bridge again',
      'The crossing links Crimea and Russia.', 'BY KYIV INDEPENDENT'),
    ('MIDDLE EAST', 'missile', 'Houthi missiles shot down',
      'The missiles were intercepted in flight.', 'BY AL RASHEED'),
    ('NORTH AMERICA', 'chart', 'Nvidia slides 28% this month',
      'Shares fell as Anthropic went public.', 'BY CNBC'),
    ('NORTH AMERICA', 'game', 'GTA VI goes on sale',
      'Rockstar releases its latest game.', 'FROM LOS ANGELES'),
    ('SOUTH AMERICA', 'fist', 'Colombian unions strike',
      'Protesters take to the streets.', 'FROM BOGOTA'),
    ('OCEANIA', 'medal', 'Champion breaks marathon record',
      'Melbourne gets a new course best.', 'FROM MELBOURNE'),
)

DISPATCHES = (
    ('ASIA', 'Cyclone Alakar heads\nfor India', 'CYCLONE ALAKAR'),
    ('ASIA', 'Court seeks former\nPM Han', 'SEOUL'),
    ('NORTH AMERICA', 'Greenland backs\nArctic pact', 'NUUK'),
    ('NORTH AMERICA', '2,000+ walrus haul\nout in Alaska', 'ANCHORAGE'),
    ('NORTH AMERICA', 'Anthropic rises 17%\nafter $81bn IPO', 'NEW YORK / CNBC'),
)

# Pin coordinates are (longitude, latitude); the index is the printed ticker number.
BULLETINS = (
    ('Xi opens a hall in Shenzhen', (114.1, 22.5)),
    ('Ankara moves to strengthen ties', (32.9, 39.9)),
    ('Sheinbaum addresses tariffs', (-99.1, 19.4)),
    ('Mosque collapses in Jakarta', (106.8, -6.2)),
    ('Korean court proceedings continue', None),
    ('UK inquiry moves forward', (-0.1, 51.5)),
    ('Catalonia in the headlines', None),
    ('Roma author in the spotlight', None),
    ('Cook Islands in the headlines', (-159.8, -21.2)),
    ('Floods hit Spain', None),
    ('US and Venezuela resume military ties', None),
    ('Allies pledge support for Kyiv in Berlin', None),
    ('EU weighs EUR 45bn loan for Ukraine', None),
    ('Putin rejects sea and energy truce', None),
    ('Russian strikes kill 2 and injure 23', None),
    ('Israel ends Gaza operation', None),
    ('Troops mass near Ethiopia-Eritrea border', (39.0, 14.5)),
    ('Bitcoin closes at $62,942', None),
    ('US Senate blocks bid to end Iran war', None),
)

DESK_COLORS = {
    'EUROPE': (31, 78, 156), 'MIDDLE EAST': (136, 82, 20),
    'NORTH AMERICA': (164, 57, 48), 'SOUTH AMERICA': (130, 52, 99),
    'OCEANIA': (39, 104, 91), 'ASIA': (142, 65, 38),
}


def label(page, text, x, baseline, width, size=8, color=GREY, *,
          weight=2, font=TAG, tracking=TAG_TRACK):
    # Snap the left edge to the same raster grid used to check glyph bounds.
    left = round(x*SCALE)/SCALE
    return page.text(text, left, baseline, size, color, weight, font, x+width-left,
                     tracking, hang=tracking == HEAD_TRACK)


def centered(page, text, x, baseline, width, size, color=INK, *,
             weight=2, font=SANS, tracking=TAG_TRACK):
    margin = (width-measure(text, size, font, tracking))/2
    assert margin >= 1, (text, width)
    label(page, text, x+margin, baseline, width-margin, size, color,
          weight=weight, font=font, tracking=tracking)


def byline(page, text, x, baseline, width, card_bottom):
    previous_bottom = page.text_boxes[-1][1][3]
    first = len(page.text_boxes)
    page.rect(x, baseline-4, 8, 1, RED)
    label(page, text, x+13, baseline, width-13, 7.2, GREY, tracking=SOURCE_TRACK)
    _, (_,top,_,bottom) = page.text_boxes[first]
    assert top-previous_bottom >= 8, (text,'byline top gap')
    assert card_bottom-bottom >= 10, (text,'byline bottom gap',card_bottom,bottom)
    return bottom


def check_bounds(page, first, x, y, w, h):
    for text, (left, top, right, bottom) in page.text_boxes[first:]:
        assert x <= left < right <= x+w and y <= top < bottom <= y+h, (
            text, 'section bounds', (left, top, right, bottom), (x, y, x+w, y+h))


def column_rules(page, top, bottom):
    assert 3*COLUMN+2*GUTTER == WIDTH
    for index in (1, 2):
        center = EDGE+index*(COLUMN+GUTTER)-GUTTER/2
        page.rect(center-.5, top, 1, bottom-top, RULE)


def desk_chip(page, desk, x, y):
    width = math.ceil(measure(desk, 7, TAG, TAG_TRACK))+16
    page.rect(x, y, width, 12, DESK_COLORS[desk])
    label(page, desk, x+INSET, y+8, width-INSET, 7.0, PAPER)


def masthead(page, count):
    label(page, f'THE WORLD IN ONE DAY · {count} STORIES · ACROSS THE GLOBE',
          EDGE, 32, 783, 10, RED)
    label(page, 'WORLD EDITION', 872, 32, 124, 10, GREY)
    centered(page, 'THURSDAY 19 NOVEMBER 2026', EDGE, 96, WIDTH, 44, weight=6,
             font=MASTHEAD, tracking=HEAD_TRACK)
    page.rect(EDGE, 129, WIDTH, 2, INK)
    page.rect(EDGE, 135, WIDTH, .5, INK)


def stats_bar(page):
    stats = (
        ('3', 'TRILATERAL SUMMIT'), ('9-6', 'WORLD COURT VOTE'),
        ('$120bn', 'COP31 CLIMATE AID'), ('$81bn', 'ANTHROPIC IPO'),
        ('109-0', 'SENATE VOTE'), ('4.9%', 'UNEMPLOYMENT'), ('+2,000', 'ALASKAN WALRUS'),
    )
    cell = WIDTH/len(stats)
    for index, (number, title) in enumerate(stats):
        x = EDGE+index*cell
        first = len(page.text_boxes)
        if index:
            page.rect(x, 145, .5, 49, RULE)
        centered(page, number, x+4, 180, cell-8, 27, (RED, BLUE)[index % 2],
                 weight=5, font=HEADLINE, tracking=HEAD_TRACK)
        centered(page, title, x+4, 196, cell-8, 8, GREY, font=TAG)
        check_bounds(page, first, x+4, 145, cell-8, 53)
    page.rect(EDGE, 202, WIDTH, 1, INK)


class Illustration:
    def __init__(self, page, x, y, width, height):
        self.page, self.x, self.y = page, x, y
        self.width, self.height = width, height
        self.shapes = 0

    def bounds(self, left, top, right, bottom):
        assert 0 <= left <= right <= self.width and 0 <= top <= bottom <= self.height
        self.shapes += 1
        assert self.shapes <= 80

    def rect(self, x, y, w, h, color):
        self.bounds(x, y, x+w, y+h)
        self.page.rect(self.x+x, self.y+y, w, h, color)

    def dot(self, x, y, r, color):
        self.bounds(x-r, y-r, x+r+.5, y+r+.5)
        self.page.dot(self.x+x, self.y+y, r, color)

    def ellipse(self, x, y, rx, ry, color):
        self.bounds(x-rx, y-ry, x+rx, y+ry)
        for row in range(round((y-ry)*SCALE), round((y+ry)*SCALE)):
            dy = ((row+.5)/SCALE-y)/ry
            span = rx*math.sqrt(max(0, 1-dy*dy))
            self.page.rect(self.x+x-span, self.y+row/SCALE, 2*span, 1/SCALE, color)

    def shadow(self, x, y, rx, ry, base, shade):
        for scale, opacity in ((1, .27), (.86, .40), (.66, .60)):
            self.ellipse(x, y, rx*scale, ry*scale, blend(base, shade, opacity))

    def sky(self, base, shade, highlight):
        self.rect(0, 0, self.width, self.height, shade)
        x, y, w, h = 8, 8, self.width-16, self.height-16
        self.bounds(x, y, x+w, y+h)
        for row in range(h):
            level = (1-row/(h-1))*8
            band = int(level)
            colors = [bytes(blend(base, highlight, min(8, band+step)/8)) for step in (0, 1)]
            tile = b''.join(colors[(level-band)*16 > rank] * SCALE for rank in BAYER[row%4])
            scanline = (tile*((w+3)//4))[:w*SCALE*3]
            start = ((self.y+y+row)*SCALE*SIDE+(self.x+x)*SCALE)*3
            for subrow in range(SCALE):
                offset = start+subrow*SIDE*3
                self.page.pixels[offset:offset+len(scanline)] = scanline

    def path(self, points, color, weight=3):
        xs, ys = zip(*points)
        pad = weight/2+.5
        self.bounds(min(xs)-pad, min(ys)-pad, max(xs)+pad, max(ys)+pad)
        self.page.polyline(tuple((self.x+x, self.y+y) for x, y in points),
                           color, max(1, round(weight*SCALE)))

    def polygon(self, points, color):
        xs, ys = zip(*points)
        self.bounds(min(xs), min(ys), max(xs), max(ys))
        edges = list(zip(points, points[1:]+points[:1]))
        for row in range(round(min(ys)*SCALE), round(max(ys)*SCALE)):
            y = (row+.5)/SCALE
            hits = sorted(x+(y-y0)*(xx-x)/(y1-y0) for (x, y0), (xx, y1) in edges
                          if min(y0, y1) <= y < max(y0, y1))
            assert len(hits) % 2 == 0
            for left, right in zip(hits[::2], hits[1::2]):
                self.page.rect(self.x+left, self.y+row/SCALE, right-left, 1/SCALE, color)

    def type(self, text, x, baseline, width, size, color, font=TAG, weight=2,
             tracking=TAG_TRACK):
        first = len(self.page.text_boxes)
        centered(self.page, text, self.x+x, self.y+baseline, width, size, color,
                 font=font, weight=weight, tracking=tracking)
        check_bounds(self.page, first, self.x+x, self.y, width, self.height)


def summit_art(art):
    base, shade, highlight = (54, 52, 67), (37, 35, 48), (101, 86, 97)
    cream, gold, scarlet = (248, 240, 222), (243, 191, 86), (190, 61, 57)
    art.sky(base, shade, highlight)
    for center, name, jacket, skin, hair in (
        (56, 'TRUMP', (53, 78, 113), (241, 181, 142), (224, 185, 105)),
        (154, 'XI', (64, 63, 76), (221, 159, 116), (47, 40, 41)),
        (252, 'PUTIN', (64, 84, 111), (236, 191, 162), (165, 146, 129)),
    ):
        def poly(points, color):
            art.polygon(tuple((center+x, y) for x, y in points), color)

        # One nameplate and one national flag per portrait.
        fx = center+19
        art.rect(fx-1, 20, 1, 37, cream)
        if name == 'TRUMP':
            art.rect(fx, 21, 24, 13, cream)
            for stripe in range(0, 13, 2):
                art.rect(fx, 21+stripe, 24, 1, scarlet)
            art.rect(fx, 21, 10, 7, (47, 73, 118))
            for dx, dy in ((2, 2), (5, 2), (8, 2), (3.5, 4), (6.5, 4), (2, 6), (8, 6)):
                art.dot(fx+dx, 20.5+dy, .34, cream)
        elif name == 'XI':
            art.rect(fx, 21, 24, 15, scarlet)
            star = tuple((fx+5+math.cos(i*math.pi/5-math.pi/2)*r,
                          26+math.sin(i*math.pi/5-math.pi/2)*r)
                         for i, r in enumerate((2.7, 1.1)*5))
            art.polygon(star, gold)
            for dx, dy in ((9, 2), (11, 4), (11, 7), (9, 9)):
                art.dot(fx+dx, 21+dy, .5, gold)
        else:
            for row, color in enumerate((cream, (62, 101, 169), scarlet)):
                art.rect(fx, 21+row*5, 24, 5, color)

        skin_shade = blend(skin, (114, 62, 53), .37)
        suit_shade = blend(jacket, shade, .45)
        art.ellipse(center, 51, 20, 26, skin)
        poly(((6, 35), (19, 39), (20, 55), (15, 68), (7, 74), (10, 60)), skin_shade)
        art.rect(center-8, 68, 16, 16, skin)
        poly(((-8, 68), (8, 71), (8, 80), (-8, 76)), skin_shade)
        if name == 'TRUMP':
            profile = ((-19, 47), (-22, 34), (-13, 25), (7, 23), (22, 29),
                       (17, 36), (9, 34), (-14, 40))
        elif name == 'XI':
            profile = ((-19, 52), (-21, 39), (-17, 29), (-7, 24), (9, 25),
                       (18, 32), (20, 47), (14, 37), (-12, 36))
        else:
            profile = ((-20, 48), (-19, 37), (-13, 29), (-3, 26), (12, 29),
                       (18, 35), (10, 33), (-10, 34), (-15, 39))
        poly(profile, hair)
        art.path(((center+1, 50), (center-2, 57), (center+2, 58)), skin_shade, 1)
        poly(((-43, 109), (-37, 92), (-27, 85), (-10, 78), (10, 78),
              (28, 85), (38, 92), (43, 109)), jacket)
        poly(((10, 78), (28, 85), (38, 92), (43, 109), (5, 109)), suit_shade)
        poly(((-11, 78), (11, 78), (0, 105)), cream)
        poly(((0, 83), (4, 88), (0, 102), (-4, 88)), scarlet if name != 'XI' else gold)
        poly(((-11, 78), (-1, 83), (-8, 89), (-14, 83)), PAPER)
        poly(((11, 78), (1, 83), (8, 89), (14, 83)), (222, 214, 198))
        art.rect(center-37, 108, 74, 18, cream)
        art.type(name, center-37, 120, 74, 8.5, INK)


def court_art(art):
    base, shade, highlight = (41, 65, 81), (28, 44, 57), (99, 130, 143)
    stone, light, gold = (174, 157, 128), (243, 229, 202), (222, 172, 83)
    art.sky(base, shade, highlight)
    art.shadow(112, 119, 91, 8, base, shade)
    art.rect(43, 54, 138, 53, stone)
    for x in (57, 83, 135, 161):
        art.rect(x, 68, 12, 22, light)
        art.rect(x+2, 70, 8, 17, shade)
    art.rect(104, 72, 16, 35, blend(stone, shade, .70))
    art.polygon(((28, 53), (112, 20), (196, 53)), light)
    art.polygon(((47, 49), (112, 26), (177, 49)), stone)
    art.dot(112, 39, 6, shade)
    art.dot(112, 39, 4, gold)
    art.rect(34, 53, 156, 6, light)
    art.rect(38, 59, 148, 3, blend(stone, shade, .31))
    for x in (43, 69, 95, 121, 147, 173):
        art.rect(x-2, 62, 12, 5, light)
        art.rect(x, 67, 8, 33, light)
        art.rect(x+5, 67, 3, 33, blend(light, stone, .73))
        art.rect(x-2, 100, 12, 5, light)
    for x, y, w in ((37, 105, 150), (32, 110, 160), (25, 115, 174)):
        art.rect(x, y, w, 5, stone)
        art.rect(x, y, w, 2, light)
    art.rect(209, 22, 1, 98, blend(base, light, .28))
    art.path(((252, 31), (252, 85)), gold, 2)
    art.path(((230, 42), (274, 42)), gold, 2)
    art.dot(252, 33, 4, light)
    for x in (230, 274):
        art.path(((x-11, 67), (x, 44), (x+11, 67)), light, 1)
        art.polygon(((x-13, 67), (x+13, 67), (x+7, 74), (x-7, 74)), gold)
    art.rect(236, 84, 32, 4, gold)
    art.rect(221, 99, 62, 25, light)
    art.type('9-6', 221, 120, 62, 13, INK, weight=3, tracking=HEAD_TRACK)


def climate_art(art):
    base, shade, highlight = (40, 69, 66), (26, 48, 47), (101, 139, 126)
    water, leaf, grid = (110, 163, 178), (66, 108, 96), (154, 191, 194)
    white, heat = (244, 232, 206), (205, 67, 51)
    art.sky(base, shade, highlight)
    art.shadow(154, 105, 79, 9, base, shade)
    cx, cy, radius = 122, 59, 42
    art.ellipse(cx, cy, radius, radius, (66, 116, 138))
    art.ellipse(cx-3, cy-2, radius-5, radius-4, water)
    for dy, bow in ((-18, 5), (0, 7), (18, 5)):
        half = math.sqrt((radius-2)**2-dy**2)
        art.path(tuple((cx+half*t, cy+dy+bow*(1-t*t))
                       for t in (i/12 for i in range(-12, 13))), grid, .8)
    for bow in (-22, -5, 21):
        art.path(tuple((cx+bow*math.sin(i*math.pi/24), cy-(radius-2)*math.cos(i*math.pi/24))
                       for i in range(25)), grid, .8)
    art.polygon(((90, 40), (101, 29), (114, 25), (123, 28), (122, 35), (113, 40),
                 (112, 46), (105, 49), (108, 57), (100, 55), (94, 48)), leaf)
    art.polygon(((109, 55), (118, 54), (132, 62), (136, 69), (130, 78), (124, 83),
                 (119, 93), (115, 87), (116, 77), (111, 70)), leaf)
    art.polygon(((134, 36), (146, 32), (155, 41), (158, 51), (154, 59), (146, 53),
                 (141, 61), (133, 52), (129, 44)), leaf)
    art.dot(209, 85, 14, shade)
    art.dot(208, 83, 12, white)
    art.dot(208, 30, 7, white)
    art.rect(201, 30, 14, 51, white)
    art.rect(205, 30, 6, 48, blend(white, shade, .30))
    art.rect(205, 49, 6, 35, heat)
    art.dot(208, 83, 8, heat)
    for i, y in enumerate(range(32, 73, 5)):
        art.rect(220, y, 9 if i%2 == 0 else 5, 1, white)
    art.rect(25, 108, art.width-50, 20, white)
    art.rect(25, 108, 3, 20, AMBER)
    art.type('"leaves out the goal for fossil-fuel aid"', 33, 120, art.width-66,
             8.5, INK, font=condensed(.9, ROMAN), weight=3, tracking=BODY_TRACK)


def section_header(page, title, right, y):
    label(page, title, EDGE, y, 400, 10.5, RED, weight=3)
    width = measure(right, 8.5, TAG, TAG_TRACK)
    label(page, right, EDGE+WIDTH-width-2, y, width+2, 8.5)


def hero_row(page):
    section_header(page, 'THE FRONT PAGE', 'DIPLOMACY · JUSTICE · CLIMATE', 224)
    art_top, bottom = 232, 520
    column_rules(page, art_top, bottom-6)
    for index, ((title, caption, lines, detail, source), draw) in enumerate(zip(
            HEROES, (summit_art, court_art, climate_art))):
        x = EDGE+index*(COLUMN+GUTTER)
        first = len(page.text_boxes)
        draw(Illustration(page, x, art_top, COLUMN, 138))
        copy_start = len(page.text_boxes)
        tx, inner = x+INSET, COLUMN-2*INSET
        label(page, title, tx, 388, inner, 10, RED, weight=3)
        label(page, caption, tx, 400, inner, 6.7)
        headline = wrap(' '.join(lines), 18, inner, HEADLINE, HEAD_TRACK, min_lines=2)
        for line_index, line in enumerate(headline):
            label(page, line, tx, 424+line_index*28, inner, 18, weight=4,
                   font=HEADLINE, tracking=HEAD_TRACK)
        detail_size = 9
        detail_lines = wrap(detail, detail_size, inner, SANS, BODY_TRACK)
        assert len(detail_lines) == 2, (source, detail_lines)
        for line_index, line in enumerate(detail_lines):
            label(page, line, tx, 472+line_index*16, inner, detail_size, font=SANS, tracking=BODY_TRACK)
        byline(page, source, tx, 508, inner, bottom)
        # Consecutive text blocks must have visible clearance, including descenders.
        copy = page.text_boxes[copy_start:]
        for (a, box), (b, following) in zip(copy, copy[1:]):
            assert round((following[1]-box[3])*SCALE) >= 2, (a, b, box, following)
        check_bounds(page, first, x, art_top, COLUMN, bottom-art_top)
        page.rendered.append(lines[0])


def small_icon(art, icon, color):
    tile = blend(PAPER, color, .10)
    light, dark = blend(color, PAPER, .32), blend(color, INK, .48)
    art.page.rounded_rect(art.x, art.y, art.width, art.height, 2, blend(tile, dark, .19))
    art.page.rounded_rect(art.x+1, art.y+1, art.width-2, art.height-2, 1, tile)

    def contour(points, fill):
        art.polygon(points, fill)
        art.path(points+points[:1], dark, 1)

    if icon == 'bridge':
        art.path(((7, 25), (14, 15), (24, 25), (34, 15), (42, 25)), light, 1.5)
        for x in (13, 33):
            contour(((x, 14), (x+3, 14), (x+3, 37), (x, 37)), light)
        contour(((6, 27), (43, 27), (43, 32), (6, 32)), color)
        art.path(((8, 40), (41, 40)), light, 1)
    elif icon == 'missile':
        contour(((14, 26), (10, 24), (17, 17), (23, 17), (31, 25), (31, 31),
                 (24, 38), (22, 33)), light)
        contour(((12, 30), (30, 12), (40, 9), (37, 19), (19, 37), (13, 36)), color)
        art.path(((18, 30), (34, 14)), light, 1)
        art.path(((9, 40), (12, 37)), AMBER, 1.5)
    elif icon == 'chart':
        for x, h in ((14, 12), (20, 9), (26, 11), (32, 5)):
            art.rect(x, 38-h, 4, h, light)
        art.path(((9, 10), (9, 39), (41, 39)), dark, 1)
        trend = ((13, 15), (22, 22), (27, 19), (39, 32))
        art.path(trend, dark, 4)
        art.path(trend, color, 2)
        contour(((32, 32), (40, 25), (40, 34)), color)
    elif icon == 'game':
        contour(((9, 18), (39, 18), (43, 31), (39, 36), (34, 35), (29, 30),
                 (20, 30), (15, 35), (9, 36), (6, 31)), color)
        art.rect(11, 19, 26, 2, light)
        art.rect(12, 23, 10, 2, PAPER)
        art.rect(16, 19, 2, 10, PAPER)
        art.dot(33, 23, 1.6, PAPER)
        art.dot(37, 27, 1.6, PAPER)
    elif icon == 'fist':
        contour(((16, 37), (16, 29), (10, 23), (10, 18), (14, 16), (18, 21),
                 (18, 11), (22, 10), (23, 8), (28, 9), (33, 10), (37, 12),
                 (38, 26), (32, 33), (32, 37)), color)
        art.path(((14, 20), (23, 24), (29, 22)), light, 1)
        for x in (23, 28, 33):
            art.rect(x, 12, 1, 7, light)
        art.rect(16, 39, 16, 3, dark)
    else:
        assert icon == 'medal'
        contour(((12, 8), (20, 8), (28, 27), (19, 29)), light)
        contour(((28, 8), (36, 8), (29, 29), (21, 27)), color)
        art.dot(24, 32, 9, dark)
        art.dot(24, 32, 8, AMBER)
        art.dot(24, 32, 5, blend(AMBER, color, .56))
        art.rect(23, 29, 2, 6, PAPER)


def secondary_grid(page):
    page.rect(EDGE, 520, WIDTH, 1, INK)
    section_header(page, 'AROUND THE WORLD', 'SIX STORIES IN FOCUS', 536)
    column_rules(page, 540, 724)
    for index, (desk, icon, headline, detail, source) in enumerate(FEATURES):
        row, col = divmod(index, 3)
        x, y = EDGE+col*(COLUMN+GUTTER), 540+row*92
        height = 91
        first = len(page.text_boxes)
        card = (250, 246, 236)
        page.rounded_rect(x+2, y+2, COLUMN-2, height, 2, blend(PAPER, INK, .15))
        page.rounded_rect(x, y, COLUMN-2, height, 2, card)
        page.rect(x+INSET, y+2, COLUMN-2-2*INSET, 1, blend(card, RULE, .48))
        small_icon(Illustration(page, x+INSET, y+8, 49, 49), icon, DESK_COLORS[desk])
        tx = x+INSET+49+INSET
        inner = x+COLUMN-2-INSET-tx
        desk_chip(page, desk, tx, y+4)
        headline_size, leading = 12.5, 16
        lines = wrap(headline, headline_size, inner, CARD_HEADLINE, HEAD_TRACK)
        assert 1 <= len(lines) <= 2
        for line_index, line in enumerate(lines):
            label(page, line, tx, y+28+line_index*leading, inner, headline_size, INK, weight=3,
                   font=CARD_HEADLINE, tracking=HEAD_TRACK)
        label(page, detail, tx, y+60, inner, 9, font=TAG, tracking=BODY_TRACK)
        page.rect(tx, y+67, inner, 1, blend(card, RULE, .48))
        byline(page, source, tx, y+80, inner, y+height)
        check_bounds(page, first, x, y, COLUMN, height)
        page.rendered.append(headline)


def dispatch_row(page):
    page.rect(EDGE, 727, WIDTH, 1, INK)
    cell = WIDTH/len(DISPATCHES)
    for index, (desk, headline, source) in enumerate(DISPATCHES):
        left = EDGE+index*cell
        x = round((left+INSET)*SCALE)/SCALE
        inner = left+cell-x-INSET
        first = len(page.text_boxes)
        if index:
            page.rect(left, 735, .5, 61, RULE)
        label(page, desk, x, 740, inner, 7.5, DESK_COLORS[desk], weight=3)
        lines = wrap(headline, 10.5, inner, HEADLINE, HEAD_TRACK, min_lines=2)
        for line_index, line in enumerate(lines):
            label(page, line, x, 756+line_index*24, inner, 10.5, INK, weight=3,
                  font=HEADLINE, tracking=HEAD_TRACK)
        label(page, source, x, 796, inner, 7.3, tracking=SOURCE_TRACK)
        check_bounds(page, first, x, 731, inner, 68)
        page.rendered.append(headline)


def dot_map(page, x, y):
    step = 1.45
    mw, mh = MASK_COLS*step, MASK_ROWS*step
    packed = base64.b64decode(LANDMASK_B64, validate=True)
    assert len(packed)*8 == MASK_COLS*MASK_ROWS
    # Sample every other row and column to preserve visible paper between dots.
    for row in range(0, MASK_ROWS, 2):
        for col in range(0, MASK_COLS, 2):
            bit = row*MASK_COLS+col
            if packed[bit//8] & (0x80 >> (bit % 8)):
                page.dot(x+(col+.5)*step, y+(row+.5)*step, .55, LAND)
    pins = []
    for index, (_, location) in enumerate(BULLETINS, 1):
        if location is None:
            continue
        lon, lat = location
        px, py = x+(lon+180)/360*mw, y+(90-lat)/180*mh
        baseline = GRID*round((py+2.5)/GRID)
        py = baseline-2.5
        assert all(math.hypot(px-xx, py-yy) >= 13 for xx, yy in pins), (index, 'pin overlap')
        assert x <= px-6.5 and px+6.5 <= x+mw and y <= py-6.5 and py+6.5 <= y+mh
        pins.append((px, py))
        page.dot(px, py, 6.25, PAPER)
        page.dot(px, py, 5, RED)
        centered(page, str(index), px-6, baseline, 12, 5, PAPER, font=TAG)


def ticker(page):
    page.rect(EDGE, 799, WIDTH, 1.5, INK)
    section_header(page, 'WHERE IT HAPPENED', 'NEWS IN BRIEF · MAP PINS MATCH STORY NUMBERS', 820)
    dot_map(page, EDGE, 827)
    label(page, 'DOT MAP: NATURAL EARTH 1:110M', EDGE, 964, 260, 6.5, tracking=SOURCE_TRACK)
    for col, x in enumerate((307, 654)):
        page.rect(x-9, 828, 1, 122, RULE)
        for row, (headline, _) in enumerate(BULLETINS[col*10:(col+1)*10]):
            number = col*10+row+1
            y = 840+row*12
            label(page, f'{number:02d}', x, y, 22, 8.3, RED, weight=3)
            label(page, headline, x+25, y, 309, 9, INK, font=BRIEF, tracking=HEAD_TRACK)
            page.rendered.append(headline)
    page.rect(307, 953, 689, 1, RULE)
    label(page, 'BY THE NUMBERS', 307, 964, 149, 7.5, RED, weight=3)
    for x, item in zip((456, 636, 816), ('9-6 COURT VOTE', '$81bn IPO', '4.9% UNEMPLOYMENT')):
        page.rect(x, 958, 1, 8, RULE)
        label(page, item, x+INSET, 964, 172, 7.5)


def footer(page):
    page.rect(EDGE, 971, WIDTH, 1.5, INK)
    page.rect(EDGE, 975, WIDTH, .5, RULE)
    centered(page, 'DATE CHECK: Every story on this paper happened on or before 19 Nov 2026',
             EDGE, 996, WIDTH, 8.8, INK, weight=2, tracking=BODY_TRACK)
    centered(page, 'SOURCES: REUTERS, AP, AFP, BBC, AL JAZEERA, CNN, NBC, TIMES OF INDIA, GUARDIAN, '
             'LE MONDE, KYIV INDEPENDENT, SYDNEY MORNING HERALD — 2026-11-19',
             EDGE, 1012, WIDTH, 7.2, GREY, font=TAG, tracking=SOURCE_TRACK)


def main():
    page = Page()
    count = sum(map(len, (HEROES, FEATURES, DISPATCHES, BULLETINS)))
    masthead(page, count)
    stats_bar(page)
    hero_row(page)
    secondary_grid(page)
    dispatch_row(page)
    ticker(page)
    footer(page)
    assert len(page.rendered) == len(set(page.rendered)) == count == 33
    # Compare spacing for equal-length samples after removing proportional glyph
    # advances and pair kerning, which depend on the letters even at equal length.
    assert {tracking for tracking, _ in page.tracking_widths} == {
        HEAD_TRACK, TAG_TRACK, BODY_TRACK, SOURCE_TRACK}
    assert all(max(widths)-min(widths) < 2 for widths in page.tracking_widths.values())
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
                        'layout':'The World in One Day newspaper front page'},sort_keys=True))


if __name__ == '__main__':
    main()
