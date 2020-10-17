# -*- coding: utf-8 -*-
"""
Created on Fri Oct 2 16:52:29 2020

@author: Abhimanyu Trakroo
"""


import numpy as np
import pandas as pd

loan_data_backup = pd.read_csv('......\\loan_data_2007_2014.csv')
loan_data = loan_data_backup.copy()

## Explore Data
#loan_data
pd.options.display.max_columns = None # used to display all data at once.. no truncating
#note that above code .. can be modified to display certain number of columns
#loan_data

loan_data.head()
loan_data.tail()
loan_data.columns.values #displaying all the columns heads
loan_data['emp_length'].isnull().sum()
#When we imported the data, we got a message that column contains different value types. Thus, just 
# to know
loan_data.info() 
loan_data.describe()
    # Displays column names, complete (non-missing) cases per column, and datatype per column.
#Please note that the describe method still shows the mean if there are missing values

#PREPROCESSING STARTS
## General Preprocessing


### Preprocessing few CONTINUOUS VARIBALES /start
#SPOT THE OBJECT categories which should be Float/Integers
loan_data['emp_length'].unique()
# Displays unique values of a column.
#Notice the years at the end of numbers and the data type = object 
#CONVERSION into numbers/continuous variables

#BE VERY VIGIL ABOUT THE SEQUENCE OF REPLACEMENT
loan_data['emp_length_int'] = loan_data['emp_length'].str.replace('\+ years', '')
#'\' above indicates that there is a number before it which we do not wanna replace
#Now, note the unique values
#loan_data['emp_length_int'].unique() #10 is still an object but do not worry. Will convert that later

loan_data['emp_length_int'] = loan_data['emp_length_int'].replace('< 1 year', int(0))
#notice that value you are replacing with is '0'
#str(0)
#<1 year is classified as 0 as we already have 1 year in the dataset

loan_data['emp_length_int'] = loan_data['emp_length_int'].replace('n/a',  int(0))
#Also, NOTE THAT 'NAN' VALUES ARE PROCESSED AS 'n/a' 
#'n/a' is classified as 0 as we assume that it is 0<<<------ IMPORTANT to note when to replace
#with 0 and when to use no value as ''


loan_data['emp_length_int'] = loan_data['emp_length_int'].str.replace(' years', '')
loan_data['emp_length_int'] = loan_data['emp_length_int'].str.replace(' year', '')
# We store the preprocessed ‘employment length’ variable in a new variable called ‘employment length int’,
# We assign the new ‘employment length int’ to be equal to the ‘employment length’ variable with the string ‘+ years’
# replaced with nothing. Next, we replace the whole string ‘less than 1 year’ with the string ‘0’.
# Then, we replace the ‘n/a’ string with the string ‘0’. Then, we replace the string ‘space years’ with nothing.
# Finally, we replace the string ‘space year’ with nothing. 

#type(loan_data['emp_length_int'][0])
# Checks the datatype of a single element of a column.

loan_data['emp_length_int'] = pd.to_numeric(loan_data['emp_length_int'])
# Transforms the values to numeric.

#type(loan_data['emp_length_int'][0])
# Checks the datatype of a single element of a column.
#pd.DataFrame(loan_data['emp_length_int']).info()
loan_data['emp_length_int'].unique()

####################emp_length_int has been converted to integer########################

#converting TERM into integer
loan_data['term'].unique()
#There is only 'space months' as extra

loan_data['term_int']=loan_data['term'].str.replace(' months','')
loan_data['term_int'].unique()
loan_data['term_int']=pd.to_numeric(loan_data['term_int'])
loan_data['term_int'].unique()
#type(loan_data['term_int'][0]) #important to mention index to pick any value and check it's type

##### Preprocessing Date variables #######
loan_data['earliest_cr_line'].unique()
# Displays a column.
loan_data['earliest_cr_line'].isnull().sum()

loan_data['earliest_cr_line_date'] = pd.to_datetime(loan_data['earliest_cr_line'], format='%b-%y')
#loan_data['earliest_cr_line_date'][loan_data['earliest_cr_line_date']=='Jan-1985']

# Extracts the date and the time from a string variable that is in a given format.
pd.DataFrame(loan_data['earliest_cr_line_date']).info() #CHECK THE CHANGE ----->> IT IS TIMESTAMP
#type(loan_data['earliest_cr_line_date'][0])
# Checks the datatype of a single element of a column.
#pd.to_datetime('2017-12-01') - loan_data['earliest_cr_line_date']
# Calculates the difference between two dates and times.
# Assume we are now in December 2017
loan_data['mths_since_earliest_cr_line'] = round(pd.to_numeric((pd.to_datetime('2017-12-01') - loan_data['earliest_cr_line_date']) / np.timedelta64(1, 'M')))
#pd.to_numeric was not required here but may be to make the code reusable, this is done
# We calculate the difference between two dates in months, turn it to numeric datatype and round it.
# We save the result in a new variable.

#loan_data['mths_since_earliest_cr_line'].describe()
# Shows some descriptive statisics for the values of a column.
# Dates from 1969 and before are not being converted well, i.e., they have become 2069 and similar,
# and negative differences are being calculated.
loan_data['mths_since_earliest_cr_line'].max()
loan_data['mths_since_earliest_cr_line'].min()
#loan_data.loc[: , ['earliest_cr_line', 'earliest_cr_line_date', 'mths_since_earliest_cr_line']][loan_data['mths_since_earliest_cr_line'] < 0]
# We take three columns from the dataframe. Then, we display them only for the rows where a variable has negative value.
# There are 2303 strange negative values.

loan_data['mths_since_earliest_cr_line'][loan_data['mths_since_earliest_cr_line'] < 0] = loan_data['mths_since_earliest_cr_line'].max()
# We set the rows that had negative differences to the maximum value.

#min(loan_data['mths_since_earliest_cr_line'])
# Calculates and shows the minimum value of a column.

################## earliiest credit line done##################

##########preprocessing - issue_d##########################

#loan_data['issue_d']
loan_data['issue_d_date'] = pd.to_datetime(loan_data['issue_d'],format='%b-%y')
loan_data['mths_since_issue_d'] = round(pd.to_numeric((pd.to_datetime('2017-12-01')-loan_data['issue_d_date'])/np.timedelta64(1,'M')))
#loan_data['mths_since_issue_d'].describe()
##################

#########Just for fun - processing one more --> last_pymnt_d, This is not needed as it's a payment date not a variable##########################
loan_data['last_pymnt_d']
loan_data['mths_since_last_pymnt_d'] = round((pd.to_datetime('2017-12-01')-pd.to_datetime(loan_data['last_pymnt_d'],format='%b-%y'))/np.timedelta64(1,'M'))
#loan_data['mths_since_last_pymnt_d'].describe()
###################################This was not useful, but good practice########################################

### Preprocessing few CONTINUOUS VARIBALES /ends

### Preprocessing few CATEGORICAL VARIBALES /starts######################################
#loan_data.info() #SPOT THE OBJECT categories
###################### trying to pull only object categories
#list_objects = list() ## trying to pull only object categories
#for i in range(len(loan_data.iloc[1:2,:])) ## trying to pull only object categories
 #   if type(loan_data.iloc[:1,i])==object## trying to pull only object categories
  #     list_objects=list_objects.append(list(loan_data.iloc[0,i]))## trying to pull only object categories
######################        

# Starting with Grade variable
#pd.get_dummies(loan_data['grade']) #created the dummy variables
#pd.get_dummies(loan_data['grade'], prefix = 'Grade', prefix_sep=':') #created dummy variables with separators

#We want to create a new dataframe consisting all the dummy variables and then append it to the original dataframe as we 
#run regressions on the original dataset
#### FOR NOW THE DUMMIES ARE JUST BEING CREATED FOR DISCRETE VARIABLES 
### lATER WE WOULD USE np.where METHOD WITH isin(range()) TO COMPARE THE values of continuous variables
###... and assign them 0 or 1 and save them in a class ##Dummies for continouos variables 
loan_data_dummies = [pd.get_dummies(loan_data['grade'], prefix = 'grade', prefix_sep = ':'),
                     pd.get_dummies(loan_data['sub_grade'], prefix = 'sub_grade', prefix_sep = ':'),
                     pd.get_dummies(loan_data['home_ownership'], prefix = 'home_ownership', prefix_sep = ':'),
                     pd.get_dummies(loan_data['verification_status'], prefix = 'verification_status', prefix_sep = ':'),
                     pd.get_dummies(loan_data['loan_status'], prefix = 'loan_status', prefix_sep = ':'),
                     pd.get_dummies(loan_data['purpose'], prefix = 'purpose', prefix_sep = ':'),
                     pd.get_dummies(loan_data['addr_state'], prefix = 'addr_state', prefix_sep = ':'),
                     pd.get_dummies(loan_data['initial_list_status'], prefix = 'initial_list_status', prefix_sep = ':')]
# We create dummy variables from all 8 original independent variables, and save them into a list.
# Note that we are using a particular naming convention for all variables: original variable name, colon, category name.

#pd.get_dummies(loan_data['addr_state'], prefix = 'addr_state', prefix_sep = ':').to_csv("C:\\Users\\Abhimanyu Trakroo\\Downloads\\Udemy-Credit_risk_in_python\\test for add_state.csv")

loan_data_dummies = pd.concat(loan_data_dummies, axis = 1)
# We concatenate the dummy variables and this turns them into a dataframe.
#type(loan_data_dummies)
# Returns the type of the variable.

loan_data = pd.concat([loan_data, loan_data_dummies], axis = 1)
# Concatenates two dataframes.
# Here we concatenate the dataframe with original data with the dataframe with dummy variables, along the columns. 

