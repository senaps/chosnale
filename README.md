# Chosnale

we all have some shity stuff that we want to say right? do you know of anywhere you can say shit and don't care about the consequenses? no body knows you, there is no fans, bands, follow and backfollow bullshit, it's just shit to make it go away.

for now, it's developer's only. but it might get bigger if people liked it and started using it! :) we have pagination too(if you know what i mean)

# Useage
okay, enough of bullshit, How to use it right?

## get latest bullshits

it's easy! just send a `GET` request for `/get_chosnale/` to receive latest 10 chosnales by the community, sorted by publish time.

you have some options to pass though, just send a `POST` request to the same url, with all or one of the bellow options:

|key|type|description|
|:---|:---|:---|
|page|int|the page of chosnale content!|
|per_page|int|How many chosnale's per page do you want?|
|order|str|What do you want as sorting pivot?|

now, to use `order`, you should one of the following arguments as the value. note these should be `str` types.

|argument|description|
|:---|:---|
|featured|show featured ones(ones with most votes)/ doesn't work!|
|votes|sort by the votes. always see the most voted ones|
|pub_date|default, sort based on the publish date|

## send a chosnale

to send over a chosnale, you should `POST` an chosnale object to the `add_chosnale/` endpoint.

following are the values you should include:

|key|type|description|
|:---|:---|:---|
|text|str|the actual chosnale text! it should be less than 240 chars!|

## vote a chosnale
votes will eventually make a chosnale to be featured and sent over to twitter or be shown in their actual order. **note** sending the tweet isn't implemented yet.
to cast your vote, you need to send a `GET` request to the `/vote/`, only that you have to pass in the `id` for the tweet you want to vote for after the url. your final url to vote should look like this:

    /vote/<id>
    /vote/5

in above examples, the second one is how your `url` should look like when you are actually voting!:)