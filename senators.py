import tweetratio
import logging

from tweepy.error import TweepError

logging.basicConfig(filename='log.log', level=logging.INFO,
                    format='%(levelname)s:%(asctime)s:%(message)s')

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
    "alfranken", "SenThadCochran", "SenatorWicker", "clairemc", "RoyBlunt",
    "SenatorTester", "SteveDaines", "SenatorFischer", "BenSasse",
    "SenDeanHeller", "CatherineForNV", "SenatorShaheen", "SenatorHassan",
    "SenatorMenendez", "CoryBooker", "SenatorTomUdall", "MartinHeinrich",
    "SenSchumer", "SenGillibrand", "SenatorBurr", "ThomTillis",
    "SenJohnHoeven", "SenatorHeitkamp", "SenSherrodBrown", "ropbportman",
    "JimInhofe", "SenatorLankford", "RonWyden", "SenJeffMerkley",
    "SenBobCasey", "SenToomey", "SenJackReed", "SenWhitehouse",
    "LindseyGrahamSC", "SenatorTimScott", "SenJohnThune", "SenatorRounds",
    "SenAlexander", "SenBobCorker", "JohnCornyn", "SenTedCruz",
    "SenOrrinHatch", "SenMikeLee", "SenatorLeahy", "SenatorSanders",
    "timkaine", "MarkWarner", "PattyMurray", "SenatorCantwell", "SenCapito",
    "Sen_JoeManchin", "SenatorBaldwin", "SenRonJohnson", "SenJohnBarrasso",
    "SenatorEnzi"
]


if __name__ == '__main__':
    for i, senator in enumerate(senators, 1):
        print(f'{i}/{len(senators)}: {senator}')
        try:
            tweets = tweetratio.get_user(senator, rescrape=False, save=True)
        except TweepError as e:
            logging.exception(senator)
            pass