#loan_data.columns.values
# Displays all column names. and check if all the dummy variables are concatenated




########################## Check for missing values and clean ###########################
loan_data.isnull()
# It returns 'False' if a value is not missing and 'True' if a value is missing, for each value in a dataframe.
#pd.options.display.max_rows = None
# Sets the pandas dataframe options to display all columns/ rows.
loan_data.isnull().sum()
#pd.options.display.max_rows = 100
# Sets the pandas dataframe options to display 100 columns/ rows.
# 'Total revolving high credit/ credit limit', so it makes sense that the missing values are equal to funded_amnt.
loan_data['total_rev_hi_lim'].fillna(loan_data['funded_amnt'], inplace=True)
# We fill the missing values with the values of another variable.

#loan_data['total_rev_hi_lim'].isnull().sum()


############      TREATMENT OF MISSING VARIABLES FOR THE: (‘annual_inc’) (MEAN REPLACEMENT), 
#ZERO REPLACEMENT:‘mths_since_earliest_cr_line’, ‘acc_now_delinq’, ‘total_acc’, ‘pub_rec’, ‘open_acc’,
#‘inq_last_6mths’
#‘delinq_2yrs’
#‘emp_length_int’  ###############

#loan_data['annual_inc'].isnull().sum()
loan_data['annual_inc'].fillna(loan_data['annual_inc'].mean(),inplace=True)
#loan_data['annual_inc'].isnull().sum()
######

#loan_data['mths_since_earliest_cr_line'].isnull().sum()
loan_data['mths_since_earliest_cr_line'].fillna(int(0),inplace=True)
#loan_data['mths_since_earliest_cr_line'].isnull().sum()

########
#Remember this thing
#type(int(0))
#type(str(0))

#loan_data['acc_now_delinq'].isnull().sum()
loan_data['acc_now_delinq'].fillna(int(0),inplace=True)
#loan_data['acc_now_delinq'].isnull().sum()
#loan_data['acc_now_delinq'][loan_data['acc_now_delinq']==str(0)]=int(0)
########

#loan_data['total_acc'].isnull().sum()
loan_data['total_acc'].fillna(int(0),inplace=True)
#loan_data['total_acc'].isnull().sum()
#loan_data['total_acc'][loan_data['total_acc']==str(0)]=int(0)
###############

#loan_data['pub_rec'].isnull().sum()
loan_data['pub_rec'].fillna(int(0),inplace=True)
#loan_data['pub_rec'].isnull().sum()
#loan_data['pub_rec'][loan_data['pub_rec']==str(0)]=int(0)
###########

#loan_data['open_acc'].isnull().sum()
loan_data['open_acc'].fillna(int(0),inplace=True)
#loan_data['open_acc'].isnull().sum()
#loan_data['open_acc'][loan_data['open_acc']==str(0)]=int(0)

##################

#loan_data['inq_last_6mths'].isnull().sum()
loan_data['inq_last_6mths'].fillna(int(0),inplace=True)
#loan_data['inq_last_6mths'].isnull().sum()
#loan_data['inq_last_6mths'][loan_data['inq_last_6mths']==str(0)]=int(0)

#the following statements helped me find the replaced str(0) characters
#loan_data['inq_last_6mths'].value_counts() #finding out replaced str(0)
#loan_data['inq_last_6mths'][loan_data['inq_last_6mths']==int(0)]
#and now they will be replaced
#loan_data['inq_last_6mths'][loan_data['inq_last_6mths']==str(0)]=int(0)
#loan_data['inq_last_6mths'].isnull().sum()
##########

#loan_data['delinq_2yrs'].isnull().sum()
loan_data['delinq_2yrs'].fillna(int(0),inplace=True)
#loan_data['delinq_2yrs'].isnull().sum()
#loan_data['delinq_2yrs'][loan_data['delinq_2yrs']==str(0)]=int(0)

################

#loan_data['emp_length_int'].isnull().sum()
loan_data['emp_length_int'].fillna(int(0),inplace=True)
#loan_data['emp_length_int'].isnull().sum()
#loan_data['emp_length_int'][loan_data['emp_length_int']==str(0)]=int(0)

###############################################################################################


################# PD MODEL BEGINS ######################################
################# PD MODEL BEGINS ######################################
################# PD MODEL BEGINS ######################################
################# PD MODEL BEGINS ######################################
################# PD MODEL BEGINS ######################################

#STEP 1: DEFINING GOOD / BAD: 
#Dependent Variable. Good/ Bad (Default) Definition. Default and Non-default Accounts. 

#loan_data['loan_status'].unique()
# Displays unique values of a column. ALLOWS US TO DECIDE WHICH LOANS TO PUT AS DEFAULT AND WHICH NOT

#loan_data['loan_status'].value_counts()
# Calculates the number of observations for each unique value of a variable.

#loan_data['loan_status'].value_counts() / loan_data['loan_status'].count()
# We divide the number of observations for each unique value of a variable by the total number of observations.
# Thus, we get the proportion of observations for each unique value of a variable.

# Good/ Bad Definition MOST IMPORTANT: PLEASE NOTE THAT WE HAVE USED 1 FOR NON-DEFAULT I.E. GOOD LOANS

loan_data['good_bad'] = np.where(loan_data['loan_status'].isin(['Charged Off', 'Default','Does not meet the credit policy. Status:Charged Off','Late (31-120 days)']), 0, 1)
#MOST IMPORTANT DECISIVE FACTOR # We create a new variable that has the value of '0' if a condition is met, and the value of '1' if it is not met.

#loan_data['good_bad'] #LOANS CLASSIFIED AS DEFAULT OR NON-DEFAULT
########################################################################################
################# PART OF THE PD MODEL ######################################

#SPLITTING THE DATA INTO TRAINING AND TESTING
from sklearn.model_selection import train_test_split

#NOTICE THAT THE FOLLOWING CODE MAKES US DROP A VARIABLE (DEPENDENT VARIABLE).

#train_test_split(loan_data.drop('good_bad', axis = 1), loan_data['good_bad'])
# Takes a set of inputs and a set of targets as arguments. Splits the inputs and the targets into four dataframes:
# Inputs - Train, Inputs - Test, Targets - Train, Targets - Test.

#loan_data_inputs_train, loan_data_inputs_test, loan_data_targets_train, loan_data_targets_test = train_test_split(loan_data.drop('good_bad', axis = 1), loan_data['good_bad'])
# We split two dataframes with inputs and targets, each into a train and test dataframe, and store them in variables.

#loan_data_inputs_train.shape
# Displays the size of the dataframe.

#loan_data_targets_train.shape
# Displays the size of the dataframe.

#loan_data_inputs_test.shape
# Displays the size of the dataframe.

#loan_data_targets_test.shape
# Displays the size of the dataframe.

loan_data_inputs_train, loan_data_inputs_test, loan_data_targets_train, loan_data_targets_test = train_test_split(loan_data.drop('good_bad', axis = 1), loan_data['good_bad'], test_size = 0.2, random_state = 42)

# We split two dataframes with inputs and targets, each into a train and test dataframe, and store them in variables.
# This time we set the size of the test dataset to be 20%.
# Respectively, the size of the train dataset becomes 80%.
# We also set a specific random state.
# This would allow us to perform the exact same split multimple times.
# This means, to assign the exact same observations to the train and test datasets.

loan_data_inputs_train.shape
# Displays the size of the dataframe.

loan_data_targets_train.shape
# Displays the size of the dataframe.

loan_data_inputs_test.shape
# Displays the size of the dataframe.

loan_data_targets_test.shape
# Displays the size of the dataframe.


########################## Data Preparation OF THE TRAINING DATASET ##################################
##########################This would include automating the process of calculating WoE and IV for several 
#variables
################# PART OF THE PD MODEL ######################################
#IF THE FOLLOWING TWO CODES ARE HASHED OUT MEANS THAT WE HAVE ALREADY PREPROCESSED TRAINING VARIABLES
# AND NOW ARE GONNA PREPROCESS TEST VARIABLES
#Otherwise hash them when preprocessing test variables


df_inputs_prepr = loan_data_inputs_train
df_targets_prepr = loan_data_targets_train




##### CREATED WORKING DATAFRAMES JUST LIKE A ROUGH SHEET, OPERATIONS ON WHICH WOULD NOT IMPACT MAIN DATASET

#IMPORTANT: Note that the folloowing two lines of codes would be unhashed when we complete the preprocessing of training dataset
# When we complete the preprocessing the training dataset, we would need to save the results contained in 'df_inputs_prepr' in 
#.. in 'loan_data_inputs_train (i.e. reverse the above code)
# This is becasue the automated version of the code that we create in the following, is gonna basically run on 'df_input_prepr' 
#....as an input. Thus we need to save the dataframe, once the preprocessing of the inputs and targets is done 
#..for each, training and test data




#    
#df_inputs_prepr = loan_data_inputs_test
#df_targets_prepr = loan_data_targets_test
#... AND RUN THE FOLLOWING CODE AFTER UNHASHING THE ABOVE TWO LINES




######Preprocessing using different variables starting with 'grade': Calculation of WoE in predicting good/bad split
df_inputs_prepr['grade'].unique()
# Displays unique values of a column.
#JUST LIKE A REGRESSION MODEL WHERE ONE VARIABLE OF INDEPENDENT IS MATCHED WITH INDEPENDENT FOR THE MODEL TO LEARN 
df1 = pd.concat([df_inputs_prepr['grade'], df_targets_prepr], axis = 1)
# Concatenates two dataframes along the columns.
#df1.head()

