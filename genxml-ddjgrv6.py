#!/usr/bin/env python3 

import datetime
from collections import defaultdict

brand = 'Pioneer'
controller_id = 'DDJ-GRV6'
model = f'{brand}-{controller_id}'
prefix = 'PioneerDDJGRV6'

def getIndent(level):
    return ' '*(4*level)

class XmlConfig:
    """
    Simplify printing of the repeatitive control/output blocks
    """
    def __init__(self):
        self.kv = {}
        self.out_sections = defaultdict(list)

    def dump(self, indentLevel, block, entries):
        result = []
        result.append(getIndent(indentLevel+1)+f'<{block}>')
        ident = getIndent(indentLevel+2)

        for key in entries:
            val = self.kv.get(key)
            result.append(f'{ident}<{key}>{val}</{key}>')
        result.append(getIndent(indentLevel+1)+f'</{block}>')
        return result
    def print(self, indentLevel, block, entries):
        s = self.dump(indentLevel, block, entries)
        self.out_sections[block].append('\n'.join(s))


    def comment(self, indentLevel, block, text):
        self.out_sections[block].append(getIndent(indentLevel)+text)

    def print_section(self, indentLevel, name):
        print(getIndent(indentLevel)+f'<{name}s>')
        print('\n'.join(self.out_sections.get(name)))
        print(getIndent(indentLevel)+f'</{name}s>')


    #def close_block(self, indentLevel):
        #return getIndent(indentLevel)+f'</{self.block}s>'



def hexfmt(val):
    return f'0x{val:02X}'

def gen_description(hwid, feature, deck_num, modus):
    return f'{hwid} {feature} - Deck {deck_num} - {modus}'

def section_header():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f'''\
<?xml version="1.0" encoding="utf-8"?>
<MixxxMIDIPreset schemaVersion="1" mixxxVersion="2.5">
    <info>
        <name>{brand} {controller_id}</name>
        <author>Jörg Beyer</author>
        <description>Midi Mapping for the {brand} {controller_id}, {now}</description>
        <forums>TBD</forums>
    </info>
    <controller id="{controller_id}">
        <scriptfiles>
            <file filename="common-controller-scripts.js"/>
            <file functionprefix="{prefix}" filename="{model}-scripts.js"/>
        </scriptfiles>
''')

def section_footer():
    print('''\
    </controller>
</MixxxMIDIPreset>
''')

def section_browsing(xc, num_decks):
    il = 2 # indent level
    xc.comment(il, 'control', '<!--')
    xc.comment(il, 'control', '**')
    xc.comment(il, 'control', '** Browsing functionality: top middle section with the jogwhhel')
    xc.comment(il, 'control', '**')
    xc.comment(il, 'control', '-->')

    entries = ['description', 'group', 'key', 'status', 'midino', 'options']

    xc.kv['description'] = 'B1 BROWSE - rotate - Scroll tracklist/tree view'
    xc.kv['group'] = '[Library]'
    xc.kv['key'] = 'MoveVertical'
    xc.kv['status'] = '0xB6'
    xc.kv['midino'] = '0x40'
    xc.kv['key'] = 'MoveVertical'
    xc.kv['options'] = '<SelectKnob/>'
    xc.print(il, 'control', entries)

    xc.kv['description'] = 'B1 BROWSE - press - Move cursor between track list and tree view'
    xc.kv['key'] = 'MoveFocusForward'
    xc.kv['status'] = '0x96'
    xc.kv['midino'] = '0x41'
    xc.kv['options'] = '<Normal/>'
    xc.print(il, 'control', entries)

    xc.kv['description'] = 'B1 BROWSE +SHIFT - press - Move cursor between track list and tree view'
    xc.kv['key'] = 'MoveFocusBackward'
    xc.kv['midino'] = '0x42'
    xc.print(il, 'control', entries)

    xc.kv['status'] = '0x96'
    xc.kv['midino'] = '0x46'
    xc.kv['key'] = 'LoadSelectedTrack'
    xc.kv['options'] = '<Normal/>'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('B6', 'LOAD', i+1, 'normal')
        xc.kv['midino'] = hexfmt(int("0x46",16)+i)
        xc.print(il, 'control', entries)

    xc.comment(il, 'control', '<!-- not mapped: tilt in all 4 directions. B2-B5 -->')


