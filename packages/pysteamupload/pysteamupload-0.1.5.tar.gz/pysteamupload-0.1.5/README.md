# PySteamUpload

A convenient tool to upload easily your binaries to Steam.

## How does it work ?

`PySteamUpload` requires several environment variables:
- `STEAM_USERNAME`
- `STEAM_PASSWORD`
- `STEAM_CONFIG_VDF_FILE_CONTENT`
- `STEAM_SSFN_FILE_CONTENT`
- `STEAM_SSFN_FILE_NAME`

`STEAM_USERNAME` and `STEAM_PASSWORD` are pretty obvious.<br>
The three following exist to deal with [SteamGuard](https://help.steampowered.com/en/faqs/view/06B0-26E6-2CF8-254C) (if not setup on your account, do it now !).
This is helping to integrate `PySteamUpload` into your `Continous Deployment` framework.<br>

`STEAM_CONFIG_VDF_FILE_CONTENT` and `STEAM_SSFN_FILE_CONTENT` should be <u>encoded in `base64`</u> and <u>double-quoted</u> in `.env` file.

## Using PySteamUpload in local

Create a `.env` file and fill the 5 variables (see example below).<br>
Or you can set the variables directly in your environment.

### Example of `.env`
```ini
STEAM_USERNAME=PySteamUpload
STEAM_PASSWORD=PySteamUpload

STEAM_CONFIG_VDF_FILE_CONTENT="ABCDEFD
ABCDEFABCDEFABCDEFABCDEFABCDEFABCDEF
ABCDEFABCDEFABCDEFABCDEFABCDEFABCDEF"

STEAM_SSFN_FILENAME=ABCDEFDABCDEFD

STEAM_SSFN_FILE_CONTENT="ABCDEFDABCDEFD
ABCDEFDABCDEFDABCDEFDABCDEFDABCDEFDABCDEFD
ABCDEFDABCDEFDABCDEFDABCDEFDABCDEFDABCDEFD"
```

### Call PySteamUpload by command line

`python -m pysteamupload --app_id="123456" --depot_id="1234567" --build_description="My first upload" --content_path="C:\Temp\MyBinariesAreLocatedHere"`

### Packaging

- `python -m install twine setuptools wheel`
- `python setup.py sdist bdist_wheel`
- `python -m twine upload dist/*`