######Part of data preparation: Calculation of weight of index
#we want to split and count the data for good and bad
#Thus, we need to group it
#IMPORTANT: Since we want this code to be reusable thus using indexes i.e. df1.columns.values[0] because we know 
#whichever variable we use it will always be in the first column which is 0th index
#df1.groupby(df1.columns.values[0], as_index = False)[df1.columns.values[1]].count()
#df1.groupby(df1.columns.values[0])[df1.columns.values[1]].count() #Notice the difference in result when run 
#without index=False
#as_index=False lets the values in the dataframe be the part of dataset and not as an index
# Groups the data according to a criterion contained in one column.
# Does not turn the names of the values of the criterion (sub category of a variable) as indexes.
# Aggregates the data in another column, using a selected function.
# In this specific case, we group by the column with index 0 and we aggregate the values of the column with index 1.
# More specifically, we count them.
# In other words, we count the values in the column with index 1 for each value of the column with index 0.

####### REMINDER THAT WE ARE WORKING WITH THE Train DATA and we will run the similar code for the test data as well
df1.groupby(df1.columns.values[0], as_index = False)[df1.columns.values[1]].mean()
#the statement works as to calculate the propostion of good borrowers as bad borrowers would anyway have the value
#of '0' 
# Groups the data according to a criterion contained in one column.
# Does not turn the names of the values of the criterion as indexes.
# Aggregates the data in another column, using a selected function.
# Here we calculate the mean of the values in the column with index 1 for each value of the column with index 0.

#Merging the dataframes with the count of each grade and the mean (i.e. % of good borrowers in each grade) 
df1 = pd.concat([df1.groupby(df1.columns.values[0], as_index = False)[df1.columns.values[1]].count(),
                df1.groupby(df1.columns.values[0], as_index = False)[df1.columns.values[1]].mean()], axis = 1)
# Concatenates two dataframes along the columns.

df1

#keeping just one coulmn of grades
df1 = df1.iloc[:, [0, 1, 3]]
# Selects only columns with specific indexes.
df1


df1.columns = [df1.columns.values[0], 'n_obs', 'prop_good'] #df1.columns and df1.columns.values are same
# Changes the names of the columns of a dataframe.
df1


df1['prop_n_obs'] = df1['n_obs'] / df1['n_obs'].sum()
# We divide the values of one column by he values of another column and save the result in a new variable.
df1


df1['n_good'] = df1['prop_good'] * df1['n_obs']
# We multiply the values of one column by he values of another column and save the result in a new variable.
df1['n_bad'] = (1 - df1['prop_good']) * df1['n_obs']
df1

#### REMINDER THAT WE ARE WORKING WITH THE TEST DATA

df1['prop_n_good'] = df1['n_good'] / df1['n_good'].sum()
df1['prop_n_bad'] = df1['n_bad'] / df1['n_bad'].sum()
df1

df1['WoE'] = np.log(df1['prop_n_good'] / df1['prop_n_bad'])
# We take the natural logarithm of a variable and save the result in a nex variable.
df1


df1 = df1.sort_values(['WoE'])
# Sorts a dataframe by the values of a given column.


#In the above result the index was also showing and it was messed up as the values of WoE were sorted. Thus, we 
#have to sort the index now for the visual easyness (I hope).
df1 = df1.reset_index(drop = True)
# We reset the index of a dataframe and overwrite it.
df1

##########The difference does not solve any real purpose (I guess, find out about this more). May be the coach uses
#these later
# .diff() function subtracts the values of two subsequent values in the column (or rows altogether)
df1['diff_prop_good'] = df1['prop_good'].diff().abs()
# We take the difference between two subsequent values of a column. Then, we take the absolute value of the result.
#Absolute values are taken as they are more intuitive in understanding the differences

####### REMINDER THAT WE ARE WORKING WITH THE TEST DATA

df1['diff_WoE'] = df1['WoE'].diff().abs()
# We take the difference between two subsequent values of a column. Then, we take the absolute value of the result.
#Absolute values are taken as they are more intuitive in understanding the differences

df1
##########The difference does not solve any real purpose (I guess, find out about this more)


df1['IV'] = (df1['prop_n_good'] - df1['prop_n_bad']) * df1['WoE'] #CALCULATES IV FOR EACH 
#VARIABLE - IN A NONTECHNICAL SENSE AS IV IS FOR A VARIABLE WHOLE NOT CATEGORY INDIVIDUAL

df1['IV'] = df1['IV'].sum() #Asigns the same value to each category
# We sum all values of a given column.

df1
################# PART OF THE PD MODEL ######################################
################# PART OF THE PD MODEL ######################################
############################ AUTOMATING THE CALCULATION OF WoE FOR ALL VARIABLES #################################


def woe_discrete(df, discrete_variable_name, good_bad_variable_df):
    df = pd.concat([df[discrete_variable_name], good_bad_variable_df], axis = 1) 
    #Before this function is involed the df remains the same as the one broken into train and test......
    # We will be using TRAINING_INPUTS_data for 'df' and TRAINING_TARGETS_data for 'good_bad_variable_df'
    
    #which was after we treated it for: 
        # Continuous variables- date formats, number formats
        # Discrete variables - created the dummies, set individual columns for each dummy except for good/bad
        # Checked for missing values and rectifying the places
        # Analyzing the loan status values and assigning 0 and 1 to the status depending on the business logic
        # splitting the data into training and testing; training data set dropped the dependent variable
        # Calculating of WoE and IV for an variable to set basis for this code
        # Training dataset is called into this function with the reference to a specific variable 
    #
    
    #Inside this function we remake the df. Invoking this function will then use the above code to recreate the 
    #usable dataframe in df
    #Remember that good_bad_variable_df has only dependent variable dataframe
    
                    # groups the variables as per the variable,#provides the count(Total people) for each category
    df = pd.concat([df.groupby(df.columns.values[0], as_index = False)[df.columns.values[1]].count(),
                df.groupby(df.columns.values[0], as_index = False)[df.columns.values[1]].mean()], axis = 1)
                    # groups the variables as per the variable, #provides the mean (%good) for each category                    
            
    #The above creates a dataframe as per the classes of the specified grade variable and provides the counts for
    #total borrowers and proportion of good borrowers in each category. 
    
    
    df = df.iloc[:, [0, 1, 3]] #separates the extra column of the variable which gets repeated from the abo ve process 
    df.columns = [df.columns.values[0], 'n_obs', 'prop_good'] #renaming of columns to make it intuitive
    df['prop_n_obs'] = df['n_obs'] / df['n_obs'].sum() #adding column of proportion of observations in each category
    df['n_good'] = df['prop_good'] * df['n_obs'] #propotion of good converted into numbers. 
    
    #From the mean() used earlier, we got the mean of the CATEGORY (prop_good). But to convert it to the mean of
    #the total good population, we multiply prop_good--->> number of goods in the category --->> add number of 
    #goods across categories----> find prop_n_good which is total % of goods from the total goods handled by the
    #category
    
    #Also instead of going round the busheS, we could have simply calculated .sum() instead of .mean(), and 
    #avoided confusion
    #BUT WE NEED PROPN_GOOD LATER TO COMBINE CATEGORIES
     
    
    df['n_bad'] = (1 - df['prop_good']) * df['n_obs'] #number of bad borrowers in each category
    df['prop_n_good'] = df['n_good'] / df['n_good'].sum() #Categorywise % of good borrowers out of Total Good borrowers 
    df['prop_n_bad'] = df['n_bad'] / df['n_bad'].sum() #Categorywise % of bad borrowers out of Total Bad borrowers
    df['WoE'] = np.log(df['prop_n_good'] / df['prop_n_bad']) #Calculating WoE
    df = df.sort_values(['WoE']) #sorting values by WoE
    df = df.reset_index(drop = True) #resetting index to avoid confusion
    df['diff_prop_good'] = df['prop_good'].diff().abs() #calculating difference between % good borrowers row-wise. 
    
    df['diff_WoE'] = df['WoE'].diff().abs()
    df['IV'] = (df['prop_n_good'] - df['prop_n_bad']) * df['WoE'] #calculating weight*WoE operation for each category
    df['IV'] = df['IV'].sum() #assigning same IV i.e. total of categories to the whole column
    
    return df #now df consists of all the things we want 

df_temp = woe_discrete(df_inputs_prepr, 'grade', df_targets_prepr) #testing whether it works good
df_temp

df_temp2 = woe_discrete(df_inputs_prepr, 'emp_length', df_targets_prepr) #calling it on emp_length to check implementation
df_temp2


################# PART OF THE PD MODEL ######################################
################### Preprocessing Discrete Variables: Automating Visualization of Results ############################

import matplotlib.pyplot as plt
import seaborn as sns
# Imports the libraries we need.
sns.set()
# We set the default style of the graphs to the seaborn style. 

# Below we define a function that takes 2 arguments: a dataframe and a number.
# The number parameter has a default value of 0.
# IMPORTANT: Setting a predefined value means that if we call the function and omit the number parameter, it will be executed with it having a value of 0.
# The function displays a graph.
def plot_by_woe(df_WoE, rotation_of_x_axis_labels = 0):
    x = np.array(df_WoE.iloc[:, 0].apply(str))
    # Turns the values of the column with index 0 to strings, makes an array from these strings, and passes it to variable x.
    #apply str was necessary to make sure that we have usable text on x-axis
    # np.array is applied as matplotlib works well with numpy and scipy instead of dataframes 
    y = df_WoE['WoE']
    # Selects a column with label 'WoE' and passes it to variable y.
    plt.figure(figsize=(18, 6))
    # Sets the graph size to width 18 x height 6. #INCHES
    plt.plot(x, y, marker = 'o', linestyle = '--', color = 'k')
    # Plots the datapoints with coordiantes variable x on the x-axis and variable y on the y-axis.
    # Sets the marker for each datapoint to a circle, the style line between the points to dashed, and the color to black.
    plt.xlabel(df_WoE.columns[0])
    # Names the x-axis with the name of the column with index 0.
    plt.ylabel('Weight of Evidence')
    # Names the y-axis 'Weight of Evidence'.
    plt.title(str('Weight of Evidence by ' + df_WoE.columns[0]))
    # Names the grapth 'Weight of Evidence by ' the name of the column with index 0.
    plt.xticks(rotation = rotation_of_x_axis_labels)
    #IMPORTANT # Rotates the labels of the x-axis a predefined number of degrees.

