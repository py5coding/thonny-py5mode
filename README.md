# thonny-py5mode

*A py5 plug-in for Thonny*

Use the [Thonny Python IDE](https://thonny.org/) as a Processing PDE alternative for creative coding. *Thonny-py5mode* is a plug-in that installs and configures Thonny for use with [py5](https://py5coding.org/), a Python (3.8+) framework that leverages Processing's core libraries.


## Instructions

If you already have some version of Thonny *that includes Python 3.8+* on your computer, you can skip straight to step 4.

1. Download and install the Thonny IDE from [https://github.com/thonny/thonny/releases](https://github.com/thonny/thonny/releases). Expanding the *Assets* will reveal the downloads for Windows/macOS/Linux --

   ![](https://raw.githubusercontent.com/py5coding/thonny-py5mode/main/screenshots/01-download-thonny.png)
   
   For your convenience, here are direct links to the downloads for Thonny 4.1.7:
   
    - [thonny-4.1.7.exe](https://github.com/thonny/thonny/releases/download/v4.1.7/thonny-4.1.7.exe) 🢠 for Windows
    - [thonny-4.1.7.pkg](https://github.com/thonny/thonny/releases/download/v4.1.7/thonny-4.1.7.pkg) 🢠 for MacOS
    - [thonny-4.1.7.bash](https://github.com/thonny/thonny/releases/download/v4.1.7/thonny-4.1.7.bash) 🢠 for Linux
   
   The thonny-py5mode plug-in will run fine with Thonny 4 because it ships with Python 3.10.

2. Start Thonny. If you're running it for the first time, just accept the *Standard* settings.

   ![](https://raw.githubusercontent.com/py5coding/thonny-py5mode/main/screenshots/02-start-splash.png)

3a. Once Thonny is open, select *Tools > Manage packages...*

   Then search for and install the __py5__ library --
   
3b. Still in Thonny, select *Tools > Manage plugins...*

   ![](https://raw.githubusercontent.com/py5coding/thonny-py5mode/main/screenshots/03.01-manage-plug-ins.png)

   Then search for and install the __thonny-py5mode__ plug-in --

   ![](https://raw.githubusercontent.com/py5coding/thonny-py5mode/main/screenshots/03.02-install-plug-in.png)

   You must __restart Thonny__ after this step.

4. When you've restarted Thonny, select *py5 > Imported mode for py5* --

   ![](https://raw.githubusercontent.com/py5coding/thonny-py5mode/main/screenshots/04.01-activate-imported-mode.png)

   Click *Proceed* to download, extract, and set up JDK-17 (if you need to know: the plug-in installs JDK in the Thonny user-config directory). Thonny only needs to download JDK the first time you switch to imported mode.

   ![](https://raw.githubusercontent.com/py5coding/thonny-py5mode/main/screenshots/04.02-download-jdk.png)

   You'll be notified once this process completes --

   ![](https://raw.githubusercontent.com/py5coding/thonny-py5mode/main/screenshots/04.03-download-jdk-done.png)

5. *This step is optional.* There are several Thonny settings that I recommend you apply for working with py5 (including a Processing 4 inspired theme, Kyanite). You can apply those settings in one simple step using  *py5 > Apply recommended py5 settings*

   ![](https://raw.githubusercontent.com/py5coding/thonny-py5mode/main/screenshots/05-apply-recommended-settings.png)

6. When the py5 *Imported mode for py5* option is checked, Thonny can run your py5 code --

   ![](https://raw.githubusercontent.com/py5coding/thonny-py5mode/main/screenshots/06.01-imported-activated.png)

   Test out an [imported mode](https://py5coding.org/content/py5_modes.html#imported-mode) sketch by clicking the green play button (or using the F5 or Ctrl+R keyboard shortcuts). Here is some code:

   ```python
   def setup():
       size(300, 200)
       rect_mode(CENTER)

   def draw():
       rect(mouse_x, mouse_y, 10, 10)
   ```

   ![](https://raw.githubusercontent.com/py5coding/thonny-py5mode/main/screenshots/06.02-running-sketch.png)

   NOTE: This mode also runs [static mode](https://py5coding.org/content/py5_modes.html#static-mode) sketches (when you don't need a `draw()` function for animation).

   Click the stop-sign (🛑) button in the Thonny toolbar to stop your sketch.


## Module Mode Sketches

To run a py5 [module mode](https://py5coding.org/content/py5_modes.html#module-mode) sketch, deactivate/uncheck *py5 > Imported mode for py5* first so that Thonny returns to its normal run behaviour (for running any Python script). As an example, you can try this code:

```python
import py5

def setup():
    py5.size(300, 200)
    py5.rect_mode(py5.CENTER)

def draw():
    py5.square(py5.mouse_x, py5.mouse_y, 10)

py5.run_sketch()
```

Note that module mode requires an `import py5` and `run_sketch()` line, and `py5.` prefixes.


## Useful py5 resources

py5 is a new version of Processing for Python 3.8+. It makes the Java Processing jars available to the CPython interpreter using JPype. It can do just about everything Processing can do, except with Python instead of Java code. Here are some useful py5 resources (alphabetically listed) --

* [py5 cheatsheet](https://raw.githubusercontent.com/py5coding/processing.py-cheat-sheet/master/py5/py5_cc.pdf)
* [py5 discussions/forum](https://github.com/py5coding/py5generator/discussions)
* [py5 documentation](https://py5coding.org/)
* [py5 examples](https://github.com/py5coding/py5examples)
* [Processing forum (py5 channel)](https://discourse.processing.org/c/28)
* [Villares' sketch-a-day archive](https://abav.lugaralgum.com/sketch-a-day/)


## Credits

Thanks [villares](https://github.com/villares/thonny-py5-runner) for inspiring me to develop this plug-in, [hx2A](https://github.com/hx2A/) for the awesome [py5 project](https://py5coding.org/), and the [Thonny folks](https://github.com/thonny) for their fantastic IDE. The *Color selector* incorporates Juliette Monsel's excellent [tkColorPicker](https://github.com/j4321/tkColorPicker) module.


## Todo List

See [discussions on GitHub repo](https://github.com/py5coding/thonny-py5mode/discussions/17). This plug-in is a work in progress ... please report issues [here](https://github.com/py5coding/thonny-py5mode/issues).
