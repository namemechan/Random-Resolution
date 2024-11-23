# Random-Resolution
webui Random Resolution script

This is a script for WebUI that randomly selects and applies one of the chosen resolutions during image generation.

Additionally, you can specify the number of iterations for repeated generation and set a delay between generations.

It was created for use with the amazing TIPO extension.(https://github.com/KohakuBlueleaf/z-tipo-extension)

Note: Its functionality with Forge (reforge) has not been tested.

[Set up]
======
`Random-Resolution.py` in to `stable-diffusion-webui\scripts`


[How to Use]
======

From the script list, select [Random-Resolution], and check [Enable Random Resolution].

Enter your desired width * height resolution combinations and select the ones you want to use (up to 9 combinations).

If you want to generate multiple images, input the number in [Number of Batches].

To add a delay between generations, enter the time (in seconds) in [Delay between batches (seconds)].
(It’s always good to give your GPU some breathing time!)

Even if you don’t check [Enable Random Resolution], you can still use the functions in steps 3 and 4 as long as [Random-Resolution] is selected in the script list.

---
![yes](https://github.com/user-attachments/assets/a8d0fb53-b2ff-4653-9ad2-415d509ff56d)