plot_by_woe(df_temp) #calling this to check the implementation
# We execute the function we defined with the necessary arguments: a dataframe.
# We omit the number argument, which means the function will use its default value, 0.

################# PART OF THE PD MODEL ######################################
################## Preprocessing Discrete Variables: Creating Dummy Variables, Part 1

pd.options.display.max_columns=None
###################### 'home_ownership'
df_temp = woe_discrete(df_inputs_prepr, 'home_ownership', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp)
# We plot the weight of evidence values.

#FROM OBSERVING THE WoE TABLE, THE FOLLOWING:
    # There are many categories with very few observations and many categories with very different "good" %.
    # Therefore, we create a new discrete variable where we combine some of the categories.
    # 'OTHERS' and 'NONE' are riskiest but HAVE very few LOANS. 'RENT' is the next riskiest.
    # 'ANY' are least risky but are too few. Conceptually, they belong to the same category. Also, their inclusion would not change anything.
    # We combine them in one category, 'RENT_OTHER_NONE_ANY'.
    # We end up with 3 categories: 'RENT_OTHER_NONE_ANY', 'OWN', 'MORTGAGE'.

#HOW DOES THE FOLLOWING SUM FUNCTION FIT IN
#columnwise sum of 0s and 1s to create a new category
df_inputs_prepr['home_ownership:RENT_OTHER_NONE_ANY'] = sum([df_inputs_prepr['home_ownership:RENT'], df_inputs_prepr['home_ownership:OTHER'],
                                                      df_inputs_prepr['home_ownership:NONE'],df_inputs_prepr['home_ownership:ANY']])
# 'RENT_OTHER_NONE_ANY' will be the reference category.
#Whatever the values for the initial dummy variables for 'Home_ownership' were, will 
#now get added and assigned to  'home ownership: RENT_OTHER_NONE_ANY' category
    
    
# Alternatively:
#loan_data.loc['home_ownership' in ['RENT', 'OTHER', 'NONE', 'ANY'], 'home_ownership:RENT_OTHER_NONE_ANY'] = 1
#loan_data.loc['home_ownership' not in ['RENT', 'OTHER', 'NONE', 'ANY'], 'home_ownership:RENT_OTHER_NONE_ANY'] = 0
#loan_data.loc['loan_status' in ['OWN'], 'home_ownership:OWN'] = 1
#loan_data.loc['loan_status' not in ['OWN'], 'home_ownership:OWN'] = 0
#loan_data.loc['loan_status' in ['MORTGAGE'], 'home_ownership:MORTGAGE'] = 1
#loan_data.loc['loan_status' not in ['MORTGAGE'], 'home_ownership:MORTGAGE'] = 0

########Preprocessing Discrete Variables: Creating Dummy Variables, Part 2#########

#### 'addr_state'
df_inputs_prepr['addr_state'].unique()
df_temp = woe_discrete(df_inputs_prepr, 'addr_state', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp)
# We plot the weight of evidence values.


#Following code is written in case borrowers from North Dakota come in later
if ['addr_state:ND'] in df_inputs_prepr.columns.values: #if there are we don't do anything
    pass
else:
    df_inputs_prepr['addr_state:ND'] = 0 #if not we set all the values to 0

#This also brings to liight that we should always keep the mind open just in case any other 
    #value not included in the model pops up, we should make arrangements for that

#Note that WoE is very less for the NE and IA, and that their proportion of obsn is very less
    #Also their WoE is exceptionally high (NE and IA). WoE is also very high in case of Maine and Idaho (ME and ID)
    #which also have low obsn
    # We will include them in the first the worst and last the best categories (as per WOE)

#Merging them with other categories will let us analyse the nuances among states
    
#Analysing the values excluding the 4 states
plot_by_woe(df_temp.iloc[2: -2, : ])
# We plot the weight of evidence values.
#After running the above function we got to know that
    # the chart is more like waht we expect
    # NV and FL are different but can be clubbed as their prop_n_obs (observations) is less
    # Further, we notice due to low no. of obs, we should combine first 6 and last 6 states
    # Unknown variable North Dakota (ND) should be included in the .........


plot_by_woe(df_temp.iloc[6: -6, : ])
# We plot the weight of evidence values.
# California and NYC can be separate groups because of larger obs
#COARSE CLASSING can begin by combining similar WOE (and/ or low obs) states but it should be kept in mind 
#that if they are separated by larger obs category, separate groups of states will have to be 
#created
#Larger obs group CAN'T be clubbed with lower obs on the both, right and left, to create a
#separate category
#North Dakota is included in the riskiest category as we do not have any information about it


# We create the following categories:
# 'ND' 'NE' 'IA' NV' 'FL' 'HI' 'AL'
# 'NM' 'VA'
# 'NY'
# 'OK' 'TN' 'MO' 'LA' 'MD' 'NC'
# 'CA'
# 'UT' 'KY' 'AZ' 'NJ'
# 'AR' 'MI' 'PA' 'OH' 'MN'
# 'RI' 'MA' 'DE' 'SD' 'IN'
# 'GA' 'WA' 'OR'
# 'WI' 'MT'
# 'TX'
# 'IL' 'CT'
# 'KS' 'SC' 'CO' 'VT' 'AK' 'MS'
# 'WV' 'NH' 'WY' 'DC' 'ME' 'ID'

# 'IA_NV_HI_ID_AL_FL' will be the reference category.

df_inputs_prepr['addr_state:ND_NE_IA_NV_FL_HI_AL'] = sum([df_inputs_prepr['addr_state:ND'], df_inputs_prepr['addr_state:NE'],
                                              df_inputs_prepr['addr_state:IA'], df_inputs_prepr['addr_state:NV'],
                                              df_inputs_prepr['addr_state:FL'], df_inputs_prepr['addr_state:HI'],
                                                          df_inputs_prepr['addr_state:AL']])

df_inputs_prepr['addr_state:NM_VA'] = sum([df_inputs_prepr['addr_state:NM'], df_inputs_prepr['addr_state:VA']])

df_inputs_prepr['addr_state:OK_TN_MO_LA_MD_NC'] = sum([df_inputs_prepr['addr_state:OK'], df_inputs_prepr['addr_state:TN'],
                                              df_inputs_prepr['addr_state:MO'], df_inputs_prepr['addr_state:LA'],
                                              df_inputs_prepr['addr_state:MD'], df_inputs_prepr['addr_state:NC']])

df_inputs_prepr['addr_state:UT_KY_AZ_NJ'] = sum([df_inputs_prepr['addr_state:UT'], df_inputs_prepr['addr_state:KY'],
                                              df_inputs_prepr['addr_state:AZ'], df_inputs_prepr['addr_state:NJ']])

df_inputs_prepr['addr_state:AR_MI_PA_OH_MN'] = sum([df_inputs_prepr['addr_state:AR'], df_inputs_prepr['addr_state:MI'],
                                              df_inputs_prepr['addr_state:PA'], df_inputs_prepr['addr_state:OH'],
                                              df_inputs_prepr['addr_state:MN']])

df_inputs_prepr['addr_state:RI_MA_DE_SD_IN'] = sum([df_inputs_prepr['addr_state:RI'], df_inputs_prepr['addr_state:MA'],
                                              df_inputs_prepr['addr_state:DE'], df_inputs_prepr['addr_state:SD'],
                                              df_inputs_prepr['addr_state:IN']])

df_inputs_prepr['addr_state:GA_WA_OR'] = sum([df_inputs_prepr['addr_state:GA'], df_inputs_prepr['addr_state:WA'],
                                              df_inputs_prepr['addr_state:OR']])

df_inputs_prepr['addr_state:WI_MT'] = sum([df_inputs_prepr['addr_state:WI'], df_inputs_prepr['addr_state:MT']])

df_inputs_prepr['addr_state:IL_CT'] = sum([df_inputs_prepr['addr_state:IL'], df_inputs_prepr['addr_state:CT']])

df_inputs_prepr['addr_state:KS_SC_CO_VT_AK_MS'] = sum([df_inputs_prepr['addr_state:KS'], df_inputs_prepr['addr_state:SC'],
                                              df_inputs_prepr['addr_state:CO'], df_inputs_prepr['addr_state:VT'],
                                              df_inputs_prepr['addr_state:AK'], df_inputs_prepr['addr_state:MS']])

df_inputs_prepr['addr_state:WV_NH_WY_DC_ME_ID'] = sum([df_inputs_prepr['addr_state:WV'], df_inputs_prepr['addr_state:NH'],
                                              df_inputs_prepr['addr_state:WY'], df_inputs_prepr['addr_state:DC'],
                                              df_inputs_prepr['addr_state:ME'], df_inputs_prepr['addr_state:ID']])
#WHAT DOES THE SUM FUNCTION DO?
    #Sums across the columns

############################# RUNNING THE WOE FN ON OTHER VARIABLES
    
df_inputs_prepr['verification_status'].unique()
df_temp = woe_discrete(df_inputs_prepr, 'verification_status', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp)

##################

