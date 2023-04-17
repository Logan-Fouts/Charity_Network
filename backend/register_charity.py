import textrazor
import pickle
import mysql.connector
import secrets

# Setup textrazor API.
textrazor.api_key = secrets.API_KEY

client = textrazor.TextRazor(extractors=["entities", "topics"])
client.set_cleanup_mode("cleanHTML")
client.set_classifiers(["textrazor_newscodes"])

def get_tags(charity):
    """
    Finds relavent tags fron desired charity website. Uses textrazor API.

    Requires: 
        charity(Array with charity details[name, description, url])
    """
    response = client.analyze_url(charity[2])
    entities = list(response.entities())
    entities.sort(key=lambda x: x.relevance_score, reverse=True)
    tmp = []
    for topic in response.topics():
        if topic.score > .9:
            tag = topic.label
            tmp.append(tag)
    charity.append(tmp)
    return charity

def sql_POST(charity):
    """
    Inserts an element into mysql db.

    Requires: 
        charity(Array with charity details[name, description, url, tags])
    """
    cnx = mysql.connector.connect(
        host=secrets.MYSQL_HOST,
        user=secrets.MYSQL_USER,
        password=secrets.MYSQL_PASSWORD,
        database=secrets.MYSQL_DATABASE
    )

    cursor = cnx.cursor()
    query = "INSERT INTO `charities`(`name`, `description`, `url`, `tags`) VALUES (%s, %s, %s, %s)"
    data = (str(charity[0]), str(charity[1]), str(charity[2]), str(charity[3]))
    cursor.execute(query, data)
    cnx.commit()

    cursor.close()
    cnx.close()

def sql_GET():
    """
    Returns all elements from the mysql db.
    """
    cnx = mysql.connector.connect(
        host=secrets.MYSQL_HOST,
        user=secrets.MYSQL_USER,
        password=secrets.MYSQL_PASSWORD,
        database=secrets.MYSQL_DATABASE
    )

    cursor = cnx.cursor()
    query = "SELECT * FROM `charities`"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    return rows


############################ Temp Stuff Below ############################
# def sql_POST(array):
#     with open('backend/db.txt', 'ab') as file:
#         pickle.dump(array, file)

# def sql_GET():
#     arrays = []
#     with open('backend/db.txt', 'rb') as file:
#         while True:
#             try:
#                 array = pickle.load(file)
#                 arrays.append(array)
#             except EOFError:
#                 break
#     return arrays

# test_charity1 = ['Dog Helper', 'Help Save Dogs From Abusive Homes', 'https://www.dogstrust.org.uk/']
# test_charity2 = ['Alley Cat Allies', 'Rescue Cats in Need of Homes', 'https://www.alleycat.org/']
# test_charity3 = ['NAACP Legal Defense and Educational Fund', 'To support litigation in the areas of poverty and justice, education, voting rights, fair employment, capital punishment, administration of criminal justice, and to increase educational opportunities through scholarships.', 'https://www.naacpldf.org/']
# test_charity4 = ['Learning Ally', 'Dedicated to equipping educators with proven solutions that help struggling learners to reach their potential.', 'https://www.learningally.org/']
# test_charity5 = ['Cancer Research Foundation', 'Fund Research to Find a Cure for Cancer', 'https://www.cancerresearchfoundation.org/']
# test_charity6 = ['Arts Education Foundation', 'Support Arts Education and Access to the Arts', 'https://www.artseducationfoundation.org/']
# test_charity7 = ['Hunger Relief Organization', 'Combat Hunger and Food Insecurity', 'https://www.hungerrelieforganization.org/']
# test_charity8 = ['Reach Out and Read, Inc', 'To give young children a foundation for success by incorporating books into pediatric care and encouraging families to read aloud together.', 'https://www.reachoutandread.org/']
# test_charity9 = ['Alzheimers Association', 'To eliminate Alzheimers disease through the advancement of research; provide & enhance care & support for all affected; & reduce the risk of dementia through the promotion of brain health.', 'https://www.alz.org/']
# test_charity10 = ['Action on Smoking and Health', 'To advocate for innovative legal & policy measures to end the global tobacco epidemic.', 'https://www.ash.org/']
# test_charity11 = ['Ducks Unlimited', 'Conserves, restores, and manages wetlands and associated habitats for North Americas waterfowl.', 'https://www.ducks.org/']
# test_charity12 = ['Crohns & Colitis Foundation', 'To cure Crohns disease and ulcerative colitis, and to improve the quality of life of children and adults affected by these diseases.', 'https://www.crohnscolitisfoundation.org/']
# test_charity13 = ['Hispanic Federation', 'To empower and advance the Hispanic community.', 'https://www.hispanicfederation.org/']
# test_charity14 = ['Coalition for the Homeless', 'Nations oldest advocacy and direct service organization helping homeless men, women & children; believes that affordable housing, sufficient food, and the chance to work for a living wage are fundamental rights in a civilized society.', 'https://www.coalitionforthehomeless.org/']
# test_charity15 = ['Human Rights First', 'To empower Americans to work for justice in our own communities and around the world.', 'https://www.humanrightsfirst.org/']
# test_charity16 = ['Good360', 'To close the need gap by partnering with socially responsible companies to source highly needed donated goods and distribute them through our network of diverse nonprofits.', 'https://www.good360.org/']
# test_charity17 = ['Bread for the World Institute', 'To provide analysis and education on hunger issues in the U.S. and around the world.', 'https://www.bread.org/']
# test_charity18 = ['The Hunger Project', 'To end hunger and poverty by pioneering sustainable, grassroots, women-centered strategies and advocating for their widespread adoption in countries throughout the world.', 'https://www.thp.org/']
# test_charity19 = ['All Hands and Hearts', 'All Hands and Hearts provides community-inspired, volunteer-powered disaster relief.', 'https://www.allhandsandhearts.org/']
# test_charity20 = ['charity: water', 'To bring clean and safe drinking water to people in developing countries.', 'https://www.charitywater.org/']

# charities = [test_charity1, test_charity2, test_charity3, test_charity4, test_charity5, test_charity6, test_charity7, test_charity8, test_charity9, test_charity10, test_charity11, test_charity12, test_charity13, test_charity14, test_charity15, test_charity16, test_charity17, test_charity18, test_charity19, test_charity20]

# for charity in charities:
#     tmp = get_tags(charity)
#     sql_POST(tmp)