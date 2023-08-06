Project flashcam
================

`FLASk supported Http webCAM`

IN DEVELOPMENT

/Here, the merge of several ideas will form the package for easy
installable webcam surveylance via PyPI. The basic aim is to access view
to various technical devices during an experiment./

Usage screen
------------

``` {.bash org-language="sh"}
... usage:
    flashcam ls
    flashcam getres [product | IDpath ]        # flashcam getres "Webcam C270"
    flashcam show ... show
    flashcam show  "Webcam C270"  -r 320x176

    flashcam flask & # (just a hint for gunicorn+wget)
    flashcam flask5000 [-w]   #  view on port 5000, immediatelly start browser tab

    flashcam savecfg [-a 11 ...]  # save cmdline parameters to congig for flask/gunicorn

..... advanced usage .... (accumulation, blur, threshold, frame_kind)
    flashcam show -a 19 -b 3 -t 100 -f [direct|delta|detect|histo]  [-h]  [-l 3600]

....  v4l setting .......... (exposure, gain  for automatically recommended video)
    flashcam v4l -e [auto | 0.0..1.0]  -g [0.0..1.0]

...... uninteruptable stream .....................
    flashcam uni http://192.168.0.91:8000/video  [-s ] # to save avi

```

Typical usecase
---------------

### motion

``` {.bash org-language="sh"}
# tune parameters with flask5000 or show; no parameter == default value
# -w means - open web view
flashcam.py flask5000  -w -l 1 -a 11 -b 11 -t 30
# save config
flashcam.py savecfg -l 1 -a 11 -b 11 -t 50
# run server - ONE worker, many threads
#    option flask should start wget with delay to start the camera
flashcam.py flask& gunicorn --threads 5  -w 1 -b 0.0.0.0:8000  --timeout 15 web:app
```

### astro

``` {.bash org-language="sh"}
#  x:- is compensate to right y:- is compensate to down;   -x -0.35  -y -0.015
# repair broken AVI
ls -1 *avi | xargs -n 1 -I III ffmpeg -i III -c:v copy -c:a copy repIII
```

### join many avi files from UNI

``` {.bash org-language="sh"}
ls zen_192.168.0.91_* | while read line; do echo file \'$line\'; done | ffmpeg -protocol_whitelist file,pipe -f concat -i - -c copy output.avi

```

Status:
-------

-   `usbcheck` can identify the camera by `product` or `IDpath`
-   `v4l2` prove of concept - exposure/gain autotune - worked
-   `show` (imshow) was tuned, now it needs a rewrite with `base_camera`
-   `flask` interface is responsive
-   `web.py` must be same with `flask5000` option
-   `base_camera` (with greenlets) and `real_camera` modules work with
    flask
    -   initialized with `recommend`
    -   never-stopping (unlike the original version)
    -   more tricky tuning classmethod andstaticmethod was needed
-   `flask` interface works
-   gray frame is sent when no camera through web
-   autostarts (threading) with `wget -u -p -O /dev/null` for 3 sec. and
    then kill
-   properly taken `product` in `real_cam`
-   rewrite proprerly for gunicorn (no gevent; --w 1 --t 5+); flashcam
    flask
-   with automatic wget to start, with debugprint for gunicorn too
-   !! `product` may not work now
-   `stream_enhancer` decorations ON
-   =detect motion basics ON -t threshold (0 - means NO)
-   three modes -a 10 -b 3 -t 100 -f \[direct\|delta\|detect\]
-   v4l commandline and in-image display works
-   astro delta x,y per second works
-   saving to \$HOME path
-   `uni` option ... uninteruptable view, \'s\' to save \'q\' to quit,
    -s to save avi

To see next
-----------

-   automatic exposure
-   save jpg from web

V4l2
----

Camera sometimes needs to tune at dark conditions. Nicely done project
to call `v4l2-ctrl` was used

Identification of a camera
--------------------------

Several devices on USB, replugging or an built-in webcam of the notebok
or sevral dev/video devices per CAM can make identification via
`/dev/video` more difficult.
