KEYWORDS = ["software", "developer", "engineer", "sde", "backend", "fullstack", "frontend"]
LOCATIONS = ["india", "ind", "bengaluru", "hyderabad", "bangalore", "pune", "chennai", "mumbai"]


COMPANY_RULES = {

    "jpmorgan": {
        "exclude_titles": ["lead", "manager", "iii"],
        "limit": 20
    },

    "oracle": {
        "exclude_titles": ["manager", "4", "director", "staff", "principal", "consultant", "reliability"],
        "limit": 20
    },

    "qualcomm": {
        "exclude_titles": ["staff", "lead"],
        "limit": 20
    },

    "salesforce": {
        "include_titles": ["mts", "smts"],
        "exclude_titles": ["architect", "pmts", "manager"],
        "limit": 20
    },

    "goldmansachs": {
        "include_titles": ["associate", "analyst"],
        "limit": 20
    },

    "paypal": {
        "exclude_titles": ["manager", "staff"],
        "limit": 20
    },

    "visa": {
        "exclude_titles": ["staff", "manager", "consultant", "lead"],   
        "limit": 20 
    },

    "wells_fargo": {
        "exclude_titles": ["manager", "lead", "director"],
        "limit": 20
    },

    "morgan_stanley": {
        "exclude_titles": ["director", "manager", "lead", "vice president"],
        "limit": 20
    }

}


def company_filter(company, title, location):

    rules = COMPANY_RULES.get(company, {})

    title = title.lower()
    location = location.lower().strip()

    keyword_match = any(k in title for k in KEYWORDS)
    location_match = any(loc in location for loc in LOCATIONS)

    # include rule
    if "include_titles" in rules:
        if not any(x in title for x in rules["include_titles"]):
            return False

    # exclude rule
    if "exclude_titles" in rules:
        if any(x in title for x in rules["exclude_titles"]):
            return False

    return keyword_match and location_match

# def amazon_filter(title, location):

#     title = title.lower()
#     location = location.lower().strip()

#     keyword_match = any(k in title for k in KEYWORDS)

#     country_code = location.split(",")[0].strip()

#     location_match = country_code in LOCATIONS

#     return keyword_match and location_match


# def microsoft_filter(title, location):

#     title = title.lower()
#     location = location.lower().strip()

#     keyword_match = any(k in title for k in KEYWORDS)

#     country_code = location.split(",")[0].strip()

#     location_match = country_code in LOCATIONS

#     return keyword_match and location_match


# def visa_filter(title, location):

#     title = title.lower()
#     location = location.lower().strip()

#     keyword_match = any(k in title for k in KEYWORDS)

#     # staff, manager, consultant, lead not allowed in title
#     # write code
#     keyword_match = keyword_match and not any(x in title for x in ["staff", "manager", "consultant", "lead"])

#     country_code = location.split(",")[0].strip()

#     location_match = country_code in LOCATIONS

#     return keyword_match and location_match