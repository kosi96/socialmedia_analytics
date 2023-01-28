# Social media analytics 

Social media corporations are collecting and utilizing user data to enhance various kinds of algorithms.
Collected user data need to be available to the user and can be retrieved via a manual request from their website.   
This data can be further analysed
with the help of __social media analytics tool__, which outputs a PDF with a brief insight into the texting behavior of the participants.

![Generated PDF](pdf/sample/myusername_friendusername.png)

## Description
Currently supported sources:
* [instagram](https://help.instagram.com/181231772500920), 
* [facebook](https://www.facebook.com/help/212802592074644), 
* [whatsapp](https://faq.whatsapp.com/1180414079177245/?cms_platform=android).


Only peer to peer conversation is supported (you vs friend).  
Data export from a specific source usually consist of 
multiple folder named as __namesurname_RandomID__. If this is not the case, you need to rename conversation folder manually.

## Supported use cases
**Message throughout the history**.shows overall texting trend. 

**Favorite emojis**.shows favorite use of emojis (reactions are omitted).

**Response time**.shows response time per source. Response time is recorded only during daytime (07:00 - 23:00), 
where response time can not be longer than 24h (people often forget to replay).

**Message throughout the day**.shows person texting habit during the day.

## Getting Started


### Dependencies

* Python 3.9
* packages: os, csv, glob, json, re, pandas, collection, emoji, plotly fpdf


### Installing

* Collected data should be put into _data/raw/*SOCIAL_MEDIA_SOURCE*_


Structure sample:
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

**Config sample**:
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

Generated PDF can be found in `pdf/results` folder (see example).

## Authors

[Blaž Košenina](https://si.linkedin.com/in/blaz-kosenina)

## Version History

* 1.0 Version
    * Initial Release

## License

This project is licensed under the MIT License

