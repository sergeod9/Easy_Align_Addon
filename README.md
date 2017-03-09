# Easy_Align_Addon
<H3>Alignment tool for mesh objects for Blender 2.78</H3>

Easy Align addon allows you to align mesh objects origins and align mesh objects to each others easily, it works in both Edit mode and Object mode.<br>

To download this addon in Blender, click download at the top right corner of this page, when downloaded, unzip the downloaded file, open Blender, go to File > User Preferences, under Add-ons tab, choose Install from file, navigate to the addon file (Easy_Align_Addon_ver_1_0_2.py) and install. Check the checkbox in the addon's name to activate, if you want this addon to be available every time you start Blender, don't forget to Save User Settings.<br>

After installing Easy Align addon, the panel will be available in 3D View window, Properties shelf, if Properties shelf is hidden, press <kbd>N</kbd> while hovering over 3D View window.

<H3>Easy Align is devided into 4 distinctive functions:</H3>
1- <b>Align Origin:</b> This button allows you to align the origins of selected mesh objects according to the selected axis.<br>
2- <b>Align Objects:</b> Align Selected mesh object to Active mesh object. This will move the Selected mesh objects to the Active mesh object using selected axis input, other axes will be cetered, which is the main difference between this button and the next button's functionality.<br>
3- <b>Exclusively Align Objects:</b> Align Selected mesh objects to Active mesh object using selected axis exclusively, the Selected objects other axes location will not be affected.<br>
4- <b>Convenient Set Origin and Snap buttons:</b> This are the same functions that you can achieve in Blender using shortcuts <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>C</kbd> and <kbd>Shift</kbd> + <kbd>S</kbd> respectively in Object mode and Edit mode, I included them in the addon panel because I find the first shortcut awkward, so I could use a button to make it more accessible. The option <I>Snap Selection to Active</I> will through an error in Blender 2.77 since this function is not available in that Blender version.

<H3>Warnings:</H3> <br>
- If no selected object is mesh object, Easy Align panel will not be available.<br>
- This addon manipulates Selected and Active mesh objects origins, sets their selection method in Edit mode to Vertices, and changes their selected vertices. Before using this addon, make sure you apply any modifier that is affected by objects origins, such as Mirror modifier. In case you have selected faces or edges or vertices you need to keep, make sure you save these selections first before using this addons functions.<br>

I created this addon to use it in my work production, I'm publishing it under GPL license, for free, hoping other Blender users will find it useful.
Created for Blender 2.78, tested using Blender 2.78 and Blender 2.77, on machines running Windows 10 and Windows 7 respectively.
