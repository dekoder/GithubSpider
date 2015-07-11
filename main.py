'''
Created on Jul 4, 2015

@author: Tommi Unruh
'''

from crawler import Crawler
import sys
import getopt

USAGE_ARGS = [
        ("ratelimit", "", "Show current rate limit"),
        ("links\t"    , "", "Crawl repository cloning links."),
#         ("-w", "--write", "Activate the custom logging function.\n"
#         "\t\t\t\tIf you do not specify your own custom logger, then the standard\n"
#         "\t\t\t\tcustom logger will be used. It creates HTML pages from the\n"
#         "\t\t\t\tvulnerability scanning results."),
        ("-q", "--query"  , "Specify a GitHub search query for the link " 
         "crawling.\n\t\t\t\tThe default value is \"language:PHP\""),
        ("-d", "--days", "(Necessary for 'crawlDays' command.)\n"
         "\t\t\t\tSpecify a start and end date for the link "
         "crawling\n\t\t\t\twhich respects the creation day of repositories.\n"
         "\t\t\t\tThe search query will be repeated for every day in [start, end].\n"
         "\t\t\t\tExample: -d '2015-05-15,2015-05-20' will\n"
         "\t\t\t\ttrigger search queries for five days."),
        ("-h", "--help"  , "Print this help."),
        ]

ARGS_RATELIMIT   = "ratelimit"
ARGS_GET_LINKS   = "get_links"
# ARGS_CRAWL_1000  = "crawl1000"
# ARGS_CRAWL_DAYS  = "crawlDays"
ARGS_CRAWL_REPOS = "repo_links"

def main(argv):
    """
    Entry point of execution. Handles program arguments and
    acts accordingly. 
    """
    crawler = Crawler()
    
    flow = controlFlow(argv)
    
    if flow[0] == ARGS_RATELIMIT:
        crawler.showRateLimit()
        
#     elif flow[0] == ARGS_CRAWL_1000:
#         if len(flow) == 2:
#             crawler.crawlSearching(flow[1])
#         else:
#             crawler.crawlSearching()
#     elif flow[0] == ARGS_CRAWL_DAYS:
#         if len(flow) == 4:
#             crawler.crawlSearchDays(flow[1], flow[2], flow[3])
#         else:
#             crawler.crawlSearchDays(flow[1], flow[2])
    elif flow[0] == ARGS_CRAWL_REPOS:
            if len(flow) == 3:
                crawler.crawlRepos(flow[1], flow[2])
            else:
                crawler.crawlRepos(flow[1])
    elif flow[0] == ARGS_GET_LINKS:
        crawler.transformCrawlDataToLinks(flow[1], flow[2])
            
def controlFlow(argv):
    """
    Handle command line arguments.
    """
    # argv[1] determines code control flow.
    if len(argv) < 2:
        usage(argv[0])
        sys.exit(0)
    
    query = None
    days  = None
    
    try:
        opts, _ = getopt.getopt(argv[2:], "hq:d:", ["help", "query=",
                                                    "days="])

    except getopt.GetoptError as err:
        print str(err)
        usage(argv[0])
        sys.exit(0)
    
    for o, v in opts:
        if o in (USAGE_ARGS[2][0], USAGE_ARGS[2][1]):
            if v:
                query = v
            else:
                usage(argv[0])
                sys.exit(0)
        
        # -d, --days
        elif o in(USAGE_ARGS[3][0], USAGE_ARGS[3][1]):
            v = v.replace(" ", "")
            days = v.split(",")
            if len(days) != 2:
                usage(argv[0])
                sys.exit(0)
        # -h, --help
        elif o in(USAGE_ARGS[-1][0], USAGE_ARGS[-1][1]):
            usage(argv[0])
            sys.exit(0)
        ## -i, --ignore
        #elif o in(USAGE_ARGS[1][0], USAGE_ARGS[1][1]):
        #    ignore_arg = v
    
    if argv[1] == ARGS_RATELIMIT:
        return [ARGS_RATELIMIT,]
#     elif argv[1] == ARGS_CRAWL_1000:
#         return [ARGS_CRAWL_1000, query] if query else [ARGS_CRAWL_1000,]
#     elif argv[1] == ARGS_CRAWL_DAYS:
#         if days:
#             return (
#                 [ARGS_CRAWL_DAYS, days[0], days[1], query] if query else 
#                 [ARGS_CRAWL_DAYS, days[0], days[1]]
#                  )
    elif argv[1] == ARGS_CRAWL_REPOS:
        if len(argv[2:]) == 1:
            return [ARGS_CRAWL_REPOS, argv[2]]
        
    elif argv[1] == ARGS_GET_LINKS:
        if len(argv[2:]) == 2:
            return [ARGS_GET_LINKS, argv[2], argv[3]]
        
    
    usage(argv[0])
    sys.exit(0)

def usage(path):
    """
    Prints help.
    """
    usage = "[%s/%s/%s/%s] <options>" % (
                                            ARGS_RATELIMIT, ARGS_CRAWL_1000,
                                            ARGS_CRAWL_DAYS, "-h"
                                            )
    
    # for each option available, construct its usage string
    for option, longoption, description in USAGE_ARGS:
        usage += "\n\t%s%s%s\t:\t%s\n" % (
                                    option, 
                                    ", " if longoption else "", 
                                    longoption, 
                                    description
                                    )

    slash_count = path.count("/")
    
    # shorten program path if necessary for readability
    if slash_count:        
        slash_index = path.rfind("/")
        
        if slash_count > 2:
            path = ".../" + path[slash_index+1:]
            
    print "Usage: " + path + " " + usage

if __name__ == '__main__':
    main(sys.argv)