.. :changelog:

History
-------

==================
3.1.3 (2022-06-03)
++++++++++++++++++

* New tutorials 
* Refactored likelihood module. Now has PCA and MOPED compression.
* Included new emulator with neural network.  

==================
2.0.0 (2021-10-05)
++++++++++++++++++

* Better tests and generally more stable version

==================
0.5.1 (2020-06-30)
++++++++++++++++++

* [FIX]: Fixed healpy sign flip for data mode in NGSF
* Allow to adjust float pointing precision for saving RAM
* Solved an issue that can cause scrambling of statistics output when jobs fail
* Deallocating INCOVS object in likelihood to save RAM
* Added peakprofile, boost-factor and peak-loc modules
* Added option in summary to rescale data vectors -> Easier use of SVD in likelihood

==================
0.4.1 (2020-06-30)
++++++++++++++++++

* Added normalize option to catalog
* Allow lower float point precision for maps

==================
0.4.1 (2020-06-24)
++++++++++++++++++

* First release
