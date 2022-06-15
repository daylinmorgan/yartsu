CONSOLE_SVG_FORMAT = """\
<svg class="rich-terminal" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <!-- Generated with Rich https://www.textualize.io -->
    <style>
    @font-face {{
        font-family: "Fira Code";
        src: local("FiraCode-Regular"),
            url("https://cdn.jsdelivr.net/gh/ryanoasis/nerd-fonts@2.1.0/patched-fonts/FiraCode/Regular/complete/Fira%20Code%20Regular%20Nerd%20Font%20Complete.ttf") format("truetype");
        font-style: normal;
        font-weight: 400;
    }}
    @font-face {{
        font-family: "Fira Code";
        src: local("FiraCode-Bold"),
            url("https://cdn.jsdelivr.net/gh/ryanoasis/nerd-fonts@2.1.0/patched-fonts/FiraCode/Bold/complete/Fira%20Code%20Bold%20Nerd%20Font%20Complete.ttf") format("truetype");
        font-style: bold;
        font-weight: 700;
    }}
    .{unique_id}-matrix {{
        font-family: Fira Code, monospace;
        font-size: {char_height}px;
        line-height: {line_height}px;
        font-variant-east-asian: full-width;
    }}
    .{unique_id}-title {{
        font-size: 18px;
        font-weight: bold;
        font-family: arial;
    }}
    {styles}
    </style>
    <defs>
    <clipPath id="{unique_id}-clip-terminal">
      <rect x="0" y="0" width="{terminal_width}" height="{terminal_height}" />
    </clipPath>
    {lines}
    </defs>
    {chrome}
    <g transform="translate({terminal_x}, {terminal_y})" clip-path="url(#{unique_id}-clip-terminal)">
    {backgrounds}
    <g class="{unique_id}-matrix">
    {matrix}
    </g>
    </g>
</svg>
"""
