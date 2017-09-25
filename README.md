Introduction
============================================

Goolag creates a web browser (through Selenium) with AdNauseum enabled which
randomly crawls a predefined list of websites. Browser behavior is governed
by Markov chain. At regular intervals, the browswer will either remain on a
webpage (example.com), visit a random page within a domain (example.com/news),
go to a different site (otherexample.com), or start a new browswer with
modified parameters, like the browser's user agent or proxy.

The basic theory behind operation is that Goolag traffic should appear as
close to real user traffic as possible. There should be no consistent patterns
of browser behavior which could make its traffic easily filtered. Thus, the
automated ad-clicking should be indistinguishable from authentic user traffic,
resulting in inflated metrics for advertising.

Ideally, Goolag is something you should be able to run while you're asleep or
away from home, giving you the smug satisfaction of sticking it to the corrupt
world of internet advertising. Currently, data from the "ad vault" is not
carried over from one session to the next, which means that you can't see the
total predicted costs of the clicks to advertisers for a long session or track
progress over the course of days. Adding this feature is a development priority,
so stay tuned. With default settings, a rural internet connection, and using the
TOR network, $3-15/minute of clicks were observed ($5/minute being about average).

Remember, "don't be evil."

Options
==============================================================================
Proxy
------------------------------------------------------------------------------
The -p option will cause the program to fetch a list of public proxies from
us-proxy.org. While there are some advantages to this approach over TOR in terms
of anonymity and randomizing behavior (TOR exit nodes are often on IP blacklists
for obvious reasons), the process of randomly selecting a proxies from this list
and validating that they support HTTP-CONNECT is very slow.

Tor
-------------------------------------------------------------------------------
The -t option will cause the program to connect through the TOR network using
default parameters (localhost:9050). You would need to run TOR before running
the program. The changes to performance are minimal. The irony of using an NSA-
funded "anonymity" network to exploit the profit model of company which heavily
overlaps with the 'intelligence community' is pretty funny.

Interval
-------------------------------------------------------------------------------
The -i option will set the amount of time it takes for each cycle (1 second default)

Crawling
-------------------------------------------------------------------------------
The -c option sets the maximum probability the program can set for crawling (as
expressed as a decimal value 0.0 - 0.99). Probabilities at run time are randomly
assigned to make traffic less regular, but larger values mean more frequent visits
to pages within a website.

Domain
-------------------------------------------------------------------------------
The -d option sets the maximum probability the program can set for changing
domains (site.com -> othersite.com). Only domains within the "Domains" file will
be read and used.

Reset
--------------------------------------------------------------------------------
The -r option sets the maximum probability the program can set for restarting the
browser with new parameters. All cookies, cache and history are lost in the process
and a random user agent is selected. If the option is selected, proxies will be
randomly tested until a viable one is found.