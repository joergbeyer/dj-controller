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

## support & known limitations

The mapping is currently incomplete. While selecting a track, cueing and playing, using the
mixer and fading works, effects are not fully implemented. You can pick an effect and mix it 
in, but the roation knob to select the effects is not working.

Basic jog-wheel support is implemented: you can scratch and touching the wheel from the top stops playing.

