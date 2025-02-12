"""
<Cyber Threat Intelligence Relevance and Actionability Quality Metrics Implementation.>
    Copyright (C) 2025  Georgios Sakellariou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
INDUSTRIES = {0: 'abrasives and nonmetallic minerals manufacturing', 1: 'accessible architecture and design',
              2: 'accessible hardware manufacturing', 3: 'accommodation and food services', 4: 'accounting',
              5: 'administration of justice', 6: 'administrative and support services', 7: 'advertising services',
              8: 'agricultural chemical manufacturing', 9: 'agriculture, construction, mining machinery manufacturing',
              10: 'air, water, and waste program management', 11: 'airlines and aviation',
              12: 'alternative dispute resolution', 13: 'alternative fuel vehicle manufacturing',
              14: 'alternative medicine', 15: 'ambulance services', 16: 'amusement parks and arcades',
              17: 'animal feed manufacturing', 18: 'animation', 19: 'animation and post-production',
              20: 'apparel & fashion', 21: 'apparel manufacturing',
              22: 'appliances, electrical, and electronics manufacturing',
              23: 'architectural and structural metal manufacturing', 24: 'architecture and planning',
              25: 'armed forces', 26: 'artificial rubber and synthetic fiber manufacturing', 27: 'artists and writers',
              28: 'arts & crafts', 29: 'assurances', 30: 'audio and video equipment manufacturing',
              31: 'automation machinery manufacturing', 32: 'automotive', 33: 'aviation & aerospace',
              34: 'aviation and aerospace component manufacturing', 35: 'baked goods manufacturing', 36: 'banking',
              37: 'bars, taverns, and nightclubs', 38: 'bed-and-breakfasts, hostels, homestays',
              39: 'beverage manufacturing', 40: 'biomass electric power generation', 41: 'biotechnology',
              42: 'biotechnology research', 43: 'blockchain services', 44: 'blogs',
              45: 'boilers, tanks, and shipping container manufacturing', 46: 'book and periodical publishing',
              47: 'book publishing', 48: 'breweries', 49: 'broadcast media production and distribution',
              50: 'building construction', 51: 'building equipment contractors', 52: 'building finishing contractors',
              53: 'building materials', 54: 'building structure and exterior contractors',
              55: 'business consulting and services', 56: 'business content', 57: 'business intelligence platforms',
              58: 'business supplies & equipment', 59: 'cable and satellite programming', 60: 'capital markets',
              61: 'caterers', 62: 'chemical manufacturing', 63: 'chemical raw materials manufacturing',
              64: 'child day care services', 65: 'chiropractors', 66: 'circuses and magic shows',
              67: 'civic and social organizations', 68: 'civil engineering', 69: 'claims adjusting, actuarial services',
              70: 'clay and refractory products manufacturing', 71: 'climate data and analytics',
              72: 'climate technology product manufacturing', 73: 'coal mining', 74: 'collection agencies',
              75: 'commercial and industrial equipment rental', 76: 'commercial and industrial machinery maintenance',
              77: 'commercial and service industry machinery manufacturing', 78: 'commercial real estate',
              79: 'communications equipment manufacturing', 80: 'community development and urban planning',
              81: 'community services', 82: 'computer and network security', 83: 'computer games',
              84: 'computer hardware', 85: 'computer hardware manufacturing', 86: 'computer networking',
              87: 'computer networking products', 88: 'computers and electronics manufacturing',
              89: 'conservation programs', 90: 'construction', 91: 'construction hardware manufacturing',
              92: 'consumer electronics', 93: 'consumer goods', 94: 'consumer goods rental', 95: 'consumer services',
              96: 'correctional institutions', 97: 'cosmetics', 98: 'cosmetology and barber schools',
              99: 'courts of law', 100: 'credit intermediation', 101: 'cutlery and handtool manufacturing',
              102: 'dairy', 103: 'dairy product manufacturing', 104: 'dance companies',
              105: 'data infrastructure and analytics', 106: 'data security software products', 107: 'defense & space',
              108: 'defense and space manufacturing', 109: 'dentists', 110: 'design', 111: 'design services',
              112: 'desktop computing software products', 113: 'digital accessibility services', 114: 'distilleries',
              115: 'e-learning', 116: 'e-learning providers', 117: 'economic programs', 118: 'education',
              119: 'education administration programs', 120: 'education management',
              121: 'electric lighting equipment manufacturing', 122: 'electric power generation',
              123: 'electric power transmission, control, and distribution', 124: 'electrical equipment manufacturing',
              125: 'electronic and precision equipment maintenance', 126: 'embedded software products',
              127: 'emergency and relief services', 128: 'engineering services',
              129: 'engines and power transmission equipment manufacturing', 130: 'entertainment',
              131: 'entertainment providers', 132: 'environmental quality programs', 133: 'environmental services',
              134: 'equipment rental services', 135: 'events services', 136: 'executive offices',
              137: 'executive search services', 138: 'fabricated metal products',
              139: 'fabrication de véhicules à moteur', 140: 'facilities services', 141: 'family planning centers',
              142: 'farming', 143: 'farming, ranching, forestry', 144: 'fashion accessories manufacturing',
              145: 'financial services', 146: 'fine art', 147: 'fine arts schools', 148: 'fire protection',
              149: 'fisheries', 150: 'flight training', 151: 'food & beverages', 152: 'food and beverage manufacturing',
              153: 'food and beverage retail', 154: 'food and beverage services', 155: 'food production',
              156: 'footwear and leather goods repair', 157: 'footwear manufacturing', 158: 'forestry and logging',
              159: 'fossil fuel electric power generation', 160: 'freight and package transportation',
              161: 'fruit and vegetable preserves manufacturing', 162: 'fuel cell manufacturing', 163: 'fundraising',
              164: 'funds and trusts', 165: 'furniture', 166: 'furniture and home furnishings manufacturing',
              167: 'gambling facilities and casinos', 168: 'geothermal electric power generation',
              169: 'glass product manufacturing', 170: 'glass, ceramics and concrete manufacturing',
              171: 'golf courses and country clubs', 172: 'government administration', 173: 'government relations',
              174: 'government relations services', 175: 'graphic design', 176: 'ground passenger transportation',
              177: 'health and human services', 178: 'health, wellness & fitness', 179: 'higher education',
              180: 'highway, street, and bridge construction', 181: 'historical sites', 182: 'holding companies',
              183: 'home health care services', 184: 'horticulture', 185: 'hospitality', 186: 'hospitals',
              187: 'hospitals and health care', 188: 'hotels and motels',
              189: 'household and institutional furniture manufacturing', 190: 'household appliance manufacturing',
              191: 'household services', 192: 'housing and community development', 193: 'housing programs',
              194: 'human resources', 195: 'human resources services',
              196: 'hvac and refrigeration equipment manufacturing', 197: 'hydroelectric power generation',
              198: 'import & export', 199: 'individual and family services', 200: 'industrial automation',
              201: 'industrial machinery manufacturing', 202: 'industry associations', 203: 'information services',
              204: 'information technology & services', 205: 'information technology and services', 206: 'insurance',
              207: 'insurance agencies and brokerages', 208: 'insurance and employee benefit funds',
              209: 'insurance carriers', 210: 'interior design', 211: 'international affairs',
              212: 'international trade and development', 213: 'internet marketplace platforms', 214: 'internet news',
              215: 'internet publishing', 216: 'interurban and rural bus services', 217: 'investment advice',
              218: 'investment banking', 219: 'investment management', 220: 'it services and it consulting',
              221: 'it system custom software development', 222: 'it system data services',
              223: 'it system design services', 224: 'it system installation and disposal',
              225: 'it system operations and maintenance', 226: 'it system testing and evaluation',
              227: 'it system training and support', 228: 'janitorial services', 229: 'landscaping services',
              230: 'language schools', 231: 'laundry and drycleaning services', 232: 'law enforcement',
              233: 'law practice', 234: 'leasing non-residential real estate', 235: 'leasing residential real estate',
              236: 'leather product manufacturing', 237: 'legal services', 238: 'legislative offices',
              239: 'leisure, travel & tourism', 240: 'libraries', 241: 'lime and gypsum products manufacturing',
              242: 'loan brokers', 243: 'luxury goods & jewelry', 244: 'machinery manufacturing',
              245: 'magnetic and optical media manufacturing', 246: 'manufacturing', 247: 'maritime',
              248: 'maritime transportation', 249: 'market research', 250: 'marketing services',
              251: 'mattress and blinds manufacturing', 252: 'measuring and control instrument manufacturing',
              253: 'meat products manufacturing', 254: 'mechanical or industrial engineering',
              255: 'media and telecommunications', 256: 'media production', 257: 'medical and diagnostic laboratories',
              258: 'medical device', 259: 'medical equipment manufacturing', 260: 'medical practices',
              261: 'mental health care', 262: 'metal ore mining', 263: 'metal treatments',
              264: 'metal valve, ball, and roller manufacturing', 265: 'metalworking machinery manufacturing',
              266: 'military and international affairs', 267: 'mining', 268: 'mobile computing software products',
              269: 'mobile food services', 270: 'mobile gaming apps', 271: 'motor vehicle manufacturing',
              272: 'motor vehicle parts manufacturing', 273: 'movies and sound recording',
              274: 'movies, videos, and sound', 275: 'museums', 276: 'museums, historical sites, and zoos',
              277: 'music', 278: 'musicians', 279: 'nanotechnology research', 280: 'natural gas distribution',
              281: 'natural gas extraction', 282: 'newspaper publishing', 283: 'non-profit organization management',
              284: 'non-profit organizations', 285: 'nonmetallic mineral mining',
              286: 'nonresidential building construction', 287: 'nuclear electric power generation',
              288: 'nursing homes and residential care facilities', 289: 'office administration',
              290: 'office furniture and fixtures manufacturing', 291: 'oil and coal product manufacturing',
              292: 'oil and gas', 293: 'oil extraction', 294: 'oil, gas, and mining',
              295: 'online and mail order retail', 296: 'online audio and video media', 297: 'online media',
              298: 'operations consulting', 299: 'optometrists', 300: 'outpatient care centers',
              301: 'outsourcing and offshoring consulting', 302: 'outsourcing/offshoring',
              303: 'packaging & containers', 304: 'packaging and containers manufacturing',
              305: 'paint, coating, and adhesive manufacturing', 306: 'paper & forest products',
              307: 'paper and forest product manufacturing', 308: 'pension funds', 309: 'performing arts',
              310: 'performing arts and spectator sports', 311: 'periodical publishing',
              312: 'personal and laundry services', 313: 'personal care product manufacturing',
              314: 'personal care services', 315: 'pet services', 316: 'pharmaceutical manufacturing',
              317: 'philanthropic fundraising services', 318: 'philanthropy', 319: 'photography',
              320: 'physical, occupational and speech therapists', 321: 'physicians', 322: 'pipeline transportation',
              323: 'plastics and rubber product manufacturing', 324: 'plastics manufacturing',
              325: 'political organizations', 326: 'postal services', 327: 'primary and secondary education',
              328: 'primary metal manufacturing', 329: 'printing services', 330: 'professional organizations',
              331: 'professional services', 332: 'professional training and coaching', 333: 'program development',
              334: 'public assistance programs', 335: 'public health', 336: 'public policy',
              337: 'public policy offices', 338: 'public relations and communications services', 339: 'public safety',
              340: 'racetracks', 341: 'radio and television broadcasting', 342: 'rail transportation',
              343: 'railroad equipment manufacturing', 344: 'ranching', 345: 'ranching and fisheries',
              346: 'real estate', 347: 'real estate agents and brokers',
              348: 'real estate and equipment rental services', 349: 'recreational facilities',
              350: 'regenerative design', 351: 'religious institutions',
              352: 'renewable energy equipment manufacturing', 353: 'renewable energy power generation',
              354: 'renewable energy semiconductor manufacturing', 355: 'renewables & environment',
              356: 'repair and maintenance', 357: 'research', 358: 'research services',
              359: 'residential building construction', 360: 'restaurants', 361: 'retail',
              362: 'retail apparel and fashion', 363: 'retail appliances, electrical, and electronic equipment',
              364: 'retail art dealers', 365: 'retail art supplies', 366: 'retail books and printed news',
              367: 'retail building materials and garden equipment', 368: 'retail florists',
              369: 'retail furniture and home furnishings', 370: 'retail gasoline', 371: 'retail groceries',
              372: 'retail health and personal care products', 373: 'retail luxury goods and jewelry',
              374: 'retail motor vehicles', 375: 'retail musical instruments', 376: 'retail office equipment',
              377: 'retail office supplies and gifts', 378: 'retail pharmacies',
              379: 'retail recyclable materials & used merchandise', 380: 'reupholstery and furniture repair',
              381: 'robot manufacturing', 382: 'robotics engineering', 383: 'rubber products manufacturing',
              384: 'satellite telecommunications', 385: 'savings institutions', 386: 'school and employee bus services',
              387: 'seafood product manufacturing', 388: 'secretarial schools',
              389: 'securities and commodity exchanges', 390: 'security and investigations',
              391: 'security guards and patrol services', 392: 'security systems services', 393: 'seguros',
              394: 'semiconductor manufacturing', 395: 'semiconductors', 396: 'services for renewable energy',
              397: 'services for the elderly and disabled', 398: 'serviços e consultoria de ti',
              399: 'sheet music publishing', 400: 'shipbuilding',
              401: 'shuttles and special needs transportation services', 402: 'sightseeing transportation',
              403: 'skiing facilities', 404: 'smart meter manufacturing',
              405: 'soap and cleaning product manufacturing', 406: 'social networking platforms',
              407: 'software development', 408: 'solar electric power generation', 409: 'sound recording',
              410: 'space research and technology', 411: 'specialty trade contractors', 412: 'spectator sports',
              413: 'sporting goods', 414: 'sporting goods manufacturing', 415: 'sports and recreation instruction',
              416: 'sports teams and clubs', 417: 'spring and wire product manufacturing',
              418: 'staffing and recruiting', 419: 'steam and air-conditioning supply',
              420: 'strategic management services', 421: 'subdivision of land',
              422: 'sugar and confectionery product manufacturing', 423: 'surveying and mapping services',
              424: 'taxi and limousine services', 425: 'technical and vocational training',
              426: 'technology, information and internet', 427: 'technology, information and media',
              428: 'telecommunications', 429: 'telecommunications carriers', 430: 'telephone call centers',
              431: 'temporary help services', 432: 'textile manufacturing', 433: 'theater companies',
              434: 'think tanks', 435: 'tobacco', 436: 'tobacco manufacturing', 437: 'translation and localization',
              438: 'transportation equipment manufacturing', 439: 'transportation programs',
              440: 'transportation, logistics, supply chain and storage', 441: 'transportation/trucking/railroad',
              442: 'travel arrangements', 443: 'truck transportation', 444: 'trusts and estates',
              445: 'turned products and fastener manufacturing', 446: 'urban transit services', 447: 'utilities',
              448: 'utilities administration', 449: 'utility system construction',
              450: 'vehicle repair and maintenance', 451: 'venture capital and private equity principals',
              452: 'veterinary', 453: 'veterinary services', 454: 'vocational rehabilitation services',
              455: 'warehousing', 456: 'warehousing and storage', 457: 'waste collection',
              458: 'waste treatment and disposal', 459: 'water supply and irrigation systems',
              460: 'water, waste, steam, and air conditioning services', 461: 'wellness and fitness services',
              462: 'wholesale', 463: 'wholesale alcoholic beverages', 464: 'wholesale apparel and sewing supplies',
              465: 'wholesale appliances, electrical, and electronics', 466: 'wholesale building materials',
              467: 'wholesale chemical and allied products', 468: 'wholesale computer equipment',
              469: 'wholesale drugs and sundries', 470: 'wholesale food and beverage', 471: 'wholesale footwear',
              472: 'wholesale furniture and home furnishings', 473: 'wholesale hardware, plumbing, heating equipment',
              474: 'wholesale import and export', 475: 'wholesale luxury goods and jewelry', 476: 'wholesale machinery',
              477: 'wholesale metals and minerals', 478: 'wholesale motor vehicles and parts',
              479: 'wholesale paper products', 480: 'wholesale petroleum and petroleum products',
              481: 'wholesale photography equipment and supplies', 482: 'wholesale raw farm products',
              483: 'wholesale recyclable materials', 484: 'wind electric power generation', 485: 'wine & spirits',
              486: 'wineries', 487: 'wireless services', 488: "women's handbag manufacturing",
              489: 'wood product manufacturing', 490: 'writing and editing', 491: 'zoos and botanical gardens'}