df_inputs_prepr['purpose'].unique()
df_temp = woe_discrete(df_inputs_prepr, 'purpose', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp,90)

# We combine 'educational', 'small_business', 'wedding', 'renewable_energy', 'moving', 'house' in one category: 'educ__sm_b__wedd__ren_en__mov__house'.
# We combine 'other', 'medical', 'vacation' in one category: 'oth__med__vacation'.
# We combine 'major_purchase', 'car', 'home_improvement' in one category: 'major_purch__car__home_impr'.
# We leave 'debt_consolidtion' in a separate category.
# We leave 'credit_card' in a separate category.
# 'educ__sm_b__wedd__ren_en__mov__house' will be the reference category.
df_inputs_prepr['purpose:educ__sm_b__wedd__ren_en__mov__house'] = sum([df_inputs_prepr['purpose:educational'], df_inputs_prepr['purpose:small_business'],
                                                                 df_inputs_prepr['purpose:wedding'], df_inputs_prepr['purpose:renewable_energy'],
                                                                 df_inputs_prepr['purpose:moving'], df_inputs_prepr['purpose:house']])
df_inputs_prepr['purpose:oth__med__vacation'] = sum([df_inputs_prepr['purpose:other'], df_inputs_prepr['purpose:medical'],
                                             df_inputs_prepr['purpose:vacation']])
df_inputs_prepr['purpose:major_purch__car__home_impr'] = sum([df_inputs_prepr['purpose:major_purchase'], df_inputs_prepr['purpose:car'],
                                                        df_inputs_prepr['purpose:home_improvement']])

###################################

    # 'initial_list_status'
df_temp = woe_discrete(df_inputs_prepr, 'initial_list_status', df_targets_prepr)
df_temp

plot_by_woe(df_temp)
# We plot the weight of evidence values.
######################Preprocessing for the discrete variable is  done############



######################Preprocessing for continuous variables begins: Automating calculations$$$$$
######################Preprocessing for continuous variables begins: Automating calculations$$$$$
######################Preprocessing for continuous variables begins: Automating calculations$$$$$

#first the fine classing and then coarse classing
#we ordered the dicrete functions by WoE as they showed no quantitative differences by the virtue 
#... of the category itself

#but the continuous variables diiffer quantitatively in the categories itself. Thus, we order them...
#... by the category, and not by WoE

#Preprocessing Continuous Variables: Automating Calculations and Visualizing Results
# WoE function for ordered discrete and continuous variables
def woe_ordered_continuous(df, discrete_variabe_name, good_bad_variable_df):
    df = pd.concat([df[discrete_variabe_name], good_bad_variable_df], axis = 1)
    df = pd.concat([df.groupby(df.columns.values[0], as_index = False)[df.columns.values[1]].count(),
                    df.groupby(df.columns.values[0], as_index = False)[df.columns.values[1]].mean()], axis = 1)
    df = df.iloc[:, [0, 1, 3]]
    df.columns = [df.columns.values[0], 'n_obs', 'prop_good']
    df['prop_n_obs'] = df['n_obs'] / df['n_obs'].sum()
    df['n_good'] = df['prop_good'] * df['n_obs']
    df['n_bad'] = (1 - df['prop_good']) * df['n_obs']
    df['prop_n_good'] = df['n_good'] / df['n_good'].sum()
    df['prop_n_bad'] = df['n_bad'] / df['n_bad'].sum()
    df['WoE'] = np.log(df['prop_n_good'] / df['prop_n_bad'])
    #df = df.sort_values(['WoE'])
    #df = df.reset_index(drop = True)
    #This function is similar to the discrete one with the difference that we do not wanna order them by WoE, instead 
    #retain their natural order
    df['diff_prop_good'] = df['prop_good'].diff().abs()
    df['diff_WoE'] = df['WoE'].diff().abs()
    df['IV'] = (df['prop_n_good'] - df['prop_n_bad']) * df['WoE']
    df['IV'] = df['IV'].sum()
    return df
# Here we define a function similar to the one above, ...
# ... with one slight difference: we order the results by the values of a different column.
# The function takes 3 arguments: a dataframe, a string, and a dataframe. The function returns a dataframe as a result.

### Preprocessing Continuous Variables: Creating Dummy Variables, Part 1

# term
df_inputs_prepr['term_int'].unique()
# There are only two unique values, 36 and 60.

df_temp = woe_ordered_continuous(df_inputs_prepr, 'term_int', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp)
# We plot the weight of evidence values.

# Leave as is.
# '60' will be the reference category.
df_inputs_prepr['term:36'] = np.where((df_inputs_prepr['term_int'] == 36), 1, 0)
df_inputs_prepr['term:60'] = np.where((df_inputs_prepr['term_int'] == 60), 1, 0)

# emp_length_int
df_inputs_prepr['emp_length_int'].unique()
# Has only 11 levels: from 0 to 10. Hence, we turn it into a factor with 11 levels.

df_temp = woe_ordered_continuous(df_inputs_prepr, 'emp_length_int', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp)
# We plot the weight of evidence values.

# We create the following categories: '0', '1', '2 - 4', '5 - 6', '7 - 9', '10'
# '0' will be the reference category
df_inputs_prepr['emp_length:0'] = np.where(df_inputs_prepr['emp_length_int'].isin([0]), 1, 0)
df_inputs_prepr['emp_length:1'] = np.where(df_inputs_prepr['emp_length_int'].isin([1]), 1, 0)
df_inputs_prepr['emp_length:2-4'] = np.where(df_inputs_prepr['emp_length_int'].isin(range(2, 5)), 1, 0)
df_inputs_prepr['emp_length:5-6'] = np.where(df_inputs_prepr['emp_length_int'].isin(range(5, 7)), 1, 0)
df_inputs_prepr['emp_length:7-9'] = np.where(df_inputs_prepr['emp_length_int'].isin(range(7, 10)), 1, 0)
df_inputs_prepr['emp_length:10'] = np.where(df_inputs_prepr['emp_length_int'].isin([10]), 1, 0)

## isin() is analogous to putting in filters on one of the heading in excel and being able to view the whole
#... dataset just related for that filter 

## We had to use in the ISIN() function because it can be clubbed with range() beautifully


### Preprocessing Continuous Variables: Creating Dummy Variables, Part 2#########################

#####REMEMBER THAT SINCE CONTINUOUS VARIABLE HAS NUMERICAL VALUES, THE LIMITS THAT WE CAN ASSIGN IN 
#### FINE CLASSING HAVE TO BE VALUES - fAIRLY OBVIOUS...

#####WHENEVR THE WOE FUNCTION OSCILLATES TOO MUCH.. THAT IS A RED FLAG AND CHECK FOR THE NO. OF OBSRVN
## WE SHOULD ANYWAY KEEP A REFERENCE TO NO OF OBSERVATIONS

###eVEN IF THE WOE OSCILLATING TOO MUCH BUT IF THE NUMBER OF OBSRVTNS ARE LESS, WE CAN CLUB THE X CATEGORIES
## OR DIVIDE THEM IN TWO

 
df_inputs_prepr['mths_since_issue_d'].unique()
df_inputs_prepr['mths_since_issue_d_factor'] = pd.cut(df_inputs_prepr['mths_since_issue_d'], 50)

# Here we do fine-classing: using the 'cut' method, we split the variable into 50 categories by its values.

df_inputs_prepr['mths_since_issue_d_factor']
# mths_since_issue_d
df_temp = woe_ordered_continuous(df_inputs_prepr, 'mths_since_issue_d_factor', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp)
# We plot the weight of evidence values.
# We have to rotate the labels because we cannot read them otherwise.

plot_by_woe(df_temp, 90)
# We plot the weight of evidence values, rotating the labels 90 degrees.

plot_by_woe(df_temp.iloc[3: , : ], 90)
# We plot the weight of evidence values.

# We create the following categories:
# < 38, 38 - 39, 40 - 41, 42 - 48, 49 - 52, 53 - 64, 65 - 84, > 84.
df_inputs_prepr['mths_since_issue_d:<38'] = np.where(df_inputs_prepr['mths_since_issue_d'].isin(range(38)), 1, 0)
df_inputs_prepr['mths_since_issue_d:38-39'] = np.where(df_inputs_prepr['mths_since_issue_d'].isin(range(38, 40)), 1, 0)
df_inputs_prepr['mths_since_issue_d:40-41'] = np.where(df_inputs_prepr['mths_since_issue_d'].isin(range(40, 42)), 1, 0)
df_inputs_prepr['mths_since_issue_d:42-48'] = np.where(df_inputs_prepr['mths_since_issue_d'].isin(range(42, 49)), 1, 0)
df_inputs_prepr['mths_since_issue_d:49-52'] = np.where(df_inputs_prepr['mths_since_issue_d'].isin(range(49, 53)), 1, 0)
df_inputs_prepr['mths_since_issue_d:53-64'] = np.where(df_inputs_prepr['mths_since_issue_d'].isin(range(53, 65)), 1, 0)
df_inputs_prepr['mths_since_issue_d:65-84'] = np.where(df_inputs_prepr['mths_since_issue_d'].isin(range(65, 85)), 1, 0)
df_inputs_prepr['mths_since_issue_d:>84'] = np.where(df_inputs_prepr['mths_since_issue_d'].isin(range(85, int(df_inputs_prepr['mths_since_issue_d'].max()))), 1, 0)

# int_rate
df_inputs_prepr['int_rate_factor'] = pd.cut(df_inputs_prepr['int_rate'], 50)
# Here we do fine-classing: using the 'cut' method, we split the variable into 50 categories by its values.

df_inputs_prepr['int_rate_factor']

