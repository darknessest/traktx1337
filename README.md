# Trakt.tv *x* 1337x

## Purpose

- automated tv shows torrents downloading, with trakt.tv synchronization 
- trakt.tv watched shows history export(?)

## General Information
**THIS PROJECT IS CURRENTLY UNFINISHED**

At the end this script should be deployable on a RPI0 (or any armv6 device).

Trakt.tv synchronization should be done only once(as trakt.tv might be unavailable), for the script initialization.
And later it'll keep info only about downloaded episodes and will periodically check for new episodes.

Torrents choosing should be done in intelligent way prioritizing following characteristics: 
- higher resolution(1080p) 
- smaller size(HEVC) 
- higher number of seeds/peers.

Reports about added/dowloaded tv shows can be delivered using IFTTT's API. 
Currently it's push notification. Considering to switch to emails.

Configuration info should be kept in `config.ini`. Considering to add encryption.


## Requirements

Python 3

Transmission (CLI)

*other requirements to be added*


## Usage

*to be added*


## ~~Support~~


## Acknowledgements
[xbgmsharp](https://github.com/xbgmsharp/trakt)'s repository was used as a reference for this project

## Licence

This script is free software:  you can redistribute it and/or  modify  it under  the  terms  of the  GNU  General  Public License  as published by the Free Software Foundation.

This program is distributed in the hope  that it will be  useful, but WITHOUT ANY WARRANTY; without even the  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

See <http://www.gnu.org/licenses/gpl.html>.
