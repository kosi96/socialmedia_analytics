# Social media analytics 

Social media corporations are collecting and using your data to enhance various kinds of algorithms.  
To get at least some use of collected data, you can request it manually from the corporations and analyse it
to see yours and friends texting behaviour.

## Description
You need to request data from social media manually. Currently we support social media exports from:
* instagram, 
* facebook, 
* whatsapp.

Analysis is done for 1 year.  
Only peer to peer conversation is supported (you vs friend).  
Friend username usually consist of __namesurname__ and exported data is collected in folder named as  __namesurname_RandomID__.  
If this is not the case you need to rename it manually.



## Getting Started

### Dependencies

* Python 3.9
* packages: os, csv, glob, json, re, pandas, collection, emoji, plotly fpdf


### Installing

* Collected data should be put into _data/raw/*SOCIAL_MEDIA_SOURCE*_

Example:
```bash
├── data/
    ├── raw/
        ├── facebook/
        │    └── messages/
        │          └── inbox/
        │              ├── name1surname1_randomid/
        │                        ├── gifs/
        │                        ├── photos/
        │                        └── message_1.json
        │              └── name2surname2_randomid/
        ├── instagram
        └── whatsapp

```

* A `config.json` is used to change the settings of an analysis. All fields are mandatory (`sources` can range from 1-3 sources).

Example:
```bash
{
  "my_username": "mynamemysurname",
  "friend_username": "name1surname1",
  "my_custom_name": "Me",
  "friend_custom_name": "Friend",
  "sources": [
    "whatsapp",
    "instagram",
    "facebook"
  ]
}

```
### Executing program

* How to run the program
```
python socialmedia_analytics/src/main.py
```

* Results

Generated PDF can be found in `pdf` folder.

## Authors

[Blaz Kosenina](https://si.linkedin.com/in/blaz-kosenina)

## Version History

[//]: # (* 0.2)

[//]: # (    * Various bug fixes and optimizations)

[//]: # (    * See [commit change]&#40;&#41; or See [release history]&#40;&#41;)
* 1.0 Version
    * Initial Release

## License

This project is licensed under the MIT License

