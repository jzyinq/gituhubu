# gituhubu

CLI tool for speeding up searching repositories in your organization. 

It fetches your organization repository list and store it in local cache file, 
then utilize [fuzzy search finder](https://github.com/junegunn/fzf) 
through [iterfzf](https://github.com/dahlia/iterfzf) to speed up finding specific repository you'll need to clone, preview, or check it's changelog.

## Installation

```
pip3 install gituhubu
```

## Configuration

At first launch `gituhubu` will ask you to create a file `config.json` in specific location for your OS.

Example configuration:
```json
{
  "organization": "ORGANIZATION_NAME",
  "token": "API_TOKEN"
}
```

Where ORGANIZATION_NAME is a github organization you want to search and API_TOKEN is a github personal access token with minimum scope of `repos`.

More details about creating such token you can find in [github docs](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token). 

## Usage

### CLI mode
```
gituhubu
``` 

to invoke search list. Type any part of repository name you'll searching for and hit enter to select it.

After selection you will get a short details about repo and possible actions:

```
Repository Name - last update: 2020-09-25T07:51:48Z #TODO fix that date 
Actions: 
- (o)pen in browser
- (c)lone
- view c(h)angelog
```

- `o` - will open given repository in your default browser
- `c` - will clone through ssh given repository to current working directory
- `h` - will try to open `/CHANGELOG.md` repository file in your default browser

### Rofi mode

For those using [rofi](https://github.com/davatorium/rofi) as application launcher, you can use gituhubu as a custom mode.
```
rofi -modi gituhubu:"gituhubu --rofi" -show gituhubu
```
Selecting given repository in rofi mode opens it in your default browser.