df_temp = woe_ordered_continuous(df_inputs_prepr, 'int_rate_factor', df_targets_prepr)
# We calculate weight of evidence.
df_temp


plot_by_woe(df_temp, 90)
# We plot the weight of evidence values.


# '< 9.548', '9.548 - 12.025', '12.025 - 15.74', '15.74 - 20.281', '> 20.281'
#There is a bit of stability after 9.548, thus it is a cut off
## Also, note that we used rounded off values in creating dummies for 'mths_since_issue_d'
###but we kept the categories of int_rate within the integer range

df_inputs_prepr['int_rate:<9.548'] = np.where((df_inputs_prepr['int_rate'] <= 9.548), 1, 0)
df_inputs_prepr['int_rate:9.548-12.025'] = np.where((df_inputs_prepr['int_rate'] > 9.548) & (df_inputs_prepr['int_rate'] <= 12.025), 1, 0)
df_inputs_prepr['int_rate:12.025-15.74'] = np.where((df_inputs_prepr['int_rate'] > 12.025) & (df_inputs_prepr['int_rate'] <= 15.74), 1, 0)
df_inputs_prepr['int_rate:15.74-20.281'] = np.where((df_inputs_prepr['int_rate'] > 15.74) & (df_inputs_prepr['int_rate'] <= 20.281), 1, 0)
df_inputs_prepr['int_rate:>20.281'] = np.where((df_inputs_prepr['int_rate'] > 20.281), 1, 0)

####Note that everything is being stored in df_inputs_prepr, which is the copy of the 
#inputs_test that we created

#### After 1st round of preprocessing inputs, we would hash out df_inputs_prepr = loan_data_inputs_train
# and df_targets_prepr = loan_data_targets_train

#But before that we would save df_inputs_prepr in loan_data_inputs_train and
# df_targets_prepr in loan_data_targets_train ## This is just the reverese of what we did
#after splitting the data 

####At that stage, we would hash in #df_inputs_prepr = loan_data_inputs_test and 
# df_targets_prepr = loan_data_targets_test 

# funded_amnt
df_inputs_prepr['funded_amnt_factor'] = pd.cut(df_inputs_prepr['funded_amnt'], 50)
# Here we do fine-classing: using the 'cut' method, we split the variable into 50 categories by its values.
df_temp = woe_ordered_continuous(df_inputs_prepr, 'funded_amnt_factor', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp, 90)
# We plot the weight of evidence values.

#WoE does not seem to have any relation with the Funded Amount whatsoever. Because the
## chart is all zig zag.. Thus, we would NOT use this variable in the model 


# mths_since_earliest_cr_line
df_inputs_prepr['mths_since_earliest_cr_line_factor'] = pd.cut(df_inputs_prepr['mths_since_earliest_cr_line'], 50)
# Here we do fine-classing: using the 'cut' method, we split the variable into 50 categories by its values.
df_temp = woe_ordered_continuous(df_inputs_prepr, 'mths_since_earliest_cr_line_factor', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp, 90)
# We plot the weight of evidence values.

plot_by_woe(df_temp.iloc[6: , : ], 90)
# We plot the weight of evidence values.

# We create the following categories:
# < 140, # 141 - 164, # 165 - 247, # 248 - 270, # 271 - 352, # > 352
df_inputs_prepr['mths_since_earliest_cr_line:<140'] = np.where(df_inputs_prepr['mths_since_earliest_cr_line'].isin(range(0,140)), 1, 0)
df_inputs_prepr['mths_since_earliest_cr_line:141-164'] = np.where(df_inputs_prepr['mths_since_earliest_cr_line'].isin(range(140, 165)), 1, 0)
df_inputs_prepr['mths_since_earliest_cr_line:165-247'] = np.where(df_inputs_prepr['mths_since_earliest_cr_line'].isin(range(165, 248)), 1, 0)
df_inputs_prepr['mths_since_earliest_cr_line:248-270'] = np.where(df_inputs_prepr['mths_since_earliest_cr_line'].isin(range(248, 271)), 1, 0)
df_inputs_prepr['mths_since_earliest_cr_line:271-352'] = np.where(df_inputs_prepr['mths_since_earliest_cr_line'].isin(range(271, 353)), 1, 0)
df_inputs_prepr['mths_since_earliest_cr_line:>352'] = np.where(df_inputs_prepr['mths_since_earliest_cr_line'].isin(range(353, int(df_inputs_prepr['mths_since_earliest_cr_line'].max()))), 1, 0)


# delinq_2yrs
df_temp = woe_ordered_continuous(df_inputs_prepr, 'delinq_2yrs', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp)
# We plot the weight of evidence values.

# Categories: 0, 1-3, >=4
df_inputs_prepr['delinq_2yrs:0'] = np.where((df_inputs_prepr['delinq_2yrs'] == 0), 1, 0)
df_inputs_prepr['delinq_2yrs:1-3'] = np.where((df_inputs_prepr['delinq_2yrs'] >= 1) & (df_inputs_prepr['delinq_2yrs'] <= 3), 1, 0)
df_inputs_prepr['delinq_2yrs:>=4'] = np.where((df_inputs_prepr['delinq_2yrs'] >= 4), 1, 0)


# inq_last_6mths
df_temp = woe_ordered_continuous(df_inputs_prepr, 'inq_last_6mths', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp)
# We plot the weight of evidence values.

df_inputs_prepr['inq_last_6mths'].unique()
# Categories: 0, 1 - 2, 3 - 6, > 6
df_inputs_prepr['inq_last_6mths:0'] = np.where((df_inputs_prepr['inq_last_6mths'] == 0), 1, 0)
df_inputs_prepr['inq_last_6mths:1-2'] = np.where((df_inputs_prepr['inq_last_6mths'] >= 1) & (df_inputs_prepr['inq_last_6mths'] <= 2), 1, 0)
df_inputs_prepr['inq_last_6mths:3-6'] = np.where((df_inputs_prepr['inq_last_6mths'] >= 3) & (df_inputs_prepr['inq_last_6mths'] <= 6), 1, 0)
df_inputs_prepr['inq_last_6mths:>6'] = np.where((df_inputs_prepr['inq_last_6mths'] > 6), 1, 0)


# open_acc
df_temp = woe_ordered_continuous(df_inputs_prepr, 'open_acc', df_targets_prepr)
# We calculate weight of evidence.
df_temp


plot_by_woe(df_temp, 90)
# We plot the weight of evidence values.

plot_by_woe(df_temp.iloc[ : 40, :], 90)
# We plot the weight of evidence values.

# Categories: '0', '1-3', '4-12', '13-17', '18-22', '23-25', '26-30', '>30'
df_inputs_prepr['open_acc:0'] = np.where((df_inputs_prepr['open_acc'] == 0), 1, 0)
df_inputs_prepr['open_acc:1-3'] = np.where((df_inputs_prepr['open_acc'] >= 1) & (df_inputs_prepr['open_acc'] <= 3), 1, 0)
df_inputs_prepr['open_acc:4-12'] = np.where((df_inputs_prepr['open_acc'] >= 4) & (df_inputs_prepr['open_acc'] <= 12), 1, 0)
df_inputs_prepr['open_acc:13-17'] = np.where((df_inputs_prepr['open_acc'] >= 13) & (df_inputs_prepr['open_acc'] <= 17), 1, 0)
df_inputs_prepr['open_acc:18-22'] = np.where((df_inputs_prepr['open_acc'] >= 18) & (df_inputs_prepr['open_acc'] <= 22), 1, 0)
df_inputs_prepr['open_acc:23-25'] = np.where((df_inputs_prepr['open_acc'] >= 23) & (df_inputs_prepr['open_acc'] <= 25), 1, 0)
df_inputs_prepr['open_acc:26-30'] = np.where((df_inputs_prepr['open_acc'] >= 26) & (df_inputs_prepr['open_acc'] <= 30), 1, 0)
df_inputs_prepr['open_acc:>=31'] = np.where((df_inputs_prepr['open_acc'] >= 31), 1, 0)

# pub_rec
df_temp = woe_ordered_continuous(df_inputs_prepr, 'pub_rec', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp, 90)
# We plot the weight of evidence values.

# Categories '0-2', '3-4', '>=5'
df_inputs_prepr['pub_rec:0-2'] = np.where((df_inputs_prepr['pub_rec'] >= 0) & (df_inputs_prepr['pub_rec'] <= 2), 1, 0)
df_inputs_prepr['pub_rec:3-4'] = np.where((df_inputs_prepr['pub_rec'] >= 3) & (df_inputs_prepr['pub_rec'] <= 4), 1, 0)
df_inputs_prepr['pub_rec:>=5'] = np.where((df_inputs_prepr['pub_rec'] >= 5), 1, 0)

# total_acc
df_inputs_prepr['total_acc_factor'] = pd.cut(df_inputs_prepr['total_acc'], 50)
# Here we do fine-classing: using the 'cut' method, we split the variable into 50 categories by its values.
df_temp = woe_ordered_continuous(df_inputs_prepr, 'total_acc_factor', df_targets_prepr)
# We calculate weight of evidence.
df_temp


plot_by_woe(df_temp, 90)
# We plot the weight of evidence values.

# Categories: '<=27', '28-51', '>51'
df_inputs_prepr['total_acc:<=27'] = np.where((df_inputs_prepr['total_acc'] <= 27), 1, 0)
df_inputs_prepr['total_acc:28-51'] = np.where((df_inputs_prepr['total_acc'] >= 28) & (df_inputs_prepr['total_acc'] <= 51), 1, 0)
df_inputs_prepr['total_acc:>=52'] = np.where((df_inputs_prepr['total_acc'] >= 52), 1, 0)

