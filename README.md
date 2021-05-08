# Flickr Image Downloader

This repository implements a simple image downloader from flickr.

I build to download images to train computer vision models.

## Demo
<img src="demo.gif">


## Configurations
You need a flickr ID and Secret Code that can be obtained [here](https://www.flickr.com/services/api/misc.api_keys.html). After that, insert those values in the file [config.yaml](web-app/config.yaml).


## Install
1. Clone this repository
```bash
git clone https://github.com/renatoviolin/flickr-downloader.git
cd flickr-downloader
```

2. Install packages
```bash
pip install -r requirements.txt
```

3. Start the web-app
```bash
cd web-server
uvicorn server:app --host 0.0.0.0 --port 8000 &
```


5. Open your browser
http://localhost


## References

[Jeff Heaton repository](https://github.com/jeffheaton) 