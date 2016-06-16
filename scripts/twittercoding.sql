select coding_tweet.tweet_id, coding_tweet.user_name, coding_tweet.label, coding_code.user_id, auth_user.username, coding_category.name, coding_feature.name FROM coding_tweet, coding_code, auth_user, coding_category, coding_feature WHERE coding_tweet.id==coding_code.tweet_id AND coding_code.user_id==auth_user.id AND coding_code.category_id==coding_category.id AND coding_code.feature_id==coding_feature.id limit 10;
