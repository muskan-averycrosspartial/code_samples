# Data and Programming for Public Policy II - Python Programming
# PPHA 30538


## Final Project: Electoral Politics in India
## Autumn 2022




#### Research Questions

  1. How has the voting share and number of parliamentary consitutencies(pc) won by the Bharatiya Janata Party in the general election in Indian states changed over the year 1999-2019, broadly considered the period where hindu nationalism has been at its peak. 
  2. How do these contituencies fare on indicators of women status, such as sex ratio in the last 5 years and female literacy. 
  3. Narendra Modi, the PM of India and a member of the BJP addresses the country on several occasions in pre-planned speeches. His charisma and popularlity are considered major factors to the success of the BJP in India. What are some main characterisitcs of his speeches? Are these speeches objective, polarizing and what are the most commonly used words?
  4. What affects a person's chances of winning in an election?
        
### Project Description:
  1. Data wrangling
  
- Dataset 1: Elections dataset from the Trivedi Centre for Political Data: TCPD-IED is a dataset of Indian election results – both Vidhan Sabha (state level) and Lok Sabha (national level) – beginning 1962. I have subset this to reflect years after 1999. 
- Dataset 2: Affidavit data from candidates declaring assets, liabilities, criminal record etc from parliamentary constituencies from 2002 to 2017. 
- Dataset 3: Speeches by Narendra Modi since 2014. There are about 900 speeches out of which 491 are in english. 
- Dataset 4: I parse a pdf table of constituency level data on socio-economic indicators. This is necessary because india reports socio-economic indicators on the subdistrict level (administrative unit), instead of poltiical unit(constituency). 
- Scraped district level census data from a webpage. 
- Shape files for each state in India organized in a folder for easy retrieval. 

I cleaned, standardized, merge and reshape this data in my code to make it useable. 

  2. Plotting
  
- static plot 1: A sentiment analysis plot showing polarity and subjectivity of Narendra Modi's english speeches. 
- static plot showing the 15 most frequently used words by Narendra Modi in these speeches
- Shiny plot showing the vote share of the winner in a pc in a chosen state for a chosen year. Possibility to see which pcs won by the BJP. 
- Shiny plot showing socio-economic indicators in the same state.  Possibility to see which pcs won by the BJP. 
  
  3. Text processing

- Parsing the pdf table using regex  and saving data in a csv. 
- Sentiment analysis of speeches. Used spacy.
- Word frequency analysis of speeches.Removed stopwords etc. 
- Web scraping using BeautifulSoup
  
  Finding : NLP is powerful, but it only has capacity to process 1 million tokens. Therefore I had to truncate my data which was 7 million tokens. 
      

  4. Analysis
  
- I use a probit model to see the relationship between the probability of winning in a pc and a number of covariates such as party, age, assets, liabilities, criminal record etc. 
- I reshaped and formatted the df for modelling, and added dummy variables. 

  5. Approach to Coding
  
- I have broken up my .py files into data wrangling (including statistical model), text processing and automatic data retrieval for better organization. 
- I have used functions to make my code efficient, but also easy to understand
- I have used meaningful variable names
- I have included comments wehre necessary
- I have saved output in well-sectioned folders

  6. Substantive Findings

- Text Analysis and static plots : Modi's speeches score relatively high on subjectivity, even during the early stages covid pandemic. This is consistent with a populist ruler. His speeches also have a posiitve tone to them overall, which is not surprising as they are tools to persuade the masses and project a particular image to the world (especially his english speeches). The word frequency analysis reveals a similar trend, as India, country, new, today and world are all posiitve terms selling a better future.  
- Shiny plots : Shiny plots are instructive as one can change interactive parameters to see not only how to BJP gains/loses popularity in a constituency over the years, but also how that consituency fares on development indicators. Helps understand if how people vote is connected to the outcomes of the parliament member from their constituency or not. 
- Probit model : The probit model shows significant results but should be treated as indicative correlational suggestion that the probability of winning an election constuency highly depends on whether you belong to a major national party and not so much on your criminal record, or wealth. It is also positively correlated with age. 

  7. Next steps
  
- A topic model of Modi's speeches could be interesting. Especially a comparison of his english and hindi speeches, which are meant for different audiences. 
- A textual analysis of questions asked in the parliament by members elected from these pcs, to check the level of activity of these members in holding the government accountable and whether that impact development outcomes for their pcs. 
- Improving the preliminary probit model by getting clean data on the candidates caste/religion. 
- linking different datasets, especially the election and affidavit datasets was imperfect, a closer check to ensure more matches will help gain more confidence in my findings. 
- scraping more tables from the PDF to plot more indicators of socio-economics development. 
  
  8. Note
- The shiny app should be run after running the text_processing file if the user is not cloning my entire repo with the processed.csv file. 
- My github username is muskan-averycrosspartial, and the repo name is final-project-hindutva_politics

#### Code Citations

   1. Asher, Sam and Lunt, Tobias and Matsuura, Ryu and Novosad, Paul, 2021, The World Bank Economic Review, Development Research at High Geographic Resolution: An Analysis of Night Lights, Firms, and Poverty in India using the SHRUG Open Data Platform, https://www.devdatalab.org/shrug_download/shrug_select
   2. Susewind, R. (2014). GIS shapefiles for India's parliamentary and assembly constituencies including polling booth localities. Bielefeld University. doi:10.4119/unibi/2674065
   3. Kim R, Swaminathan A, Swaminathan G, Kumar R, Rajpal S, Blossom J, Joe W, Subramanian S V. 2019. Parliamentary Constituency Factsheet for Indicators of Nutrition, Health and Development in India. HCPDS Working Paper Vol. 18, No. 4.
   4. “TCPD Indian Elections Data v2.0″, Trivedi Centre for Political Data, Ashoka University.Ananay Agarwal, Neelesh Agrawal, Saloni Bhogale, Sudheendra Hangal, Francesca Refsum Jensenius, Mohit Kumar, Chinmay Narayan, Basim U Nissa, Priyamvada Trivedi, and Gilles Verniers. 2021.
   5. Abhishek Ajmera, 2022, Kaggle, PM_Modi_speeches




