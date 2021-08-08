# capstone1

### Cryptocurrency Tracker

1. What goal will your website be designed to achieve?

  - Display current data on most popular cryptocurrencies on a scrolling ticker.

  - ***Display historical data on most popular crytocurrencies through graph (tabs for a few hours to full timeline).  If possible include candlestick option.  Likely require them to favorite a currency to get this feature.  This appears to be a paid feature for most APIs that I have found, so may not be able to do this.***

  - Allow users to create an account and favorite cryptocurrencies.  These will display persistently on the main page when logged in, along with scrolling ticker, but favorited currency displays will show more detailed information.  I will include some static graphics on the main page showing users what this all looks like to entice them to create an account to gain access to these features.  This way, even if they don't take the time to create an account, they will see what it is capable of at just a quick glance.

  - ***Allow users to create an account and receive updates when cryptocurrencies reach a certain value.  Not sure how to do this yet...***

  - Give information on cryptocurrency investments and how the block chain works (guides).  Users will have to agree to a disclaimer that this information is not financial advice and to use any information at their own financial risk before being able to view this information (modal for non logged in users, and logged in users will have had to agree to this to create an account).

  - Display latest cryptocurrency news (may have to display headlines and a snippet, then make it so full article opens in a new tab when they click read more...).

  - Price calculator (fiat to crypto, and vice versa).

2. What kind of users will visit your site? In other words, what is the demographic of your users?

  - Anyone interested in cryptocurrencies.

3. What data are you planning on using?

  - Crytocurrency values, current **and historical.**

4. Brief outline of approach.

  a. What does your database schema look like?

    - Database of users, and database containing crytocurrency names.  Connected at which ones have been favorited by which users.

  b. What kinds of issues might you run into with your API?

    - Making more than limited number of API calls.

    - No access to certain types of data, making it so I have to not include certain features without paying.

  c. Is there any sensitive information you need to secure?

    - User information (names, passwords, emails) and API key (I will treat it as if it is paid, although I will just use a free API key).

  d. What functionality will your app include?

    - See answers to question 1, as they are detailed there.

  e. What will user flow look like?

    - User gets to landing page.  Is met with a ticker going by with all the cryptocurrencies supported on API.  This will list the benefits/features of creating an account, but basic information will not require an account to see.

    - If user logs in or creates an account, can favorite (or remove from favorite) and get more detailed information about whichever cryptocurrencies they favorite.  They can also change their information or delete their account if they want.

  f. What features make your site more than CRUD? Do you have any stretch goals?

    - Cryptocurrency guides, features, and other information will be static.  The stretch goals are bold and italic in answers 1 and 3.
