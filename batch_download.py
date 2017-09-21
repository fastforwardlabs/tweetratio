import analysis
import tweetratio
import logging

from tweepy.error import TweepError

# users = [
#     "SenShelby", "lutherstrange", "lisamurkowski", "SenDanSullivan",
#     "SenJohnMcCain", "JeffFlake", "JohnBoozman", "SenTomCotton",
#     "SenFeinstein", "SenKamalaHarris", "SenBennetCO", "SenCoryGardner",
#     "SenBlumenthal", "ChrisMurphyCT", "SenatorCarper", "ChrisCoons",
#     "SenBillNelson", "marcorubio", "sendavidperdue", "SenatorIsakson",
#     "SenBrianSchatz", "maziehirono", "MikeCrapo", "SenatorRisch",
#     "SenatorDurbin", "SenDuckworth", "SenDonnelly", "SenToddYoung",
#     "ChuckGrassley", "joniernst", "SenPatRoberts", "JerryMoran",
#     "SenateMajLdr", "RandPaul", "BillCassidy", "SenJohnKennedy",
#     "SenatorCollins", "SenAngusKing", "SenatorCardin", "ChrisVanHollen",
#     "SenWarren", "senmarkey", "SenStabenow", "SenGaryPeters", "amyklobuchar",
#     "alfranken", "SenThadCochran", "SenatorWicker", "clairecmc", "RoyBlunt",
#     "SenatorTester", "SteveDaines", "SenatorFischer", "BenSasse",
#     "SenDeanHeller", "CatherineForNV", "SenatorShaheen", "SenatorHassan",
#     "SenatorMenendez", "CoryBooker", "SenatorTomUdall", "MartinHeinrich",
#     "SenSchumer", "SenGillibrand", "SenatorBurr", "ThomTillis",
#     "SenJohnHoeven", "SenatorHeitkamp", "SenSherrodBrown", "robportman",
#     "JimInhofe", "SenatorLankford", "RonWyden", "SenJeffMerkley",
#     "SenBobCasey", "SenToomey", "SenJackReed", "SenWhitehouse",
#     "LindseyGrahamSC", "SenatorTimScott", "SenJohnThune", "SenatorRounds",
#     "SenAlexander", "SenBobCorker", "JohnCornyn", "SenTedCruz",
#     "SenOrrinHatch", "SenMikeLee", "SenatorLeahy", "SenSanders",
#     "timkaine", "MarkWarner", "PattyMurray", "SenatorCantwell", "SenCapito",
#     "Sen_JoeManchin", "SenatorBaldwin", "SenRonJohnson", "SenJohnBarrasso",
#     "SenatorEnzi", "BernieSanders"
# ]

# users = [
#     "JoyAnnReid", "CillizzaCNN", "ananavarro", "judgejeanine", "mattyglesias",
#     "MeghanMcCain", "davidfrum", "jonathanchait", "cher"
# ]

users = ["SpeakerRyan", "jimmykimmel", "kamalaharris", "SenWarren",
         "berniesanders", "BillCassidy", "realDonaldTrump", "lindseygrahamsc",
         "SenateMajLdr"]


def missing(users=users):
    '''Check for users that have not been fully downloaded.'''
    for i, user in enumerate(users, 1):
        try:
            tweets = tweetratio.load_json(f'raw/{user}.json')
            missing = len(tweets) - tweetratio.count_reply_counts(tweets)
            if missing:
                print(f'{user}: {missing} reply_counts')
        except FileNotFoundError:
            print(f'{user}: unscraped')


if __name__ == '__main__':
    for i, user in enumerate(users, 1):
        print(f'{i}/{len(users)}: {user}')
        try:
            tweets = tweetratio.get_user(user, rescrape=False, save=True)
            analysis.process(user, min_year='1970', min_retweet_count=0)
        except TweepError as e:
            logging.exception(user)
            pass
