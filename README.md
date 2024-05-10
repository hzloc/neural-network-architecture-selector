# Neural Network Architecture Selector

## Overview

This Python project assists in selecting the appropriate neural network architecture for a given problem domain. It operates in two main parts: batch loading of articles and neural network architecture selection.

### Installation
1. Clone the repository:
```bash
git clone https://github.com/your-username/neural-network-architecture-selector.git
cd neural-network-architecture-selector
```
2. Install the required dependencies:  
```bash
pip install -r requirements.txt
```
### Usage
1. Batch Loading of Articles
To batch load articles related to a specific topic and from a specified year using Scopus and PapersWithML:  
```bash
python -m src.main --from_year 2018 --search 'generative ai' --search 'anything'
```
:unamused: in order to be able to search with scopus you need an api key. 

2. See the fetched articles by powering UI, by running command:
```bash
streamlit run rank.py
```   
3. Choose an article, read and add their metrics, findings into database. In order to be able to add an article results, you must add the metrics, the architectures, and the dataset they've used in the study.

![add page](/pics/add.png)

4. After you've added the results, you can go to page which is called rank, and then see the best performing architectures and make your choice.

[!rank page](/pics/rank.png)