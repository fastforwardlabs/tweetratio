import analysis
import tweetratio
import logging

from tweepy.error import TweepError

senators = [
    "SenShelby", "lutherstrange", "lisamurkowski", "SenDanSullivan",
    "SenJohnMcCain", "JeffFlake", "JohnBoozman", "SenTomCotton",
    "SenFeinstein", "SenKamalaHarris", "SenBennetCO", "SenCoryGardner",
    "SenBlumenthal", "ChrisMurphyCT", "SenatorCarper", "ChrisCoons",
    "SenBillNelson", "marcorubio", "sendavidperdue", "SenatorIsakson",
    "SenBrianSchatz", "maziehirono", "MikeCrapo", "SenatorRisch",
    "SenatorDurbin", "SenDuckworth", "SenDonnelly", "SenToddYoung",
    "ChuckGrassley", "joniernst", "SenPatRoberts", "JerryMoran",
    "SenateMajLdr", "RandPaul", "BillCassidy", "SenJohnKennedy",
    "SenatorCollins", "SenAngusKing", "SenatorCardin", "ChrisVanHollen",
    "SenWarren", "senmarkey", "SenStabenow", "SenGaryPeters", "amyklobuchar",
    "alfranken", "SenThadCochran", "SenatorWicker", "clairecmc", "RoyBlunt",
    "SenatorTester", "SteveDaines", "SenatorFischer", "BenSasse",
    "SenDeanHeller", "CatherineForNV", "SenatorShaheen", "SenatorHassan",
    "SenatorMenendez", "CoryBooker", "SenatorTomUdall", "MartinHeinrich",
    "SenSchumer", "SenGillibrand", "SenatorBurr", "ThomTillis",
    "SenJohnHoeven", "SenatorHeitkamp", "SenSherrodBrown", "robportman",
    "JimInhofe", "SenatorLankford", "RonWyden", "SenJeffMerkley",
    "SenBobCasey", "SenToomey", "SenJackReed", "SenWhitehouse",
    "LindseyGrahamSC", "SenatorTimScott", "SenJohnThune", "SenatorRounds",
    "SenAlexander", "SenBobCorker", "JohnCornyn", "SenTedCruz",
    "SenOrrinHatch", "SenMikeLee", "SenatorLeahy", "SenSanders",
    "timkaine", "MarkWarner", "PattyMurray", "SenatorCantwell", "SenCapito",
    "Sen_JoeManchin", "SenatorBaldwin", "SenRonJohnson", "SenJohnBarrasso",
    "SenatorEnzi", "BernieSanders"
]


def missing():
    '''Check for senators that have not been fully downloaded.'''
    for i, senator in enumerate(senators, 1):
        try:
            tweets = tweetratio.load_json(f'raw/{senator}.json')
            missing = len(tweets) - tweetratio.count_reply_counts(tweets)
            if missing:
                print(f'{senator}: {missing} reply_counts')
        except FileNotFoundError:
            print(f'{senator}: unscraped')


if __name__ == '__main__':
    for i, senator in enumerate(senators, 1):
        print(f'{i}/{len(senators)}: {senator}')
        try:
            tweets = tweetratio.get_user(senator, rescrape=False, save=True)
            analysis.process(senator, min_year='1970', min_retweet_count=0)
        except TweepError as e:
            logging.exception(senator)
            pass
