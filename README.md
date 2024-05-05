OpenSfM ![Docker workflow](https://github.com/mapillary/opensfm/workflows/Docker%20CI/badge.svg)
=======

## Overview
This is a sfm server using OpenSfM. Currently supports REST services.

Checkout this for more about [OpenSfM](https://opensfm.org/docs/using.html)


## Getting Started

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

## License
OpenSfM is BSD-style licensed, as found in the LICENSE file.  See also the Facebook Open Source [Terms of Use][] and [Privacy Policy][]

[Terms of Use]: https://opensource.facebook.com/legal/terms (Facebook Open Source - Terms of Use)
[Privacy Policy]: https://opensource.facebook.com/legal/privacy (Facebook Open Source - Privacy Policy)
