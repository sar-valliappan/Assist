import json
import time
import urllib
import urllib.request
import ssl
import certifi

context = ssl.create_default_context(cafile=certifi.where())

origin_acronym = input("Receiving institution (type acronym): ")
origin_acronym = origin_acronym.strip().upper()

with urllib.request.urlopen(
        "https://assist.org/api/institutions",
        context=context
    ) as url:
        data = json.loads(url.read().decode())

origin_id = None
for inst in data:
    if inst["code"].strip().upper() == origin_acronym:
        origin_id = inst["id"]

if origin_id is None:
    print("Institution not found. Please check the acronym and try again.")
    exit()

with urllib.request.urlopen(
        f'https://assist.org/api/institutions/{origin_id}/agreements', 
        context=context
    ) as url:
        data = json.loads(url.read().decode())

cc_codes = []
for college in list(data):
    if college['isCommunityCollege']:
        school_id = college['institutionParentId']
        school_name = college['institutionName']
        curr = {'name': school_name, 'id': school_id}
        if not any(d['name'] == school_name for d in cc_codes):
            cc_codes.append(curr)

prefix = input("Prefix: ")
number = input("Number: ")

start_time = time.time()

def getPrefixCode(code):
    with urllib.request.urlopen(
        f'https://assist.org/api/agreements?receivingInstitutionId={origin_id}&sendingInstitutionId={code}&academicYearId=76&categoryCode=prefix',
        context=context
    ) as url:
        data = json.loads(url.read().decode())
    data = data['reports']
    for report in list(data):
        label_parts = report['label'].upper().split()
        if label_parts[0] == prefix.upper() and report['ownerInstitutionId'] == origin_id:
            return report['key']
        
    return None

def getAgreementData(key):
    encoded_key = urllib.parse.quote(key, safe="")
    url = f"https://prod.assistng.org/articulation/api/Agreements?Key={encoded_key}"

    req = urllib.request.Request(url)

    with urllib.request.urlopen(req, context=context) as response:
        return json.loads(response.read().decode())

def searchAgreement(data):
    if not data.get("isSuccessful"):
        return None

    result = data.get("result", {})

    articulations_raw = result.get("articulations")
    if not articulations_raw:
        return None

    articulations = json.loads(articulations_raw)

    target_prefix = prefix.upper()
    target_number = number.upper()

    for articulation in articulations:
        course = articulation.get("course")
        if not course:
            continue

        rec_prefix = course.get("prefix", "").upper()
        rec_number = course.get("courseNumber", "").upper()

        if rec_prefix == target_prefix and rec_number == target_number:
            return articulation   # return full articulation block

    return None

def parse_articulation(data):
    sending = data.get("sendingArticulation", {})
    groups = sending.get("items", [])
    group_conjunctions = sending.get("courseGroupConjunctions", [])

    group_strings = []

    # Build each group string
    for group in groups:
        conj = group.get("courseConjunction", "And")
        courses = []

        for course in group.get("items", []):
            prefix_c = course.get("prefix", "")
            number_c = course.get("courseNumber", "")
            courses.append(f"{prefix_c} {number_c} ".strip())

        if len(courses) == 1:
            group_strings.append(courses[0])
        else:
            joiner = f" {conj.upper()} "
            group_strings.append("(" + joiner.join(courses) + ")")

    # Apply group-level conjunctions
    if group_conjunctions:
        conj = group_conjunctions[0]
        begin = conj["sendingCourseGroupBeginPosition"]
        end = conj["sendingCourseGroupEndPosition"]
        operator = conj["groupConjunction"].upper()
        combined = f"{group_strings[begin]} {operator} {group_strings[end]}"
        return combined

    return group_strings[0] if group_strings else None

for code in cc_codes:
    name = code["name"]
    sending_id = code["id"]

    # Compton Community College doesn't exist anymore
    if sending_id == 34:
        continue

    try:
        prefix_key = getPrefixCode(sending_id)

        agreement_data = getAgreementData(prefix_key)

        articulation = searchAgreement(agreement_data)

        result = parse_articulation(articulation)

        if result:
            print(name)
            print(result)

    except Exception as e:
        continue

end_time = time.time()
print(end_time - start_time)