# acc_now_delinq
df_temp = woe_ordered_continuous(df_inputs_prepr, 'acc_now_delinq', df_targets_prepr)
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp)
# We plot the weight of evidence values.

# Categories: '0', '>=1'
df_inputs_prepr['acc_now_delinq:0'] = np.where((df_inputs_prepr['acc_now_delinq'] == 0), 1, 0)
df_inputs_prepr['acc_now_delinq:>=1'] = np.where((df_inputs_prepr['acc_now_delinq'] >= 1), 1, 0)


# total_rev_hi_lim
#df_inputs_prepr['total_rev_hi_lim'].describe() #IMPORTANT to analyze quartiles and make suitable cuts
#Analyze a bit of numbers, see number is covering 95% data (for instance) --> set everything into one category above that 
# analyze the population % observations  
#df_inputs_prepr['total_rev_hi_lim'].to_excel('.....\\total_rev_hi_lim_prepr.xlsx')
df_inputs_prepr['total_rev_hi_lim_factor'] = pd.cut(df_inputs_prepr['total_rev_hi_lim'], 2000)
# Here we do fine-classing: using the 'cut' method, we split the variable into 2000 categories by its values.
df_temp = woe_ordered_continuous(df_inputs_prepr, 'total_rev_hi_lim_factor', df_targets_prepr)
# We calculate weight of evidence.
#I analysed the numbers % population observations and above that make the highest category
#df_temp.to_excel('............\\total_rev_hi_lim.xlsx')
#pd.options.display.max_columns=None
df_temp

plot_by_woe(df_temp.iloc[: 50, : ], 90)
# We plot the weight of evidence values.
plot_by_woe(df_temp.iloc[: 25, : ], 90)
# Categories
# '<=5K', '5K-10K', '10K-20K', '20K-30K', '30K-40K', '40K-55K', '55K-95K', '>95K'
df_inputs_prepr['total_rev_hi_lim:<=5K'] = np.where((df_inputs_prepr['total_rev_hi_lim'] <= 5000), 1, 0)
df_inputs_prepr['total_rev_hi_lim:5K-10K'] = np.where((df_inputs_prepr['total_rev_hi_lim'] > 5000) & (df_inputs_prepr['total_rev_hi_lim'] <= 10000), 1, 0)
df_inputs_prepr['total_rev_hi_lim:10K-20K'] = np.where((df_inputs_prepr['total_rev_hi_lim'] > 10000) & (df_inputs_prepr['total_rev_hi_lim'] <= 20000), 1, 0)
df_inputs_prepr['total_rev_hi_lim:20K-30K'] = np.where((df_inputs_prepr['total_rev_hi_lim'] > 20000) & (df_inputs_prepr['total_rev_hi_lim'] <= 30000), 1, 0)
df_inputs_prepr['total_rev_hi_lim:30K-40K'] = np.where((df_inputs_prepr['total_rev_hi_lim'] > 30000) & (df_inputs_prepr['total_rev_hi_lim'] <= 40000), 1, 0)
df_inputs_prepr['total_rev_hi_lim:40K-55K'] = np.where((df_inputs_prepr['total_rev_hi_lim'] > 40000) & (df_inputs_prepr['total_rev_hi_lim'] <= 55000), 1, 0)
df_inputs_prepr['total_rev_hi_lim:55K-95K'] = np.where((df_inputs_prepr['total_rev_hi_lim'] > 55000) & (df_inputs_prepr['total_rev_hi_lim'] <= 95000), 1, 0)
df_inputs_prepr['total_rev_hi_lim:>95K'] = np.where((df_inputs_prepr['total_rev_hi_lim'] > 95000), 1, 0)

# installment
df_inputs_prepr['installment_factor'] = pd.cut(df_inputs_prepr['installment'], 50)
# Here we do fine-classing: using the 'cut' method, we split the variable into 50 categories by its values.
df_temp = woe_ordered_continuous(df_inputs_prepr, 'installment_factor', df_targets_prepr)
# We calculate weight of evidence.
df_temp
# May be we do not consider this factor
plot_by_woe(df_temp, 90)
# We plot the weight of evidence values.




### Preprocessing Continuous Variables: Creating Dummy Variables, Part 3
##########Thiis is a bit indirect variable to split...
## You analyse the data and look what is covering most of the values like about 99%
# Split the categories into reasonable gaps
##look at the data if any of the category is pulling the weight or are they too light (in which case split has to be reduced)
## Head and Tail might be light so club couple of categories over there, rest split equally in 10K range
 
# annual_inc
df_inputs_prepr['annual_inc_factor'] = pd.cut(df_inputs_prepr['annual_inc'], 50)
# Here we do fine-classing: using the 'cut' method, we split the variable into 50 categories by its values.
df_temp = woe_ordered_continuous(df_inputs_prepr, 'annual_inc_factor', df_targets_prepr)
# We calculate weight of evidence.
df_temp

#WE OBSERVED HERE THAT THE FIRST INTERVAL CARRIES 94% OF THE TOTAL OBSERVATIONS. THUS, WE AGAIN SPLIT IT INTO
##100 CATEGORIES

df_inputs_prepr['annual_inc_factor'] = pd.cut(df_inputs_prepr['annual_inc'], 100)
# Here we do fine-classing: using the 'cut' method, we split the variable into 100 categories by its values.
df_temp = woe_ordered_continuous(df_inputs_prepr, 'annual_inc_factor', df_targets_prepr)
# We calculate weight of evidence.
df_temp
#DIVIDING INTO 100 CATEGORIES GAVE US A FAIR SPLIT BETWEEN THE CLASSES

plot_by_woe(df_temp, 90)

# Initial examination shows that there are too few individuals with large income and too many with small income.
# Hence, we are going to have one category for more than 150K, and we are going to apply our approach to determine
# the categories of everyone with 140k or less.
df_inputs_prepr_temp  = df_inputs_prepr.loc[df_inputs_prepr['annual_inc'] <= 140000, : ]
#loan_data_temp = loan_data_temp.reset_index(drop = True)
#df_inputs_prepr_temp

df_inputs_prepr_temp["annual_inc_factor"] = pd.cut(df_inputs_prepr_temp['annual_inc'], 50)
# Here we do fine-classing: using the 'cut' method, we split the variable into 50 categories by its values.
df_temp = woe_ordered_continuous(df_inputs_prepr_temp, 'annual_inc_factor', df_targets_prepr[df_inputs_prepr_temp.index])
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp, 90)
# We plot the weight of evidence values.
# WoE is monotonically decreasing with income, so we split income in 10 equal categories, each with width of 10k.
df_inputs_prepr['annual_inc:<20K'] = np.where((df_inputs_prepr['annual_inc'] <= 20000), 1, 0)
df_inputs_prepr['annual_inc:20K-30K'] = np.where((df_inputs_prepr['annual_inc'] > 20000) & (df_inputs_prepr['annual_inc'] <= 30000), 1, 0)
df_inputs_prepr['annual_inc:30K-40K'] = np.where((df_inputs_prepr['annual_inc'] > 30000) & (df_inputs_prepr['annual_inc'] <= 40000), 1, 0)
df_inputs_prepr['annual_inc:40K-50K'] = np.where((df_inputs_prepr['annual_inc'] > 40000) & (df_inputs_prepr['annual_inc'] <= 50000), 1, 0)
df_inputs_prepr['annual_inc:50K-60K'] = np.where((df_inputs_prepr['annual_inc'] > 50000) & (df_inputs_prepr['annual_inc'] <= 60000), 1, 0)
df_inputs_prepr['annual_inc:60K-70K'] = np.where((df_inputs_prepr['annual_inc'] > 60000) & (df_inputs_prepr['annual_inc'] <= 70000), 1, 0)
df_inputs_prepr['annual_inc:70K-80K'] = np.where((df_inputs_prepr['annual_inc'] > 70000) & (df_inputs_prepr['annual_inc'] <= 80000), 1, 0)
df_inputs_prepr['annual_inc:80K-90K'] = np.where((df_inputs_prepr['annual_inc'] > 80000) & (df_inputs_prepr['annual_inc'] <= 90000), 1, 0)
df_inputs_prepr['annual_inc:90K-100K'] = np.where((df_inputs_prepr['annual_inc'] > 90000) & (df_inputs_prepr['annual_inc'] <= 100000), 1, 0)
df_inputs_prepr['annual_inc:100K-120K'] = np.where((df_inputs_prepr['annual_inc'] > 100000) & (df_inputs_prepr['annual_inc'] <= 120000), 1, 0)
df_inputs_prepr['annual_inc:120K-140K'] = np.where((df_inputs_prepr['annual_inc'] > 120000) & (df_inputs_prepr['annual_inc'] <= 140000), 1, 0)
df_inputs_prepr['annual_inc:>140K'] = np.where((df_inputs_prepr['annual_inc'] > 140000), 1, 0)

# mths_since_last_delinq
# We have to create one category for missing values and do fine and coarse classing for the rest.
df_inputs_prepr['mths_since_last_delinq']
df_inputs_prepr['mths_since_last_delinq'].unique
df_inputs_prepr_temp = df_inputs_prepr[pd.notnull(df_inputs_prepr['mths_since_last_delinq'])]
df_inputs_prepr_temp['mths_since_last_delinq_factor'] = pd.cut(df_inputs_prepr_temp['mths_since_last_delinq'], 50)
df_temp = woe_ordered_continuous(df_inputs_prepr_temp, 'mths_since_last_delinq_factor', df_targets_prepr[df_inputs_prepr_temp.index])
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp, 90)
# We plot the weight of evidence values.
plot_by_woe(df_temp.iloc[:16,:], 90)


