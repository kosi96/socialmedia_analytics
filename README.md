# Social media analytics 

Social media corporations are collecting and using user data to enhance various kinds of algorithms.
Collected data is user property, and he can request it from their website.   
This data can be further analysed
with the help of __social media analytics tool__, which outputs a nice PDF with a brief insight into 
pearson texting behavior.


## Description
You need to request data exports from social media manually. Currently, we support sources from:
* instagram, 
* facebook, 
* whatsapp.


Only peer to peer conversation is supported (you vs friend).  
Friend username usually consist of __namesurname__. Collected data export from a source usually consist of 
multiple folder named as __namesurname_RandomID__. If this is not the case you need to rename it manually.

## Supported use cases
**Message throughout the history**.shows texting trend in the past the history.

**Favorite emojis**.shows favorite use of emojis (reactions are omitted from the analysis).

**Response time**.shows response time per source. Response time is recorded only during the "day" (23:00 - 07:00 is considered sleep time) and can be 24h max
(people usually see message within one day, but often forget to replay).

**Message throughout the day**.shows person texting habit during the day.

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
        │   │
        │   ├── name1surname1_randomid/
        │           ├── gifs/
        │           ├── photos/
        │           └── message_1.json
        │   └── name2surname2_randomid/
        │
        │
        ├── instagram
        └── whatsapp

```

* Settings from `config.json` are used for social media analysis, where all fields are mandatory.

**Config example**:
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
cd socialmedia_analytics
python src/main.py
```

* Results

Generated PDF can be found in `pdf/results` folder (See an example in pdf folder).

## Authors

[Blaž Košenina](https://si.linkedin.com/in/blaz-kosenina)

## Version History

* 1.0 Version
    * Initial Release

## License

This project is licensed under the MIT License

