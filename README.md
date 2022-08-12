Manual for Search_Sentinel-2_L1C_by_tile

Introduction 

This app was developed for research purposes. The user inputs the conditions under which the search through the Copernicus Open Access Hub api. The Sentinel 2 satellite imagery search is tile based. The app gives the opportunity to make single variable search and multiple variables search 

Tile search

The search is conducted to find and download  Sentinel-2 L1C imagery using MGRS tile . On the Copernicus Open Access Hub, it seems to be available for most L1C products (product type S2MSI1C) from recent years, but this differs by region, too .
The Military Grid Reference System (MGRS) is the geocoordinate standard used by NATO militaries for locating points on Earth. The MGRS is derived from the Universal Transverse Mercator (UTM) grid system and the Universal Polar Stereographic (UPS) grid system, but uses a different labeling convention. The MGRS is used as geocode for the entire Earth

The products returned from the search are dictionaries containing the metadata items.

Tutorial

1.	Insert user’s credentials to get access to Copernicus Open Access Hub .
2.	Decide if you want to do a simple and single search for a specific area (tile/s ) for a specific period of time  and  a certain cloud coverage percentage in the satellite image of the previous mentioned area .
3.	Otherwise if the user wants to search for a specific area (tile/s ) for either different periods of time or different cloud coverage percentages in the satellite image .
4.	After the filter variables are filled the search starts (for the multi variable search ,all the searches are happening in parallel using threads) the products - satellite image files and their details  that fulfill the requirements are printed 
5.	Then the user has the ability to decide what wants to do with the products  ,download all of them ,some or none
