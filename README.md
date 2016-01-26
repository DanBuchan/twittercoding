# INSTALL

```
> git clone https://github.com/DanBuchan/twittercoding.git
> pip -r install requirements
> python manage.py createsuperuser
```

# HOW IT WORKS

To start the system you **MUST** do these steps in this numerical order.

## 1. Format you tweet csv correctly

First of all you **MUST** format your tweet file correctly. For now it is required
to be in csv format with the following columns

1. Numeric column
2. Tweet ID
3. tweet timestamp
4. twitter username
5. language
6. coordinates
7. text
8. label

The label is the broad category of the tweet and is used to assign which users
will code which tweets. For instance if our tweets were for UK politicians we
might use the label CON for conservative politician tweets and LAB for labour
politician tweets and so forth

If you look in the data dir there is and example correctly formatted input file called test_tweets.csv

## 2. Upload the tweets

Login as the admin user then visit `http://DOMAIN/coding/upload/`

Here you can upload your file of tweets.

## 3. Add coding categories

Login in to the admin interface (see below). Select the Categories section. On
the next page click the "+ Add Category" button to add a coding category and its fields.

The interface allows categories to be contingent to on a prior selection. Although
selections may only have 1 child Category.  

**IMPORTANT**

First input all the Categories you wish to display inputing them in the left
to right order you wish them to appear to the users. Only once this is done can
you go back and add child_categories.

## 4. Register users to code tweets

Once the tweets are in the database with the correct labels now you can
create users and assign them a label to encode. **DO NOT** add users
until the tweets are successfully loaded. Visit `http://DOMAIN/coding/register/`
to add users. Note that the Tweet Label field is taken from column 8 in the csv
in step 1. The selection on user registration assigns which tweets a user will
be shown.

## 5. Register 0 or more recoder users

If you wish to allow users to re-code previously coded tweets select the
Recoder option which creating a user. This overrides the Tweet Label setting.
Recoding users are instead shown random tweets from the complete set of previously
coded tweets.

## 6. Monitoring progress

### Summary stats

Visit `http://DOMAIN/coding/summary` to see broad count stats on the number
of tweets in the database and the number that have been coded and recoded.

Counts of tweets assigned to each category are also listed

### Tweet assignments

If you have a tweet ID you can check it's coding and recoding at
`http://DOMAIN/coding/tweet/[TWITTER_ID]`

## 7. Dump all coded tweets

If you wish to download the coding data this can be dumped at `http://DOMAIN/coding/dump/`

# CODING TWEETS

Go to the login page `http://DOMAIN/coding/login` and log in as a user other than
Admin. The user will now be shown uncoded tweets for their coding category. Some progress stats are listed.

# ADMINISTRATION

Visit `http://DOMAIN/admin/` and log in to access the administrative interface.
From here you can administer various portions of the system.

## Authentication

### Users

From here you can add or remove users or edit their settings. Notably you can
change the Tweet Label the user code and alter their recoder status.

## Coding

### Categorys

From here add coding categories and their labels

### Codes

This table holds the codes users have assigned for tweets you can edit or delete
these. Not if you delete a code here you must unset the coding or recoding setting for the tweet in the tweet table.

### Tweets

This table holds all the tweets and you can edit, delete or add them here. You can also empty the db here. If you do this be sure to empty the Codes table too.
