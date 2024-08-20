# Machine-Learning-Flask-App-with-ChatGPT-Analysis
### Jira
https://jerryevalentine.atlassian.net/browse/GPT-62 for Epic </br>
https://jerryevalentine.atlassian.net/browse/GPT-74 for Story/Module Development issue

### Portfolio Objective
1) Compare the project hours between those that use AI for code generation versus those that are not assisted by AI.
2) Develop a methodology for developing Flask applications using Generative AI.
3) Earlier Flask functionality, first written as seperate apps and then integrated into the main application, were practice runs.
4) display_table_metadata.py was the first application that contained only two errors.
   
### Summary
1) This is a work in progress.
2) The main flask application (display_table_metadata.py) was developed by creating seperate flask applications using ChatGPT.
3) All functionality was developed by creating a stand-alone Flask application coded by ChatGPT.
4) While the functionality was developed by ChatGPT, a human integrated the modules into the main flask application.
5) Each flask application went through the workflow shown in image 1 below.

### Data
1) GPT-112 took 1 hour and five minutes.
2) took 25 minutes

### ChatGPT Requirements Documents and Methodology
- All code was created by ChatGPT.
- Code was created by submitting text files to ChatGPT (examples are in the 'ChatGPT Requirements' folder.
- The text files contain both user requirements and functional requirements.
- Each text file is focuses on one piece of functionality and has a user story.
- Each story is associated with a Jira issue (see example below).
- Integration of the module functionality into the main Flask application was done by a human, not ChatGPT.

### Project Functionality Outline for Data Science Application
- Below is the functionality needed for the Data Science Application.
- All items will have a Jira issue, User Story, text file with ChatGPT functionality submission, and a stand-alone Flask Application.

##### Business Glossary Terms
- Create metadata for columns in a table and save in a database.

##### Both tables and columns
- Connect to data tables and columns

##### File Upload
- **Upload File:** Allow users to upload CSV, Excel, or other data formats - Done
- **File Validation:** Ensure the uploaded file is in the correct format and contains data - Done
- **Display Data Preview:** Show the first few rows of the dataset so users can confirm successful upload - Done

##### Data Preprocessing
- **Select Target Variable:** Provide a drop-down to select the target variable (dependent variable).
- **Handle Missing Values:** Allow users to delete rows with missing values, fill them with mean/median, or impute them.
- **Convert Data Types:** Enable users to convert columns (e.g., convert numerical columns to categorical).
- **Normalization/Scaling:** Offer options for normalizing or scaling data.
- **Numeric to Dummy:** A numeric column can be re-coded to 0 or 1.

##### Exploratory Data Analysis (EDA)
- **Data Summary:** Present basic statistics (mean, median, mode, min, max, etc.) of the dataset.
- **Top 10:** Display top 10 records in any table.
- **Correlation Heatmap:** Display a heatmap to visualize correlations between variables.
- **Distribution Plots:** Create histograms or box plots for continuous variables.
- **Missing Data Analysis:** Display the percentage of missing data per column.

##### Model Selection
- **Choose Model:** Allow users to select a machine learning model (e.g., Logistic Regression, Decision Tree, Random Forest).
- **Hyperparameter Tuning:** Provide basic hyperparameter settings (e.g., regularization strength for Logistic Regression).
- **Train-Test Split:** Allow the user to specify the percentage for training and testing sets.

##### Model Training
- **Run Model:** A button to run the selected model on the dataset.
- **Show Training Progress:** Optionally show a progress bar or training details.
- **Cross-validation:** Optionally allow cross-validation to evaluate model robustness.

##### Model Evaluation
- **Display Results:** Show model metrics such as accuracy, precision, recall, F1 score, confusion matrix, and ROC curve.
- **Save Results to Table:** Model results need to have a name and be saved to a database table.
- **Save Model:** Option to save the trained model for future use.
- **Feature Importance:** If applicable, display feature importance to show which features contributed the most to the predictions.
- **ChatGPT:** Must receive the model results and user text using an API and return the results.

##### Results Interpretation
- **Prediction Results:** Provide options to show predictions on test data.
- **Model Report:** Generate a summary report with key metrics, model parameters, and performance.
- **Visualization:** Present plots for metrics such as ROC, precision-recall curves, or confusion matrix.

##### Model Optimization
- **Parameter Tuning:** Offer options for hyperparameter tuning (e.g., grid search, random search).
- **Re-run Model:** Allow users to re-train the model with new parameters.
- **Factor Analysis and Recode:** Can unsupervised learning create better predictive models?

##### Export Results
- **Download Report:** Allow users to download a report with model details and performance metrics.
- **Export Predictions:** Provide the ability to download model predictions as a CSV file.

##### User Interface and Navigation
- **User-Friendly Navigation:** Ensure intuitive navigation between upload, preprocessing, modeling, and results pages.
- **Error Handling:** Provide clear error messages for invalid inputs or issues during model training.
- **Help and Documentation:** Offer help pages or tooltips to guide users through each step.

# Values used for estimate:
- 35 Flask Routes needed.
- 30 minutes for each route.