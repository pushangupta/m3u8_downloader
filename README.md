# m3u8_downloader

A simple Python3 library for downloading mp4 files from m3u8 files fetched over the internet or from from the local path.
Currently supports Unix.

## Installation

Simply copy the python file in your working directory, then in terminal call 

``` python3 m3u8_downloader.py -p "https://somedomain.com/somelink/temp.m3u8"```

## Options

``` --path      -p```  Path: The path of the m3u8 file over the internet or the local machine

``` --output    -O```  Output directory: The directory where you want to store the file

``` --filename  -n```  Filename: The name of the file you want to keep (including the extension)

``` --base-link -b```  Base Link of the domain to fetch the chunks from. Useful in cases where the chunk's url is missing domain inside the m3u8 file.



## Todo 
##### [done] Create fetch domain of chunks if not provided
##### [done] Create custom path for saving the files
##### [•] Create custom headers
##### [•] Create custom proxies
##### [•] Create platform independence
##### [•] Check for 100% fail-safe
##### [•] Check for multiple resolutions

Pull requests, suggestions and issues are most welcome :)


###Important note: 
Please make sure that the m3u8 file you provide has a single resolution format.

If your file contains multiple resolutions, you may want to remove them manually. 
