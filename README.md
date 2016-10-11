
## metis_project_movies  repository:

### Script Files:   
Initial webscraping for list of [movie IDs e.g. ] (http://www.boxofficemojo.com/yearly/chart/?yr=2016&p=.htm) from [1980--2016] (http://www.boxofficemojo.com/yearly/)  was performed with `Movies_getChartsMoviesIDurls.py` for subsequent scraping of individual movie info with `Movies_getIndvMovieInfo.py`. 

Movies_getBudget_matchMvNames_binGenreNStudio.py -- retrieves budget information from [The Numbers] (http://www.the-numbers.com/movie/budgets/all) , matches movie names from both box-office-derived info and budget info, and generates pivot tables for Genres and Studios of interest.

Exploratory and regression modelling analyses are performed with `Movies_combineData_exploreModels_revised.ipynb`

Summary of findings can be found in HRM-Tan_MovieGenreNStudio_presentation.pdf# metis_project_movies
