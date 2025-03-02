# ATcapstone

## Summary
We implement a statistical arbitrage trading strategy using cointegration-based pairs trading for specifically share class stocks; ETFs and indexes, at times on three or more assets in addition to pairs. The strategy leverages Johansen and Cointegrated Augmented Dickey-Fuller (CADF) tests for cointegration, Bollinger Bands for trade signal generation, batch processing for efficient data fetching from Yahoo Finance as well as data scraping.

In addition, we propose a regime-switching algorithm as the hierarchical decision-maker to switch to a more appropriate trading strategy depending on the price series. 

## **Authors and Contributors**
| Name                     | GitHub Username          |
|---------------------------|--------------------------|
| **Erin Xu**     | [**xuerin**](https://github.com/xuerin)          |
| **Igor Taratov**          | [**gosha003**](https://github.com/gosha003)        |
| **Petru Codrescu**| [**petrucodrescu**](https://github.com/petrucodrescu)|

## Installation
1. Before installing the project, ensure you have at least 200MB of memory or disk space on your computer, as well as a Python IDE.
2. Clone the repository `git clone [repo link]`
3. Download missing requirements in `requirements.txt`
4. Run `main.py`.


## Notes for contributors
1. Open your terminal. Get to the directory you want to store the project.
```
cd Desktop
```
For example, this will store the files in Desktop.

2. Open your terminal or command prompt. Run the following command to clone the repository:
```
git clone <repository-url>
```
Replace <repository-url> with the actual URL of the repository. You can find this under the green Code button. 

3. **Open the project in PyCharm by navigating to the cloned repository**\
  You should be able to see the project stucture in PyCharm now. There should be files like `preprocessing.py`. 

5. **IMPORTANT: Create and Switch to a New Branch**
```
git checkout -b <branch-name>
```
Replace `<branch-name>` with your name.

## Before you make any edits make sure you're on your branch:
```
git checkout <your-branch-name>
```

## After making changes:
```
git checkout <your-branch-name>
git add <file-name>
```
OR 
```
git checkout <your-branch-name>
git add .
```
THEN:
```
git commit -m "Describe your changes here"
```
Always include a short message describing your changes to help everyone understand what you did. 
```
git push origin <branch-name>
```
DON'T PUSH TO MAIN. PUSH TO YOUR OWN BRANCH. THIS IS BEST PRACTICE.

## If you are done with your feature: OPEN A PULL REQUEST.
1. Tell everyone you opened one.
2. Resolve the conflicts.
3. Have someone approve the pr.
4. **AFTER YOUR PULL REQUEST HAS BEEN COMPLETED: DELETE YOUR OLD BRANCH. THEN CREATE A NEW ONE, PULL NEW CHANGES AND MAKE CHANGES ON THAT.**
5. Pull new changes
```
git checkout <your-new-branch-name>
git pull origin main
```


