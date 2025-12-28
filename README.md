# dj-controller
provide a mixxx mapping for the Pioneer DDJ GRV6 DJ Controller

This work is currently experimental and the Controller is not yet fully supported.

## How to use

Copy the javascript and xml file into your local mixxx controllers folder. That is `~/.mixxx/controllers/`. 
Restart mixxx and pick the controller in the Options > Preferences > Controllers, then "Load Mapping" and 
pick "DDJ-GRV6 Midi1". That controller in close to the top of the list. 
The list is not alphabethical sorted.

If you have trouble, then start mixxx in a shell an collect the debug output, eg:
```
$ mixxx --controller-debug --developer 2>&1 | tee log.txt
```

Feedback welcome

## Support & known limitations

The mapping is currently incomplete. While selecting a track, cueing and playing, using the
mixer and fading works, effects are not fully implemented. You can pick an effect and mix it 
in, but the roation knob to select the effects is not working.

Basic jog-wheel support is implemented: you can scratch and touching the wheel from the top stops playing.

## The Mapping

The mapping is a very repetetive XML file. Lots of sections are repeated multiple times, eg 4 times as there
are 4 decks supported by this controller. The sections  are very similar but have a counter the increments per
deck. I use the python file `genxml-ddjgrv6.py` to generate the full XML file. 

This generates the XML file in the current folder. You can review it and copy it over the the mixxx folder
with the custom mappings.
```
$ ./genxml-ddjgrv6.py  > Pioneer-DDJ-GRV6.midi.xml
```

Or you can just generate it in that mixxx folder. The javascript file has to be in the the same mixxx folder.
```
$ ./genxml-ddjgrv6.py  > ~/.mixxx/controllers/Pioneer-DDJ-GRV6.midi.xml
```

You can avoid the copy, if you simply link from the mixxx controllers folder to this folder with the 
checked out or generated javascript and XML file.

Once this matured and if there is demand then I can integrate it into mixxx.

## Resources
 * Pioneer lists at [their website](https://support.pioneerdj.com/hc/en-us/articles/37284057102489-DDJ-GRV6-MIDI-compatible-software)
the [list of midi messages](https://www.pioneerdj.com/-/media/pioneerdj/software-info/controller/ddj-grv6/ddj-grv6_midi_message_list_e1.pdf) 