# Categories: Missing, 0-3, 4-30, 31-56, >=57
df_inputs_prepr['mths_since_last_delinq:Missing'] = np.where((df_inputs_prepr['mths_since_last_delinq'].isnull()), 1, 0)
df_inputs_prepr['mths_since_last_delinq:0-3'] = np.where((df_inputs_prepr['mths_since_last_delinq'] >= 0) & (df_inputs_prepr['mths_since_last_delinq'] <= 3), 1, 0)
df_inputs_prepr['mths_since_last_delinq:4-30'] = np.where((df_inputs_prepr['mths_since_last_delinq'] >= 4) & (df_inputs_prepr['mths_since_last_delinq'] <= 30), 1, 0)
df_inputs_prepr['mths_since_last_delinq:31-56'] = np.where((df_inputs_prepr['mths_since_last_delinq'] >= 31) & (df_inputs_prepr['mths_since_last_delinq'] <= 56), 1, 0)
df_inputs_prepr['mths_since_last_delinq:>=57'] = np.where((df_inputs_prepr['mths_since_last_delinq'] >= 57), 1, 0)

### Preprocessing Continuous Variables: Creating Dummy Variables, Part 3: Homework

# dti
df_inputs_prepr['dti_factor'] = pd.cut(df_inputs_prepr['dti'], 100)
# Here we do fine-classing: using the 'cut' method, we split the variable into 100 categories by its values.
df_temp = woe_ordered_continuous(df_inputs_prepr, 'dti_factor', df_targets_prepr)
# We calculate weight of evidence.
df_temp
#df_temp.to_excel('.....//dti_factor.xlsx')
plot_by_woe(df_temp, 90)
# We plot the weight of evidence values.

# Similarly to income, initial examination shows that most values are lower than 200.
# Hence, we are going to have one category for more than 35, and we are going to apply our approach to determine
# the categories of everyone with 150k or less.
df_inputs_prepr_temp = df_inputs_prepr.loc[df_inputs_prepr['dti'] <= 35, : ]
df_inputs_prepr_temp['dti_factor'] = pd.cut(df_inputs_prepr_temp['dti'], 50)
# Here we do fine-classing: using the 'cut' method, we split the variable into 50 categories by its values.
df_temp = woe_ordered_continuous(df_inputs_prepr_temp, 'dti_factor', df_targets_prepr[df_inputs_prepr_temp.index])
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp, 90)
# We plot the weight of evidence values.

# Categories:
df_inputs_prepr['dti:<=1.4'] = np.where((df_inputs_prepr['dti'] <= 1.4), 1, 0)
df_inputs_prepr['dti:1.4-3.5'] = np.where((df_inputs_prepr['dti'] > 1.4) & (df_inputs_prepr['dti'] <= 3.5), 1, 0)
df_inputs_prepr['dti:3.5-7.7'] = np.where((df_inputs_prepr['dti'] > 3.5) & (df_inputs_prepr['dti'] <= 7.7), 1, 0)
df_inputs_prepr['dti:7.7-10.5'] = np.where((df_inputs_prepr['dti'] > 7.7) & (df_inputs_prepr['dti'] <= 10.5), 1, 0)
df_inputs_prepr['dti:10.5-16.1'] = np.where((df_inputs_prepr['dti'] > 10.5) & (df_inputs_prepr['dti'] <= 16.1), 1, 0)
df_inputs_prepr['dti:16.1-20.3'] = np.where((df_inputs_prepr['dti'] > 16.1) & (df_inputs_prepr['dti'] <= 20.3), 1, 0)
df_inputs_prepr['dti:20.3-21.7'] = np.where((df_inputs_prepr['dti'] > 20.3) & (df_inputs_prepr['dti'] <= 21.7), 1, 0)
df_inputs_prepr['dti:21.7-22.4'] = np.where((df_inputs_prepr['dti'] > 21.7) & (df_inputs_prepr['dti'] <= 22.4), 1, 0)
df_inputs_prepr['dti:22.4-35'] = np.where((df_inputs_prepr['dti'] > 22.4) & (df_inputs_prepr['dti'] <= 35), 1, 0)
df_inputs_prepr['dti:>35'] = np.where((df_inputs_prepr['dti'] > 35), 1, 0)

# mths_since_last_record
# We have to create one category for missing values and do fine and coarse classing for the rest.
df_inputs_prepr_temp = df_inputs_prepr[pd.notnull(df_inputs_prepr['mths_since_last_record'])]
#sum(loan_data_temp['mths_since_last_record'].isnull())
df_inputs_prepr_temp['mths_since_last_record_factor'] = pd.cut(df_inputs_prepr_temp['mths_since_last_record'], 50)
# Here we do fine-classing: using the 'cut' method, we split the variable into 50 categories by its values.
df_temp = woe_ordered_continuous(df_inputs_prepr_temp, 'mths_since_last_record_factor', df_targets_prepr[df_inputs_prepr_temp.index])
# We calculate weight of evidence.
df_temp

plot_by_woe(df_temp, 90)
# We plot the weight of evidence values.

# Categories: 'Missing', '0-2', '3-20', '21-31', '32-80', '81-86', '>86'
df_inputs_prepr['mths_since_last_record:Missing'] = np.where((df_inputs_prepr['mths_since_last_record'].isnull()), 1, 0)
df_inputs_prepr['mths_since_last_record:0-2'] = np.where((df_inputs_prepr['mths_since_last_record'] >= 0) & (df_inputs_prepr['mths_since_last_record'] <= 2), 1, 0)
df_inputs_prepr['mths_since_last_record:3-20'] = np.where((df_inputs_prepr['mths_since_last_record'] >= 3) & (df_inputs_prepr['mths_since_last_record'] <= 20), 1, 0)
df_inputs_prepr['mths_since_last_record:21-31'] = np.where((df_inputs_prepr['mths_since_last_record'] >= 21) & (df_inputs_prepr['mths_since_last_record'] <= 31), 1, 0)
df_inputs_prepr['mths_since_last_record:32-80'] = np.where((df_inputs_prepr['mths_since_last_record'] >= 32) & (df_inputs_prepr['mths_since_last_record'] <= 80), 1, 0)
df_inputs_prepr['mths_since_last_record:81-86'] = np.where((df_inputs_prepr['mths_since_last_record'] >= 81) & (df_inputs_prepr['mths_since_last_record'] <= 86), 1, 0)
df_inputs_prepr['mths_since_last_record:>86'] = np.where((df_inputs_prepr['mths_since_last_record'] > 86), 1, 0)

## Most important line of the PREPROCESSING CODES AFTER COMPLETION
## Most important line of the PREPROCESSING CODES AFTER COMPLETION
## Most important line of the PREPROCESSING CODES AFTER COMPLETION
## Most important line of the PREPROCESSING CODES AFTER COMPLETION
## Most important line of the PREPROCESSING CODES AFTER COMPLETION
df_inputs_prepr.isnull().sum()
df_inputs_prepr.columns.values
df_inputs_prepr.shape
pd.options.display.max_rows = None

#Unhash the following lines while training the data

#loan_data_inputs_train = df_inputs_prepr
#loan_data_targets_train = df_targets_prepr

## Most important line of the PREPROCESSING CODES AFTER COMPLETION
## Most important line of the PREPROCESSING CODES AFTER COMPLETION


####################################### Preprocessing the Test Dataset #####################################
####################################### Preprocessing the Test Dataset #####################################
####################################### Preprocessing the Test Dataset #####################################
####################################### Preprocessing the Test Dataset #####################################

#####First read this:
# Test data needs to be exactly similar to the train data.. Thus, we need to use the same code as above
# We do not care for WoE as it does not matter in test data. We are gonna ignore it
# Now, you know that the fuctions that you have created work for 'df_inputs_prepr'
# Since we are moving into a test space, we need to save the preprocessed data
# Initially, we created a variable loan_data_inputs_train, it is now wtime to use it

############################ The following is a very skillful part where steps in codes iis extremely important....####


#loan_data_inputs_train = df_inputs_prepr ###You will need to move step by step and first execute this code 
#.. to save the preprocessing data results for train and then move on to the following
## then go right below the train_test_split, where we created the dataframes equal to df_inputs_prepr
    #hash out the df_inputs_prepr = loan_data_inputs_train 
    # and write that df_inputss_prepr= loan_data_inputs_test
    #run the code again till this point BUT hashing out 'loan_data_inputs_train = df_inputs_prepr'
    #.....as you now want to save the results in 'loan_data_inputs_test 
    # save the result
#####
loan_data_inputs_test = df_inputs_prepr
loan_data_targets_test = df_targets_prepr
#################################################################

#loan_data_inputs_train.to_csv('........Resources\\Train_Test dataset after running the code\\loan_data_inputs_train.csv')
#loan_data_targets_train.to_csv('.....Resources\\Train_Test dataset after running the code\\loan_data_targets_train.csv')
loan_data_inputs_test.to_csv('.......Resources\\Train_Test dataset after running the code\\loan_data_inputs_test.csv')
loan_data_targets_test.to_csv('.......Resources\\Train_Test dataset after running the code\\loan_data_targets_test.csv')



#..... this section is complete.. This section included:
#    1. preprocessing dates, time, integer, floats, objects 
#    2. creating dummies
#    3. splitting the training and testing data
# On training data
#    4. creating WoE and IV function, visualising and automating it
#    5. Fine classing and coarse classing
#    6. Creating dummies for the classes
#    7. Saving the df_inputs_prepr dataframe into inputs dataframe
#    8. Hashing out the df_inputs_train
# On training data
#    4. assigning test data to df_inputs_prepr 
#      running the automated code for WoE and IV function
#    5. Fine classing and coarse classing
#    6. Creating dummies for the classes      

