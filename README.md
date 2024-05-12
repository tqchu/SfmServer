OpenSfM ![Docker workflow](https://github.com/mapillary/opensfm/workflows/Docker%20CI/badge.svg)
=======

## Overview
This is a sfm server using OpenSfM. Currently supports REST services.

Checkout this for more about [OpenSfM](https://opensfm.org/docs/using.html)

## Recommended python version
3.8
3.10 will not work

## Workaround
```
chmod +x set_up.sh
./set_up.sh
./run_server
```

## Getting Started

- Clone the repo recursively: `git clone --recursive https://github.com/tqchu/SfmServer`
- [Setup](https://opensfm.org/docs/building.html) (no need to build the docs)
- [Construction](https://opensfm.org/docs/using.html)
  + Setup viewer: `./viewer/node_modules.sh`
  + Reconstruct images: `bin/opensfm_run_all data/berlin`
  + [Optional] Dense point clouds:
  ```
    bin/opensfm undistort data/berlin
    bin/opensfm compute_depthmaps data/berlin
  ```
  + Start the server and view: `python3 viewer/server.py -d data/berlin`
  + [Optional - Do if densing point]: Open Meshlab and import the mesh file `data/berlin/unidtorted/depthmaps/merged.ply`
- Run rest server:
  + 
    ```
    cd rest
    flask run
    ```
  + Checkout: http://127.0.0.1:5000
  + View the apidocs at: `api_doc/openapi.yaml`
## License
OpenSfM is BSD-style licensed, as found in the LICENSE file.  See also the Facebook Open Source [Terms of Use][] and [Privacy Policy][]

[Terms of Use]: https://opensource.facebook.com/legal/terms (Facebook Open Source - Terms of Use)
[Privacy Policy]: https://opensource.facebook.com/legal/privacy (Facebook Open Source - Privacy Policy)
