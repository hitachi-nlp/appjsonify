Prerequisites
===
[Go back to top](../README.md)

If your environment does not have `poppler`, please first follow below and install it.
This is necessary to obtain PDF images for bounding box detection, using [`pdf2image`](https://github.com/Belval/pdf2image).

## macOS
```bash
brew install poppler
```

## Linux
### Configs
```bash
echo "export PATH=$HOME/usr/poppler/bin:$PATH" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=${HOME}/usr/poppler/lib:$LD_LIBRARY_PATH" >> ~/.bashrc
source ~/.bashrc
mkdir $HOME/usr
mkdir $HOME/usr/poppler
```
> Here we assume that we do not have the `root` privilege.

### poppler-data
```bash
wget https://poppler.freedesktop.org/poppler-data-0.4.7.tar.gz
tar -xf poppler-data-0.4.7.tar.gz
cd poppler-data-0.4.7
```

Then, please modify `Makefile` accordingly:  
```Makefile
PACKAGE    = poppler-data
VERSION    = 0.4.7
distdir    = $(PACKAGE)-$(VERSION)
prefix     = ${HOME}/usr/poppler
datadir    = $(prefix)/share
pkgdatadir = $(datadir)/poppler
```
> Please edit `prefix` to install locally.

Finally, please run the followings:
```bash
make install
cd ..
```

### poppler-utils  
```bash
wget https://poppler.freedesktop.org/poppler-0.48.0.tar.xz
tar -xf poppler-0.48.0.tar.xz
cd poppler-0.48.0
./configure --prefix=${HOME}/usr/poppler
make
make install
```
