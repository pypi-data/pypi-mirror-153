Welcome
====
Hey! Thanks for checking out this repo. This library is something I hacked together out of frustration due to managing localized strings for an iOS and Android application. The process is tedious, manual, and consumes more time than it's worth.

There's plenty of tools that make managing translations faily hands off for developers. However, those tools are rather pricy and I'd rather spend my budget on other tools to improve the quality and efficiency of our applications.

This library is by no means optimal but it fits our workflow. Please feel free to create issues or pull requests to help improve it and make it more generic.

*Note:* I can think of several other languages I should have written this in but I already had a chuck of this process written in python from 4 years ago. So I decided to build off of that to get a proof of concept.

Setup
====
Example `config.json` file:
```
{
    "string_index_filename": "string_index.json",
    "sheets_api": {
        "spreadsheet_id": "<sheet id from url>"
    },
    "applications": [
        {
            "platform": "android",
            "project_dir": "path/to/android/project",
            "strings_filename": "strings.xml",
            "languages": [
                "",
                "es-rMX", 
                "es-rEC",
                "es-rES"
            ],
            "default_language": "",
            "string_dirs": [
                "path/to/each/strings/dir"
            ]
        },
        {
            "platform": "ios",
            "project_dir": "path/to/ios/project",
            "strings_filename": "Localizable.strings",
            "languages": [
                "en",
                "es-MX", 
                "es-EC",
                "es-ES"
            ],
            "default_language": "",
            "string_dirs": [
                "path/to/each/strings/dir"
            ]
        }
    ]
}
```

You'll need to also have a `credentials.json` in order for this library to access the Google Sheet. You can follow [these instructions](https://developers.google.com/workspace/guides/create-credentials). An API key or service account is probably the most perferred option here but the library uses OAuth for now.

Usage
====
Install
----
```
pip install mobile-translation-manager
```


Init
----
```
>>> from mtm import manager
>>> manager.init("config.json")
```
This will create an index file of your current translations.

Sync
----
```
>>> from mtm import manager
>>> manager.sync("config.json")
```
This will sync the index file with all the translations from your applications and the google sheet.

Save
----
```
>>> from mtm import manager
>>> manager.save("config.json")
```
This will save all the translations in the index file to your application's project.

Deploy
----
```
>>> from mtm import manager
>>> manager.deploy("config.json")
```
This will sync all translations and deploy all the translations in the index file to the google sheet.
