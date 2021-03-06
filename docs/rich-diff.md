
# Deviation From Rich

## Versions

- Rich: 12.4.4
- Yartsu: 22.6b5

## CONSOLE_SVG_FORMAT Diff

```diff
--- 
+++ 
@@ -1,20 +1,17 @@
-<svg class="rich-terminal" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
+<svg class="rich-terminal shadow" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
     <!-- Generated with Rich https://www.textualize.io -->
     <style>
-
     @font-face {{
         font-family: "Fira Code";
         src: local("FiraCode-Regular"),
-                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2") format("woff2"),
-                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff") format("woff");
+            url("https://cdn.jsdelivr.net/gh/ryanoasis/nerd-fonts@2.1.0/patched-fonts/FiraCode/Regular/complete/Fira%20Code%20Regular%20Nerd%20Font%20Complete.ttf") format("truetype");
         font-style: normal;
         font-weight: 400;
     }}
     @font-face {{
         font-family: "Fira Code";
         src: local("FiraCode-Bold"),
-                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2") format("woff2"),
-                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff") format("woff");
+            url("https://cdn.jsdelivr.net/gh/ryanoasis/nerd-fonts@2.1.0/patched-fonts/FiraCode/Bold/complete/Fira%20Code%20Bold%20Nerd%20Font%20Complete.ttf") format("truetype");
         font-style: bold;
         font-weight: 700;
     }}
@@ -32,6 +29,10 @@
         font-family: arial;
     }}
 
+    .shadow {{
+        -webkit-filter: drop-shadow( 2px 5px 2px rgba(0, 0, 0, .7));
+        filter: drop-shadow( 2px 5px 2px rgba(0, 0, 0, .7));
+    }}
     {styles}
     </style>
 
@@ -43,7 +44,7 @@
     </defs>
 
     {chrome}
-    <g transform="translate({terminal_x}, {terminal_y})" clip-path="url(#{unique_id}-clip-terminal)">
+    <g transform="translate({terminal_x}, {terminal_y}) scale(.95)" clip-path="url(#{unique_id}-clip-terminal)">
     {backgrounds}
     <g class="{unique_id}-matrix">
     {matrix}

```

## Console.export_svg Diff

```diff
--- 
+++ 
@@ -64,9 +64,9 @@
         line_height = char_height * 1.22
 
         margin_top = 1
-        margin_right = 1
-        margin_bottom = 1
-        margin_left = 1
+        margin_right = char_width * 5 / 6
+        margin_bottom = 20 * 5 / 3
+        margin_left = char_width * 5 / 6
 
         padding_top = 40
         padding_right = 8
@@ -214,8 +214,8 @@
                 x=terminal_width // 2,
                 y=margin_top + char_height + 6,
             )
-        chrome += f"""
-            <g transform="translate(26,22)">
+        chrome += """
+            <g transform="translate(32,22)">
             <circle cx="0" cy="0" r="7" fill="#ff5f57"/>
             <circle cx="22" cy="0" r="7" fill="#febc2e"/>
             <circle cx="44" cy="0" r="7" fill="#28c840"/>

```

AUTO-GENERATED by ./scripts/rich-diff
