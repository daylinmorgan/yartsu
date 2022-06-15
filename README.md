# YARTSU


<div id="top"></div>

<!-- PROJECT LOGO -->
<div align="center">
  <a href="https://github.com/daylinmorgan/yartsu">
    <img src="https://raw.githubusercontent.com/daylinmorgan/yartsu/main/assets/logo.svg" alt="Logo" width=600 >
  </a>
  <p align="center">
    yartsu, another rich terminal screenshot utility
  </p>
</div>
<br />

<!-- PROJECT SHIELDS -->
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



**NOTE**: this is a currently in a beta release and the API is subject to change (feedback welcome)

Inspired by recent commits in the wonderful library [`rich`](https://github.com/Textualize/rich) I decided to write ` yartsu`.

I needed to programatically generate screenshots for documentation purposes. The new `export_svg` methods in `rich` were a godsend.
So I wanted to try to make this feature a little more generalizable to program ouptut outside of `rich`/`python`.
Hopefully, you find it useful.

If you come across anything unexpected please submit an issue.

## Install

```bash
pip install yartsu
```

You can also install the [`shiv`](https://github.com/linkedin/shiv) based zipapp from the releases page.

With `cURL`:
```bash
curl -o ~/bin/yartsu -fL https://github.com/daylinmorgan/yartsu/releases/download/v22.06-beta1/yartsu
chmod u+x ~/bin/yartsu
```

With [`eget`](https://github.com/zyedidia/eget):

```bash
eget daylinmorgan/yartsu
```

## Usage

<div align="center"><img src="https://raw.githubusercontent.com/daylinmorgan/yartsu/main/assets/yartsu.svg" alt="Logo" width=600 ></div>

Getting a properly formatted output from a terminal screenshot is challenging.

There are three options for generating a screenshot.

If one of the below option causes you any headaches consider first trying a different option.

### Option 1: Pipes

Many tools that color output (i.e. `grep` or `ls`) additionally allow
you to force ANSI color codes to be included even when piping output.

In these cases you can simply pipe the output directly into `yartsu`

```bash
ls --color=always | yartsu -w 50 -o assets/ls_color.svg
```

### Option 2: Subprocess/Pty

With this option `yartsu` will deploy a `subprocess` and `pty`
to run your command for you in an attempt to preserve ANSI.

Note with this option you need to seperate
the command you want to run with `yartsu` args using `--`.

```bash
yartsu -w 50 -o assets/ls_color.svg -- ls --color /
```

### Option 3: Text File

Finally, if you neither of the above options work and you can
manage to preserve the codes in a plain text file you can pass this as input to `yartsu`.

```bash
ls --color > ls.txt
yartsu -w 50 -i ls.txt -o assets/ls_color.svg
```

By default svgs will be saved at `./capture.svg`.

Additionally, for options 1 and 3 you may want to define your own title with `-t/--title`.
For option 2 the title will by default be the cmd ran by `yartsu`.

### Themes:

There are a number of themes you can use to style output.
Use `yartsu --list-themes` to see the available options.
Then you can specify the theme you want with `--theme`, i.e. `yartsu --theme rich_default`.
You may also use the environment variable `YARTSU_THEME`.

See [here](https://github.com/daylinmorgan/yartsu/blob/main/docs/themes.md) a preview of the available themes

### Supported Characters

Currently `yartsu` loads the `nerd font` patched FiraCode font.
This should result in general support for emoji's and `nerd font` icons.

<div align="center"><img src="https://raw.githubusercontent.com/daylinmorgan/yartsu/main/assets/demo.svg" alt="Logo" width=400 ></div>

**Note**: github won't load the font's when displaying on the README. Click on the `svg` to see the `nerd font` icons.


## TODO

- [ ] add unit tests
- [x] add support for nerd-fonts
- [ ] add optional shadow
- [ ] add more themes


<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/daylinmorgan/yartsu.svg?style=flat
[contributors-url]: https://github.com/daylinmorgan/yartsu/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/daylinmorgan/yartsu.svg?style=flat
[forks-url]: https://github.com/daylinmorgan/yartsu/network/members
[stars-shield]: https://img.shields.io/github/stars/daylinmorgan/yartsu.svg?style=flat
[stars-url]: https://github.com/daylinmorgan/yartsu/stargazers
[issues-shield]: https://img.shields.io/github/issues/daylinmorgan/yartsu.svg?style=flat
[issues-url]: https://github.com/daylinmorgan/yartsu/issues
[license-shield]: https://img.shields.io/github/license/daylinmorgan/yartsu.svg?style=flat
[license-url]: https://github.com/daylinmorgan/yartsu/blob/main/LICENSE.txt