def section_deck(xc, num_decks):
    il = 2 # indent level
    xc.comment(il, 'control', '<!--')
    xc.comment(il, 'control', '**')
    xc.comment(il, 'control', '** the decks')
    xc.comment(il, 'control', '**')
    xc.comment(il, 'control', '-->')

    entries = ['description', 'group', 'key', 'status', 'midino', 'options']
    
    # shift pressed
    xc.kv['key'] = f'{prefix}.shiftPressed'
    xc.kv['midino'] = '0x3F'
    xc.kv['options'] = '<Script-Binding/>'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D3', 'SHIFT', i+1, 'normal')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)

    # Play/Pause
    xc.kv['key'] = 'play'
    xc.kv['midino'] = '0x0B'
    xc.kv['options'] = '<Toggled/>'
    xc.kv['on'] = '0x7F'
    xc.kv['off'] = '0x00'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D1', 'Play/Pause', i+1, 'normal')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)
        #for i in range(num_decks):
        #xc.kv['group'] = f'[Channel{i+1}]'
        #xc.kv['description'] = gen_description('D1', 'Play/Pause', i+1, 'normal')
        #xc.kv['status'] = hexfmt(int("0x90",16)+i)
        #xc.print(il, 'output', entries+['on', 'off'])


    # reverse roll
    xc.kv['key'] = 'reverseroll'
    xc.kv['midino'] = '0x47'
    xc.kv['options'] = '<Normal/>'
    xc.kv['minimum'] = '0.5'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D1', 'shift Play/Pause', i+1, 'reverse playback')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D1', 'shift Play/Pause', i+1, 'reverse playback')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'output', entries+['on', 'off'])

    xc.kv['key'] = 'cue_default'
    xc.kv['midino'] = '0x0C'
    xc.kv['options'] = '<Normal/>'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D2', 'set/call cue, back cue', i+1, 'normal')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)
        xc.print(il, 'output', entries+['on', 'off'])

    xc.kv['key'] = 'start_play'
    xc.kv['midino'] = '0x48'
    xc.kv['options'] = '<Normal/>'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D2', 'jump to track start', i+1, 'normal')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D2', 'jump to track start', i+1, 'normal')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'output', entries+['on', 'off'])


    # turn the jog
    xc.comment(il, 'control', '<!-- jog dial start -->')
    xc.kv['key'] = f'{prefix}.jogTurn'
    xc.kv['midino'] = '0x22'
    xc.kv['options'] = '<Script-Binding/>'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D4', 'Jog Platter Vinyl mode ON', i+1, 'scratch')
        xc.kv['status'] = hexfmt(int("0xB0",16)+i)
        xc.print(il, 'control', entries)


    xc.kv['midino'] = '0x21'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D4', 'Jog Platter', i+1, 'pitch bend')
        xc.kv['status'] = hexfmt(int("0xB0",16)+i)
        xc.print(il, 'control', entries)

    xc.kv['midino'] = '0x23'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D4', 'Jog Platter Vinyl mode OFF', i+1, 'pitch bend')
        xc.kv['status'] = hexfmt(int("0xB0",16)+i)
        xc.print(il, 'control', entries)
    
    xc.kv['key'] = f'{prefix}.jogSearch'
    xc.kv['midino'] = '0x29'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D4', 'Jog Platter', i+1, 'search')
        xc.kv['status'] = hexfmt(int("0xB0",16)+i)
        xc.print(il, 'control', entries)


    xc.kv['key'] = f'{prefix}.jogTouch'
    xc.kv['midino'] = '0x36'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D4', 'Jog Platter touch', i+1, 'enable on touch / disable on release')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)

    xc.kv['midino'] = '0x67'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D4', 'Jog Platter touch scratch / pitch bend', i+1, 'enable on touch / disable on release high speed')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)
    
    xc.comment(il, 'control', '<!-- jog dial end -->')

    xc.comment(il, 'control', '<!-- tempo slider start -->')
    xc.kv['key'] = f'{prefix}.tempoSliderMSB'
    xc.kv['midino'] = '0x00'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D18', 'Tempo Slider', i+1, 'fade MSB')
        xc.kv['status'] = hexfmt(int("0xB0",16)+i)
        xc.print(il, 'control', entries)
    xc.kv['key'] = f'{prefix}.tempoSliderLSB'
    xc.kv['midino'] = '0x20'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D18', 'Tempo Slider', i+1, 'fade LSB')
        xc.kv['status'] = hexfmt(int("0xB0",16)+i)
        xc.print(il, 'control', entries)
    xc.comment(il, 'control', '<!-- tempo slider end -->')

    xc.kv['midino'] = '0x10'
    xc.kv['key'] = f'{prefix}.loopIn'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D7', 'LOOP IN/4 BEAT', i+1, 'press, set loop in')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)

    xc.kv['midino'] = '0x11'
    xc.kv['key'] = f'{prefix}.loopOut'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D7', 'LOOP IN/4 BEAT', i+1, 'press, set loop out')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)

    xc.kv['midino'] = '0x4D'
    xc.kv['key'] = f'{prefix}.reloopExit'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D7', 'RELOOP/EXIT', i+1, 'loop off, loop on')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)

    xc.kv['midino'] = '0x50'
    xc.kv['key'] = 'reloop_andstop'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D7', 'RELOOP/EXIT + shift', i+1, 'reloop and  stop')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)

    xc.kv['midino'] = '0x4C'
    xc.kv['key'] = f'{prefix}.toggleLoopAdjustIn'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D7', 'shift LOOP in', i+1, 'adjust loop in')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)

    xc.kv['midino'] = '0x4E'
    xc.kv['key'] = f'{prefix}.toggleLoopAdjustOut'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D7', 'shift LOOP out', i+1, 'adjust loop out')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)


    # beat sync
    xc.kv['midino'] = '0x58'
    xc.kv['options'] = '<Script-Binding/>'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D19', 'Deck ', i+1, 'beat sync')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.kv['key'] = f'{prefix}.beatSyncHandler'
        xc.print(il, 'control', entries)
        xc.kv['key'] = 'sync_enabled'
        xc.print(il, 'output', entries+['on', 'off'])

    xc.kv['midino'] = '0x5C'
    xc.kv['options'] = '<Script-Binding/>'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('D19', 'Deck ', i+1, 'beat sync off')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.kv['key'] = f'{prefix}.beatSyncHandler'
        xc.print(il, 'control', entries)
        xc.kv['key'] = 'sync_enabled'
        xc.print(il, 'output', entries+['on', 'off'])

    #xc.kv['description'] = 'Channelfader - slider'


