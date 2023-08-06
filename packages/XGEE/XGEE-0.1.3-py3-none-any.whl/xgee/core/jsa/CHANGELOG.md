# jsApplication Changelog

### v0.6.1
* Transparent menus and popups introduced (uses backdropFilter, which is disabled in the current firefox by default. Can be enabled in the settings)
* Visual adaptation of tabs: inactive tabs are now partially transparent
* Visual adaptation of the application tabbar: is now borderless
* Made view header high equal to tabbar height, which looks better by default
* Various CSS simplifications especially for tabs and popup arrows

### v0.6.0

* Removed boostrap as a dependecy.
* Added UI elements: Progressbar, Label, and Icon.
* Refactored the implementation of Menu, MenuEntry, Bubble, Sticky, View, Dash, and Tool such that they contain less HTML code. 
* Many of the abstract base classes were refactored to reduce the code and ease the creation of complex UI element, e.g. with AddChild forwarding to subelements.
* Refactored event system: Use jsa.EVENT as new central focal point. It provides static definitions of common event types as well as checker functions.
* Refactored Bubble, Sticky and View controls with new icons and a generic implementation.
* Added tooltip: Every UI element can have a tooltip, which shows if the mouse stops for a short period over the element.
* Added the possibility to have close controls on Tabs
* Added the option to have a Bubble to be docked as a View in a ViewManager
* Refactored the CSS styles completly: All jsa styles are not starting with "jsa-". Devided global vars in the categories ctrl, dialog, popup, and app.
* Many bugfixes in js, CSS, and the documentation.

### v0.5.3

* Added raw set and get functions to TextCtrl.

### v0.5.2

* SettingsManager changed to local storage.

### v0.5.1

* SettingsManager added, which can store abitrary user settings in cookies.
* Smaller spelling and bugfixes

### v0.5.0

* Initial version