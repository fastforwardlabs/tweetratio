import analysis
import tqdm
import tweetratio

senators = ["SenShelby", "lutherstrange", "lisamurkowski", "SenDanSullivan",
            "SenJohnMcCain", "JeffFlake", "JohnBoozman", "SenTomCotton",
            "SenFeinstein", "SenKamalaHarris", "SenBennetCO", "SenCoryGardner",
            "SenBlumenthal", "ChrisMurphyCT", "SenatorCarper", "ChrisCoons",
            "SenBillNelson", "marcorubio", "sendavidperdue", "SenatorIsakson",
            "SenBrianSchatz", "maziehirono", "MikeCrapo", "SenatorRisch",
            "SenatorDurbin", "SenDuckworth", "SenDonnelly", "SenToddYoung",
            "ChuckGrassley", "joniernst", "SenPatRoberts", "JerryMoran",
            "SenateMajLdr", "SenRandPaul", "BillCassidy", "SenJohnKennedy",
            "SenatorCollins", "SenAngusKing", "SenatorCardin",
            "ChrisVanHollen", "SenWarren", "senmarkey", "SenStabenow",
            "SenGaryPeters", "amyklobuchar", "alfranken", "SenThadCochran",
            "SenatorWicker", "clairemc", "RoyBlunt", "SenatorTester",
            "SteveDaines", "SenatorFischer", "BenSasse", "SenDeanHeller",
            "CatherineForNV", "SenatorShaheen", "SenatorHassan",
            "SenatorMenendez", "CoryBooker", "SenatorTomUdall",
            "MartinHeinrich", "SenSchumer", "SenGillibrand", "SenatorBurr",
            "ThomTillis", "SenJohnHoeven", "SenatorHeitkamp",
            "SenSherrodBrown", "ropbportman", "JimInhofe", "SenatorLankford",
            "RonWyden", "SenJeffMerkley", "SenBobCasey", "SenToomey",
            "SenJackReed", "SenWhitehouse", "LindseyGrahamSC",
            "SenatorTimScott", "SenJohnThune", "SenatorRounds", "SenAlexander",
            "SenBobCorker", "JohnCornyn", "SenTedCruz", "SenOrrinHatch",
            "SenMikeLee", "SenatorLeahy", "SenatorSanders", "timkaine",
            "MarkWarner", "PattyMurray", "SenatorCantwell", "SenCapito",
            "Sen_JoeManchin", "SenatorBaldwin", "SenRonJohnson",
            "SenJohnBarrasso", "SenatorEnzi"]


def write_csv(df, fname, keep=None):
    if keep is None:
        keep = ['created_at', 'text', 'user', 'retweet_count',
                'favorite_count', 'reply_count']
    df[keep].to_csv(fname)


if __name__ == '__main__':
    for senator in tqdm.tqdm(senators[:2]):
        tweetratio.get_and_save_user(senator)
        tweets = analysis.load_json(f'raw/{senator}')
        df = analysis.tweets_to_df(tweets)
        write_csv(df, f'csv/{senator}.csv')
