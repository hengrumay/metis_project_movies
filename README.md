
## metis_project_movies repository

#### Description of Script Files:   
Initial webscraping for list of [movie IDs e.g. ] (http://www.boxofficemojo.com/yearly/chart/?yr=2016&p=.htm) from [1980--2016] (http://www.boxofficemojo.com/yearly/)  was performed with [`Movies_getChartsMoviesIDurls.py`] (https://github.com/hengrumay/metis_project_movies/blob/master/docs/Movies_getChartsMoviesIDurls.py) for subsequent scraping of individual movie info with [`Movies_getIndvMovieInfo.py`] (https://github.com/hengrumay/metis_project_movies/blob/master/docs/Movies_getIndvMovieInfo.py). 

[`Movies_getBudget_matchMvNames_binGenreNStudio.py`] (https://github.com/hengrumay/metis_project_movies/blob/master/docs/Movies_getBudget_matchMvNames_binGenreNStudio.py) retrieves budget information from [The Numbers] (http://www.the-numbers.com/movie/budgets/all) , matches movie names from both box-office-derived info and budget info, and generates pivot tables for Genres and Studios of interest. [`Movies_combineData.py`] (https://github.com/hengrumay/metis_project_movies/blob/master/docs/Movies_combineData.py) combined all data across different fields.

Exploratory and regression modelling analyses are performed with [`Movies_exploreModels_revised.ipynb`] (https://github.com/hengrumay/metis_project_movies/blob/master/docs/Movies_exploreModels_revised.ipynb)

Summary of findings can be found in [HRM-Tan_MovieGenreNStudio_presentation.pdf] (https://github.com/hengrumay/metis_project_movies/blob/master/docs/HRM-Tan_MovieGenreNStudio_presentation.pdf)