def section_mixer (xc, num_decks):
    il = 2 # indent level
    xc.comment(il, 'control', '<!--')
    xc.comment(il, 'control', '**')
    xc.comment(il, 'control', '** the Mixxer')
    xc.comment(il, 'control', '**')
    xc.comment(il, 'control', '-->')

    entries = ['description', 'group', 'key', 'status', 'midino', 'options']

    xc.kv['description'] = 'Crossfader - slider M1'
    xc.kv['group'] = '[Master]'
    xc.kv['key'] = 'crossfader'
    xc.kv['status'] = '0xB6'
    xc.kv['group'] = '[Master]'
    
    xc.kv['midino'] = '0x1F'
    xc.kv['options'] = '<FourteenBitCC/><soft_takeover/>'
    xc.print(il, 'control', entries)
    
    # shift pressed
    xc.kv['key'] = 'volume'
    xc.kv['midino'] = '0x13'
    xc.kv['options'] = '<FourteenBitCC/><soft_takeover/>'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('M2', 'CH Fader', i+1, 'normal')
        xc.kv['status'] = hexfmt(int("0xB0",16)+i)
        xc.print(il, 'control', entries)


    xc.kv['key'] = 'pfl'
    xc.kv['midino'] = '0x54'
    xc.kv['options'] = '<Normal/>'
    xc.kv['on'] = '0x7F'
    xc.kv['minimum'] = '0.5'
    for i in range(num_decks):
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('M7', 'CH CUE', i+1, 'normal')
        xc.kv['status'] = hexfmt(int("0x90",16)+i)
        xc.print(il, 'control', entries)
        xc.print(il, 'output', entries+['on', 'minimum'])

    xc.kv['key'] = 'pregain'
    for i in range(num_decks):
        xc.kv['midino'] = '0x04'
        xc.kv['options'] = '<FourteenBitCC/>'
        xc.kv['group'] = f'[Channel{i+1}]'
        xc.kv['description'] = gen_description('M3', 'TRIM', i+1, 'normal')
        xc.kv['status'] = hexfmt(int("0xB0",16)+i)
        xc.print(il, 'control', entries)

    xc.kv['key'] = 'parameter3'
    for i in range(num_decks):
        xc.kv['midino'] = '0x07'
        xc.kv['options'] = '<FourteenBitCC/>'
        xc.kv['group'] =  f'[EqualizerRack1_[Channel{i+1}]_Effect1]'
        xc.kv['description'] = gen_description('M4', 'EQ Hi', i+1, 'normal')
        xc.kv['status'] = hexfmt(int("0xB0",16)+i)
        xc.print(il, 'control', entries)

    xc.kv['key'] = 'parameter2'
    for i in range(num_decks):
        xc.kv['midino'] = '0x0B'
        xc.kv['options'] = '<FourteenBitCC/>'
        xc.kv['group'] =  f'[EqualizerRack1_[Channel{i+1}]_Effect1]'
        xc.kv['description'] = gen_description('M5', 'EQ Mid', i+1, 'normal')
        xc.kv['status'] = hexfmt(int("0xB0",16)+i)
        xc.print(il, 'control', entries)

    xc.kv['key'] = 'parameter1'
    for i in range(num_decks):
        xc.kv['midino'] = '0x0F'
        xc.kv['options'] = '<FourteenBitCC/>'
        xc.kv['group'] =  f'[EqualizerRack1_[Channel{i+1}]_Effect1]'
        xc.kv['description'] = gen_description('M5', 'EQ Mid', i+1, 'normal')
        xc.kv['status'] = hexfmt(int("0xB0",16)+i)
        xc.print(il, 'control', entries)

    xc.kv['key'] = 'headMix'
    xc.kv['group'] =  '[Master]'
    xc.kv['description'] = 'M12 HEADPHONES MIXING - rotate - Monitor Balance'
    xc.kv['status'] = '0xB6'
    xc.kv['midino'] = '0x0C'
    xc.kv['options'] = '<FourteenBitCC/>'
    xc.print(il, 'control', entries)

    xc.kv['key'] = 'headGain'
    xc.kv['group'] =  '[Master]'
    xc.kv['description'] = 'M13 HEADPHONES Level - rotate - Monitor Balance'
    xc.kv['status'] = '0xB6'
    xc.kv['midino'] = '0x0D'
    xc.kv['options'] = '<FourteenBitCC/>'
    xc.print(il, 'control', entries)

    xc.kv['key'] = 'super1'
    xc.kv['status'] = '0xB6'
    xc.kv['midino'] = '0x0D'
    xc.kv['options'] = '<FourteenBitCC/>'
    for i in range(num_decks):
        xc.kv['description'] = 'Effect Color FX (CH {i+1})'
        xc.kv['group'] =  '[QuickEffectRack1_{i+1}]'
        xc.print(il, 'control', entries)

    xc.kv['group'] = '[EffectRack1_EffectUnit1]'
    xc.kv['description'] = 'F5 BEAT FX SELECT - rotate to change effect'
    xc.kv['key'] = f'{prefix}.fxSelectAbsolute'
    xc.kv['options'] = '<Script-Binding/>'
    xc.kv['group'] = '[EffectRack1_EffectUnit1]'
    xc.kv['status'] = '0x94'
    for i in range(14):
        xc.kv['midino'] = hexfmt(int("0x20",16)+i)
        xc.print(il, 'control', entries)

    
    xc.kv['description'] = 'F6 BEAT FX CH SELECT - Select target deck, samplers (SP) or master'
    xc.kv['key'] = f'{prefix}.fxChannelAbsolute'
    xc.kv['options'] = '<Script-Binding/>'
    xc.kv['status'] = '0x94'
    for i in range(12):
        xc.kv['midino'] = hexfmt(int("0x10",16)+i)
        xc.print(il, 'control', entries)


    xc.kv['description'] = 'F7 BEAT FX LEVEL/DEPTH (Hi/Res)'
    # xc.kv['key'] = f'{prefix}.levelDepthHiRes'
    #xc.kv['key'] = 'mix'
    xc.kv['key'] = f'{prefix}.levelDepthDirect'
    xc.kv['options'] = '<FourteenBitCC/><Script-Binding/>'
    xc.kv['status'] = '0xB4'
    xc.kv['midino'] = '0x02'
    xc.print(il, 'control', entries)




    xc.kv['description'] = 'F8 BEAT FX ON/OFF - Toggle effect on/off'
    xc.kv['key'] = f'{prefix}.beatFxOnOff'
    xc.kv['options'] = '<Script-Binding/>'
    xc.kv['status'] = '0x94'
    xc.kv['midino'] = '0x47'
    xc.print(il, 'control', entries)





def main():
    xc = XmlConfig()
    num_decks = 4

    section_browsing(xc, num_decks)
    section_deck(xc, num_decks)
    section_mixer(xc, num_decks)

    section_header()
    xc.print_section(2, 'control')
    xc.print_section(2, 'output')
    section_footer()



if __name__ == '__main__':
    main() 

#            <control>
#                <description>D1 Play/Pause - Deck 1 - normal</description>
#                <group>[Channel1]</group>
#                <key>PioneerDDJGRV6.scanEffects</key>
#               <status>0x90</status>
#                <midino>0x0B</midino>
#                <options><Script-Binding/></options>
#            </control>

