<div align="center">
  <h1>Auto Chiseler</h1>
</div>

[![License][shield-license]][link-license]
[![GitHub][shield-github]][link-github]
[![Git][shield-git]][link-git]
[![GitHub Actions][shield-ghactions]][link-ghactions]
[![Build][shield-build]][link-build]
[![Python][shield-python]][link-python]
[![Contributors welcome][shield-contributing]][link-contributing]

## Overview

**Auto Chiseler** (*olim* *Pip Reroller*, intra systema vocatus *PIPRR*) is a Pythonic, image-analytic, event-driven automation apparatus engineered to orchestrate rank-based object detection and iterative interaction within the [*Dig!* Roblox Experience](https://www.roblox.com/games/3233893879/Dig). It harnesses the computational vision faculties of OpenCV, the interface gestalt of tkinter, and the input synthesis capabilities of the `ahk` AutoHotkey binding to achieve precise manipulation of graphical user elements.

This system performs continuous raster interrogation (*interrogatio bitmapica*) over dynamically sampled screen regions, employing spectral and structural classification to discern object ranks (SS, S, A, et cetera). Upon fulfillment of user-configured quality predicates, the execution loop effectuates controlled click emissions and halts operation, thereby optimizing user input cycles during the reroll process.

Also see: [Auto Appraiser](https://github.com/AlinaWan/kc-dig-tool-configs/tree/main/KC-Tool-Suite/auto-appraiser)

---

## Setup Instructions

### Option 1. Use the pre-compiled executable

1. Download the latest executable from the [releases page](https://github.com/AlinaWan/auto-chiseler/releases/latest).
2. Run the executable file. The Python and AutoHotkey interpreters are already bundled; no external installations are required.

> [!IMPORTANT]
> If Windows Defender quarantines or deletes the file, restore it or temporarily turn off real-time protection in your system settings.
> This issue is a **false positive**. The macro does not contain any malicious code.

### Option 2. Run from source


#### Requirements

* Python 3.x
* [AutoHotkey](https://www.autohotkey.com/) v1.1 (must be installed and on your system PATH)
* Python packages listed in `requirements.txt`

1. **Clone the repository**

   ```bash
   git clone https://github.com/AlinaWan/auto-chiseler.git
   cd pip-reroller
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** If you encounter an error related to `AutoHotkey.exe` not being found on your system `PATH`, try installing the binary extras with:
   >
   > ```bash
   > pip install "ahk[binary]"
   > ```

3. **Run the application**

   ```bash
   python main.pyw
   ```

4. (Optional) If you also want to **compile the executable**, the build command is:
   ```bash
   nuitka main.pyw --standalone --onefile --windows-console-mode=disable --enable-plugin=tk-inter --enable-plugin=pylint-warnings --include-module=ahk --include-module=jinja2 --include-package=ahk --include-package=jinja2 --include-package-data=ahk --include-package-data=jinja2 --include-package=markupsafe --include-package=cv2 --include-package=pynput --include-package=win32gui --include-package=win32ui --include-package=win32con --include-package=six --windows-icon-from-ico=assets/favicon.ico --include-data-files=assets/AutoHotkey.exe=assets/AutoHotkey.exe --output-filename=AutoChiseler.exe --output-dir=build --assume-yes-for-downloads
   ```

---

## Usage

1. **Select Area**  
   Click the **Select Area** button, then drag on the screen to select the region containing the pip ranks (e.g. SS, S, A).  
   ![Selection Example](/assets/piprr_selection_example.png)
> [!IMPORTANT]
> The area should include only the pip rank area, not the area where stat value is (see the example image above).

2. **Set Chisel Button**  
   Click **Set Chisel Button**, then click on the orange pencil icon for the charm you want to reroll.  
   ![Chisel Button](/assets/chisel_button.png)

3. **Set Buy Button**  
   Click **Set Buy Button**, then click on the confirmation "Yes" button that appears after clicking the chisel button.

4. **(Optional) Adjust Input Fields**

   * **Click Delay (ms):** Milliseconds to wait between clicking the chisel and buy buttons.
   * **Post Reroll Delay (ms):** Extra time to wait after buying a reroll, before continuing. Helps prevent accidental rerolls or deletion caused by inventory shifting if the game or network is slow.
   * **Image Poll Delay (ms):** How frequently the script captures and processes a new screenshot. Lower values mean faster detection but higher CPU usage.
   * **Color Tolerance:** How close a pixel’s color must be to the target rank color for it to be detected (higher = more lenient).
   * **Object Tolerance (px):** Pixel distance threshold for merging close detected bounding boxes into a single object.
   * **Minimum SS:** The minimum number of **SS** ranks required to stop rerolling. For example, if set to **1**, the tool stops when at least one SS is found.
   * **Minimum Objects:** The minimum number of detected objects of at least the chosen minimum quality required to stop.
   * **Minimum Quality:** Select the lowest rank (F, D, C, B, A, S, SS) you accept for stopping. Only pips **at least this rank** or higher are counted toward the minimum objects condition.
  
> [!NOTE]
> This tool does not evaluate stat values themselves. It only detects each pip's visual rank based on color.

> [!CAUTION]
> If the **post reroll delay** is too short, the charm underneath may get deleted or rerolled.  
> This happens because the old charm briefly disappears from your inventory before the new one is added, and during that time, the charm below it can temporarily take its place for a few milliseconds.
> Equipping the charm below can prevent rerolling it, but it won't prevent deletion if it's a deletable charm.

5. **(Optional) Start Preview**  
   Use **Start Preview** to see bounding boxes around detected objects in real time in a separate window. Press **Q** in the preview window to exit.

6. **Start/Stop Automation**  
   Press **F5** to toggle the automation running state. The status text on the GUI indicates whether the tool is **Running** or **Suspended**.

7. **(Advanced) Dumping Logs**  
   To enable debug logging and access the log dumping feature:

   1. Open the `config.py` file in the project directory.
   2. Set the `ENABLE_LOGGING` variable to `True`:

      ```python
      ENABLE_LOGGING = True
      ```

   Once enabled:

   * A **DEBUG: Dump Logs** button will appear in the **top-left corner** of the GUI.
   * The **top-right corner** will show a status message indicating how many logs are currently stored in memory.
   * Clicking the dump button writes the buffered logs into a `.txt` file in the **current working directory**.

> [!NOTE]
> Logs are collected in memory during execution and only written to disk when the dump button is pressed.

---

## Stopping Logic: Condition Hierarchy

Pip Reroller will only stop rerolling when **both** of the following conditions are met:

1. **Minimum Objects:** At least the specified number of pips (`Minimum Objects`) are detected that are >= your chosen `Minimum Quality`.
2. **Minimum SS:** At least the specified number of pips are detected that are of the **SS** rank.

> **Both conditions must be true at the same time before the tool will stop.**

### Example Stopping Cases

Suppose:
- Minimum Objects = 3
- Minimum SS = 1
- Minimum Quality = C

| Detected Ranks     | Stops? | Reason                           |
|--------------------|--------|----------------------------------|
| SS, F, F           | No     | Only 1 ≥C, needs 3               |
| SS, C, F           | No     | Only 2 objects ≥C, at least 1 SS |
| SS, SS             | No     | Only 2 objects                   |
| A, B, B            | No     | 3 objects ≥C, but no SS          |
| SS, C, B           | Yes    | 3 objects ≥C, at least 1 SS      |
| SS, SS, SS         | Yes    | 3 objects ≥C, all SS             |
| SS, C, C, F        | Yes    | 3 objects ≥C, at least 1 SS      |

### Example Goal-Based Configurations

> Want to build your configuration based on a *target outcome*? Here are some examples:

#### Example Goal 1: You want to stop only if you get **A, A, SS**

* Set **Minimum Objects** = 3
  (because you want 3 A+ pips total)
* Set **Minimum Quality** = A
  (because you want all pips to be at least A)
* Set **Minimum SS** = 1
  (because you require at least one SS pip)

> This ensures all pips are A or higher, and one must be SS before it stops.

#### Example Goal 2: You want **at least 2 SS**, regardless of other pips

* **Minimum Objects** = 2
* **Minimum Quality** = F (or the lowest allowed)
* **Minimum SS** = 2

> Tool stops when there are at least 2 pips total, both of which are SS.

#### Example Goal 3: You want **S+, but don’t care if SS appears**

* **Minimum Objects** = 3
* **Minimum Quality** = S
* **Minimum SS** = 0

> Will stop when at least 3 ranks are S or higher, even if SS is not present.

---

## Notes

* The tool detects pip ranks based on their colors (SS, S, A, etc) using default reference colors. Adjust the color tolerance for best results depending on your screen and lighting.
* You must select the area and both button positions before starting automation.
* Automation clicks use AutoHotkey for compatibility with games and programs that block simulated clicks from other libraries.

---

## Troubleshooting

Having issues? Here are some common problems and how to fix them:

* **Wrong stats being detected (e.g. detecting bottom charm's stats):**
  This usually means your ping is too high. After a reroll, the game takes longer to return the new charm, and the tool may detect the charm below it instead.

* **Charm gets deleted or rerolled unintentionally:**
  Another ping-related issue. Try increasing the **Post Reroll Delay** in the app settings to give the game more time to refresh the inventory before the next action is taken.

* **Tool clicks the chisel button but doesn’t click the buy button afterward:**
  Increase the **Click Delay** setting. If the delay is too short, the confirmation dialog may not appear in time for the buy click to register.

* **Nothing is being detected at all:**
  Increase the **Color Tolerance** slider. The app might be too strict in matching pip rank colors, especially if your screen has unusual brightness or color settings.

* **Wrong ranks being detected or multiple ranks detected as the same:**
  Decrease the **Color Tolerance**. It’s likely the app is being too lenient and is matching different colors as the same rank.

* **An object is split into multiple bounding boxes:**
  Increase the **Object Tolerance** (in pixels). This setting controls how close detected pixels must be to be merged into the same object. If it's too low, even parts of the same pip might be counted as separate objects.

* **Automation starts but nothing happens:**
  Make sure you selected an area and both buttons (Chisel and Buy) before pressing **F5**. The automation won’t do anything without those.

---

## End Notes
Join the [Dig Tool Discord server](https://discord.com/invite/mxE7dzXMGf).

---

## License

Pip Reroller and this repository are licensed under the [MIT License](LICENSE).

> The pre-compiled binary files under [Releases](https://github.com/AlinaWan/auto-chiseler/releases) are licensed under the [GNU GPLv3](/assets/GPLv3.LICENSE). [Learn more](/assets/binary_license_notice.md).

## Credits

Some logic for **selection area handling** and **bounding box preview** was borrowed and adapted from [iamnotbobby](https://github.com/iamnotbobby), also under the MIT License.

<!-- Badge Variables -->
[shield-license]: https://img.shields.io/github/license/AlinaWan/auto-chiseler
[link-license]: LICENSE

[shield-github]: https://img.shields.io/badge/GitHub-%23121011.svg?logo=github&logoColor=white
[link-github]: https://github.com/

[shield-git]: https://img.shields.io/badge/Git-F05032?logo=git&logoColor=fff
[link-git]: https://git-scm.com/

[shield-ghactions]: https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white
[link-ghactions]: https://docs.github.com/en/actions

[shield-build]: https://img.shields.io/github/actions/workflow/status/AlinaWan/auto-chiseler/build_and_release.yml
[link-build]: https://github.com/AlinaWan/auto-chiseler/actions/workflows/build_and_release.yml

[shield-contributing]: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
[link-contributing]: /CONTRIBUTING.md

<!--
[shield-json-validate]: https://img.shields.io/github/actions/workflow/status/AlinaWan/kc-dig-tool-configs/validate_jsons.yml?label=JSON%20Validity
[link-json-validate]: https://github.com/AlinaWan/kc-dig-tool-configs/actions/workflows/validate_jsons.yml

[shield-pattern-suite-ci]: https://img.shields.io/github/actions/workflow/status/AlinaWan/kc-dig-tool-configs/render_patterns.yml?label=Pattern%20Suite%20CI
[link-pattern-suite-ci]: https://github.com/AlinaWan/kc-dig-tool-configs/actions/workflows/render_patterns.yml

[shield-readme-ci]: https://img.shields.io/github/actions/workflow/status/AlinaWan/kc-dig-tool-configs/shovel_readme_update.yml?label=README%20CI
[link-readme-ci]: https://github.com/AlinaWan/kc-dig-tool-configs/actions/workflows/shovel_readme_update.yml

[shield-md]: https://img.shields.io/badge/Markdown-%23000000.svg?logo=markdown&logoColor=white
[link-md]: https://www.markdownguide.org/basic-syntax/

[shield-json]: https://img.shields.io/badge/JSON-000?logo=json&logoColor=fff
[link-json]: https://www.json.org/json-en.html
-->

[shield-python]: https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff
[link-python]: https://www.python.org/

<!--
[shield-autohotkey]: https://img.shields.io/badge/AutoHotkey-green?logo=autohotkey&logoColor=white
[link-autohotkey]: https://www.autohotkey.com/
-->

